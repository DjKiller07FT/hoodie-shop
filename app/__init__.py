"""
Factory de la aplicación Flask.
Inicializa Flask, MongoDB, Flask-Login y registra blueprints.
"""

import os
from flask import Flask, g
from flask_login import LoginManager
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from .config import config


# Instancia global de LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'warning'


def get_db():
    """
    Obtiene la conexión a la base de datos MongoDB.
    Usa Flask's 'g' object para almacenar la conexión durante el request.
    
    Returns:
        Database: Objeto de base de datos de MongoDB
    """
    if 'db' not in g:
        mongo_uri = os.getenv('MONGO_URI')
        if not mongo_uri:
            raise ValueError("MONGO_URI no está configurado en las variables de entorno")
        
        client = MongoClient(mongo_uri)
        g.db = client.get_database()  # Obtiene la BD del URI
    
    return g.db


def close_db(e=None):
    """
    Cierra la conexión a MongoDB al finalizar el request.
    
    Args:
        e: Excepción (si existe)
    """
    db = g.pop('db', None)
    if db is not None:
        db.client.close()


def test_mongo_connection(app):
    """
    Prueba la conexión a MongoDB al iniciar la aplicación.
    
    Args:
        app: Instancia de Flask
        
    Returns:
        bool: True si la conexión es exitosa
    """
    try:
        with app.app_context():
            db = get_db()
            # Ejecutar comando ping para verificar conexión
            db.command('ping')
            app.logger.info("✅ Conexión a MongoDB exitosa")
            return True
    except ConnectionFailure as e:
        app.logger.error(f"❌ Error de conexión a MongoDB: {e}")
        return False
    except Exception as e:
        app.logger.error(f"❌ Error inesperado al conectar a MongoDB: {e}")
        return False


@login_manager.user_loader
def load_user(user_id):
    """
    Carga un usuario desde la base de datos para Flask-Login.
    
    Args:
        user_id (str): ID del usuario
        
    Returns:
        User: Objeto User o None si no existe
    """
    from bson import ObjectId
    from .models.user import User
    
    try:
        db = get_db()
        user_data = db.users.find_one({'_id': ObjectId(user_id)})
        return User.from_dict(user_data)
    except Exception as e:
        return None


def create_app(config_name='default'):
    """
    Factory para crear la aplicación Flask.
    
    Args:
        config_name (str): Nombre de la configuración ('development', 'production')
        
    Returns:
        Flask: Instancia de la aplicación Flask configurada
    """
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Inicializar Flask-Login
    login_manager.init_app(app)
    
    # Registrar función para cerrar conexión DB
    app.teardown_appcontext(close_db)
    
    # Probar conexión a MongoDB
    test_mongo_connection(app)
    
    # Registrar blueprints (rutas)
    from .routes import auth, shop, admin, user
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(shop.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(user.bp)
    
    # Ruta principal
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('shop.catalog'))
    
    # Contexto global para templates
    @app.context_processor
    def inject_globals():
        from flask_login import current_user
        return {
            'current_user': current_user
        }
    
    # Crear carpeta de uploads si no existe
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    app.logger.info(f"🚀 Aplicación Flask iniciada en modo {config_name}")
    
    return app