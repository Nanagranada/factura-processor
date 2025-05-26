cat > app/__init__.py << 'EOF'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app():
    app = Flask(__name__)
    
    # Configuración básica
    app.config['SECRET_KEY'] = 'clave-secreta-para-desarrollo'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuración de uploads
    upload_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
    app.config['UPLOAD_FOLDER'] = upload_folder
    app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
    
    # Crear directorio uploads
    os.makedirs(upload_folder, exist_ok=True)

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)

    # Ruta de prueba simple
    @app.route('/')
    def index():
        return "<h1>¡Aplicación funcionando!</h1><p>La estructura está correcta.</p>"

    return app
EOF
