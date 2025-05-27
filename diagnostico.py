cat > diagnostico.py << 'EOF'
import os
import sys

print("=== DIAGNÓSTICO DEL PROYECTO ===")
print(f"Directorio actual: {os.getcwd()}")
print(f"Python version: {sys.version}")

# Verificar estructura de archivos
archivos_requeridos = [
    'run.py',
    'config.py',
    'app/__init__.py',
    'app/routes.py',
    'app/models.py',
    'app/templates/login.html'
]

print("\n=== ARCHIVOS ===")
for archivo in archivos_requeridos:
    existe = "✓" if os.path.exists(archivo) else "✗"
    print(f"{existe} {archivo}")

# Verificar dependencias
print("\n=== DEPENDENCIAS ===")
try:
    import flask
    print(f"✓ Flask: {flask.__version__}")
except ImportError:
    print("✗ Flask no instalado")

try:
    import flask_login
    print("✓ Flask-Login disponible")
except ImportError:
    print("✗ Flask-Login no instalado")

try:
    import flask_sqlalchemy
    print("✓ Flask-SQLAlchemy disponible")
except ImportError:
    print("✗ Flask-SQLAlchemy no instalado")

# Verificar carpetas
print("\n=== CARPETAS ===")
carpetas = ['app', 'app/templates', 'app/static', 'uploads']
for carpeta in carpetas:
    existe = "✓" if os.path.exists(carpeta) else "✗"
    print(f"{existe} {carpeta}")

print("\n=== PRUEBA DE IMPORTACIÓN ===")
try:
    from app import create_app
    print("✓ create_app se puede importar")

    app = create_app()
    print("✓ Aplicación se puede crear")

    with app.app_context():
        from app import db
        print("✓ Base de datos se puede importar")

except Exception as e:
    print(f"✗ Error: {e}")

print("\n=== FIN DIAGNÓSTICO ===")
EOF
