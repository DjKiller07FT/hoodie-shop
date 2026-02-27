"""
Modelo de Usuario.
Representa a usuarios (clientes y administradores) en el sistema.
"""

from datetime import datetime
from bson import ObjectId
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin):
    """
    Modelo de Usuario con autenticación.
    Implementa UserMixin de Flask-Login para gestión de sesiones.
    """
    
    def __init__(self, nombre, email, telefono, direccion, ciudad, 
                 password_hash=None, rol='user', _id=None, 
                 created_at=None, updated_at=None):
        """
        Constructor del usuario.
        
        Args:
            nombre (str): Nombre completo del usuario
            email (str): Email único del usuario
            telefono (str): Número de teléfono
            direccion (str): Dirección de envío
            ciudad (str): Ciudad de residencia
            password_hash (str): Hash de la contraseña
            rol (str): Rol del usuario ('user' o 'admin')
            _id (ObjectId): ID de MongoDB
            created_at (datetime): Fecha de creación
            updated_at (datetime): Fecha de última actualización
        """
        self._id = _id or ObjectId()
        self.nombre = nombre
        self.email = email.lower()  # Normalizar email a minúsculas
        self.telefono = telefono
        self.direccion = direccion
        self.ciudad = ciudad
        self.password_hash = password_hash
        self.rol = rol
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def get_id(self):
        """Retorna el ID del usuario como string (requerido por Flask-Login)"""
        return str(self._id)
    
    def set_password(self, password):
        """
        Hashea y guarda la contraseña del usuario.
        
        Args:
            password (str): Contraseña en texto plano
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Verifica si la contraseña es correcta.
        
        Args:
            password (str): Contraseña en texto plano
            
        Returns:
            bool: True si la contraseña es correcta
        """
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Verifica si el usuario es administrador"""
        return self.rol == 'admin'
    
    def to_dict(self):
        """
        Convierte el objeto User a diccionario para MongoDB.
        
        Returns:
            dict: Representación del usuario para guardar en BD
        """
        return {
            '_id': self._id,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'direccion': self.direccion,
            'ciudad': self.ciudad,
            'password_hash': self.password_hash,
            'rol': self.rol,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @staticmethod
    def from_dict(data):
        """
        Crea un objeto User desde un diccionario de MongoDB.
        
        Args:
            data (dict): Documento de MongoDB
            
        Returns:
            User: Instancia del usuario
        """
        if not data:
            return None
        
        return User(
            nombre=data.get('nombre'),
            email=data.get('email'),
            telefono=data.get('telefono'),
            direccion=data.get('direccion'),
            ciudad=data.get('ciudad'),
            password_hash=data.get('password_hash'),
            rol=data.get('rol', 'user'),
            _id=data.get('_id'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def __repr__(self):
        """Representación string del usuario"""
        return f'<User {self.email} ({self.rol})>'