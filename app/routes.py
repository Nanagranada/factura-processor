cat > app/routes.py << 'EOF'
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import User, Invoice
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
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            invoice = Invoice(
                filename=filename,
                invoice_number=f"INV-{timestamp}",
                supplier_name="Proveedor por determinar",
                total_amount=0.0,
                description="Factura subida - pendiente de procesamiento OCR",
                user_id=current_user.id
            )

            db.session.add(invoice)
            db.session.commit()

            flash('Factura subida exitosamente', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Tipo de archivo no permitido. Solo se permiten archivos PDF.', 'error')

    return render_template('upload.html')

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
