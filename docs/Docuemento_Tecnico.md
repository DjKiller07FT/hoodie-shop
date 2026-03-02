# DOCUMENTO TÉCNICO DE SOFTWARE

**Proyecto: Hoodie Shop – E-commerce**
**Versión 1.0**
**Fecha: Marzo 2026**
**Autor: Nicolas Camilo Bocanegra Vaca**
**Repositorio: https://github.com/DjKiller07FT/hoodie-shop**

---

## Tabla de Contenido

1. [Introducción](#1-introducción)
2. [Descripción General del Sistema](#2-descripción-general-del-sistema)
3. [Arquitectura del Sistema](#3-arquitectura-del-sistema)
4. [Tecnologías y Herramientas](#4-tecnologías-y-herramientas)
5. [Estructura del Proyecto](#5-estructura-del-proyecto)
6. [Descripción de Módulos](#6-descripción-de-módulos)
7. [Modelo de Datos](#7-modelo-de-datos)
8. [Descripción de Clases y Métodos](#8-descripción-de-clases-y-métodos)
9. [API de Endpoints (Rutas HTTP)](#9-api-de-endpoints-rutas-http)
10. [Flujos de Datos Principales](#10-flujos-de-datos-principales)
11. [Seguridad del Sistema](#11-seguridad-del-sistema)
12. [Configuración del Entorno](#12-configuración-del-entorno)
13. [Manual de Instalación](#13-manual-de-instalación)
14. [Manual de Despliegue en Producción](#14-manual-de-despliegue-en-producción)
15. [Pruebas del Sistema](#15-pruebas-del-sistema)
16. [Mantenimiento y Versionamiento](#16-mantenimiento-y-versionamiento)

---

## 1. Introducción

### 1.1 Propósito del documento

Este documento describe la arquitectura técnica, el diseño interno, las clases, los métodos, los endpoints y los flujos de datos del sistema **Hoodie Shop**. Está dirigido a desarrolladores, técnicos de mantenimiento y cualquier persona que necesite entender, modificar o extender el sistema.

### 1.2 Alcance

El documento cubre la totalidad del sistema **Hoodie Shop**, incluyendo:
- Backend desarrollado en Python 3.14 con Flask 3.0
- Base de datos MongoDB Atlas
- Frontend con HTML5, Bootstrap 5.3, CSS3 y JavaScript
- Integración con WhatsApp Web
- Sistema de autenticación con Flask-Login
- Panel de administración completo

### 1.3 Audiencia

| Perfil | Uso del documento |
|--------|------------------|
| Desarrollador Backend | Entender la lógica de negocio, servicios y modelos |
| Desarrollador Frontend | Entender los templates, rutas y datos disponibles |
| DBA / Administrador de BD | Entender el modelo de datos y los índices MongoDB |
| DevOps | Seguir el manual de instalación y despliegue |
| Docente evaluador | Verificar la calidad técnica del proyecto |

---

## 2. Descripción General del Sistema

**Hoodie Shop** es una aplicación web de comercio electrónico que permite la venta de hoodies (buzos) a través de internet. El sistema implementa dos roles de usuario:

- **Cliente:** Navega el catálogo, agrega productos al carrito, realiza pedidos y hace seguimiento del estado de sus compras.
- **Administrador:** Gestiona el inventario de productos, administra los pedidos y visualiza estadísticas del negocio.

### 2.1 Características principales

-  Autenticación y autorización con roles (`user` / `admin`)
-  Catálogo de productos con búsqueda en tiempo real
-  Carrito de compras persistente en sesión del servidor
-  Proceso de checkout con validación de stock en tiempo real
-  Confirmación de pedidos por WhatsApp con mensaje prellenado
-  Panel administrativo con dashboard, CRUD de productos y gestión de pedidos
-  Exportación de pedidos a CSV
-  Historial inmutable de estados por pedido
-  Diseño responsivo para móvil, tablet y escritorio

---

## 3. Arquitectura del Sistema

### 3.1 Patrón arquitectónico

El sistema implementa una arquitectura **MVC (Modelo – Vista – Controlador)** adaptada a Flask, complementada con una **capa de servicios** para separar la lógica de negocio:

```
┌──────────────────────────────────────────────────────┐
│                    CLIENTE HTTP                      │
│              (Navegador Web del usuario)             │
└──────────────────────────┬───────────────────────────┘
                           │ HTTP Request/Response
┌──────────────────────────▼───────────────────────────┐
│                   FLASK APPLICATION                  │
│                                                      │
│  ┌─────────────┐    ┌─────────────┐                  │
│  │   ROUTES    │    │  TEMPLATES  │                  │
│  │(Controlador)│───▶│   (Vista)   │                  │
│  │             │    │  Jinja2     │                  │
│  │ auth.py     │    │ HTML+CSS+JS │                  │
│  │ shop.py     │    └─────────────┘                  │
│  │ admin.py    │                                     │
│  │ user.py     │                                     │
│  └──────┬──────┘                                     │
│         │ llama a                                    │
│  ┌──────▼──────────────────────────┐                 │
│  │           SERVICES              │                 │
│  │        (Lógica de negocio)      │                 │
│  │                                 │                 │
│  │ AuthService    ProductService   │                 │
│  │ OrderService   WhatsAppService  │                 │
│  └──────┬──────────────────────────┘                 │
│         │ usa                                        │
│  ┌──────▼──────────────────────────┐                 │
│  │            MODELS               │                 │
│  │        (Entidades de datos)     │                 │
│  │                                 │                 │
│  │  User    Product    Order       │                 │
│  └──────┬──────────────────────────┘                 │
│         │ lee/escribe                                │
└─────────┼────────────────────────────────────────────┘
          │ PyMongo (mongodb+srv://)
┌─────────▼────────────────────────────────────────────┐
│               MONGODB ATLAS (Cloud)                  │
│                                                      │
│   Colección: users                                   │
│   Colección: products                                │
│   Colección: orders                                  │
└──────────────────────────────────────────────────────┘
          │
┌─────────▼────────────────────────────────────────────┐
│           SERVICIO EXTERNO - WHATSAPP                │
│   https://wa.me/{numero}?text={mensaje_encoded}      │
└──────────────────────────────────────────────────────┘
```

### 3.2 Patrón de diseño: Factory Pattern

La aplicación se instancia mediante el patrón **Factory** en `app/__init__.py`:

```python
def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # Inicializar extensiones, blueprints, etc.
    return app
```

**Ventajas:**
- Permite crear instancias diferentes para desarrollo, producción y testing.
- Facilita las pruebas unitarias aisladas.
- Centraliza toda la configuración de la aplicación.

### 3.3 Organización de Blueprints

Flask organiza las rutas en **Blueprints** (módulos de rutas independientes):

| Blueprint | Prefijo URL | Archivo | Responsabilidad |
|-----------|-------------|---------|-----------------|
| `auth` | `/auth` | `routes/auth.py` | Registro, login, logout |
| `shop` | `/` | `routes/shop.py` | Catálogo, carrito, checkout |
| `admin` | `/admin` | `routes/admin.py` | Panel administrativo |
| `user` | `/user` | `routes/user.py` | Perfil, mis pedidos |

### 3.4 Gestión de conexión a base de datos

Se utiliza el objeto `g` de Flask para gestionar la conexión por request:

```python
def get_db():
    if 'db' not in g:
        client = MongoClient(mongo_uri)
        g.db = client.get_database()
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.client.close()

# Registrado en create_app():
app.teardown_appcontext(close_db)
```

**Beneficio:** Una conexión por request, cierre automático al finalizar.

---

## 4. Tecnologías y Herramientas

### 4.1 Stack tecnológico completo

| Capa | Tecnología | Versión | Rol |
|------|-----------|---------|-----|
| **Lenguaje** | Python | 3.14 | Lenguaje principal del backend |
| **Framework web** | Flask | 3.0.0 | Servidor HTTP y enrutamiento |
| **Seguridad HTTP** | Werkzeug | 3.0.1 | Hashing de contraseñas, utilidades HTTP |
| **Autenticación** | Flask-Login | 0.6.3 | Gestión de sesiones y protección de rutas |
| **Base de datos** | MongoDB Atlas | Cloud M0 | Almacenamiento NoSQL en la nube |
| **Driver BD** | PyMongo | 4.6.1 | Conexión y operaciones con MongoDB |
| **DNS** | dnspython | 2.4.2 | Resolución de `mongodb+srv://` |
| **Variables de entorno** | python-dotenv | 1.0.0 | Carga del archivo `.env` |
| **Validación email** | email-validator | 2.1.0 | Validación de formato de emails |
| **Utilidades de fecha** | python-dateutil | 2.8.2 | Manejo avanzado de fechas y horas |
| **Testing** | pytest | 7.4.3 | Framework de pruebas unitarias |
| **Testing Flask** | pytest-flask | 1.3.0 | Extensión de pytest para Flask |
| **CORS** | flask-cors | 4.0.0 | Manejo de Cross-Origin Resource Sharing |
| **Templates** | Jinja2 | 3.x | Motor de templates HTML (incluido en Flask) |
| **CSS Framework** | Bootstrap | 5.3.x | Diseño responsivo y componentes UI |
| **Iconos** | Bootstrap Icons | 1.x | Iconografía del sistema |
| **Control de versiones** | Git + GitHub | - | Versionamiento del código fuente |

### 4.2 Herramientas de desarrollo

| Herramienta | Uso |
|-------------|-----|
| Visual Studio Code | Editor de código principal |
| MongoDB Atlas | Base de datos en la nube (tier gratuito M0) |
| GitHub | Repositorio remoto del código fuente |
| Navegador Chrome/Firefox | Pruebas del sistema |
| Terminal / CMD | Ejecución de comandos y scripts |

---

## 5. Estructura del Proyecto

```
hoodie-shop/                          ← Raíz del proyecto
│
├── app/                              ← Paquete principal de la aplicación
│   ├── __init__.py                   ← Factory Pattern: create_app(), get_db(), close_db()
│   ├── config.py                     ← Clases de configuración por entorno
│   │
│   ├── models/                       ← Capa de modelos (entidades de datos)
│   │   ├── __init__.py               ← Exporta User, Product, Order
│   │   ├── user.py                   ← Clase User (hereda UserMixin de Flask-Login)
│   │   ├── product.py                ← Clase Product con lógica de stock
│   │   └── order.py                  ← Clase Order con estados e historial
│   │
│   ├── routes/                       ← Capa de controladores (Blueprints Flask)
│   │   ├── __init__.py               ← Declara blueprints disponibles
│   │   ├── auth.py                   ← Blueprint /auth: register, login, logout
│   │   ├── shop.py                   ← Blueprint /: catalog, product, cart, checkout
│   │   ├── admin.py                  ← Blueprint /admin: dashboard, CRUD, pedidos
│   │   └── user.py                   ← Blueprint /user: profile, my_orders
│   │
│   ├── services/                     ← Capa de servicios (lógica de negocio)
│   │   ├── __init__.py               ← Declara servicios disponibles
│   │   ├── auth_service.py           ← AuthService: registro, login, update user
│   │   ├── product_service.py        ← ProductService: CRUD, stock, búsqueda
│   │   ├── order_service.py          ← OrderService: crear pedido, cambiar estado, CSV
│   │   └── whatsapp_service.py       ← WhatsAppService: generar mensajes y enlaces
│   │
│   ├── utils/                        ← Utilidades y helpers
│   │   ├── __init__.py               ← Exporta helpers y decoradores
│   │   ├── decorators.py             ← @admin_required, @logout_required
│   │   └── helpers.py                ← formato_moneda_cop, allowed_file, save_image
│   │
│   ├── templates/                    ← Vistas HTML (Jinja2)
│   │   ├── base.html                 ← Template base con navbar y flash messages
│   │   ├── auth/
│   │   │   ├── login.html            ← Formulario de inicio de sesión
│   │   │   └── register.html         ← Formulario de registro
│   │   ├── shop/
│   │   │   ├── catalog.html          ← Grid de productos con búsqueda
│   │   │   ├── product_detail.html   ← Detalle con selectores de talla y color
│   │   │   ├── cart.html             ← Tabla del carrito con totales
│   │   │   ├── checkout.html         ← Formulario de datos de envío
│   │   │   └── order_success.html    ← Confirmación con botón WhatsApp
│   │   ├── admin/
│   │   │   ├── dashboard.html        ← Estadísticas, stock bajo, pedidos recientes
│   │   │   ├── products.html         ← Lista de productos con filtros
│   │   │   ├── product_form.html     ← Formulario crear/editar producto
│   │   │   ├── orders.html           ← Lista de pedidos con filtro por estado
│   │   │   └── order_detail.html     ← Detalle del pedido con cambio de estado
│   │   └── user/
│   │       ├── profile.html          ← Formulario de edición de perfil
│   │       ├── my_orders.html        ← Lista de pedidos del cliente
│   │       └── order_detail.html     ← Detalle del pedido del cliente
│   │
│   └── static/                       ← Archivos estáticos
│       ├── css/
│       │   └── custom.css            ← Estilos personalizados sobre Bootstrap
│       ├── js/
│       │   └── main.js               ← JavaScript: validaciones, preview imagen
│       ├── img/
│       │   └── placeholder.jpg       ← Imagen por defecto para productos sin foto
│       └── uploads/                  ← Imágenes subidas por el administrador
│
├── tests/                            ← Suite de pruebas unitarias
│   ├── __init__.py
│   ├── test_auth.py                  ← Pruebas del módulo de autenticación
│   ├── test_products.py              ← Pruebas del módulo de productos
│   └── test_orders.py                ← Pruebas del módulo de pedidos
│
├── docs/                             ← Documentación del proyecto
│   ├── SRS_HoodieShop_IEEE830_Completo.md   ← SRS en Markdown
│   └── SRS_HoodieShop_IEEE830_v1.0.pdf      ← SRS en PDF
│
├── .env                              ← Variables de entorno (NO incluido en Git)
├── .env.example                      ← Plantilla documentada de variables
├── .gitignore                        ← Exclusiones de Git
├── requirements.txt                  ← Dependencias del proyecto
├── run.py                            ← Punto de entrada: arranca el servidor Flask
├── seed_admin.py                     ← Script para crear el administrador inicial
├── setup_indexes.py                  ← Script para crear índices en MongoDB
└── README.md                         ← Documentación de instalación y uso
```

### 5.1 Métricas del proyecto

| Métrica | Valor |
|---------|-------|
| Total de archivos | 48 archivos |
| Líneas de código | 4,563 líneas |
| Python | 49.5% |
| HTML (Jinja2) | 46.4% |
| JavaScript | 2.8% |
| CSS | 1.3% |

---

## 6. Descripción de Módulos

### 6.1 Módulo `app/__init__.py` – Factory de la aplicación

**Responsabilidad:** Crear y configurar la instancia de la aplicación Flask.

**Funciones principales:**

| Función | Descripción |
|---------|-------------|
| `create_app(config_name)` | Factory: crea e inicializa la aplicación Flask con la configuración especificada |
| `get_db()` | Obtiene la conexión a MongoDB almacenada en el objeto `g` de Flask |
| `close_db(e=None)` | Cierra la conexión a MongoDB al finalizar el request (teardown) |
| `test_mongo_connection(app)` | Verifica la conexión a MongoDB al iniciar la aplicación |
| `load_user(user_id)` | Carga el usuario para Flask-Login desde MongoDB |
| `inject_globals()` | Context processor: inyecta `cart_count` en todos los templates |

---

### 6.2 Módulo `app/config.py` – Configuración

**Responsabilidad:** Centralizar la configuración del sistema por entorno.

**Clases:**

| Clase | Hereda de | Uso |
|-------|-----------|-----|
| `Config` | — | Configuración base común a todos los entornos |
| `DevelopmentConfig` | `Config` | Entorno de desarrollo (`DEBUG=True`) |
| `ProductionConfig` | `Config` | Entorno de producción (`DEBUG=False`) |

**Variables de configuración principales:**

| Variable | Valor por defecto | Descripción |
|----------|------------------|-------------|
| `SECRET_KEY` | desde `.env` | Clave para firmar sesiones y cookies |
| `MONGO_URI` | desde `.env` | URI de conexión a MongoDB Atlas |
| `SESSION_TYPE` | `'filesystem'` | Tipo de almacenamiento de sesiones |
| `PERMANENT_SESSION_LIFETIME` | `timedelta(days=7)` | Duración de la sesión activa |
| `UPLOAD_FOLDER` | `'app/static/uploads'` | Carpeta para imágenes subidas |
| `MAX_CONTENT_LENGTH` | `5 * 1024 * 1024` (5MB) | Tamaño máximo de archivo subido |
| `ALLOWED_EXTENSIONS` | `{'png','jpg','jpeg','gif','webp'}` | Extensiones de imagen permitidas |
| `WHATSAPP_NUMBER` | desde `.env` | Número WhatsApp con código de país |
| `PRODUCTS_PER_PAGE` | `12` | Productos por página en catálogo |
| `ORDERS_PER_PAGE` | `20` | Pedidos por página en panel admin |

---

### 6.3 Módulo `app/utils/decorators.py` – Decoradores de seguridad

**Responsabilidad:** Proteger rutas mediante decoradores personalizados.

```python
@admin_required
def vista_admin():
    # Solo accesible si current_user.is_admin() == True
    pass

@logout_required
def login():
    # Solo accesible si el usuario NO está autenticado
    pass
```

| Decorador | Condición | Si falla |
|-----------|-----------|----------|
| `@admin_required` | `current_user.is_admin() == True` | Flash error + redirect a `/catalog` |
| `@logout_required` | `current_user.is_authenticated == False` | Redirect a `/catalog` |

---

### 6.4 Módulo `app/utils/helpers.py` – Funciones auxiliares

| Función | Parámetros | Retorno | Descripción |
|---------|-----------|---------|-------------|
| `formato_moneda_cop(valor)` | `float` | `str` | Formatea número como `$1.250.000 COP` |
| `allowed_file(filename)` | `str` | `bool` | Verifica si la extensión del archivo está permitida |
| `save_image(file, upload_folder)` | `FileStorage`, `str` | `str` o `None` | Guarda imagen de forma segura con nombre único |
| `validar_email(email)` | `str` | `bool` | Valida formato de email con `email-validator` |
| `validar_telefono(telefono)` | `str` | `bool` | Valida formato de teléfono colombiano |
| `paginar(lista, pagina, por_pagina)` | `list`, `int`, `int` | `dict` | Pagina una lista de resultados |

---

## 7. Modelo de Datos

### 7.1 Base de datos: MongoDB Atlas

**Nombre de la base de datos:** Definido en la URI de conexión (`MONGO_URI`).
**Tipo:** NoSQL orientada a documentos (BSON/JSON).
**Colecciones:** 3 colecciones principales.

---

### 7.2 Colección: `users`

Almacena los usuarios registrados del sistema (clientes y administradores).

```json
{
  "_id": ObjectId("..."),
  "nombre": "Camilo Bocanegra",
  "email": "ftcamilo07@gmail.com",
  "telefono": "3108116983",
  "direccion": "Calle 123 # 45-67",
  "ciudad": "Bogotá",
  "password_hash": "pbkdf2:sha256:260000$...",
  "rol": "admin",
  "created_at": ISODate("2026-02-22T18:00:00Z"),
  "updated_at": ISODate("2026-02-22T18:00:00Z")
}
```

**Índices:**

| Campo | Tipo | Propósito |
|-------|------|-----------|
| `email` | Único | Búsqueda rápida por email, previene duplicados |
| `rol` | Normal | Filtrar usuarios por rol |

**Valores posibles del campo `rol`:**
- `"user"` → Cliente (acceso a tienda y perfil)
- `"admin"` → Administrador (acceso completo)

---

### 7.3 Colección: `products`

Almacena los productos del catálogo (hoodies).

```json
{
  "_id": ObjectId("..."),
  "nombre": "Hoodie Negro Clásico",
  "descripcion": "Hoodie premium de algodón 100%...",
  "precio": 120000.0,
  "stock": {
    "S": 10,
    "M": 15,
    "L": 20,
    "XL": 5
  },
  "colores": ["Negro", "Gris", "Azul"],
  "imagen": "/static/uploads/hoodie_negro.jpg",
  "activo": true,
  "created_at": ISODate("2026-02-22T18:00:00Z"),
  "updated_at": ISODate("2026-02-22T18:00:00Z")
}
```

**Índices:**

| Campo | Tipo | Propósito |
|-------|------|-----------|
| `nombre` | Normal | Búsqueda por nombre de producto |
| `activo` | Normal | Filtrar productos activos/inactivos |
| `precio` | Normal | Ordenar y filtrar por precio |

**Notas:**
- `activo = false` → Producto desactivado (soft delete), no visible en catálogo.
- `imagen` → Ruta relativa a `app/static/uploads/` o URL externa.
- Si no tiene imagen se usa `/static/img/placeholder.jpg`.

---

### 7.4 Colección: `orders`

Almacena los pedidos realizados por los clientes.

```json
{
  "_id": ObjectId("..."),
  "numero_pedido": "ORD-2026-483920",
  "user_id": ObjectId("..."),
  "items": [
    {
      "product_id": ObjectId("..."),
      "nombre": "Hoodie Negro Clásico",
      "talla": "M",
      "color": "Negro",
      "cantidad": 2,
      "precio_unitario": 120000.0,
      "subtotal": 240000.0,
      "imagen": "/static/uploads/hoodie_negro.jpg"
    }
  ],
  "total": 240000.0,
  "direccion_envio": {
    "nombre": "Camilo Bocanegra",
    "telefono": "3108116983",
    "direccion": "Calle 123 # 45-67",
    "ciudad": "Bogotá",
    "notas": "Timbre 2 veces"
  },
  "estado": "RECIBIDO",
  "historial_estados": [
    {
      "estado": "RECIBIDO",
      "fecha": ISODate("2026-02-22T18:00:00Z"),
      "cambiado_por": null
    },
    {
      "estado": "ALISTAMIENTO",
      "fecha": ISODate("2026-02-23T10:00:00Z"),
      "cambiado_por": ObjectId("...")
    }
  ],
  "created_at": ISODate("2026-02-22T18:00:00Z"),
  "updated_at": ISODate("2026-02-23T10:00:00Z")
}
```

**Índices:**

| Campo | Tipo | Propósito |
|-------|------|-----------|
| `numero_pedido` | Único | Búsqueda rápida, previene duplicados |
| `user_id` | Normal | Obtener pedidos de un usuario específico |
| `estado` | Normal | Filtrar pedidos por estado |
| `created_at` | Descendente | Ordenar por fecha más reciente primero |

**Estados del pedido (flujo):**

```
RECIBIDO ──▶ ALISTAMIENTO ──▶ ENVIO ──▶ ENTREGADO
```

---

### 7.5 Diagrama de relaciones entre colecciones

```
┌─────────────────┐         ┌─────────────────┐
│     USERS       │         │    PRODUCTS      │
│─────────────────│         │─────────────────│
│ _id (PK)        │         │ _id (PK)        │
│ nombre          │         │ nombre          │
│ email (único)   │         │ descripcion     │
│ telefono        │         │ precio          │
│ direccion       │         │ stock {S,M,L,XL}│
│ ciudad          │         │ colores []      │
│ password_hash   │         │ imagen          │
│ rol             │         │ activo          │
│ created_at      │         │ created_at      │
│ updated_at      │         │ updated_at      │
└────────┬────────┘         └────────┬────────┘
         │ 1                         │ 1
         │ user_id (FK)              │ product_id (FK)
         │ N                         │ N
┌────────▼─────────────────────────▼─┐
│              ORDERS                 │
│────────────────────────────────────│
│ _id (PK)                           │
│ numero_pedido (único)              │
│ user_id (FK → users._id)           │
│ items [] → product_id (FK)         │
│ total                              │
│ direccion_envio {}                 │
│ estado                             │
│ historial_estados []               │
│ created_at                         │
│ updated_at                         │
└────────────────────────────────────┘
```

---

## 8. Descripción de Clases y Métodos

### 8.1 Clase `User` (`app/models/user.py`)

**Hereda de:** `flask_login.UserMixin`
**Propósito:** Representa a un usuario del sistema (cliente o administrador).

**Atributos:**

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `_id` | `ObjectId` | ID único de MongoDB |
| `nombre` | `str` | Nombre completo del usuario |
| `email` | `str` | Email único (usado para login) |
| `telefono` | `str` | Teléfono de contacto |
| `direccion` | `str` | Dirección de envío por defecto |
| `ciudad` | `str` | Ciudad de residencia |
| `password_hash` | `str` | Contraseña hasheada con PBKDF2-SHA256 |
| `rol` | `str` | Rol del usuario: `'user'` o `'admin'` |
| `created_at` | `datetime` | Fecha de registro |
| `updated_at` | `datetime` | Fecha de última actualización |

**Métodos:**

| Método | Parámetros | Retorno | Descripción |
|--------|-----------|---------|-------------|
| `get_id()` | — | `str` | Retorna el ID del usuario como string (requerido por Flask-Login) |
| `set_password(password)` | `str` | `None` | Genera hash PBKDF2-SHA256 y lo almacena en `password_hash` |
| `check_password(password)` | `str` | `bool` | Verifica si la contraseña coincide con el hash almacenado |
| `is_admin()` | — | `bool` | Retorna `True` si `rol == 'admin'` |
| `to_dict()` | — | `dict` | Convierte el objeto a diccionario para guardar en MongoDB |
| `from_dict(data)` | `dict` | `User` | (Estático) Crea un objeto `User` desde un documento de MongoDB |

---

### 8.2 Clase `Product` (`app/models/product.py`)

**Propósito:** Representa un producto (hoodie) del catálogo con gestión de stock por talla.

**Atributos:**

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `_id` | `ObjectId` | ID único de MongoDB |
| `nombre` | `str` | Nombre del hoodie |
| `descripcion` | `str` | Descripción detallada |
| `precio` | `float` | Precio en COP |
| `stock` | `dict` | Stock por talla: `{'S': int, 'M': int, 'L': int, 'XL': int}` |
| `colores` | `list[str]` | Lista de colores disponibles |
| `imagen` | `str` | Ruta relativa o URL de la imagen |
| `activo` | `bool` | `True` si está visible en el catálogo |
| `created_at` | `datetime` | Fecha de creación |
| `updated_at` | `datetime` | Fecha de última actualización |

**Métodos:**

| Método | Parámetros | Retorno | Descripción |
|--------|-----------|---------|-------------|
| `tiene_stock(talla, cantidad)` | `str`, `int` | `bool` | Verifica si hay suficiente stock de una talla específica |
| `reducir_stock(talla, cantidad)` | `str`, `int` | `bool` | Descuenta stock de la talla. Retorna `False` si no hay suficiente |
| `aumentar_stock(talla, cantidad)` | `str`, `int` | `None` | Incrementa stock de la talla |
| `get_stock_total()` | — | `int` | Suma el stock de todas las tallas |
| `get_tallas_disponibles()` | — | `list[str]` | Retorna las tallas con stock mayor a 0 |
| `to_dict()` | — | `dict` | Convierte el objeto a diccionario para MongoDB |
| `from_dict(data)` | `dict` | `Product` | (Estático) Crea objeto desde documento MongoDB |

---

### 8.3 Clase `Order` (`app/models/order.py`)

**Propósito:** Representa un pedido con su ciclo de vida completo e historial de estados.

**Constantes de clase:**

```python
ESTADO_RECIBIDO    = 'RECIBIDO'
ESTADO_ALISTAMIENTO = 'ALISTAMIENTO'
ESTADO_ENVIO       = 'ENVIO'
ESTADO_ENTREGADO   = 'ENTREGADO'
ESTADOS_VALIDOS    = ['RECIBIDO', 'ALISTAMIENTO', 'ENVIO', 'ENTREGADO']
```

**Atributos:**

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `_id` | `ObjectId` | ID único de MongoDB |
| `numero_pedido` | `str` | Número único formato `ORD-YYYY-NNNNNN` |
| `user_id` | `ObjectId` | Referencia al usuario que realizó el pedido |
| `items` | `list[dict]` | Lista de productos con talla, color, cantidad y subtotal |
| `total` | `float` | Total del pedido en COP |
| `direccion_envio` | `dict` | Datos de entrega: nombre, teléfono, dirección, ciudad, notas |
| `estado` | `str` | Estado actual del pedido |
| `historial_estados` | `list[dict]` | Registro inmutable de todos los cambios de estado |
| `created_at` | `datetime` | Fecha de creación del pedido |
| `updated_at` | `datetime` | Fecha de última actualización |

**Métodos:**

| Método | Parámetros | Retorno | Descripción |
|--------|-----------|---------|-------------|
| `cambiar_estado(nuevo_estado, admin_id)` | `str`, `ObjectId` | `bool` | Cambia el estado y registra el cambio en `historial_estados` |
| `get_cantidad_items()` | — | `int` | Retorna la suma de cantidades de todos los ítems |
| `formato_total()` | — | `str` | Retorna el total formateado como `$240.000` |
| `get_ultimo_cambio_estado()` | — | `dict` | Retorna el último registro del historial de estados |
| `esta_entregado()` | — | `bool` | Verifica si el estado actual es `ENTREGADO` |
| `to_dict()` | — | `dict` | Convierte el objeto a diccionario para MongoDB |
| `from_dict(data)` | `dict` | `Order` | (Estático) Crea objeto desde documento MongoDB |
| `generar_numero_pedido()` | — | `str` | (Estático) Genera número formato `ORD-YYYY-NNNNNN` |

---

### 8.4 Clase `AuthService` (`app/services/auth_service.py`)

**Propósito:** Gestiona el registro, autenticación y actualización de usuarios.

| Método | Parámetros | Retorno | Descripción |
|--------|-----------|---------|-------------|
| `register_user(nombre, email, telefono, direccion, ciudad, password)` | `str x6` | `tuple(bool, str, User)` | Registra un nuevo usuario. Valida email único, formato y contraseña |
| `login_user(email, password)` | `str`, `str` | `tuple(bool, str, User)` | Autentica un usuario verificando email y hash de contraseña |
| `create_admin(nombre, email, password)` | `str x3` | `tuple(bool, str)` | Crea un usuario con `rol='admin'` (usado por `seed_admin.py`) |
| `get_user_by_id(user_id)` | `str/ObjectId` | `User/None` | Obtiene un usuario por su ID de MongoDB |
| `update_user(user_id, **kwargs)` | `str`, `**kwargs` | `bool` | Actualiza los campos especificados del usuario |

---

### 8.5 Clase `ProductService` (`app/services/product_service.py`)

**Propósito:** Gestiona todas las operaciones CRUD sobre productos y el control de stock.

| Método | Parámetros | Retorno | Descripción |
|--------|-----------|---------|-------------|
| `create_product(nombre, descripcion, precio, stock, colores, imagen)` | Varios | `tuple(bool, str, ObjectId)` | Crea un nuevo producto con validaciones |
| `get_product_by_id(product_id)` | `str/ObjectId` | `Product/None` | Obtiene producto por ID |
| `get_all_products(solo_activos)` | `bool` | `list[Product]` | Lista todos o solo los productos activos |
| `update_product(product_id, **kwargs)` | `str`, `**kwargs` | `tuple(bool, str)` | Actualiza campos del producto |
| `delete_product(product_id)` | `str/ObjectId` | `tuple(bool, str)` | Soft delete: pone `activo=False` |
| `restore_product(product_id)` | `str/ObjectId` | `tuple(bool, str)` | Reactiva producto: pone `activo=True` |
| `reducir_stock(product_id, talla, cantidad)` | `str`, `str`, `int` | `tuple(bool, str)` | Descuenta stock al confirmar pedido |
| `aumentar_stock(product_id, talla, cantidad)` | `str`, `str`, `int` | `tuple(bool, str)` | Incrementa stock (uso administrativo) |
| `buscar_productos(query)` | `str` | `list[Product]` | Búsqueda regex insensible a mayúsculas en `nombre` y `descripcion` |
| `filtrar_productos(**filtros)` | `**kwargs` | `list[Product]` | Filtra productos con múltiples criterios dinámicos |

---

### 8.6 Clase `OrderService` (`app/services/order_service.py`)

**Propósito:** Gestiona la creación, consulta, actualización de estados y exportación de pedidos.

| Método | Parámetros | Retorno | Descripción |
|--------|-----------|---------|-------------|
| `create_order(user_id, items, direccion_envio)` | `str`, `list`, `dict` | `tuple(bool, str, Order)` | Crea un pedido con validaciones de datos y genera número único |
| `_generar_numero_pedido_unico()` | — | `str` | Genera número verificando que no exista en BD (bucle while) |
| `get_order_by_id(order_id)` | `str/ObjectId` | `Order/None` | Obtiene pedido por ID |
| `get_order_by_numero(numero_pedido)` | `str` | `Order/None` | Obtiene pedido por número |
| `get_orders_by_user(user_id)` | `str/ObjectId` | `list[Order]` | Lista pedidos de un usuario, ordenados por fecha desc |
| `get_all_orders(filtro_estado)` | `str/None` | `list[Order]` | Lista todos los pedidos con filtro opcional por estado |
| `cambiar_estado(order_id, nuevo_estado, admin_id)` | `str`, `str`, `str` | `tuple(bool, str)` | Cambia estado y registra en historial |
| `get_estadisticas()` | — | `dict` | Retorna métricas: total pedidos, ventas, pedidos por estado |
| `exportar_pedidos_csv(filtro_estado)` | `str/None` | `list[dict]` | Retorna datos de pedidos formateados para exportar a CSV |

---

### 8.7 Clase `WhatsAppService` (`app/services/whatsapp_service.py`)

**Propósito:** Genera mensajes formateados y enlaces de redirección a WhatsApp Web.

**Constructor:**
```python
WhatsAppService(numero_empresa: str)
# Ejemplo: WhatsAppService('573208816983')
```

| Método | Parámetros | Retorno | Descripción |
|--------|-----------|---------|-------------|
| `generar_mensaje_pedido(order, user)` | `Order`, `User` | `str` | Genera mensaje con número de pedido, datos del cliente, lista de ítems y total COP |
| `generar_enlace_whatsapp(order, user)` | `Order`, `User` | `str` | Codifica el mensaje con `urllib.parse.quote()` y retorna URL `wa.me` |
| `generar_mensaje_consulta(producto, user)` | `Product`, `User` | `str` | Genera enlace de consulta sobre un producto específico |

**Ejemplo de mensaje generado:**
```
Hola, quiero confirmar mi pedido:

📦 *Pedido:* ORD-2026-483920
👤 *Cliente:* Camilo Bocanegra
📞 *Teléfono:* 3108116983
📍 *Dirección:* Calle 123 # 45-67, Bogotá
📝 *Notas:* Timbre 2 veces

🛍️ *Productos:*
- Hoodie Negro (M, Negro) x2 = $240.000

💰 *Total:* $240.000 COP

🚚 Pago contraentrega 💵
```

---

## 9. API de Endpoints (Rutas HTTP)

### 9.1 Blueprint `auth` – Autenticación (`/auth`)

| Método | URL | Función | Protección | Descripción |
|--------|-----|---------|-----------|-------------|
| GET | `/auth/register` | `register()` | `@logout_required` | Muestra formulario de registro |
| POST | `/auth/register` | `register()` | `@logout_required` | Procesa el registro de nuevo usuario |
| GET | `/auth/login` | `login()` | `@logout_required` | Muestra formulario de login |
| POST | `/auth/login` | `login()` | `@logout_required` | Procesa la autenticación |
| GET | `/auth/logout` | `logout()` | `@login_required` | Cierra la sesión activa |

---

### 9.2 Blueprint `shop` – Tienda (`)

| Método | URL | Función | Protección | Descripción |
|--------|-----|---------|-----------|-------------|
| GET | `/` o `/catalog` | `catalog()` | Pública | Muestra catálogo con búsqueda `?q=texto` |
| GET | `/product/<id>` | `product_detail()` | Pública | Muestra detalle de un producto |
| GET | `/cart` | `cart()` | Pública | Muestra el carrito de compras |
| POST | `/cart/add` | `add_to_cart()` | Pública | Agrega producto al carrito |
| GET | `/cart/remove/<index>` | `remove_from_cart()` | Pública | Elimina ítem del carrito por índice |
| POST | `/cart/update` | `update_cart()` | Pública | Actualiza cantidad de un ítem |
| GET | `/cart/clear` | `clear_cart()` | Pública | Vacía el carrito completo |
| GET | `/checkout` | `checkout()` | `@login_required` | Muestra formulario de checkout |
| POST | `/checkout` | `checkout()` | `@login_required` | Crea el pedido y genera enlace WhatsApp |

---

### 9.3 Blueprint `admin` – Administración (`/admin`)

| Método | URL | Función | Protección | Descripción |
|--------|-----|---------|-----------|-------------|
| GET | `/admin/dashboard` | `dashboard()` | Admin | Estadísticas, stock bajo, pedidos recientes |
| GET | `/admin/products` | `products()` | Admin | Lista productos con filtros `?q=` y `?inactive=true` |
| GET | `/admin/products/new` | `product_new()` | Admin | Formulario de nuevo producto |
| POST | `/admin/products/new` | `product_new()` | Admin | Crea nuevo producto |
| GET | `/admin/products/<id>/edit` | `product_edit()` | Admin | Formulario de edición de producto |
| POST | `/admin/products/<id>/edit` | `product_edit()` | Admin | Actualiza producto existente |
| GET | `/admin/products/<id>/delete` | `product_delete()` | Admin | Desactiva producto (soft delete) |
| GET | `/admin/products/<id>/restore` | `product_restore()` | Admin | Reactiva producto desactivado |
| GET | `/admin/orders` | `orders()` | Admin | Lista pedidos con filtro `?estado=` |
| GET | `/admin/orders/<id>` | `order_detail()` | Admin | Detalle del pedido con info del cliente |
| POST | `/admin/orders/<id>/change-status` | `order_change_status()` | Admin | Cambia estado del pedido |
| GET | `/admin/orders/export` | `orders_export()` | Admin | Descarga CSV de pedidos con filtro `?estado=` |

---

### 9.4 Blueprint `user` – Usuario (`/user`)

| Método | URL | Función | Protección | Descripción |
|--------|-----|---------|-----------|-------------|
| GET | `/user/profile` | `profile()` | `@login_required` | Muestra perfil del usuario |
| POST | `/user/profile` | `profile()` | `@login_required` | Actualiza datos del perfil |
| GET | `/user/orders` | `orders()` | `@login_required` | Lista los pedidos del usuario |
| GET | `/user/orders/<id>` | `order_detail()` | `@login_required` | Detalle de un pedido propio |

---

## 10. Flujos de Datos Principales

### 10.1 Flujo: Registro de usuario

```
Navegador                Flask (auth.py)         AuthService         MongoDB
    │                         │                       │                    │
    │──POST /auth/register──> │                       │                    │
    │  {nombre, email, pass}  │                       │                    │
    │                         │──register_user()────> │                    │
    │                         │                       │──find_one(email)─> │
    │                         │                       │<─── None  ─────────│
    │                         │                       │──set_password()    │
    │                         │                       │  (PBKDF2-SHA256)   │
    │                         │                       │──insert_one()────> │
    │                         │                       │<────────────────── │
    │                         │<──(True, msg, user) ──│                    │
    │                         │──login_user(user)     │                    │
    │<──redirect /catalog ────│                       │                    │
```

---

### 10.2 Flujo: Realizar un pedido (Checkout)

```
Navegador           shop.py          ProductService    OrderService     MongoDB
    │                  │                    │                │               │
    │──POST /checkout─>│                    │                │               │
    │                  │──get_product()───> │                │               │
    │                  │<─product obj ──────│                │               │
    │                  │──tiene_stock()────>│                │               │
    │                  │<─ True  ───────────│                │               │
    │                  │──create_order()───────────────────> │               │
    │                  │                                     │─insert_one()─>│
    │                  │                                     │<──────────────│
    │                  │<──(True, msg, order) ───────────────│               │
    │                  │──reducir_stock()──>│                │               │
    │                  │                    │─update_one()──────────────────>│
    │                  │──session.pop(cart) │                │               │
    │                  │──WhatsAppService.generar_enlace()   │               │
    │<──order_success──│                    │                │               │
    │  (+ link WA)     │                    │                │               │
```

---

### 10.3 Flujo: Cambio de estado de pedido (Admin)

```
Admin (Browser)       admin.py          OrderService              MongoDB
      │                     │                   │                     │
      │──POST change-status>│                   │                     │
      │  {estado: ENVIO}    │                   │                     │
      │                     │─cambiar_estado()> │                     │
      │                     │                   │──get_order_by_id()─>│
      │                     │                   │<───order────────────│
      │                     │                   │──order.cambiar_estado()
      │                     │                   │  (agrega a historial)
      │                     │                   │──update_one()──────>│
      │                     │                   │<─────────────────── │
      │                     │<── (True, msg)────│                     │
      │<──redirect + flash─ │                   │                     │
```

---

### 10.4 Flujo: Gestión de conexión a MongoDB por request

```
Request HTTP                 Flask                      MongoDB
     │                         │                            │
     │──GET /catalog──────────>│                            │
     │                         │──get_db()                  │
     │                         │  (verifica si 'db' en g)   │
     │                         │──MongoClient()────────────>│
     │                         │──g.db = client.get_db()    │
     │                         │                            │
     │                         │──[procesa el request]      │
     │                         │──db.products.find()───────>│
     │                         │<──[resultados]─────────────│
     │<──Response HTML─────────│                            │
     │                         │──teardown: close_db()      │
     │                         │──db.client.close()────────>│
     │                         │                            │
```

---

## 11. Seguridad del Sistema

### 11.1 Autenticación y sesiones

| Mecanismo | Implementación | Archivo |
|-----------|---------------|---------|
| Hashing de contraseñas | Werkzeug `PBKDF2-SHA256` | `models/user.py` |
| Gestión de sesiones | Flask-Login + cookies firmadas | `app/__init__.py` |
| Expiración de sesión | `timedelta(days=7)` | `config.py` |
| Protección de rutas | `@login_required` (Flask-Login) | Todas las rutas protegidas |
| Protección admin | `@admin_required` personalizado | `utils/decorators.py` |
| Redirección post-login | Parámetro `?next=` | `routes/auth.py` |

### 11.2 Control de acceso

```python
# Ejemplo de ruta protegida con doble decorador
@bp.route('/admin/products')
@login_required        # ← Verifica sesión activa
@admin_required        # ← Verifica rol=admin
def products():
    ...
```

| Nivel | Mecanismo | Dónde |
|-------|-----------|-------|
| Sin autenticación | Rutas públicas accesibles | Catálogo, detalle producto |
| Autenticado | `@login_required` | Checkout, perfil, mis pedidos |
| Administrador | `@login_required` + `@admin_required` | Todas las rutas `/admin/*` |
| Propietario de pedido | Verificación manual `user_id == current_user.get_id()` | `routes/user.py` |

### 11.3 Seguridad en archivos subidos

```python
# Flujo de save_image() en helpers.py
archivo → allowed_file(extensión) → secure_filename() → nombre_único → guardar en uploads/
```

| Validación | Mecanismo |
|-----------|-----------|
| Extensión | `ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}` |
| Nombre seguro | `werkzeug.utils.secure_filename()` |
| Nombre único | Contador incremental si existe colisión |
| Tamaño | `MAX_CONTENT_LENGTH = 5MB` en config |

### 11.4 Variables de entorno

Todas las credenciales y datos sensibles se almacenan en `.env` (excluido de Git):
```
SECRET_KEY=...         # Nunca hardcodeada
MONGO_URI=...          # URI con usuario y contraseña
ADMIN_EMAIL=...        # Credenciales del admin
ADMIN_PASSWORD=...
WHATSAPP_NUMBER=...
```

---

## 12. Configuración del Entorno

### 12.1 Variables de entorno (`.env`)

```env
# ─── Flask ────────────────────────────────
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=tu-clave-secreta-muy-segura-cambiar-en-produccion
PORT=5000

# ─── MongoDB ──────────────────────────────
MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net/hoodie_shop?retryWrites=true&w=majority

# ─── Uploads ──────────────────────────────
UPLOAD_FOLDER=app/static/uploads
MAX_CONTENT_LENGTH=5242880

# ─── Paginación ───────────────────────────
PRODUCTS_PER_PAGE=12
ORDERS_PER_PAGE=20

# ─── Admin inicial ────────────────────────
ADMIN_EMAIL=admin@hoodieshop.com
ADMIN_PASSWORD=admin123
ADMIN_NOMBRE=Administrador

# ─── WhatsApp ─────────────────────────────
WHATSAPP_NUMBER=57XXXXXXXXXX
```

### 12.2 Dependencias del sistema

```
Python >= 3.10
pip (gestor de paquetes de Python)
Git
Conexión a internet (para MongoDB Atlas)
```

---

## 13. Manual de Instalación

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/DjKiller07FT/hoodie-shop.git
cd hoodie-shop
```

### Paso 2: Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar variables de entorno

```bash
# Windows
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

Editar el archivo `.env` con los valores reales (MongoDB URI, WhatsApp, etc.).

### Paso 5: Crear el administrador inicial

```bash
python seed_admin.py
```

**Resultado esperado:**
```
==================================================
🌱 SEED: Crear Administrador Inicial
==================================================
✅ Administrador creado exitosamente
📧 Email: (tu_email)
🔑 Contraseña: (tu_password)
==================================================
```

### Paso 6: Configurar índices de MongoDB (recomendado)

```bash
python setup_indexes.py
```

### Paso 7: Ejecutar la aplicación

```bash
python run.py
```

**Resultado esperado:**
```
==================================================
🚀 HOODIE SHOP - Iniciando aplicación
==================================================
📍 Entorno: development
🌐 URL: http://localhost:5000
🔧 Debug: True
==================================================
```

### Paso 8: Acceder al sistema

Abrir el navegador en: **http://localhost:5000**

---

## 14. Manual de Despliegue en Producción

### 14.1 Opción A: Render.com (Gratuito)

1. Crear cuenta en https://render.com
2. Nuevo servicio → "Web Service"
3. Conectar con GitHub → Seleccionar `hoodie-shop`
4. Configurar:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn run:app`
   - **Environment:** Python 3
5. Agregar variables de entorno desde `.env` en el panel de Render
6. Deploy → La URL pública se genera automáticamente

### 14.2 Opción B: Railway.app

1. Crear cuenta en https://railway.app
2. "New Project" → "Deploy from GitHub"
3. Seleccionar repositorio `hoodie-shop`
4. Agregar variables de entorno en "Variables"
5. Railway detecta automáticamente Flask y despliega

### 14.3 Variables adicionales para producción

```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=clave-muy-segura-de-64-caracteres-aleatorios
```

### 14.4 Consideraciones de producción

| Aspecto | Desarrollo | Producción |
|---------|-----------|-----------|
| Servidor | Flask dev server | Gunicorn |
| Debug | `True` | `False` |
| SECRET_KEY | Simple | Clave de 64+ caracteres aleatoria |
| HTTPS | No | Obligatorio |
| Uploads | Sistema de archivos local | CDN o almacenamiento en la nube |

---

## 15. Pruebas del Sistema

### 15.1 Estructura de pruebas

```
tests/
├── __init__.py
├── test_auth.py        ← Pruebas de registro, login, logout
├── test_products.py    ← Pruebas de CRUD de productos y stock
└── test_orders.py      ← Pruebas de creación y gestión de pedidos
```

### 15.2 Ejecutar pruebas

```bash
# Todas las pruebas
python -m pytest tests/

# Un módulo específico
python -m pytest tests/test_auth.py

# Con detalle de cada prueba
python -m pytest tests/ -v

# Con reporte de cobertura
python -m pytest tests/ --cov=app
```

### 15.3 Casos de prueba documentados

**Módulo de autenticación (`test_auth.py`):**

| ID | Caso de prueba | Resultado esperado |
|----|---------------|-------------------|
| TA-01 | Registro con datos válidos | Usuario creado, sesión activa |
| TA-02 | Registro con email duplicado | Error "El email ya está registrado" |
| TA-03 | Registro con contraseñas distintas | Error "Las contraseñas no coinciden" |
| TA-04 | Login con credenciales correctas | Sesión activa, redirección por rol |
| TA-05 | Login con contraseña incorrecta | Error "Email o contraseña incorrectos" |
| TA-06 | Login con email inexistente | Error "Email o contraseña incorrectos" |
| TA-07 | Logout con sesión activa | Sesión cerrada, redirección al catálogo |

**Módulo de productos (`test_products.py`):**

| ID | Caso de prueba | Resultado esperado |
|----|---------------|-------------------|
| TP-01 | Crear producto con datos válidos | Producto creado con `activo=True` |
| TP-02 | Crear producto con precio negativo | Error "El precio debe ser mayor a 0" |
| TP-03 | Editar producto existente | Campos actualizados correctamente |
| TP-04 | Desactivar producto | `activo=False`, no visible en catálogo |
| TP-05 | Restaurar producto desactivado | `activo=True`, visible en catálogo |
| TP-06 | Reducir stock con suficiente disponibilidad | Stock decrementado correctamente |
| TP-07 | Reducir stock sin disponibilidad | Error "Stock insuficiente para talla X" |
| TP-08 | Buscar producto existente | Lista con el producto encontrado |
| TP-09 | Buscar producto inexistente | Lista vacía |

**Módulo de pedidos (`test_orders.py`):**

| ID | Caso de prueba | Resultado esperado |
|----|---------------|-------------------|
| TO-01 | Crear pedido con datos válidos | Pedido creado con `estado=RECIBIDO` |
| TO-02 | Crear pedido con carrito vacío | Error "El pedido debe tener al menos un item" |
| TO-03 | Crear pedido sin datos de envío | Error "Datos de envío incompletos" |
| TO-04 | Número de pedido único garantizado | Formato `ORD-YYYY-NNNNNN` sin duplicados |
| TO-05 | Cambiar estado a uno válido | Estado actualizado, historial registrado |
| TO-06 | Cambiar estado a uno inválido | Error "Estado inválido" |
| TO-07 | Obtener pedidos de un usuario | Lista de pedidos filtrada por `user_id` |
| TO-08 | Exportar pedidos a CSV | Archivo con columnas correctas |

---

## 16. Mantenimiento y Versionamiento

### 16.1 Control de versiones Git

**Workflow recomendado:**

```bash
# 1. Verificar cambios
git status
git diff

# 2. Agregar cambios
git add .

# 3. Commit con mensaje semántico
git commit -m "feat: descripción del cambio"

# 4. Subir a GitHub
git push origin main
```

**Convención de mensajes de commit:**

| Prefijo | Cuándo usarlo | Ejemplo |
|---------|--------------|---------|
| `feat:` | Nueva funcionalidad | `feat: Agregar sistema de cupones` |
| `fix:` | Corrección de bug | `fix: Corregir cálculo de total` |
| `docs:` | Documentación | `docs: Actualizar README` |
| `style:` | Cambios de estilo | `style: Mejorar diseño del carrito` |
| `refactor:` | Refactorización | `refactor: Simplificar order_service` |
| `test:` | Pruebas | `test: Agregar casos de prueba para auth` |
| `chore:` | Tareas de mantenimiento | `chore: Actualizar dependencias` |

### 16.2 Historial de versiones

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0.0 | 22/02/2026 | Release inicial con funcionalidades completas |

### 16.3 Tareas de mantenimiento periódico

| Frecuencia | Tarea |
|------------|-------|
| **Mensual** | Revisar índices de MongoDB y optimizar consultas lentas |
| **Trimestral** | Actualizar dependencias de `requirements.txt` con `pip install --upgrade` |
| **Trimestral** | Rotar `SECRET_KEY` en producción |
| **Según necesidad** | Limpiar archivos huérfanos en `app/static/uploads/` |
| **Según necesidad** | Revisar logs de error del servidor |

### 16.4 Repositorio y documentación

| Recurso | URL |
|---------|-----|
| Repositorio GitHub | https://github.com/DjKiller07FT/hoodie-shop |
| SRS (IEEE 830) | `docs/SRS_IEEE830.md` |
| SRS en PDF | `docs/SRS_IEEE830_v1.pdf` |
| Documento Técnico | `docs/Documento_Tecnico_HoodieShop.md` |
| README | `README.md` |

---

**Documento elaborado por:** Nicolas Camilo Bocanegra Vaca
**GitHub:** [@DjKiller07FT](https://github.com/DjKiller07FT)
**Email:** ftcamilo07@gmail.com
**Repositorio:** https://github.com/DjKiller07FT/hoodie-shop
**Fecha:** 22 de Febrero de 2026
**Versión del documento:** 1.0