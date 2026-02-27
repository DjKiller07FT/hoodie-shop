"""
Punto de entrada de la aplicación Hoodie Shop.
Ejecuta el servidor Flask en modo desarrollo.
"""

import os
from app import create_app

# Obtener configuración del entorno
config_name = os.getenv('FLASK_ENV', 'development')

# Crear aplicación
app = create_app(config_name)

if __name__ == '__main__':
    # Ejecutar servidor de desarrollo
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("=" * 50)
    print("🚀 HOODIE SHOP - Iniciando aplicación")
    print("=" * 50)
    print(f"📍 Entorno: {config_name}")
    print(f"🌐 URL: http://localhost:{port}")
    print(f"🔧 Debug: {debug}")
    print("=" * 50)
    print("💡 Presiona Ctrl+C para detener el servidor")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )