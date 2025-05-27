cat > super_simple.py << 'EOF'
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>TEST LOGIN</h1>
    <form method="POST" action="/test-login">
        <p>Usuario: <input type="text" name="username"></p>
        <p>Contraseña: <input type="password" name="password"></p>
        <p><button type="submit">ENVIAR</button></p>
    </form>
    '''

@app.route('/test-login', methods=['POST'])
def test_login():
    username = request.form.get('username')
    password = request.form.get('password')
    return f'<h1>¡FORMULARIO FUNCIONÓ!</h1><p>Usuario: {username}<br>Contraseña: {password}</p>'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
EOF
