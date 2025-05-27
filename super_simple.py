cat > super_simple.py << 'EOF'
from flask import Flask, request

app = Flask(name)

@app.route('/')
def home():
return '''
TEST LOGIN

Usuario:
Contraseña:
ENVIAR

'''

@app.route('/test-login', methods=['POST'])
def test_login():
username = request.form.get('username')
password = request.form.get('password')
return f'¡FORMULARIO FUNCIONÓ!Usuario: {username}Contraseña: {password}'

if name == 'main':
app.run(debug=True, host='0.0.0.0', port=5000)
EO
