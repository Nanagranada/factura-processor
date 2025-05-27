cat > create_admin.py << 'EOF'
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Crear las tablas si no existen
    db.create_all()

    # Verificar si ya existe el usuario admin
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@test.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Usuario admin creado exitosamente")
    else:
        print("Usuario admin ya existe")
EOF
