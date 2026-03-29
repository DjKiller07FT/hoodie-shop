"""
Casos de Prueba – Caja Gris (WEB-CG-04: RF-15 pedido en orders)
Técnica: Caja Gris — verificación funcional + inspección del documento MongoDB.
Módulo: Pedidos (creación con estado RECIBIDO en colección orders)
"""

import pytest
from unittest.mock import MagicMock, patch
from bson import ObjectId
from app.models.order import Order
from app.services.order_service import OrderService


@pytest.fixture
def mock_db():
    """Base de datos MongoDB simulada."""
    db = MagicMock()
    db.orders = MagicMock()
    return db


@pytest.fixture
def order_service(mock_db):
    """Instancia de OrderService con BD simulada."""
    return OrderService(mock_db)


@pytest.fixture
def items_validos():
    """Lista de items de pedido válidos."""
    return [
        {
            'product_id': str(ObjectId()),
            'nombre': 'Hoodie Clásico',
            'talla': 'M',
            'color': 'Negro',
            'cantidad': 2,
            'precio_unitario': 80000,
            'subtotal': 160000
        }
    ]


@pytest.fixture
def direccion_valida():
    """Datos de dirección de envío válidos."""
    return {
        'nombre': 'Nicolas Bocanegra',
        'telefono': '3001234567',
        'direccion': 'Calle 10 # 20-30',
        'ciudad': 'Bogotá',
        'notas': ''
    }


# ──────────────────────────────────────────────────────────────
# RF-15 | Pedido registrado en `orders` con estado RECIBIDO
# ──────────────────────────────────────────────────────────────

def test_WEB_CG_04_crear_pedido_estado_recibido(order_service, mock_db, items_validos, direccion_valida):
    """
    WEB-CG-04 (RF-15): Crear pedido exitoso y verificar estado inicial RECIBIDO.
    Resultado esperado: (True, msg, order) con order.estado == 'RECIBIDO'.
    """
    user_id = str(ObjectId())

    mock_db.orders.find_one.return_value = None  # número único no existe
    mock_db.orders.insert_one.return_value = MagicMock(inserted_id=ObjectId())

    success, message, order = order_service.create_order(user_id, items_validos, direccion_valida)

    assert success is True
    assert order is not None
    assert order.estado == Order.ESTADO_RECIBIDO


def test_WEB_CG_04_pedido_insertado_en_coleccion(order_service, mock_db, items_validos, direccion_valida):
    """
    WEB-CG-04 (RF-15): Verificar que insert_one() fue llamado sobre db.orders.
    Resultado esperado: la colección orders recibe el documento.
    """
    user_id = str(ObjectId())

    mock_db.orders.find_one.return_value = None
    mock_db.orders.insert_one.return_value = MagicMock(inserted_id=ObjectId())

    order_service.create_order(user_id, items_validos, direccion_valida)

    assert mock_db.orders.insert_one.called
    inserted_doc = mock_db.orders.insert_one.call_args[0][0]
    assert inserted_doc['estado'] == 'RECIBIDO'


def test_WEB_CG_04_pedido_sin_items_falla(order_service, direccion_valida):
    """
    WEB-CG-04 (RF-15): Crear pedido sin items debe fallar.
    Resultado esperado: (False, 'El pedido debe tener al menos un item', None).
    """
    user_id = str(ObjectId())

    success, message, order = order_service.create_order(user_id, [], direccion_valida)

    assert success is False
    assert order is None
    assert 'item' in message.lower()


def test_WEB_CG_04_pedido_direccion_incompleta_falla(order_service, mock_db, items_validos):
    """
    WEB-CG-04 (RF-15): Crear pedido con datos de envío incompletos debe fallar.
    Resultado esperado: (False, 'Datos de envío incompletos', None).
    """
    user_id = str(ObjectId())
    direccion_incompleta = {'nombre': 'Nicolas', 'telefono': ''}  # faltan campos

    success, message, order = order_service.create_order(user_id, items_validos, direccion_incompleta)

    assert success is False
    assert order is None
    assert 'envío' in message.lower() or 'incompleto' in message.lower()


# ──────────────────────────────────────────────────────────────
# Modelo Order — validación interna (Caja Gris)
# ─────────────────────────���────────────────────────────────────

def test_order_model_estado_inicial_recibido():
    """Verifica que un Order nuevo tenga estado RECIBIDO por defecto."""
    order = Order(
        numero_pedido='ORD-2026-000001',
        user_id=ObjectId(),
        items=[],
        total=0,
        direccion_envio={}
    )
    assert order.estado == 'RECIBIDO'


def test_order_model_historial_estado_inicial():
    """Verifica que el historial contenga el estado inicial RECIBIDO."""
    order = Order(
        numero_pedido='ORD-2026-000002',
        user_id=ObjectId(),
        items=[],
        total=0,
        direccion_envio={}
    )
    assert len(order.historial_estados) == 1
    assert order.historial_estados[0]['estado'] == 'RECIBIDO'


def test_order_model_cambiar_estado_valido():
    """Verifica que cambiar_estado() actualiza el estado correctamente."""
    order = Order(
        numero_pedido='ORD-2026-000003',
        user_id=ObjectId(),
        items=[],
        total=0,
        direccion_envio={}
    )
    result = order.cambiar_estado('ALISTAMIENTO', admin_id=ObjectId())
    assert result is True
    assert order.estado == 'ALISTAMIENTO'