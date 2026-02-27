"""
Script para crear índices en MongoDB.
Optimiza las búsquedas en la base de datos.
Ejecutar una vez después de la primera configuración.
"""

from app import create_app, get_db

def setup_indexes():
    """Crea índices en las colecciones de MongoDB"""
    
    app = create_app()
    
    with app.app_context():
        db = get_db()
        
        print("=" * 50)
        print("🔧 CONFIGURANDO ÍNDICES EN MONGODB")
        print("=" * 50)
        
        # Índices para users
        print("\n📊 Colección: users")
        try:
            db.users.create_index("email", unique=True)
            print("   ✅ Índice único en 'email'")
        except Exception as e:
            print(f"   ⚠️  Email index: {e}")
        
        try:
            db.users.create_index("rol")
            print("   ✅ Índice en 'rol'")
        except Exception as e:
            print(f"   ⚠️  Rol index: {e}")
        
        # Índices para products
        print("\n📊 Colección: products")
        try:
            db.products.create_index("nombre")
            print("   ✅ Índice en 'nombre'")
        except Exception as e:
            print(f"   ⚠️  Nombre index: {e}")
        
        try:
            db.products.create_index("activo")
            print("   ✅ Índice en 'activo'")
        except Exception as e:
            print(f"   ⚠️  Activo index: {e}")
        
        try:
            db.products.create_index("precio")
            print("   ✅ Índice en 'precio'")
        except Exception as e:
            print(f"   ⚠️  Precio index: {e}")
        
        # Índices para orders
        print("\n📊 Colección: orders")
        try:
            db.orders.create_index("numero_pedido", unique=True)
            print("   ✅ Índice único en 'numero_pedido'")
        except Exception as e:
            print(f"   ⚠️  Numero pedido index: {e}")
        
        try:
            db.orders.create_index("user_id")
            print("   ✅ Índice en 'user_id'")
        except Exception as e:
            print(f"   ⚠️  User ID index: {e}")
        
        try:
            db.orders.create_index("estado")
            print("   ✅ Índice en 'estado'")
        except Exception as e:
            print(f"   ⚠️  Estado index: {e}")
        
        try:
            db.orders.create_index([("created_at", -1)])
            print("   ✅ Índice descendente en 'created_at'")
        except Exception as e:
            print(f"   ⚠️  Created at index: {e}")
        
        print("\n" + "=" * 50)
        print("✅ ÍNDICES CONFIGURADOS CORRECTAMENTE")
        print("=" * 50)

if __name__ == '__main__':
    setup_indexes()