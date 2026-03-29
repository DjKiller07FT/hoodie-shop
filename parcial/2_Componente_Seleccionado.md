# COMPONENTE SELECCIONADO – FICHA TÉCNICA
## Parcial de Testing de Software – Ingeniería de Software II

**Estudiante:** Nicolas Camilo Bocanegra Vaca
**Fecha:** Marzo 2026
**Proyecto:** Hoodie Shop – E-commerce
**Repositorio:** https://github.com/DjKiller07FT/hoodie-shop

---

## B.1. Análisis del Componente Web Seleccionado

**Módulo seleccionado:** Gestión de Usuarios y Autenticación

---

### Ficha Técnica

| Elemento | Descripción |
|----------|-------------|
| **Componente / Frontend** | Templates Jinja2: `app/templates/auth/login.html`, `app/templates/auth/register.html` |
| **Controlador (Blueprint)** | `app/routes/auth.py` — Blueprint `auth` con prefijo `/auth` |
| **Modelo** | `app/models/user.py` — Clase `User` (hereda `UserMixin` de Flask-Login) |
| **Servicio** | `app/services/auth_service.py` — Clase `AuthService` |
| **Endpoint(s) Backend** | `GET/POST /auth/register`, `GET/POST /auth/login`, `GET /auth/logout` |
| **Métodos HTTP** | `GET` (renderizar formulario), `POST` (procesar datos del formulario) |
| **Base de datos** | MongoDB Atlas — Colección `users` |
| **Autenticación** | Flask-Login con sesiones firmadas por `SECRET_KEY` + `PBKDF2-SHA256` (Werkzeug) |
| **Decoradores de seguridad** | `@logout_required` (registro/login), `@login_required` (logout) |

---

### Esquema de Datos – Colección `users`

```json
{
  "_id": "ObjectId()",
  "nombre": "string (requerido)",
  "email": "string (requerido, único, normalizado a minúsculas)",
  "telefono": "string (requerido, formato colombiano 10 dígitos)",
  "direccion": "string (requerido)",
  "ciudad": "string (requerido)",
  "password_hash": "string (PBKDF2-SHA256, nunca texto plano)",
  "rol": "string ('user' | 'admin', default: 'user')",
  "created_at": "ISODate()",
  "updated_at": "ISODate()"
}
```

**Índice único:** Campo `email` — Previene duplicados a nivel de base de datos.

---

### Validaciones del Servicio `AuthService`

#### `register_user()`

| Validación | Mensaje de error |
|-----------|-----------------|
| Campos vacíos | `"Todos los campos son obligatorios"` |
| Formato de email inválido | `"Formato de email inválido"` |
| Contraseña < 6 caracteres | `"La contraseña debe tener al menos 6 caracteres"` |
| Email ya registrado | `"Este email ya está registrado"` |

#### `login_user()`

| Validación | Mensaje de error |
|-----------|-----------------|
| Email o password vacíos | `"Email y contraseña son requeridos"` |
| Email no existe en BD | `"Email o contraseña incorrectos"` |
| Contraseña incorrecta | `"Email o contraseña incorrectos"` |

---

### Flujo Crítico – Registro de Usuario

```
USUARIO (Browser)
      │
      │ 1. GET /auth/register
      ▼
FRONTEND (register.html)
      │ 2. Completa formulario: nombre, email, teléfono,
      │    dirección, ciudad, password, confirm_password
      │
      │ 3. POST /auth/register
      ▼
CONTROLADOR (routes/auth.py → register())
      │ 4. Valida: password == confirm_password
      │    Si no → flash error → re-render form
      │
      │ 5. Llama AuthService.register_user()
      ▼
SERVICIO (auth_service.py → register_user())
      │ 6. Valida campos obligatorios
      │ 7. Valida formato email (email-validator)
      │ 8. Valida longitud password >= 6 chars
      │ 9. Busca email en MongoDB (find_one)
      │    Si existe → return False, mensaje, None
      │
      │ 10. Crea User(), llama set_password() → PBKDF2-SHA256
      ▼
MODELO (models/user.py → User.set_password())
      │ 11. generate_password_hash(password) → almacena hash
      ▼
BASE DE DATOS (MongoDB Atlas → colección users)
      │ 12. insert_one(user.to_dict())
      ▼
SERVICIO → CONTROLADOR
      │ 13. return True, "Usuario registrado exitosamente", user
      │ 14. login_user(user, remember=True) → sesión activa
      │ 15. redirect → /catalog
      ▼
USUARIO (Browser)
      │ 16. Catálogo de productos con sesión iniciada
```

---

### Flujo Crítico – Inicio de Sesión

```
USUARIO (Browser)
      │
      │ 1. GET /auth/login
      ▼
FRONTEND (login.html)
      │ 2. Completa: email, password, [checkbox remember]
      │
      │ 3. POST /auth/login
      ▼
CONTROLADOR (routes/auth.py → login())
      │ 4. Llama AuthService.login_user(email, password)
      ▼
SERVICIO (auth_service.py → login_user())
      │ 5. Valida campos no vacíos
      │ 6. find_one({'email': email.lower()}) en MongoDB
      │    Si no existe → return False, "Email o contraseña incorrectos"
      │
      │ 7. User.from_dict(user_data) → instancia User
      │ 8. user.check_password(password) → check_password_hash()
      │    Si falla → return False, "Email o contraseña incorrectos"
      ▼
CONTROLADOR
      │ 9. login_user(user, remember=remember) → sesión Flask-Login
      │ 10. Redirige según rol:
      │     - rol='admin' → /admin/dashboard
      │     - rol='user'  → /catalog
      │     - ?next=URL   → URL solicitada originalmente
      ▼
USUARIO (Browser)
      │ 11. Dashboard (admin) o Catálogo (cliente)
```

---

### Tecnologías involucradas en el componente

| Capa | Tecnología | Versión | Rol |
|------|-----------|---------|-----|
| Frontend | Jinja2 Templates + Bootstrap 5.3 | 3.x / 5.3 | Formularios HTML con validación visual |
| Controlador | Flask Blueprints | 3.0.0 | Enrutamiento HTTP y lógica de control |
| Servicio | Python 3.14 | 3.14 | Lógica de negocio y validaciones |
| Seguridad | Werkzeug (PBKDF2-SHA256) | 3.0.1 | Hashing y verificación de contraseñas |
| Sesiones | Flask-Login | 0.6.3 | Gestión de sesiones autenticadas |
| Base de datos | MongoDB Atlas (PyMongo) | 4.6.1 | Persistencia de usuarios |
| Validación email | email-validator | 2.1.0 | Validación de formato de email |

---

### Archivos fuente del componente

| Archivo | URL GitHub |
|---------|-----------|
| `app/routes/auth.py` | https://github.com/DjKiller07FT/hoodie-shop/blob/main/app/routes/auth.py |
| `app/models/user.py` | https://github.com/DjKiller07FT/hoodie-shop/blob/main/app/models/user.py |
| `app/services/auth_service.py` | https://github.com/DjKiller07FT/hoodie-shop/blob/main/app/services/auth_service.py |
| `app/utils/decorators.py` | https://github.com/DjKiller07FT/hoodie-shop/blob/main/app/utils/decorators.py |
| `app/templates/auth/login.html` | https://github.com/DjKiller07FT/hoodie-shop/blob/main/app/templates/auth/login.html |
| `app/templates/auth/register.html` | https://github.com/DjKiller07FT/hoodie-shop/blob/main/app/templates/auth/register.html |