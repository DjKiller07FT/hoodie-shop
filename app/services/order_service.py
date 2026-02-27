"""
Servicio de Pedidos.
Maneja creación, actualización y gestión de pedidos.
"""

from datetime import datetime
from bson import ObjectId
from app.models.order import Order


class OrderService:
    """Servicio para operaciones con pedidos"""
    
    def __init__(self, db):
        """
        Constructor del servicio.
        
        Args:
            db: Conexión a la base de datos MongoDB
        """
        self.db = db
        self.orders_collection = db.orders
    
    def create_order(self, user_id, items, direccion_envio):
        """
        Crea un nuevo pedido.
        
        Args:
            user_id (str or ObjectId): ID del usuario
            items (list): Lista de items del pedido
            direccion_envio (dict): Datos de envío
            
        Returns:
            tuple: (success: bool, message: str, order: Order or None)
        """
        # Validaciones
        if not items:
            return False, "El pedido debe tener al menos un item", None
        
        if not direccion_envio or not all([
            direccion_envio.get('nombre'),
            direccion_envio.get('telefono'),
            direccion_envio.get('direccion'),
            direccion_envio.get('ciudad')
        ]):
            return False, "Datos de envío incompletos", None
        
        # Calcular total
        total = sum(item['subtotal'] for item in items)
        
        # Generar número de pedido único
        numero_pedido = self._generar_numero_pedido_unico()
        
        # Crear pedido
        order = Order(
            numero_pedido=numero_pedido,
            user_id=user_id,
            items=items,
            total=total,
            direccion_envio=direccion_envio,
            estado=Order.ESTADO_RECIBIDO
        )
        
        try:
            self.orders_collection.insert_one(order.to_dict())
            return True, "Pedido creado exitosamente", order
        except Exception as e:
            return False, f"Error al crear pedido: {str(e)}", None
    
    def _generar_numero_pedido_unico(self):
        """
        Genera un número de pedido único verificando que no exista en BD.
        
        Returns:
            str: Número de pedido único
        """
        while True:
            numero = Order.generar_numero_pedido()
            if not self.orders_collection.find_one({'numero_pedido': numero}):
                return numero
    
    def get_order_by_id(self, order_id):
        """
        Obtiene un pedido por su ID.
        
        Args:
            order_id (str or ObjectId): ID del pedido
            
        Returns:
            Order or None: Pedido encontrado o None
        """
        try:
            order_data = self.orders_collection.find_one({'_id': ObjectId(order_id)})
            return Order.from_dict(order_data)
        except Exception:
            return None
    
    def get_order_by_numero(self, numero_pedido):
        """
        Obtiene un pedido por su número.
        
        Args:
            numero_pedido (str): Número del pedido
            
        Returns:
            Order or None: Pedido encontrado o None
        """
        order_data = self.orders_collection.find_one({'numero_pedido': numero_pedido})
        return Order.from_dict(order_data)
    
    def get_orders_by_user(self, user_id):
        """
        Obtiene todos los pedidos de un usuario.
        
        Args:
            user_id (str or ObjectId): ID del usuario
            
        Returns:
            list: Lista de pedidos ordenados por fecha (más reciente primero)
        """
        orders_data = self.orders_collection.find({
            'user_id': ObjectId(user_id)
        }).sort('created_at', -1)
        
        return [Order.from_dict(data) for data in orders_data]
    
    def get_all_orders(self, filtro_estado=None):
        """
        Obtiene todos los pedidos (admin).
        
        Args:
            filtro_estado (str): Filtrar por estado específico (opcional)
            
        Returns:
            list: Lista de pedidos
        """
        query = {}
        if filtro_estado:
            query['estado'] = filtro_estado
        
        orders_data = self.orders_collection.find(query).sort('created_at', -1)
        return [Order.from_dict(data) for data in orders_data]
    
    def cambiar_estado(self, order_id, nuevo_estado, admin_id):
        """
        Cambia el estado de un pedido.
        
        Args:
            order_id (str or ObjectId): ID del pedido
            nuevo_estado (str): Nuevo estado
            admin_id (str or ObjectId): ID del admin que hace el cambio
            
        Returns:
            tuple: (success: bool, message: str)
        """
        order = self.get_order_by_id(order_id)
        
        if not order:
            return False, "Pedido no encontrado"
        
        if nuevo_estado not in Order.ESTADOS_VALIDOS:
            return False, "Estado inválido"
        
        if order.cambiar_estado(nuevo_estado, ObjectId(admin_id)):
            try:
                self.orders_collection.update_one(
                    {'_id': ObjectId(order_id)},
                    {'$set': {
                        'estado': order.estado,
                        'historial_estados': order.historial_estados,
                        'updated_at': order.updated_at
                    }}
                )
                return True, f"Estado cambiado a {nuevo_estado}"
            except Exception as e:
                return False, f"Error al actualizar estado: {str(e)}"
        
        return False, "El pedido ya está en ese estado"
    
    def get_estadisticas(self):
        """
        Obtiene estadísticas de pedidos (para dashboard admin).
        
        Returns:
            dict: Estadísticas
        """
        total_pedidos = self.orders_collection.count_documents({})
        
        pedidos_por_estado = {}
        for estado in Order.ESTADOS_VALIDOS:
            pedidos_por_estado[estado] = self.orders_collection.count_documents({'estado': estado})
        
        # Total de ventas
        pipeline = [
            {'$group': {'_id': None, 'total_ventas': {'$sum': '$total'}}}
        ]
        resultado = list(self.orders_collection.aggregate(pipeline))
        total_ventas = resultado[0]['total_ventas'] if resultado else 0
        
        return {
            'total_pedidos': total_pedidos,
            'pedidos_por_estado': pedidos_por_estado,
            'total_ventas': total_ventas
        }
    
    def exportar_pedidos_csv(self, filtro_estado=None):
        """
        Prepara datos de pedidos para exportar a CSV.
        
        Args:
            filtro_estado (str): Filtrar por estado (opcional)
            
        Returns:
            list: Lista de diccionarios con datos para CSV
        """
        orders = self.get_all_orders(filtro_estado)
        
        csv_data = []
        for order in orders:
            csv_data.append({
                'Número Pedido': order.numero_pedido,
                'Fecha': order.created_at.strftime('%Y-%m-%d %H:%M'),
                'Cliente': order.direccion_envio['nombre'],
                'Teléfono': order.direccion_envio['telefono'],
                'Ciudad': order.direccion_envio['ciudad'],
                'Dirección': order.direccion_envio['direccion'],
                'Items': order.get_cantidad_items(),
                'Total': order.total,
                'Estado': order.estado
            })
        
        return csv_data