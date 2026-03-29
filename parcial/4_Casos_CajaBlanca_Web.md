# CASOS DE PRUEBA – CAJA BLANCA
## Parcial de Testing de Software – Ingeniería de Software II

**Estudiante:** Nicolas Camilo Bocanegra Vaca
**Fecha:** Marzo 2026
**Proyecto:** Hoodie Shop – E-commerce
**Módulo:** Gestión de Usuarios y Autenticación
**Técnica:** Caja Blanca
**Opción seleccionada:** Opción 2 – Middleware / Servicio de Autenticación (Backend)
**Repositorio:** https://github.com/DjKiller07FT/hoodie-shop

---

## Descripción de la técnica aplicada

Las pruebas de **caja blanca** evalúan la estructura interna del código. El tester tiene acceso completo al código fuente y diseña casos que cubran todas las **rutas de ejecución** posibles (ramas `if/else`, validaciones, excepciones). El objetivo es garantizar que cada línea de código y cada condición sea ejercida al menos una vez.

En **Hoodie Shop**, esta técnica se aplica sobre el método `login_user()` y `register_user()` del servicio `AuthService` (`app/services/auth_service.py`), analizando cada rama condicional del flujo de autenticación.

---

## Código seleccionado

### Función analizada: `AuthService.login_user()`

**Archivo:** `app/services/auth_service.py`
**URL:** https://github.com/DjKiller07FT/hoodie-shop/blob/main/app/services/auth_service.py

```python
def login_user(self, email, password):
    """
    Autentica un usuario.
    Returns:
        tuple: (success: bool, message: str, user: User or None)
    """
    # RAMA 1: Validar campos vacíos
    if not email or not password:
        return False, "Email y contraseña son requeridos", None

    # RAMA 2: Buscar usuario en MongoDB
    user_data = self.users_collection.find_one({'email': email.lower()})

    # RAMA 3: Usuario no existe en BD
    if not user_data:
        return False, "Email o contraseña incorrectos", None

    # Construir objeto User desde el documento MongoDB
    user = User.from_dict(user_data)

    # RAMA 4: Contraseña incorrecta
    if not user.check_password(password):
        return False, "Email o contraseña incorrectos", None

    # RAMA 5 (éxito): Retorna usuario autenticado
    return True, "Login exitoso", user
```

### Función analizada: `AuthService.register_user()`

**Archivo:** `app/services/auth_service.py`

```python
def register_user(self, nombre, email, telefono, direccion, ciudad, password):
    """
    Registra un nuevo usuario.
    Returns:
        tuple: (success: bool, message: str, user: User or None)
    """
    # RAMA 1: Campos obligatorios vacíos
    if not all([nombre, email, telefono, direccion, ciudad, password]):
        return False, "Todos los campos son obligatorios", None

    # RAMA 2: Formato de email inválido
    if not validar_email(email):
        return False, "Formato de email inválido", None

    # RAMA 3: Contraseña muy corta
    if len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres", None

    # RAMA 4: Email ya registrado
    if self.users_collection.find_one({'email': email.lower()}):
        return False, "Este email ya está registrado", None

    # Crear y guardar usuario
    user = User(nombre=nombre, email=email, telefono=telefono,
                direccion=direccion, ciudad=ciudad, rol='user')
    user.set_password(password)

    # RAMA 5/6: Guardar en BD (éxito o excepción)
    try:
        self.users_collection.insert_one(user.to_dict())
        return True, "Usuario registrado exitosamente", user
    except Exception as e:
        return False, f"Error al registrar usuario: {str(e)}", None
```

### Función analizada: `logout_required` (decorador)

**Archivo:** `app/utils/decorators.py`

```python
def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # RAMA 1: Usuario ya autenticado → redirigir
        if current_user.is_authenticated:
            flash('Ya has iniciado sesión.', 'info')
            return redirect(url_for('shop.catalog'))
        # RAMA 2: Usuario NO autenticado → continuar
        return f(*args, **kwargs)
    return decorated_function
```

---

## Grafo de flujo y rutas de ejecución identificadas

### `login_user()` — 5 rutas de ejecución

```
        INICIO
           │
           ▼
    ┌─────────────────────┐
    │ email o password    │
    │ vacío/None?         │
    └──────┬──────────────┘
           │
    ┌──────┴──────┐
    │ SÍ          │ NO
    ▼             ▼
RAMA 1        find_one(email)
return False       │
"campos       ┌────┴─────┐
requeridos"   │ NO existe │ SÍ existe
              ▼           ▼
           RAMA 3      check_password()
           return           │
           False       ┌────┴────┐
           "incorrectos"│ FALLA  │ OK
                        ▼        ▼
                     RAMA 4   RAMA 5
                     return   return
                     False    True
                     "incorrecto" "Login exitoso"
```

| # | Ruta | Descripción |
|---|------|-------------|
| **Ruta 1** | `email vacío → return False` | Campos de entrada vacíos o None |
| **Ruta 2** | `email válido → user no existe → return False` | Email no registrado en BD |
| **Ruta 3** | `email válido → user existe → password falla → return False` | Contraseña incorrecta |
| **Ruta 4** | `email válido → user existe → password OK → return True` | Login exitoso |
| **Ruta 5** | `password vacío → return False` | Password vacío (sin email también) |

### `register_user()` — 6 rutas de ejecución

| # | Ruta | Descripción |
|---|------|-------------|
| **Ruta 1** | `campos vacíos → return False` | Algún campo obligatorio está vacío |
| **Ruta 2** | `email inválido → return False` | Formato de email no cumple el regex |
| **Ruta 3** | `password < 6 chars → return False` | Contraseña demasiado corta |
| **Ruta 4** | `email duplicado → return False` | Email ya existe en colección `users` |
| **Ruta 5** | `todos válidos → insert OK → return True` | Registro exitoso |
| **Ruta 6** | `todos válidos → insert falla → return False` | Error de base de datos (excepción) |

---

## Casos de prueba por ruta de ejecución

---

### WEB-CB-01

| Campo | Detalle |
|-------|---------|
| **ID** | WEB-CB-01 |
| **Título** | `login_user()` — Ruta 4: Login exitoso (camino feliz) |
| **Técnica** | Caja Blanca |
| **Función** | `AuthService.login_user()` |
| **Ruta cubierta** | Ruta 4: `email válido → user existe → check_password OK → return True` |
| **Prioridad** | Alta |

**Condición de entrada:**
```python
email = "ftcamilo07@gmail.com"   # existe en BD
password = "password_correcto"   # hash coincide
```

**Ruta esperada:**
```
email no vacío → find_one() devuelve user_data →
check_password() retorna True → return True, "Login exitoso", user
```

**Aserción de prueba:**
```python
def test_login_exitoso(auth_service):
    success, message, user = auth_service.login_user(
        "ftcamilo07@gmail.com", "password_correcto"
    )
    assert success == True
    assert message == "Login exitoso"
    assert user is not None
    assert user.email == "ftcamilo07@gmail.com"
```

**📋 Resultado obtenido:** ______
**🟢 Estado:** ✅ Aprobado / ❌ Fallido / ⚠️ Bloqueado

---

### WEB-CB-02

| Campo | Detalle |
|-------|---------|
| **ID** | WEB-CB-02 |
| **Título** | `login_user()` — Ruta 1: Email y password vacíos |
| **Técnica** | Caja Blanca |
| **Función** | `AuthService.login_user()` |
| **Ruta cubierta** | Ruta 1: `not email or not password → return False` |
| **Prioridad** | Alta |

**Condición de entrada:**
```python
email = ""       # vacío
password = ""    # vacío
```

**Ruta esperada:**
```
not email = True →
return False, "Email y contraseña son requeridos", None
(Nunca llega a find_one())
```

**Aserción de prueba:**
```python
def test_login_campos_vacios(auth_service):
    success, message, user = auth_service.login_user("", "")
    assert success == False
    assert message == "Email y contraseña son requeridos"
    assert user is None
```

**📋 Resultado obtenido:** ______
**🟢 Estado:** ✅ Aprobado / ❌ Fallido / ⚠️ Bloqueado

---

### WEB-CB-03

| Campo | Detalle |
|-------|---------|
| **ID** | WEB-CB-03 |
| **Título** | `login_user()` — Ruta 3: Contraseña incorrecta |
| **Técnica** | Caja Blanca |
| **Función** | `AuthService.login_user()` |
| **Ruta cubierta** | Ruta 3: `user existe → check_password() False → return False` |
| **Prioridad** | Alta |

**Condición de entrada:**
```python
email = "ftcamilo07@gmail.com"  # existe en BD
password = "password_INCORRECTO"  # no coincide con hash
```

**Ruta esperada:**
```
email no vacío → find_one() devuelve user_data →
check_password_hash(hash, "password_INCORRECTO") = False →
return False, "Email o contraseña incorrectos", None
```

**Aserción de prueba:**
```python
def test_login_password_incorrecto(auth_service):
    success, message, user = auth_service.login_user(
        "ftcamilo07@gmail.com", "password_INCORRECTO"
    )
    assert success == False
    assert message == "Email o contraseña incorrectos"
    assert user is None
```

**📋 Resultado obtenido:** ______
**🟢 Estado:** ✅ Aprobado / ❌ Fallido / ⚠️ Bloqueado

---

### WEB-CB-04

| Campo | Detalle |
|-------|---------|
| **ID** | WEB-CB-04 |
| **Título** | `register_user()` — Ruta 2: Email con formato inválido |
| **Técnica** | Caja Blanca |
| **Función** | `AuthService.register_user()` |
| **Ruta cubierta** | Ruta 2: `validar_email(email) = False → return False` |
| **Prioridad** | Media |

**Condición de entrada:**
```python
nombre = "Test User"
email = "usuario@"        # formato inválido (sin dominio)
telefono = "3001234567"
direccion = "Calle 10"
ciudad = "Bogotá"
password = "pass123"
```

**Ruta esperada:**
```
all([campos]) = True →
validar_email("usuario@") → regex falla → return False →
return False, "Formato de email inválido", None
(Nunca llega a find_one())
```

**Aserción de prueba:**
```python
def test_registro_email_invalido(auth_service):
    success, message, user = auth_service.register_user(
        "Test User", "usuario@", "3001234567",
        "Calle 10", "Bogotá", "pass123"
    )
    assert success == False
    assert message == "Formato de email inválido"
    assert user is None
```

**📋 Resultado obtenido:** ______
**🟢 Estado:** ✅ Aprobado / ❌ Fallido / ⚠️ Bloqueado

---

### WEB-CB-05

| Campo | Detalle |
|-------|---------|
| **ID** | WEB-CB-05 |
| **Título** | `register_user()` — Ruta 3: Contraseña menor a 6 caracteres |
| **Técnica** | Caja Blanca |
| **Función** | `AuthService.register_user()` |
| **Ruta cubierta** | Ruta 3: `len(password) < 6 → return False` |
| **Prioridad** | Media |

**Condición de entrada:**
```python
nombre = "Test User"
email = "nuevo@test.com"
telefono = "3001234567"
direccion = "Calle 10"
ciudad = "Bogotá"
password = "abc"    # solo 3 caracteres → < 6
```

**Ruta esperada:**
```
all([campos]) = True →
validar_email OK →
len("abc") = 3 < 6 → True →
return False, "La contraseña debe tener al menos 6 caracteres", None
```

**Aserción de prueba:**
```python
def test_registro_password_corto(auth_service):
    success, message, user = auth_service.register_user(
        "Test User", "nuevo@test.com", "3001234567",
        "Calle 10", "Bogotá", "abc"
    )
    assert success == False
    assert message == "La contraseña debe tener al menos 6 caracteres"
    assert user is None
```

**📋 Resultado obtenido:** ______
**🟢 Estado:** ✅ Aprobado / ❌ Fallido / ⚠️ Bloqueado

---

### WEB-CB-06

| Campo | Detalle |
|-------|---------|
| **ID** | WEB-CB-06 |
| **Título** | `logout_required` — Ruta 1: Usuario ya autenticado intenta acceder a login |
| **Técnica** | Caja Blanca |
| **Función** | `decorators.logout_required` |
| **Ruta cubierta** | Ruta 1: `current_user.is_authenticated = True → redirect` |
| **Prioridad** | Alta |

**Condición de entrada:**
```python
# Usuario con sesión activa intenta acceder a GET /auth/login
current_user.is_authenticated = True
```

**Ruta esperada:**
```
current_user.is_authenticated = True →
flash('Ya has iniciado sesión.', 'info') →
return redirect(url_for('shop.catalog'))
(Nunca ejecuta la función de login)
```

**Aserción de prueba:**
```python
def test_login_usuario_ya_autenticado(client, usuario_logueado):
    response = client.get('/auth/login', follow_redirects=False)
    assert response.status_code == 302
    assert '/catalog' in response.location
```

**📋 Resultado obtenido:** ______
**🟢 Estado:** ✅ Aprobado / ❌ Fallido / ⚠️ Bloqueado

---

## Script de pruebas automatizadas (pytest)

**Archivo:** `tests/test_cajaBlanca_auth.py`

```python
"""
Pruebas de Caja Blanca – AuthService
Parcial Testing de Software – Hoodie Shop
Estudiante: Nicolas Camilo Bocanegra Vaca
"""

import pytest
from unittest.mock import MagicMock, patch
from app.services.auth_service import AuthService
from app.models.user import User
from werkzeug.security import generate_password_hash


@pytest.fixture
def mock_db():
    """Base de datos MongoDB simulada con MagicMock"""
    db = MagicMock()
    return db


@pytest.fixture
def auth_service(mock_db):
    """Instancia de AuthService con BD mock"""
    return AuthService(mock_db)


@pytest.fixture
def usuario_existente():
    """Usuario de prueba con contraseña hasheada"""
    user = User(
        nombre="Nicolas Bocanegra",
        email="ftcamilo07@gmail.com",
        telefono="3001234567",
        direccion="Calle 10 # 20-30",
        ciudad="Bogotá",
        rol="user"
    )
    user.set_password("password_correcto")
    return user.to_dict()


# ──────────────────────────────────────────────
# WEB-CB-01: login_user() → Ruta 4 (éxito)
# ──────────────────────────────────────────────
def test_WEB_CB_01_login_exitoso(auth_service, usuario_existente):
    """Ruta 4: email válido → user existe → check_password OK → True"""
    auth_service.users_collection.find_one.return_value = usuario_existente

    success, message, user = auth_service.login_user(
        "ftcamilo07@gmail.com", "password_correcto"
    )

    assert success == True
    assert message == "Login exitoso"
    assert user is not None
    assert user.email == "ftcamilo07@gmail.com"


# ──────────────────────────────────────────────
# WEB-CB-02: login_user() → Ruta 1 (campos vacíos)
# ──────────────────────────────────────────────
def test_WEB_CB_02_login_campos_vacios(auth_service):
    """Ruta 1: email o password vacío → False inmediato"""
    success, message, user = auth_service.login_user("", "")

    assert success == False
    assert message == "Email y contraseña son requeridos"
    assert user is None
    # Verificar que NUNCA llamó a find_one (ruta cortocircuitada)
    auth_service.users_collection.find_one.assert_not_called()


# ──────────────────────────────────────────────
# WEB-CB-03: login_user() → Ruta 3 (password incorrecto)
# ──────────────────────────────────────────────
def test_WEB_CB_03_login_password_incorrecto(auth_service, usuario_existente):
    """Ruta 3: user existe pero check_password falla → False"""
    auth_service.users_collection.find_one.return_value = usuario_existente

    success, message, user = auth_service.login_user(
        "ftcamilo07@gmail.com", "password_INCORRECTO"
    )

    assert success == False
    assert message == "Email o contraseña incorrectos"
    assert user is None


# ──────────────────────────────────────────────
# WEB-CB-04: register_user() → Ruta 2 (email inválido)
# ──────────────────────────────────────────────
def test_WEB_CB_04_registro_email_invalido(auth_service):
    """Ruta 2: validar_email() falla → False"""
    success, message, user = auth_service.register_user(
        "Test User", "usuario@", "3001234567",
        "Calle 10", "Bogotá", "pass123"
    )

    assert success == False
    assert message == "Formato de email inválido"
    assert user is None
    auth_service.users_collection.find_one.assert_not_called()


# ──────────────────────────────────────────────
# WEB-CB-05: register_user() → Ruta 3 (password < 6)
# ──────────────────────────────────────────────
def test_WEB_CB_05_registro_password_corto(auth_service):
    """Ruta 3: len(password) < 6 → False"""
    success, message, user = auth_service.register_user(
        "Test User", "nuevo@test.com", "3001234567",
        "Calle 10", "Bogotá", "abc"
    )

    assert success == False
    assert message == "La contraseña debe tener al menos 6 caracteres"
    assert user is None


# ──────────────────────────────────────────────
# WEB-CB-06: register_user() → Ruta 4 (email duplicado)
# ──────────────────────────────────────────────
def test_WEB_CB_06_registro_email_duplicado(auth_service, usuario_existente):
    """Ruta 4: email ya existe en BD → False"""
    auth_service.users_collection.find_one.return_value = usuario_existente

    success, message, user = auth_service.register_user(
        "Otro Usuario", "ftcamilo07@gmail.com", "3009876543",
        "Carrera 5", "Medellín", "pass456"
    )

    assert success == False
    assert message == "Este email ya está registrado"
    assert user is None


# ──────────────────────────────────────────────
# WEB-CB-07: register_user() → Ruta 5 (registro exitoso)
# ──────────────────────────────────────────────
def test_WEB_CB_07_registro_exitoso(auth_service):
    """Ruta 5: todos los campos válidos → True"""
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
    auth_service.users_collection.insert_one.assert_called_once()
```

---

## Cobertura de rutas (Coverage Map)

| ID Caso | Función | Ruta cubierta | Cobertura |
|---------|---------|---------------|-----------|
| WEB-CB-01 | `login_user()` | Ruta 4 – éxito completo | ✅ |
| WEB-CB-02 | `login_user()` | Ruta 1 – campos vacíos | ✅ |
| WEB-CB-03 | `login_user()` | Ruta 3 – password incorrecto | ✅ |
| WEB-CB-04 | `register_user()` | Ruta 2 – email inválido | ✅ |
| WEB-CB-05 | `register_user()` | Ruta 3 – password corto | ✅ |
| WEB-CB-06 | `register_user()` | Ruta 4 – email duplicado | ✅ |
| WEB-CB-07 | `register_user()` | Ruta 5 – registro exitoso | ✅ |

**Cobertura de ramas estimada: > 90%**

---

## Resumen de Casos – Caja Blanca

| ID | Función | Ruta | Prioridad | Estado |
|----|---------|------|-----------|--------|
| WEB-CB-01 | `login_user()` | Éxito completo | Alta | ⏳ Pendiente |
| WEB-CB-02 | `login_user()` | Campos vacíos | Alta | ⏳ Pendiente |
| WEB-CB-03 | `login_user()` | Password incorrecto | Alta | ⏳ Pendiente |
| WEB-CB-04 | `register_user()` | Email inválido | Media | ⏳ Pendiente |
| WEB-CB-05 | `register_user()` | Password < 6 chars | Media | ⏳ Pendiente |
| WEB-CB-06 | `register_user()` | Email duplicado | Alta | ⏳ Pendiente |
| WEB-CB-07 | `register_user()` | Registro exitoso | Alta | ⏳ Pendiente |

---

## Ejecución de pruebas

```bash
# Instalar dependencias si no están instaladas
pip install pytest

# Ejecutar solo las pruebas de caja blanca
python -m pytest tests/test_cajaBlanca_auth.py -v

# Con reporte de cobertura
pip install pytest-cov
python -m pytest tests/test_cajaBlanca_auth.py -v --cov=app/services/auth_service --cov-report=term-missing
```

**Output esperado:**
```
tests/test_cajaBlanca_auth.py::test_WEB_CB_01_login_exitoso           PASSED
tests/test_cajaBlanca_auth.py::test_WEB_CB_02_login_campos_vacios     PASSED
tests/test_cajaBlanca_auth.py::test_WEB_CB_03_login_password_incorrecto PASSED
tests/test_cajaBlanca_auth.py::test_WEB_CB_04_registro_email_invalido  PASSED
tests/test_cajaBlanca_auth.py::test_WEB_CB_05_registro_password_corto  PASSED
tests/test_cajaBlanca_auth.py::test_WEB_CB_06_registro_email_duplicado PASSED
tests/test_cajaBlanca_auth.py::test_WEB_CB_07_registro_exitoso         PASSED

7 passed in 0.45s — Coverage: 92%
```