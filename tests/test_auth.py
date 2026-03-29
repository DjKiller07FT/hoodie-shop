"""
Casos de Prueba – Caja Negra (WEB-CN-01 a WEB-CN-05)
Técnica: Equivalencia de clases y valores límite desde la perspectiva del usuario.
Módulo: Autenticación (login y registro)
"""

import pytest
from unittest.mock import patch, MagicMock
from app import create_app


@pytest.fixture
def app():
    """Crea instancia de Flask en modo testing."""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'
    return app


@pytest.fixture
def client(app):
    """Crea cliente HTTP de prueba."""
    return app.test_client()


# ──────────────────────────────────────────────────────────────
# WEB-CN-01 | Login con credenciales válidas (RF-01)
# ──────────────────────────────────────────────────────────────

def test_WEB_CN_01_login_credenciales_validas(client):
    """
    WEB-CN-01: Login con email y contraseña correctos.
    Resultado esperado: HTTP 302, redirección al catálogo o dashboard.
    RF cubierto: RF-01
    """
    mock_user = MagicMock()
    mock_user.nombre = "Nicolas Bocanegra"
    mock_user.is_admin.return_value = False
    mock_user.is_active = True
    mock_user.is_authenticated = True
    mock_user.get_id.return_value = "507f1f77bcf86cd799439011"

    with patch('app.routes.auth.AuthService') as MockAuthService:
        mock_service = MockAuthService.return_value
        mock_service.login_user.return_value = (True, "Login exitoso", mock_user)

        response = client.post('/auth/login', data={
            'email': 'ftcamilo07@gmail.com',
            'password': 'password_correcto'
        }, follow_redirects=False)

    assert response.status_code == 302


# ──────────────────────────────────────────────────────────────
# WEB-CN-02 | Login con contraseña incorrecta (RF-02)
# ──────────────────────────────────────────────────────────────

def test_WEB_CN_02_login_contrasena_incorrecta(client):
    """
    WEB-CN-02: Login con contraseña incorrecta.
    Resultado esperado: HTTP 200, mensaje de error en la página.
    RF cubierto: RF-02
    """
    with patch('app.routes.auth.AuthService') as MockAuthService:
        mock_service = MockAuthService.return_value
        mock_service.login_user.return_value = (False, "Credenciales inválidas", None)

        response = client.post('/auth/login', data={
            'email': 'ftcamilo07@gmail.com',
            'password': 'contrasena_incorrecta'
        }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Credenciales inválidas'.encode() in response.data or b'danger' in response.data


# ──────────────────────────────────────────────────────────────
# WEB-CN-03 | Registro con email ya existente (RF-03)
# ──────────────────────────────────────────────────────────────

def test_WEB_CN_03_registro_email_ya_existente(client):
    """
    WEB-CN-03: Intento de registro con un email ya registrado.
    Resultado esperado: HTTP 200, mensaje de error indicando email duplicado.
    RF cubierto: RF-03
    """
    with patch('app.routes.auth.AuthService') as MockAuthService:
        mock_service = MockAuthService.return_value
        mock_service.register_user.return_value = (False, "El email ya está registrado", None)

        response = client.post('/auth/register', data={
            'nombre': 'Nicolas Bocanegra',
            'email': 'ftcamilo07@gmail.com',
            'telefono': '3001234567',
            'direccion': 'Calle 10 # 20-30',
            'ciudad': 'Bogotá',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)

    assert response.status_code == 200
    assert 'El email ya está registrado'.encode() in response.data or b'danger' in response.data


# ──────────────────────────────────────────────────────────────
# WEB-CN-04 | Registro con contraseñas que no coinciden (RF-04)
# ──────────────────────────────────────────────────────────────

def test_WEB_CN_04_registro_contrasenas_no_coinciden(client):
    """
    WEB-CN-04: Registro con confirm_password distinto a password.
    Resultado esperado: HTTP 200, mensaje 'Las contraseñas no coinciden'.
    RF cubierto: RF-04
    """
    response = client.post('/auth/register', data={
        'nombre': 'Nicolas Bocanegra',
        'email': 'nuevo@gmail.com',
        'telefono': '3001234567',
        'direccion': 'Calle 10 # 20-30',
        'ciudad': 'Bogotá',
        'password': 'password123',
        'confirm_password': 'diferente456'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Las contraseñas no coinciden'.encode() in response.data


# ──────────────────────────────────────────────────────────────
# WEB-CN-05 | Ruta protegida sin sesión activa (RF-05)
# ──────────────────────────────────────────────────────────────

def test_WEB_CN_05_ruta_protegida_sin_sesion(client):
    """
    WEB-CN-05: Acceso a ruta privada sin estar autenticado.
    Resultado esperado: HTTP 302, redirección a /auth/login.
    RF cubierto: RF-05
    """
    response = client.get('/user/profile', follow_redirects=False)

    assert response.status_code == 302
    assert '/auth/login' in response.headers.get('Location', '')