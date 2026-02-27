"""
Servicio de Productos.
Maneja CRUD de productos (hoodies) y gestión de stock.
"""

from datetime import datetime
from bson import ObjectId
from app.models.product import Product


class ProductService:
    """Servicio para operaciones con productos"""
    
    def __init__(self, db):
        """
        Constructor del servicio.
        
        Args:
            db: Conexión a la base de datos MongoDB
        """
        self.db = db
        self.products_collection = db.products
    
    def create_product(self, nombre, descripcion, precio, stock, colores, imagen=None):
        """
        Crea un nuevo producto.
        
        Args:
            nombre (str): Nombre del hoodie
            descripcion (str): Descripción
            precio (float): Precio en COP
            stock (dict): Stock por talla {'S': 10, 'M': 15, 'L': 20, 'XL': 5}
            colores (list): Lista de colores
            imagen (str): Ruta de la imagen
            
        Returns:
            tuple: (success: bool, message: str, product_id: ObjectId or None)
        """
        # Validaciones
        if not nombre or not descripcion:
            return False, "Nombre y descripción son obligatorios", None
        
        try:
            precio = float(precio)
            if precio <= 0:
                return False, "El precio debe ser mayor a 0", None
        except (ValueError, TypeError):
            return False, "Precio inválido", None
        
        # Crear producto
        product = Product(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            colores=colores,
            imagen=imagen,
            activo=True
        )
        
        try:
            result = self.products_collection.insert_one(product.to_dict())
            return True, "Producto creado exitosamente", result.inserted_id
        except Exception as e:
            return False, f"Error al crear producto: {str(e)}", None
    
    def get_product_by_id(self, product_id):
        """
        Obtiene un producto por su ID.
        
        Args:
            product_id (str or ObjectId): ID del producto
            
        Returns:
            Product or None: Producto encontrado o None
        """
        try:
            product_data = self.products_collection.find_one({'_id': ObjectId(product_id)})
            return Product.from_dict(product_data)
        except Exception:
            return None
    
    def get_all_products(self, solo_activos=False):
        """
        Obtiene todos los productos.
        
        Args:
            solo_activos (bool): Si True, solo retorna productos activos
            
        Returns:
            list: Lista de objetos Product
        """
        query = {'activo': True} if solo_activos else {}
        products_data = self.products_collection.find(query).sort('created_at', -1)
        return [Product.from_dict(data) for data in products_data]
    
    def update_product(self, product_id, **kwargs):
        """
        Actualiza un producto.
        
        Args:
            product_id (str or ObjectId): ID del producto
            **kwargs: Campos a actualizar
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            kwargs['updated_at'] = datetime.utcnow()
            
            # Convertir precio a float si existe
            if 'precio' in kwargs:
                kwargs['precio'] = float(kwargs['precio'])
            
            result = self.products_collection.update_one(
                {'_id': ObjectId(product_id)},
                {'$set': kwargs}
            )
            
            if result.modified_count > 0:
                return True, "Producto actualizado exitosamente"
            else:
                return False, "No se realizaron cambios"
        except Exception as e:
            return False, f"Error al actualizar producto: {str(e)}"
    
    def delete_product(self, product_id):
        """
        Elimina (soft delete) un producto.
        
        Args:
            product_id (str or ObjectId): ID del producto
            
        Returns:
            tuple: (success: bool, message: str)
        """
        return self.update_product(product_id, activo=False)
    
    def restore_product(self, product_id):
        """
        Restaura un producto eliminado.
        
        Args:
            product_id (str or ObjectId): ID del producto
            
        Returns:
            tuple: (success: bool, message: str)
        """
        return self.update_product(product_id, activo=True)
    
    def reducir_stock(self, product_id, talla, cantidad):
        """
        Reduce el stock de un producto.
        
        Args:
            product_id (str or ObjectId): ID del producto
            talla (str): Talla (S, M, L, XL)
            cantidad (int): Cantidad a reducir
            
        Returns:
            tuple: (success: bool, message: str)
        """
        product = self.get_product_by_id(product_id)
        
        if not product:
            return False, "Producto no encontrado"
        
        if not product.tiene_stock(talla, cantidad):
            return False, f"Stock insuficiente para talla {talla}"
        
        if product.reducir_stock(talla, cantidad):
            success, msg = self.update_product(product_id, stock=product.stock)
            return success, msg if success else "Error al actualizar stock"
        
        return False, "No se pudo reducir el stock"
    
    def aumentar_stock(self, product_id, talla, cantidad):
        """
        Aumenta el stock de un producto.
        
        Args:
            product_id (str or ObjectId): ID del producto
            talla (str): Talla (S, M, L, XL)
            cantidad (int): Cantidad a aumentar
            
        Returns:
            tuple: (success: bool, message: str)
        """
        product = self.get_product_by_id(product_id)
        
        if not product:
            return False, "Producto no encontrado"
        
        product.aumentar_stock(talla, cantidad)
        success, msg = self.update_product(product_id, stock=product.stock)
        return success, msg if success else "Error al actualizar stock"
    
    def buscar_productos(self, query):
        """
        Busca productos por nombre o descripción.
        
        Args:
            query (str): Texto a buscar
            
        Returns:
            list: Lista de productos encontrados
        """
        import re
        regex = re.compile(re.escape(query), re.IGNORECASE)
        
        products_data = self.products_collection.find({
            '$or': [
                {'nombre': regex},
                {'descripcion': regex}
            ],
            'activo': True
        })
        
        return [Product.from_dict(data) for data in products_data]
    
    def filtrar_productos(self, **filtros):
        """
        Filtra productos por criterios.
        
        Args:
            **filtros: Criterios de filtrado
                - precio_min (float)
                - precio_max (float)
                - color (str)
                - talla (str)
                - activo (bool)
                
        Returns:
            list: Lista de productos filtrados
        """
        query = {}
        
        if 'activo' in filtros:
            query['activo'] = filtros['activo']
        else:
            query['activo'] = True
        
        if 'precio_min' in filtros:
            query['precio'] = query.get('precio', {})
            query['precio']['$gte'] = float(filtros['precio_min'])
        
        if 'precio_max' in filtros:
            query['precio'] = query.get('precio', {})
            query['precio']['$lte'] = float(filtros['precio_max'])
        
        if 'color' in filtros:
            query['colores'] = filtros['color']
        
        if 'talla' in filtros:
            query[f'stock.{filtros["talla"]}'] = {'$gt': 0}
        
        products_data = self.products_collection.find(query).sort('created_at', -1)
        return [Product.from_dict(data) for data in products_data]