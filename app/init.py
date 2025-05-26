cat > app/__init__.py << 'EOF'
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'clave-secreta-desarrollo'
    
    @app.route('/')
    def index():
        return '''
        <h1>¡Aplicación de Facturas Funcionando!</h1>
        <p>La aplicación está lista para usar.</p>
        <a href="/test">Ir a página de prueba</a>
        '''
    
    @app.route('/test')
    def test():
        return '<h2>Página de prueba funcionando correctamente</h2>'
    
    return app
EOF
