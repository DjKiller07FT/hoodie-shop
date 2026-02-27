"""
Blueprints de rutas.
Organiza los endpoints por funcionalidad.
"""

# Los blueprints se importan individualmente en create_app()
# para evitar importaciones circulares

__all__ = ['auth', 'shop', 'admin', 'user']