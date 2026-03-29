"""
Pruebas de Caja Blanca  AuthService
Parcial Testing de Software  Ingeniería de Software II
Estudiante: Nicolas Camilo Bocanegra Vaca
Proyecto: Hoodie Shop  E-commerce
Repositorio: https://github.com/DjKiller07FT/hoodie-shop

Ejecución:
    python -m pytest tests/test_cajaBlanca_auth.py -v
    python -m pytest tests/test_cajaBlanca_auth.py -v --cov=app/services/auth_service --cov-report=term-missing
"""

import pytest
from unittest.mock import MagicMock
from werkzeug.security import generate_password_hash

from app.services.auth_service import AuthService
from app.models.user import User


# ──────────────────────────────────────────────────────────────
# FIXTURES
# ──────────────────────────────────────────────────────────────

@pytest.fixture
def mock_db():
    """
    Simula la conexión a MongoDB con MagicMock.
    Evita dependencia de MongoDB Atlas en las pruebas unitarias.
    """
    db = MagicMock()
    db.users = MagicMock()
    return db


@pytest.fixture
def auth_service(mock_db):
    """
    Instancia de AuthService conectada a la BD simulada.
    """
    return AuthService(mock_db)


@pytest.fixture
def usuario_existente():
    """
    Documento MongoDB simulado de un usuario válido con contraseña hasheada.
    Representa lo que devolvería find_one() desde la colección users.
    """
    from bson import ObjectId
    from datetime import datetime

    user = User(
        nombre="Nicolas Bocanegra",
        email="ftcamilo07@gmail.com",
        telefono="3001234567",
        direccion="Calle 10 # 20-30",
        ciudad="Bogotá",
        rol="user",
        _id=ObjectId()
    )
    user.set_password("password_correcto")

    doc = user.to_dict()
    doc['created_at'] = datetime.utcnow()
    doc['updated_at'] = datetime.utcnow()
    return doc


# ──────────────────────────────────────────────────────────────
# LOGIN_USER — PRUEBAS DE CAJA BLANCA
# ──────────────────────────────────────────────────────────────

class TestLoginUser:
    """
    Pruebas unitarias sobre AuthService.login_user()
    Cubre todas las ramas del flujo de autenticación.
    """

    def test_WEB_CB_01_login_exitoso(self, auth_service, usuario_existente):
        """
        WEB-CB-01: Ruta 4 — email válido → user existe → check_password OK → True
        Camino feliz: credenciales correctas.
        """
        auth_service.users_collection.find_one.return_value = usuario_existente

        success, message, user = auth_service.login_user(
            "ftcamilo07@gmail.com", "password_correcto"
        )

        assert success == True
        assert message == "Login exitoso"
        assert user is not None
        assert user.email == "ftcamilo07@gmail.com"
        # Verificar que SÍ consultó la BD
        auth_service.users_collection.find_one.assert_called_once_with(
            {'email': 'ftcamilo07@gmail.com'}
        )

    def test_WEB_CB_02_login_email_vacio(self, auth_service):
        """
        WEB-CB-02: Ruta 1 — email vacío → False inmediato sin consultar BD.
        """
        success, message, user = auth_service.login_user("", "password123")

        assert success == False
        assert message == "Email y contraseña son requeridos"
        assert user is None
        # NUNCA debe consultar la BD cuando los campos están vacíos
        auth_service.users_collection.find_one.assert_not_called()

    def test_WEB_CB_03_login_password_vacio(self, auth_service):
        """
        WEB-CB-02 variante: Ruta 1 — password vacío → False inmediato.
        """
        success, message, user = auth_service.login_user("ftcamilo07@gmail.com", "")

        assert success == False
        assert message == "Email y contraseña son requeridos"
        assert user is None
        auth_service.users_collection.find_one.assert_not_called()

    def test_WEB_CB_04_login_ambos_vacios(self, auth_service):
        """
        WEB-CB-02 variante: Ruta 1 — email Y password vacíos → False inmediato.
        """
        success, message, user = auth_service.login_user("", "")

        assert success == False
        assert message == "Email y contraseña son requeridos"
        assert user is None

    def test_WEB_CB_05_login_usuario_no_existe(self, auth_service):
        """
        Ruta 2 — email no registrado en BD → find_one devuelve None → False.
        """
        auth_service.users_collection.find_one.return_value = None

        success, message, user = auth_service.login_user(
            "noexiste@test.com", "password123"
        )

        assert success == False
        assert message == "Email o contraseña incorrectos"
        assert user is None

    def test_WEB_CB_06_login_password_incorrecto(self, auth_service, usuario_existente):
        """
        WEB-CB-03: Ruta 3 — user existe pero check_password falla → False.
        """
        auth_service.users_collection.find_one.return_value = usuario_existente

        success, message, user = auth_service.login_user(
            "ftcamilo07@gmail.com", "password_INCORRECTO"
        )

        assert success == False
        assert message == "Email o contraseña incorrectos"
        assert user is None

    def test_WEB_CB_07_login_email_normalizado_mayusculas(self, auth_service, usuario_existente):
        """
        Verifica que el email se normaliza a minúsculas antes de buscar en BD.
        El sistema debe encontrar al usuario aunque el email llegue en mayúsculas.
        """
        auth_service.users_collection.find_one.return_value = usuario_existente

        success, message, user = auth_service.login_user(
            "FTCAMILO07@GMAIL.COM", "password_correcto"
        )

        assert success == True
        # Verificar que find_one fue llamado con email en minúsculas
        auth_service.users_collection.find_one.assert_called_once_with(
            {'email': 'ftcamilo07@gmail.com'}
        )


# ──────────────────────────────────────────────────────────────
# REGISTER_USER — PRUEBAS DE CAJA BLANCA
# ──────────────────────────────────────────────────────────────

class TestRegisterUser:
    """
    Pruebas unitarias sobre AuthService.register_user()
    Cubre todas las ramas del flujo de registro.
    """

    def test_WEB_CB_08_registro_campos_vacios(self, auth_service):
        """
        WEB-CB-04 variante: Ruta 1 — algún campo vacío → False inmediato.
        """
        success, message, user = auth_service.register_user(
            "", "nuevo@test.com", "3001234567",
            "Calle 10", "Bogotá", "pass123"
        )

        assert success == False
        assert message == "Todos los campos son obligatorios"
        assert user is None
        auth_service.users_collection.find_one.assert_not_called()

    def test_WEB_CB_09_registro_email_invalido(self, auth_service):
        """
        WEB-CB-04: Ruta 2 — validar_email() falla → False.
        Formatos probados: sin dominio, sin @, sin TLD.
        """
        emails_invalidos = [
            "usuario@",         # sin dominio
            "usuariosinAt",     # sin @
            "usuario@.com",     # dominio vacío
            "@dominio.com",     # sin usuario
        ]

        for email_invalido in emails_invalidos:
            success, message, user = auth_service.register_user(
                "Test User", email_invalido, "3001234567",
                "Calle 10", "Bogotá", "pass123"
            )
            assert success == False, f"Debió fallar con email: {email_invalido}"
            assert message == "Formato de email inválido"
            assert user is None

    def test_WEB_CB_10_registro_password_corto(self, auth_service):
        """
        WEB-CB-05: Ruta 3 — len(password) < 6 → False.
        Prueba con 1, 3 y 5 caracteres (todos < 6).
        """
        passwords_cortos = ["a", "abc", "12345"]

        for pwd in passwords_cortos:
            success, message, user = auth_service.register_user(
                "Test User", "nuevo@test.com", "3001234567",
                "Calle 10", "Bogotá", pwd
            )
            assert success == False, f"Debió fallar con password: '{pwd}'"
            assert message == "La contraseña debe tener al menos 6 caracteres"
            assert user is None

    def test_WEB_CB_11_registro_password_exactamente_6(self, auth_service):
        """
        Valor límite: password con exactamente 6 caracteres → debe pasar la validación.
        """
        auth_service.users_collection.find_one.return_value = None
        auth_service.users_collection.insert_one.return_value = MagicMock()

        success, message, user = auth_service.register_user(
            "Test User", "nuevo@test.com", "3001234567",
            "Calle 10", "Bogotá", "abc123"  # exactamente 6 chars
        )

        assert success == True
        assert message == "Usuario registrado exitosamente"

    def test_WEB_CB_12_registro_email_duplicado(self, auth_service, usuario_existente):
        """
        WEB-CB-06: Ruta 4 — email ya existe en BD → False.
        """
        auth_service.users_collection.find_one.return_value = usuario_existente

        success, message, user = auth_service.register_user(
            "Otro Usuario", "ftcamilo07@gmail.com", "3009876543",
            "Carrera 5", "Medellín", "pass456"
        )

        assert success == False
        assert message == "Este email ya está registrado"
        assert user is None

    def test_WEB_CB_13_registro_exitoso(self, auth_service):
        """
        WEB-CB-07: Ruta 5 — todos los campos válidos → insert_one → True.
        """
        auth_service.users_collection.find_one.return_value = None
        auth_service.users_collection.insert_one.return_value = MagicMock()

        success, message, user = auth_service.register_user(
            "Nicolas Bocanegra", "nuevo@test.com", "3001234567",
            "Calle 10 # 20-30", "Bogotá", "pass123"
        )

        assert success == True
        assert message == "Usuario registrado exitosamente"
        assert user is not None
        assert user.email == "nuevo@test.com"
        assert user.rol == "user"
        # Verificar que la contraseña se hasheó (nunca texto plano)
        assert user.password_hash != "pass123"
        assert user.password_hash.startswith("pbkdf2:sha256:") or \
        user.password_hash.startswith("scrypt:")
        # Verificar que SÍ se insertó en BD
        auth_service.users_collection.insert_one.assert_called_once()

    def test_WEB_CB_14_registro_error_base_datos(self, auth_service):
        """
        Ruta 6 — insert_one lanza excepción → False con mensaje de error.
        """
        auth_service.users_collection.find_one.return_value = None
        auth_service.users_collection.insert_one.side_effect = Exception(
            "Connection timeout"
        )

        success, message, user = auth_service.register_user(
            "Test User", "nuevo@test.com", "3001234567",
            "Calle 10", "Bogotá", "pass123"
        )

        assert success == False
        assert "Error al registrar usuario" in message
        assert user is None


# ──────────────────────────────────────────────────────────────
# USER MODEL — PRUEBAS DE CAJA BLANCA
# ──────────────────────────────────────────────────────────────

class TestUserModel:
    """
    Pruebas sobre el modelo User: set_password, check_password, is_admin.
    """

    def test_WEB_CB_15_password_se_hashea_correctamente(self):
        """
        Verifica que set_password() almacena hash PBKDF2-SHA256, nunca texto plano.
        """
        user = User(
            nombre="Test", email="test@test.com", telefono="3001234567",
            direccion="Calle 1", ciudad="Bogotá"
        )
        user.set_password("MiPassword123")

        assert user.password_hash is not None
        assert user.password_hash != "MiPassword123"
        assert user.password_hash.startswith("pbkdf2:sha256:") or \
        user.password_hash.startswith("scrypt:")

    def test_WEB_CB_16_check_password_correcto(self):
        """
        Verifica que check_password() retorna True con la contraseña original.
        """
        user = User(
            nombre="Test", email="test@test.com", telefono="3001234567",
            direccion="Calle 1", ciudad="Bogotá"
        )
        user.set_password("MiPassword123")

        assert user.check_password("MiPassword123") == True

    def test_WEB_CB_17_check_password_incorrecto(self):
        """
        Verifica que check_password() retorna False con contraseña incorrecta.
        """
        user = User(
            nombre="Test", email="test@test.com", telefono="3001234567",
            direccion="Calle 1", ciudad="Bogotá"
        )
        user.set_password("MiPassword123")

        assert user.check_password("PasswordIncorrecto") == False

    def test_WEB_CB_18_is_admin_rol_admin(self):
        """
        Verifica que is_admin() retorna True solo con rol='admin'.
        """
        user = User(
            nombre="Admin", email="admin@test.com", telefono="3001234567",
            direccion="Calle 1", ciudad="Bogotá", rol="admin"
        )
        assert user.is_admin() == True

    def test_WEB_CB_19_is_admin_rol_user(self):
        """
        Verifica que is_admin() retorna False con rol='user'.
        """
        user = User(
            nombre="Cliente", email="user@test.com", telefono="3001234567",
            direccion="Calle 1", ciudad="Bogotá", rol="user"
        )
        assert user.is_admin() == False

    def test_WEB_CB_20_email_normalizado_minusculas(self):
        """
        Verifica que el email se normaliza a minúsculas en el constructor.
        """
        user = User(
            nombre="Test", email="TEST@GMAIL.COM", telefono="3001234567",
            direccion="Calle 1", ciudad="Bogotá"
        )
        assert user.email == "test@gmail.com"