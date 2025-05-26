cat > run.py << 'EOF'
import sys
import os

# Añadir el directorio actual al path de Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import create_app
    print("✓ Importación exitosa de create_app")
    
    app = create_app()
    print("✓ Aplicación creada exitosamente")
    
    if __name__ == '__main__':
        print("✓ Iniciando servidor...")
        app.run(debug=True, host='0.0.0.0', port=5000)
        
except ImportError as e:
    print(f"✗ Error de importación: {e}")
    print("Estructura del directorio:")
    for root, dirs, files in os.walk('.'):
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")
except Exception as e:
    print(f"✗ Error general: {e}")
EOF
