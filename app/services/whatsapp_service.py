"""
Servicio de WhatsApp.
Genera mensajes formateados y enlaces para WhatsApp.
"""

from urllib.parse import quote


class WhatsAppService:
    """Servicio para generar enlaces de WhatsApp"""
    
    def __init__(self, numero_empresa):
        """
        Constructor del servicio.
        
        Args:
            numero_empresa (str): Número de WhatsApp de la empresa (con código país)
        """
        self.numero_empresa = numero_empresa
    
    def generar_mensaje_pedido(self, order, user):
        """
        Genera el mensaje de pedido para WhatsApp.
        
        Args:
            order (Order): Objeto Order con los datos del pedido
            user (User): Objeto User con datos del cliente
            
        Returns:
            str: Mensaje formateado para WhatsApp
        """
        mensaje = f"""Hola, quiero confirmar mi pedido:

📦 *Pedido:* {order.numero_pedido}
👤 *Cliente:* {order.direccion_envio['nombre']}
📞 *Teléfono:* {order.direccion_envio['telefono']}
📍 *Dirección:* {order.direccion_envio['direccion']}, {order.direccion_envio['ciudad']}"""
        
        # Agregar notas si existen
        if order.direccion_envio.get('notas'):
            mensaje += f"\n📝 *Notas:* {order.direccion_envio['notas']}"
        
        mensaje += "\n\n🛍️ *Productos:*\n"
        
        # Listar items
        for item in order.items:
            mensaje += f"- {item['nombre']} ({item['talla']}, {item['color']}) x{item['cantidad']} = ${item['subtotal']:,.0f}\n"
        
        mensaje += f"\n💰 *Total:* ${order.total:,.0f} COP"
        mensaje += "\n\n🚚 Pago contraentrega 💵"
        
        return mensaje
    
    def generar_enlace_whatsapp(self, order, user):
        """
        Genera el enlace completo de WhatsApp con el mensaje prellenado.
        
        Args:
            order (Order): Objeto Order
            user (User): Objeto User
            
        Returns:
            str: URL de WhatsApp (wa.me)
        """
        mensaje = self.generar_mensaje_pedido(order, user)
        mensaje_encoded = quote(mensaje)
        
        return f"https://wa.me/{self.numero_empresa}?text={mensaje_encoded}"
    
    def generar_mensaje_consulta(self, producto, user):
        """
        Genera mensaje de consulta sobre un producto.
        
        Args:
            producto (Product): Producto consultado
            user (User): Usuario que consulta
            
        Returns:
            str: Enlace de WhatsApp para consulta
        """
        mensaje = f"""Hola, tengo una consulta sobre este producto:

👕 *Producto:* {producto.nombre}
💰 *Precio:* ${producto.precio:,.0f} COP

👤 *Mi nombre:* {user.nombre}
📞 *Teléfono:* {user.telefono}"""
        
        mensaje_encoded = quote(mensaje)
        return f"https://wa.me/{self.numero_empresa}?text={mensaje_encoded}"