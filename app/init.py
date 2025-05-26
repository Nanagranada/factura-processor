from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    # Asegurarse de que existe la carpeta de uploads
    import os
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
