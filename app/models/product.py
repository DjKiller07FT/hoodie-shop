"""
Modelo de Producto (Hoodie).
Representa los buzos/hoodies en el catálogo.
"""

from datetime import datetime
from bson import ObjectId


class Product:
    """
    Modelo de Producto con gestión de stock por talla.
    """
    
    def __init__(self, nombre, descripcion, precio, stock, colores, 
                 imagen=None, activo=True, _id=None, 
                 created_at=None, updated_at=None):
        """
        Constructor del producto.
        
        Args:
            nombre (str): Nombre del hoodie
            descripcion (str): Descripción detallada
            precio (float): Precio en COP
            stock (dict): Stock por talla {'S': 10, 'M': 15, 'L': 20, 'XL': 5}
            colores (list): Lista de colores disponibles
            imagen (str): Ruta de la imagen
            activo (bool): Si el producto está activo (visible)
            _id (ObjectId): ID de MongoDB
            created_at (datetime): Fecha de creación
            updated_at (datetime): Fecha de última actualización
        """
        self._id = _id or ObjectId()
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = float(precio)
        self.stock = stock or {'S': 0, 'M': 0, 'L': 0, 'XL': 0}
        self.colores = colores or []
        self.imagen = imagen or '/static/img/placeholder.jpg'
        self.activo = activo
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def get_stock_total(self):
        """Retorna el stock total sumando todas las tallas"""
        return sum(self.stock.values())
    
    def tiene_stock(self, talla, cantidad=1):
        """
        Verifica si hay stock disponible para una talla.
        
        Args:
            talla (str): Talla a verificar (S, M, L, XL)
            cantidad (int): Cantidad requerida
            
        Returns:
            bool: True si hay stock suficiente
        """
        return self.stock.get(talla, 0) >= cantidad
    
    def reducir_stock(self, talla, cantidad):
        """
        Reduce el stock de una talla.
        
        Args:
            talla (str): Talla a reducir
            cantidad (int): Cantidad a reducir
            
        Returns:
            bool: True si se pudo reducir el stock
        """
        if self.tiene_stock(talla, cantidad):
            self.stock[talla] -= cantidad
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def aumentar_stock(self, talla, cantidad):
        """
        Aumenta el stock de una talla.
        
        Args:
            talla (str): Talla a aumentar
            cantidad (int): Cantidad a aumentar
        """
        if talla in self.stock:
            self.stock[talla] += cantidad
        else:
            self.stock[talla] = cantidad
        self.updated_at = datetime.utcnow()
    
    def formato_precio(self):
        """Retorna el precio formateado en COP"""
        return f"${self.precio:,.0f}"
    
    def to_dict(self):
        """
        Convierte el objeto Product a diccionario para MongoDB.
        
        Returns:
            dict: Representación del producto para guardar en BD
        """
        return {
            '_id': self._id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'stock': self.stock,
            'colores': self.colores,
            'imagen': self.imagen,
            'activo': self.activo,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @staticmethod
    def from_dict(data):
        """
        Crea un objeto Product desde un diccionario de MongoDB.
        
        Args:
            data (dict): Documento de MongoDB
            
        Returns:
            Product: Instancia del producto
        """
        if not data:
            return None
        
        return Product(
            nombre=data.get('nombre'),
            descripcion=data.get('descripcion'),
            precio=data.get('precio'),
            stock=data.get('stock', {'S': 0, 'M': 0, 'L': 0, 'XL': 0}),
            colores=data.get('colores', []),
            imagen=data.get('imagen'),
            activo=data.get('activo', True),
            _id=data.get('_id'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def __repr__(self):
        """Representación string del producto"""
        return f'<Product {self.nombre} - ${self.precio}>'