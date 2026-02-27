"""
Script para crear el usuario administrador inicial.
Ejecutar una sola vez después de configurar MongoDB.
"""

import os
from dotenv import load_dotenv
from app import create_app, get_db
from app.services.auth_service import AuthService

# Cargar variables de entorno
load_dotenv()

def seed_admin():
    """Crea el usuario administrador inicial"""
    
    # Obtener datos del admin desde .env
    admin_email = os.getenv('ADMIN_EMAIL')
    admin_password = os.getenv('ADMIN_PASSWORD')
    admin_nombre = os.getenv('ADMIN_NOMBRE')
    
    if not all([admin_email, admin_password, admin_nombre]):
        print("❌ ERROR: Faltan variables de entorno para el admin")
        print("   Verifica ADMIN_EMAIL, ADMIN_PASSWORD y ADMIN_NOMBRE en .env")
        return False
    
    # Crear aplicación y contexto
    app = create_app()
    
    with app.app_context():
        db = get_db()
        auth_service = AuthService(db)
        
        # Verificar si ya existe un admin
        existing_admin = db.users.find_one({'email': admin_email.lower()})
        
        if existing_admin:
            print(f"⚠️  El usuario {admin_email} ya existe")
            print("   No se creó un nuevo administrador")
            return False
        
        # Crear admin
        print(f"🔄 Creando usuario administrador...")
        print(f"   Email: {admin_email}")
        print(f"   Nombre: {admin_nombre}")
        
        success, message = auth_service.create_admin(
            nombre=admin_nombre,
            email=admin_email,
            password=admin_password
        )
        
        if success:
            print(f"✅ {message}")
            print("\n" + "=" * 50)
            print("🎉 ADMINISTRADOR CREADO EXITOSAMENTE")
            print("=" * 50)
            print(f"📧 Email: {admin_email}")
            print(f"🔑 Contraseña: {admin_password}")
            print("=" * 50)
            print("⚠️  IMPORTANTE: Cambia la contraseña después del primer login")
            print("=" * 50)
            return True
        else:
            print(f"❌ Error: {message}")
            return False

if __name__ == '__main__':
    print("=" * 50)
    print("🌱 SEED: Crear Administrador Inicial")
    print("=" * 50)
    
    seed_admin()