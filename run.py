cat > run.py << 'EOF'
from app import create_app, db
from app.models import User, Invoice

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Invoice': Invoice}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Crear usuario admin por defecto si no existe
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@example.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Usuario admin creado: username='admin', password='admin123'")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
EOF
