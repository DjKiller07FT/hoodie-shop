"""
Servicio de Autenticación.
Maneja registro, login y gestión de usuarios.
"""

from datetime import datetime
from bson import ObjectId
from app.models.user import User
from app.utils.helpers import validar_email


class AuthService:
    """Servicio para operaciones de autenticación"""
    
    def __init__(self, db):
        """
        Constructor del servicio.
        
        Args:
            db: Conexión a la base de datos MongoDB
        """
        self.db = db
        self.users_collection = db.users
    
    def register_user(self, nombre, email, telefono, direccion, ciudad, password):
        """
        Registra un nuevo usuario.
        
        Args:
            nombre (str): Nombre completo
            email (str): Email
            telefono (str): Teléfono
            direccion (str): Dirección
            ciudad (str): Ciudad
            password (str): Contraseña en texto plano
            
        Returns:
            tuple: (success: bool, message: str, user: User or None)
        """
        # Validaciones
        if not all([nombre, email, telefono, direccion, ciudad, password]):
            return False, "Todos los campos son obligatorios", None
        
        if not validar_email(email):
            return False, "Formato de email inválido", None
        
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres", None
        
        # Verificar si el email ya existe
        if self.users_collection.find_one({'email': email.lower()}):
            return False, "Este email ya está registrado", None
        
        # Crear usuario
        user = User(
            nombre=nombre,
            email=email,
            telefono=telefono,
            direccion=direccion,
            ciudad=ciudad,
            rol='user'
        )
        user.set_password(password)
        
        # Guardar en BD
        try:
            self.users_collection.insert_one(user.to_dict())
            return True, "Usuario registrado exitosamente", user
        except Exception as e:
            return False, f"Error al registrar usuario: {str(e)}", None
    
    def login_user(self, email, password):
        """
        Autentica un usuario.
        
        Args:
            email (str): Email del usuario
            password (str): Contraseña en texto plano
            
        Returns:
            tuple: (success: bool, message: str, user: User or None)
        """
        if not email or not password:
            return False, "Email y contraseña son requeridos", None
        
        # Buscar usuario
        user_data = self.users_collection.find_one({'email': email.lower()})
        
        if not user_data:
            return False, "Email o contraseña incorrectos", None
        
        user = User.from_dict(user_data)
        
        # Verificar contraseña
        if not user.check_password(password):
            return False, "Email o contraseña incorrectos", None
        
        return True, "Login exitoso", user
    
    def get_user_by_id(self, user_id):
        """
        Obtiene un usuario por su ID.
        
        Args:
            user_id (str or ObjectId): ID del usuario
            
        Returns:
            User or None: Usuario encontrado o None
        """
        try:
            user_data = self.users_collection.find_one({'_id': ObjectId(user_id)})
            return User.from_dict(user_data)
        except Exception:
            return None
    
    def update_user(self, user_id, **kwargs):
        """
        Actualiza datos de un usuario.
        
        Args:
            user_id (str or ObjectId): ID del usuario
            **kwargs: Campos a actualizar
            
        Returns:
            bool: True si se actualizó correctamente
        """
        try:
            kwargs['updated_at'] = datetime.utcnow()
            result = self.users_collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': kwargs}
            )
            return result.modified_count > 0
        except Exception:
            return False
    
    def create_admin(self, nombre, email, password):
        """
        Crea un usuario administrador.
        
        Args:
            nombre (str): Nombre completo
            email (str): Email
            password (str): Contraseña
            
        Returns:
            tuple: (success: bool, message: str)
        """
        # Verificar si ya existe
        if self.users_collection.find_one({'email': email.lower()}):
            return False, "Este email ya está registrado"
        
        admin = User(
            nombre=nombre,
            email=email,
            telefono="0000000000",
            direccion="Admin",
            ciudad="Admin",
            rol='admin'
        )
        admin.set_password(password)
        
        try:
            self.users_collection.insert_one(admin.to_dict())
            return True, "Administrador creado exitosamente"
        except Exception as e:
            return False, f"Error al crear administrador: {str(e)}"