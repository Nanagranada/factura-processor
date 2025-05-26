cat > app/__init__.py << 'EOF'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = 'clave-secreta-para-desarrollo'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuración de uploads
    upload_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
    app.config['UPLOAD_FOLDER'] = upload_folder
    app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Crear directorio uploads
    os.makedirs(upload_folder, exist_ok=True)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Registrar blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app

# Importar modelos para que SQLAlchemy los reconozca
from app import models
EOF
