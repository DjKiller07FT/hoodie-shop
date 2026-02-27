"""
Servicios: lógica de negocio separada de las rutas.
"""

# Los servicios se importarán individualmente donde se necesiten
# para evitar dependencias circulares

__all__ = ['auth_service', 'product_service', 'order_service', 'whatsapp_service']