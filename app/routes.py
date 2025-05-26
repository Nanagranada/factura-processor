cat > app/routes.py << 'EOF'
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_file
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import User, Invoice
from app.utils.ocr import extract_invoice_data
from app.utils.helisa import generate_helisa_file
import os
from datetime import datetime

main_bp = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('main.index'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        invoices = Invoice.query.all()
    else:
        invoices = current_user.invoices.all()
    return render_template('dashboard.html', invoices=invoices)

@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_invoice():
    if request.method == 'POST':
        if 'invoice' not in request.files:
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        
        file = request.files['invoice']
        if file.filename == '':
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Añadir timestamp para evitar conflictos
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extraer datos de la factura
            try:
                invoice_data = extract_invoice_data(filepath)
                
                # Crear registro en la base de datos
                invoice = Invoice(
                    filename=filename,
                    invoice_number=invoice_data.get('invoice_number'),
                    invoice_date=invoice_data.get('invoice_date'),
                    supplier_name=invoice_data.get('supplier_name'),
                    supplier_nit=invoice_data.get('supplier_nit'),
                    customer_name=invoice_data.get('customer_name'),
                    customer_nit=invoice_data.get('customer_nit'),
                    total_amount=invoice_data.get('total_amount'),
                    tax_amount=invoice_data.get('tax_amount'),
                    description=invoice_data.get('description'),
                    user_id=current_user.id
                )
                
                db.session.add(invoice)
                db.session.commit()
                
                flash('Factura subida y procesada exitosamente', 'success')
                return redirect(url_for('main.dashboard'))
                
            except Exception as e:
                flash(f'Error al procesar la factura: {str(e)}', 'error')
                # Eliminar archivo si hay error
                if os.path.exists(filepath):
                    os.remove(filepath)
        else:
            flash('Tipo de archivo no permitido. Solo se permiten archivos PDF.', 'error')
    
    return render_template('upload.html')

@main_bp.route('/process/<int:invoice_id>')
@login_required
def process_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    
    # Verificar permisos
    if not current_user.is_admin and invoice.user_id != current_user.id:
        flash('No tienes permisos para procesar esta factura', 'error')
        return redirect(url_for('main.dashboard'))
    
    if not invoice.processed:
        try:
            # Generar archivo para Helisa
            helisa_file = generate_helisa_file([invoice])
            invoice.processed = True
            invoice.processed_at = datetime.utcnow()
            db.session.commit()
            
            flash('Factura procesada exitosamente para Helisa', 'success')
            return send_file(helisa_file, as_attachment=True, download_name=f'helisa_import_{invoice.id}.xlsx')
            
        except Exception as e:
            flash(f'Error al procesar la factura: {str(e)}', 'error')
    else:
        flash('Esta factura ya ha sido procesada', 'info')
    
    return redirect(url_for('main.dashboard'))

@main_bp.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('No tienes permisos de administrador', 'error')
        return redirect(url_for('main.dashboard'))
    
    users = User.query.all()
    invoices = Invoice.query.all()
    return render_template('admin.html', users=users, invoices=invoices)
EOF
