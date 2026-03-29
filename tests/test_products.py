"""
Casos de Prueba – Caja Gris (WEB-CG-04 parcial: RF-14 stock)
Técnica: Caja Gris — combinación de prueba funcional + inspección interna del modelo.
Módulo: Productos (reducción de stock tras checkout)
"""

import pytest
from unittest.mock import MagicMock, patch
from bson import ObjectId
from app.models.product import Product
from app.services.product_service import ProductService


@pytest.fixture
def mock_db():
    """Base de datos MongoDB simulada."""
    db = MagicMock()
    db.products = MagicMock()
    return db


@pytest.fixture
def product_service(mock_db):
    """Instancia de ProductService con BD simulada."""
    return ProductService(mock_db)


@pytest.fixture
def producto_con_stock():
    """Producto de prueba con stock disponible."""
    return Product(
        nombre="Hoodie Clásico",
        descripcion="Hoodie de algodón",
        precio=80000,
        stock={'S': 5, 'M': 10, 'L': 3, 'XL': 0},
        colores=['Negro', 'Blanco'],
        _id=ObjectId()
    )


# ──────────────────────────────────────────────────────────────
# RF-14 | Reducción de stock tras checkout exitoso
# ──────────────────────────────────────────────────────────────

def test_reducir_stock_exitoso(product_service, mock_db, producto_con_stock):
    """
    WEB-CG-04 (RF-14): Reducir stock de una talla con unidades suficientes.
    Resultado esperado: stock disminuye correctamente, retorna (True, msg).
    """
    product_id = str(producto_con_stock._id)
    stock_inicial_m = producto_con_stock.stock['M']  # 10

    mock_db.products.find_one.return_value = producto_con_stock.to_dict()
    mock_db.products.update_one.return_value = MagicMock(modified_count=1)

    success, message = product_service.reducir_stock(product_id, 'M', 2)

    assert success is True
    assert mock_db.products.update_one.called


def test_reducir_stock_insuficiente(product_service, mock_db, producto_con_stock):
    """
    WEB-CG-04 (RF-14): Intento de reducir más stock del disponible.
    Resultado esperado: retorna (False, 'Stock insuficiente ...').
    """
    product_id = str(producto_con_stock._id)

    mock_db.products.find_one.return_value = producto_con_stock.to_dict()

    success, message = product_service.reducir_stock(product_id, 'XL', 1)

    assert success is False
    assert 'insuficiente' in message.lower() or 'XL' in message


def test_reducir_stock_producto_no_encontrado(product_service, mock_db):
    """
    WEB-CG-04 (RF-14): Reducir stock de un producto inexistente.
    Resultado esperado: retorna (False, 'Producto no encontrado').
    """
    mock_db.products.find_one.return_value = None

    success, message = product_service.reducir_stock(str(ObjectId()), 'M', 1)

    assert success is False
    assert 'no encontrado' in message.lower()


# ──────────────────────────────────────────────────────────────
# Modelo Product — validación interna (Caja Gris)
# ──────────────────────────────────────────────────────────────

def test_model_tiene_stock_true():
    """Verifica que tiene_stock() retorne True cuando hay unidades."""
    product = Product(
        nombre="Test",
        descripcion="Desc",
        precio=50000,
        stock={'M': 5},
        colores=[]
    )
    assert product.tiene_stock('M', 3) is True


def test_model_tiene_stock_false_sin_talla():
    """Verifica que tiene_stock() retorne False para talla sin stock."""
    product = Product(
        nombre="Test",
        descripcion="Desc",
        precio=50000,
        stock={'M': 0},
        colores=[]
    )
    assert product.tiene_stock('M', 1) is False


def test_model_reducir_stock_actualiza_valor():
    """Verifica que reducir_stock() descuenta la cantidad correcta."""
    product = Product(
        nombre="Test",
        descripcion="Desc",
        precio=50000,
        stock={'L': 8},
        colores=[]
    )
    result = product.reducir_stock('L', 3)
    assert result is True
    assert product.stock['L'] == 5