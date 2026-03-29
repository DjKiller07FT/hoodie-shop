"""
Configuración de la aplicación Flask.
Carga variables de entorno y define configuraciones para desarrollo y producción.
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()


class Config:
    """Configuración base para la aplicación"""
    
    # Seguridad
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # MongoDB
    MONGO_URI = os.getenv('MONGO_URI')
    
    # Sesiones
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Uploads
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'app/static/uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 5 * 1024 * 1024))  # 5MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # WhatsApp
    WHATSAPP_NUMBER = os.getenv('WHATSAPP_NUMBER', '573108116983')
    
    # Paginación
    PRODUCTS_PER_PAGE = 12
    ORDERS_PER_PAGE = 20
    
    # Admin inicial (para seed)
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
    ADMIN_NOMBRE = os.getenv('ADMIN_NOMBRE')


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Configuración para pruebas automatizadas"""
    DEBUG = True
    TESTING = True
    # Evita llamadas reales a MongoDB durante los tests
    MONGO_URI = 'mongodb://localhost/hoodie_shop_test'
    # Desactiva protección CSRF en formularios
    WTF_CSRF_ENABLED = False
    # Sesiones en memoria (no en filesystem)
    SESSION_TYPE = 'null'


# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}