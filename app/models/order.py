"""
Modelo de Pedido (Order).
Representa los pedidos de los clientes con seguimiento de estados.
"""

from datetime import datetime
from bson import ObjectId


class Order:
    """
    Modelo de Pedido con historial de estados y gestión de items.
    """
    
    # Estados posibles del pedido
    ESTADO_RECIBIDO = 'RECIBIDO'
    ESTADO_ALISTAMIENTO = 'ALISTAMIENTO'
    ESTADO_ENVIO = 'ENVIO'
    ESTADO_ENTREGADO = 'ENTREGADO'
    
    ESTADOS_VALIDOS = [
        ESTADO_RECIBIDO,
        ESTADO_ALISTAMIENTO,
        ESTADO_ENVIO,
        ESTADO_ENTREGADO
    ]
    
    def __init__(self, numero_pedido, user_id, items, total, direccion_envio,
                 estado=None, historial_estados=None, _id=None,
                 created_at=None, updated_at=None):
        """
        Constructor del pedido.
        
        Args:
            numero_pedido (str): Número único del pedido (ej: ORD-2026-000001)
            user_id (ObjectId): ID del usuario que hizo el pedido
            items (list): Lista de items del pedido con estructura:
                [{
                    'product_id': ObjectId,
                    'nombre': str,
                    'talla': str,
                    'color': str,
                    'cantidad': int,
                    'precio_unitario': float,
                    'subtotal': float
                }]
            total (float): Total del pedido en COP
            direccion_envio (dict): Datos de envío:
                {
                    'nombre': str,
                    'telefono': str,
                    'direccion': str,
                    'ciudad': str,
                    'notas': str (opcional)
                }
            estado (str): Estado actual del pedido
            historial_estados (list): Historial de cambios de estado
            _id (ObjectId): ID de MongoDB
            created_at (datetime): Fecha de creación
            updated_at (datetime): Fecha de última actualización
        """
        self._id = _id or ObjectId()
        self.numero_pedido = numero_pedido
        self.user_id = ObjectId(user_id) if not isinstance(user_id, ObjectId) else user_id
        self.items = items or []
        self.total = float(total)
        self.direccion_envio = direccion_envio
        self.estado = estado or self.ESTADO_RECIBIDO
        self.historial_estados = historial_estados or []
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        
        # Agregar estado inicial al historial si está vacío
        if not self.historial_estados:
            self.historial_estados.append({
                'estado': self.estado,
                'fecha': self.created_at,
                'cambiado_por': None  # Sistema
            })
    
    def cambiar_estado(self, nuevo_estado, admin_id=None):
        """
        Cambia el estado del pedido y registra en el historial.
        
        Args:
            nuevo_estado (str): Nuevo estado del pedido
            admin_id (ObjectId): ID del admin que cambió el estado
            
        Returns:
            bool: True si se cambió correctamente
        """
        if nuevo_estado not in self.ESTADOS_VALIDOS:
            return False
        
        if nuevo_estado == self.estado:
            return False  # Ya está en ese estado
        
        self.estado = nuevo_estado
        self.updated_at = datetime.utcnow()
        
        self.historial_estados.append({
            'estado': nuevo_estado,
            'fecha': self.updated_at,
            'cambiado_por': admin_id
        })
        
        return True
    
    def get_cantidad_items(self):
        """Retorna la cantidad total de items en el pedido"""
        return sum(item['cantidad'] for item in self.items)
    
    def formato_total(self):
        """Retorna el total formateado en COP"""
        return f"${self.total:,.0f}"
    
    def get_ultimo_cambio_estado(self):
        """Retorna el último cambio de estado del historial"""
        if self.historial_estados:
            return self.historial_estados[-1]
        return None
    
    def esta_entregado(self):
        """Verifica si el pedido ya fue entregado"""
        return self.estado == self.ESTADO_ENTREGADO
    
    def to_dict(self):
        """
        Convierte el objeto Order a diccionario para MongoDB.
        
        Returns:
            dict: Representación del pedido para guardar en BD
        """
        return {
            '_id': self._id,
            'numero_pedido': self.numero_pedido,
            'user_id': self.user_id,
            'items': self.items,
            'total': self.total,
            'direccion_envio': self.direccion_envio,
            'estado': self.estado,
            'historial_estados': self.historial_estados,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @staticmethod
    def from_dict(data):
        """
        Crea un objeto Order desde un diccionario de MongoDB.
        
        Args:
            data (dict): Documento de MongoDB
            
        Returns:
            Order: Instancia del pedido
        """
        if not data:
            return None
        
        return Order(
            numero_pedido=data.get('numero_pedido'),
            user_id=data.get('user_id'),
            items=data.get('items', []),
            total=data.get('total'),
            direccion_envio=data.get('direccion_envio'),
            estado=data.get('estado'),
            historial_estados=data.get('historial_estados', []),
            _id=data.get('_id'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    @staticmethod
    def generar_numero_pedido():
        """
        Genera un número de pedido único.
        Formato: ORD-YYYY-NNNNNN
        
        Returns:
            str: Número de pedido único
        """
        from datetime import datetime
        import random
        
        year = datetime.now().year
        random_num = random.randint(100000, 999999)
        return f"ORD-{year}-{random_num}"
    
    def __repr__(self):
        """Representación string del pedido"""
        return f'<Order {self.numero_pedido} - {self.estado} - ${self.total}>'