# Especificación de Requisitos de Software

**Proyecto: Hoodie Shop – E-commerce**
**Revisión 1.0**

---

*Marzo de 2026*

---

## Ficha del documento

| Fecha | Revisión | Autor | Verificado dep. calidad |
|-------|----------|-------|------------------------|
| 22/02/2026 | 1.0 | Nicolas Camilo Bocanegra Vaca | Pendiente |

---

**Documento validado por las partes en fecha:** 02/03/2026

| Por el cliente | Por la empresa suministradora |
|----------------|-------------------------------|
| Fdo. D. Camilo Bocanegra | Fdo. D. Camilo Bocanegra |

---

## Contenido

- [1. Introducción](#1-introducción)
  - [1.1 Propósito](#11-propósito)
  - [1.2 Alcance](#12-alcance)
  - [1.3 Personal involucrado](#13-personal-involucrado)
  - [1.4 Definiciones, acrónimos y abreviaturas](#14-definiciones-acrónimos-y-abreviaturas)
  - [1.5 Referencias](#15-referencias)
  - [1.6 Resumen](#16-resumen)
- [2. Descripción General](#2-descripción-general)
  - [2.1 Perspectiva del producto](#21-perspectiva-del-producto)
  - [2.2 Funcionalidad del producto](#22-funcionalidad-del-producto)
  - [2.3 Características de los usuarios](#23-características-de-los-usuarios)
  - [2.4 Restricciones](#24-restricciones)
  - [2.5 Suposiciones y dependencias](#25-suposiciones-y-dependencias)
  - [2.6 Evolución previsible del sistema](#26-evolución-previsible-del-sistema)
- [3. Requisitos Específicos](#3-requisitos-específicos)
  - [3.1 Requisitos comunes de los interfaces](#31-requisitos-comunes-de-los-interfaces)
  - [3.2 Requisitos funcionales (RF-01 a RF-20)](#32-requisitos-funcionales)
  - [3.3 Requisitos no funcionales (RNF-01 a RNF-20)](#33-requisitos-no-funcionales)
  - [3.4 Otros requisitos](#34-otros-requisitos)
- [4. Apéndices](#4-apéndices)

---

## 1. Introducción

Este documento constituye la Especificación de Requisitos de Software (SRS) del sistema **Hoodie Shop**, una plataforma de comercio electrónico desarrollada con Python/Flask y MongoDB Atlas, orientada a la venta de hoodies con gestión de inventario, pedidos y confirmación por WhatsApp.

### 1.1 Propósito

El propósito de este documento es definir de manera clara, completa y verificable todos los requisitos funcionales y no funcionales del sistema **Hoodie Shop**, conforme al estándar IEEE Std 830-1998.

**Audiencia a la que va dirigido:**

- **Desarrolladores:** Para comprender qué debe construirse y cómo debe comportarse el sistema.
- **Evaluadores / Testers:** Para diseñar casos de prueba que verifiquen el cumplimiento de los requisitos.
- **Cliente / Usuario final:** Para validar que el sistema cubre sus necesidades reales.
- **Docentes / Evaluadores académicos:** Para verificar el alcance y la completitud del proyecto.

---

### 1.2 Alcance

El producto a desarrollar se denomina **Hoodie Shop**.

**Hoodie Shop** es una aplicación web de comercio electrónico que permite:

- A **clientes**: Explorar catálogo de productos, gestionar carrito de compras, realizar pedidos con pago contraentrega y hacer seguimiento de sus pedidos.
- A **administradores**: Gestionar inventario de productos (CRUD completo), gestionar y actualizar estado de los pedidos, visualizar estadísticas del negocio y exportar reportes en CSV.

**El sistema NO incluye en esta versión:**
- Pasarelas de pago en línea (tarjetas, PSE, Nequi, etc.)
- Integración con sistemas de logística externos
- Aplicación móvil nativa
- Notificaciones automáticas por email

Este documento es consistente con los objetivos del proyecto académico definidos para el período **Febrero 2026**.

---

### 1.3 Personal involucrado

| Campo | Detalle |
|-------|---------|
| **Nombre** | Camilo Bocanegra |
| **Rol** | Desarrollador Full Stack / Analista de Requisitos |
| **Categoría profesional** | Estudiante de Ingeniería de Sistemas |
| **Responsabilidades** | Análisis, diseño, desarrollo, pruebas y documentación del sistema completo |
| **Información de contacto** | ftcamilo07@gmail.com / djcamilo0710@hotmail.com |
| **Aprobación** | Autor y responsable del proyecto |

---

### 1.4 Definiciones, acrónimos y abreviaturas

| Término | Definición |
|---------|------------|
| **SRS** | Software Requirements Specification – Especificación de Requisitos de Software |
| **RF** | Requisito Funcional |
| **RNF** | Requisito No Funcional |
| **CRUD** | Create, Read, Update, Delete – Operaciones básicas sobre datos |
| **COP** | Pesos Colombianos – Moneda utilizada en el sistema |
| **MongoDB** | Base de datos NoSQL orientada a documentos |
| **Atlas** | Servicio cloud de MongoDB para bases de datos administradas |
| **Flask** | Microframework web desarrollado en Python |
| **Blueprint** | Módulo de rutas de Flask que permite organizar las URLs por funcionalidad |
| **Bootstrap** | Framework CSS para diseño de interfaces web responsivas |
| **Jinja2** | Motor de plantillas HTML integrado en Flask |
| **API** | Application Programming Interface – Interfaz de programación de aplicaciones |
| **RBAC** | Role-Based Access Control – Control de acceso basado en roles |
| **Hash** | Resultado de aplicar una función criptográfica unidireccional a una contraseña |
| **PBKDF2** | Password-Based Key Derivation Function 2 – Algoritmo de hashing seguro |
| **Carrito** | Estructura temporal en sesión que almacena los productos seleccionados antes del pedido |
| **Checkout** | Proceso de confirmación y finalización de una compra |
| **Admin** | Usuario con rol `admin` con privilegios de administración del sistema |
| **Cliente** | Usuario con rol `user` que utiliza la tienda para realizar compras |
| **Placeholder** | Imagen genérica mostrada cuando un producto no tiene foto asignada |
| **WhatsApp** | Aplicación de mensajería usada para confirmar pedidos manualmente |
| **CSV** | Comma Separated Values – Archivo de texto plano para exportar datos tabulares |
| **Soft Delete** | Eliminación lógica: el registro se marca como inactivo pero no se borra físicamente |
| **Context Processor** | Función de Flask que inyecta variables globales disponibles en todos los templates |
| **Factory Pattern** | Patrón de diseño para crear instancias de la aplicación con configuración variable |
| **g** | Objeto global de Flask que almacena datos durante el ciclo de vida de un request |
| **Venv** | Entorno virtual de Python para aislamiento de dependencias |
| **dotenv** | Librería para cargar variables de entorno desde un archivo `.env` |

---

### 1.5 Referencias

| Referencia | Título | Ruta | Fecha | Autor |
|------------|--------|------|-------|-------|
| [IEEE 830] | IEEE Recommended Practice for Software Requirements Specifications | https://ieeexplore.ieee.org/document/720574 | 1998 | IEEE |
| [FLASK] | Flask Documentation v3.0 | https://flask.palletsprojects.com/ | 2024 | Pallets Projects |
| [FLASK-LOGIN] | Flask-Login Documentation v0.6.3 | https://flask-login.readthedocs.io/ | 2024 | Flask-Login |
| [MONGODB] | MongoDB Atlas Documentation | https://docs.mongodb.com/ | 2024 | MongoDB Inc. |
| [PYMONGO] | PyMongo 4.6.1 Documentation | https://pymongo.readthedocs.io/ | 2024 | MongoDB Inc. |
| [BOOTSTRAP] | Bootstrap 5.3 Documentation | https://getbootstrap.com/docs/5.3/ | 2024 | Bootstrap Team |
| [PYTHON] | Python 3.14 Documentation | https://docs.python.org/3/ | 2024 | Python Software Foundation |
| [WERKZEUG] | Werkzeug 3.0.1 Documentation | https://werkzeug.palletsprojects.com/ | 2024 | Pallets Projects |
| [GITHUB] | Repositorio del Proyecto | https://github.com/DjKiller07FT/hoodie-shop | 2026 | Camilo Bocanegra |
| [WHATSAPP] | WhatsApp Click to Chat API | https://faq.whatsapp.com/425247423114725 | 2024 | Meta |

---

### 1.6 Resumen

El presente documento está organizado en **4 secciones principales**:

- **Sección 1 – Introducción:** Proporciona el propósito, alcance, personal involucrado, definiciones, referencias y organización del documento.
- **Sección 2 – Descripción General:** Describe el contexto del producto, su perspectiva dentro del ecosistema tecnológico, funcionalidades principales, tipos de usuarios, restricciones, suposiciones y evolución futura prevista.
- **Sección 3 – Requisitos Específicos:** Contiene la descripción detallada y completa de **20 Requisitos Funcionales** y **20 Requisitos No Funcionales**, todos justificados con código real del repositorio. Incluye interfaces de usuario, hardware, software y comunicación.
- **Sección 4 – Apéndices:** Incluye el modelo de datos MongoDB, la estructura del proyecto, las tecnologías y versiones utilizadas, los casos de uso principales y la matriz de trazabilidad de requisitos.

---

## 2. Descripción General

### 2.1 Perspectiva del producto

**Hoodie Shop** es un producto **independiente** que no forma parte de un sistema mayor preexistente. Opera como una aplicación web de tres capas:

```
┌─────────────────────────────────────────────────┐
│              CAPA DE PRESENTACIÓN               │
│         NAVEGADOR WEB (Cliente HTTP)            │
│   Chrome 90+ | Firefox 88+ | Edge 90+           │
│         Dispositivos: PC, Tablet, Móvil         │
├─────────────────────────────────────────────────┤
│              CAPA DE APLICACIÓN                 │
│          SERVIDOR WEB - Flask 3.0               │
│   • Lógica de negocio (Services)                │
│   • Control de rutas (Blueprints)               │
│   • Gestión de sesiones (Flask-Login)           │
│   • Renderizado de templates (Jinja2)           │
│   • Puerto: 5000 (dev) / 80-443 (prod)          │
├─────────────────────────────────────────────────┤
│              CAPA DE DATOS                      │
│        BASE DE DATOS - MongoDB Atlas            │
│   • Colección: users                            │
│   • Colección: products                         │
│   • Colección: orders                           │
│   • Conexión: mongodb+srv:// (TLS)              │
└─────────────────────────────────────────────────┘
              ↕ Comunicación externa
┌─────────────────────────────────────────────────┐
│           SERVICIO EXTERNO - WHATSAPP           │
│   Confirmación manual de pedidos                │
│   URL: https://wa.me/{numero}?text={mensaje}    │
└─────────────────────────────────────────────────┘
```

**Punto de entrada:** `run.py` – Instancia la aplicación con `create_app(config_name)` y ejecuta el servidor Flask en `host='0.0.0.0'`, puerto configurable mediante variable de entorno `PORT` (por defecto `5000`).

---

### 2.2 Funcionalidad del producto

**Módulo de Autenticación** (`/auth/*`):
- Registro de nuevos usuarios con login automático
- Inicio de sesión con redirección por rol
- Cierre de sesión seguro

**Módulo de Catálogo / Tienda** (`/catalog`, `/product/*`, `/cart/*`):
- Catálogo de productos activos con búsqueda por texto
- Vista detallada de producto con selector de talla, color y cantidad
- Carrito de compras en sesión del servidor

**Módulo de Pedidos** (`/checkout`, `/user/*`):
- Proceso de checkout con validación de stock
- Generación de número de pedido único
- Confirmación por WhatsApp con mensaje prellenado
- Historial de pedidos del cliente con seguimiento de estado

**Módulo Administrativo** (`/admin/*`):
- Dashboard con estadísticas y alertas de stock bajo
- CRUD completo de productos con gestión de imágenes
- Gestión y cambio de estado de pedidos con historial
- Exportación de pedidos a CSV

---

### 2.3 Características de los usuarios

**Usuario tipo: Cliente**

| Campo | Detalle |
|-------|---------|
| **Tipo de usuario** | Cliente / Comprador |
| **Formación** | Educación básica o media, sin conocimientos técnicos |
| **Habilidades** | Uso básico de navegador web y WhatsApp |
| **Actividades** | Explorar catálogo, agregar al carrito, realizar pedidos, consultar estado de pedidos, editar perfil |

**Usuario tipo: Administrador**

| Campo | Detalle |
|-------|---------|
| **Tipo de usuario** | Administrador / Gestor de tienda |
| **Formación** | Educación media o superior, conocimientos básicos en gestión de tiendas online |
| **Habilidades** | Manejo de navegador web, gestión de inventarios y pedidos |
| **Actividades** | Crear/editar/desactivar productos, gestionar y actualizar pedidos, revisar dashboard, exportar reportes |

---

### 2.4 Restricciones

1. **Método de pago único:** Solo se soporta pago contraentrega. No se integran pasarelas de pago en línea.
2. **Confirmación manual:** Los pedidos requieren confirmación manual del cliente vía WhatsApp. No hay notificaciones automáticas.
3. **Lenguaje backend:** Exclusivamente Python 3.10+ con Flask 3.0.
4. **Base de datos:** Exclusivamente MongoDB (Atlas cloud o local).
5. **Dependencia de internet:** El sistema requiere conexión a internet activa (servidor Flask + MongoDB Atlas).
6. **Navegadores soportados:** Chrome 90+, Firefox 88+, Edge 90+, Safari 14+. Sin soporte para Internet Explorer.
7. **Imágenes:** Tamaño máximo 5MB. Formatos: `jpg`, `jpeg`, `png`, `gif`, `webp`.
8. **Sistema operativo servidor:** Desarrollo en Windows 10/11. Producción recomendada en Ubuntu 20.04+.

---

### 2.5 Suposiciones y dependencias

**Suposiciones:**
- Python 3.10+ disponible en el servidor de despliegue.
- Conexión a internet estable con mínimo 10 Mbps en el servidor.
- Los usuarios finales tienen acceso a un dispositivo con navegador web moderno.
- El administrador tiene acceso a WhatsApp para recibir confirmaciones de pedidos.
- MongoDB Atlas mantiene disponibilidad en el tier M0 (gratuito).

**Dependencias:**

| Dependencia | Impacto si cambia |
|-------------|------------------|
| MongoDB Atlas | Sin conexión, el sistema no puede operar |
| `wa.me` (WhatsApp) | El enlace de confirmación dejaría de funcionar |
| Bootstrap CDN | La interfaz perdería estilos si se usa CDN externo sin internet |
| Python 3.10+ | Cambios de versión incompatible requieren ajustes en el código |
| Librerías en `requirements.txt` | Actualizaciones de API pueden requerir cambios en el código |

---

### 2.6 Evolución previsible del sistema

**Versión 1.1 – Corto plazo:**
- Sistema de cupones y descuentos
- Notificaciones automáticas por email (confirmación de pedido)
- Galería de múltiples imágenes por producto
- Alertas automáticas de stock bajo por email

**Versión 1.2 – Mediano plazo:**
- Sistema de reviews y calificaciones de productos
- Lista de deseos (Wishlist)
- Filtros avanzados en catálogo (precio, talla, color)
- Múltiples direcciones de envío por usuario

**Versión 2.0 – Largo plazo:**
- Integración con pasarela de pago (Stripe, PayU, Mercado Pago)
- Aplicación móvil nativa (Android / iOS)
- Integración con logística (tracking automático)
- Panel de analíticas avanzadas con gráficas
- Inventario con alertas automáticas y reposición sugerida

---

## 3. Requisitos Específicos

### 3.1 Requisitos comunes de los interfaces

#### 3.1.1 Interfaces de usuario

- **Diseño Responsivo:** Bootstrap 5.3 adaptable a móvil (320px+), tablet (768px+) y escritorio (1200px+).
- **Esquema de colores:** Negro `#000000` como primario, blanco `#FFFFFF` como fondo, amarillo/dorado `#FFC107` como acento de botones.
- **Tipografía:** Fuente sans-serif Bootstrap, tamaño base 16px.
- **Navegación:** Barra fija en la parte superior con logo, enlaces y acceso a carrito/usuario.
- **Mensajes feedback:** Alertas flash Bootstrap (`success` verde, `danger` rojo, `warning` amarillo, `info` azul) con animación `fadeIn` definida en `custom.css`.
- **Formularios:** Validación en cliente (`main.js`) y en servidor (servicios y rutas).
- **Accesibilidad:** Atributos `alt` en imágenes y `label` en formularios.

#### 3.1.2 Interfaces de hardware

- **Servidor de desarrollo:** Mínimo 4GB RAM, 2 núcleos, 10GB en disco. Sistema actual: Windows 10/11, Python 3.14.
- **Servidor de producción:** VPS con mínimo 1GB RAM, 1 vCPU, 25GB SSD (compatible con Render, Railway, PythonAnywhere).
- **Dispositivo del usuario:** Cualquier dispositivo con navegador web moderno.
- **Almacenamiento de imágenes:** Sistema de archivos local en `app/static/uploads/`.

#### 3.1.3 Interfaces de software

| Software | Versión | Propósito |
|----------|---------|-----------|
| Python | 3.14 | Lenguaje backend |
| Flask | 3.0.0 | Framework web |
| Werkzeug | 3.0.1 | Hashing, seguridad, utilidades HTTP |
| Flask-Login | 0.6.3 | Gestión de sesiones de usuario |
| PyMongo | 4.6.1 | Driver de conexión a MongoDB |
| dnspython | 2.4.2 | Resolución DNS para conexión Atlas (`mongodb+srv://`) |
| python-dotenv | 1.0.0 | Carga de variables de entorno desde `.env` |
| email-validator | 2.1.0 | Validación de formato de emails |
| python-dateutil | 2.8.2 | Manejo avanzado de fechas |
| pytest | 7.4.3 | Framework de pruebas unitarias |
| pytest-flask | 1.3.0 | Extensión de pytest para Flask |
| flask-cors | 4.0.0 | Cross-Origin Resource Sharing |
| Bootstrap | 5.3.x | Framework CSS frontend |
| Jinja2 | 3.x | Motor de templates (incluido en Flask) |
| MongoDB Atlas | Cloud M0 | Base de datos NoSQL en la nube |

#### 3.1.4 Interfaces de comunicación

- **HTTP/HTTPS:** Toda comunicación entre navegador y servidor Flask. Puerto `5000` en desarrollo, `80/443` en producción.
- **MongoDB Wire Protocol:** Comunicación con MongoDB Atlas mediante URI `mongodb+srv://` sobre TCP/IP con TLS.
- **WhatsApp API (wa.me):** URL de redirección unidireccional `https://wa.me/{numero}?text={mensaje_encoded}`. El mensaje se codifica con `urllib.parse.quote()` en `app/services/whatsapp_service.py`.
- **Sesiones HTTP:** Cookies firmadas con `SECRET_KEY` gestionadas por Flask-Login.

---

### 3.2 Requisitos Funcionales

---

#### RF-01: Registro de usuario

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RF-01 |
| **Nombre de requisito** | Registro de nuevo usuario cliente |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Cliente / Usuario final |
| **Prioridad del requisito** | ✅ Alta / Esencial |

**Descripción:**
Ruta `GET/POST /auth/register` en `app/routes/auth.py`, protegida con `@logout_required` para evitar acceso de usuarios ya autenticados.

**Entradas:**
- Nombre completo (obligatorio)
- Email (obligatorio, formato válido, único en sistema)
- Teléfono (obligatorio, formato colombiano)
- Dirección (obligatorio)
- Ciudad (obligatorio)
- Contraseña (obligatorio, mínimo 6 caracteres)
- Confirmar contraseña (debe coincidir)

**Proceso:**
1. Valida coincidencia de contraseñas en la ruta.
2. `auth_service.register_user()` valida formato de email, unicidad y longitud de contraseña.
3. Aplica hash `PBKDF2-SHA256` con `set_password()` en `app/models/user.py`.
4. Crea el usuario con `rol = 'user'` en colección `users` de MongoDB.
5. Inicia sesión automáticamente con `login_user(user, remember=True)`.
6. Redirige al catálogo.

**Salidas:**
- ✅ Éxito: Sesión activa, mensaje flash de bienvenida, redirección a `/catalog`.
- ❌ Error: Mensaje descriptivo indicando campo y tipo de error.

---

#### RF-02: Inicio de sesión

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RF-02 |
| **Nombre de requisito** | Inicio de sesión de usuario |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Cliente / Administrador |
| **Prioridad del requisito** | ✅ Alta / Esencial |

**Descripción:**
Ruta `GET/POST /auth/login` protegida con `@logout_required`. Implementado en `app/routes/auth.py`.

**Entradas:**
- Email, contraseña, checkbox "Recordarme" (opcional).

**Proceso:**
1. `auth_service.login_user(email, password)` busca usuario en MongoDB.
2. Verifica contraseña con `check_password_hash()`.
3. `login_user(user, remember=remember)` crea la sesión.
4. Redirección por rol:
   - `rol = 'admin'` → `/admin/dashboard`
   - `rol = 'user'` → `/catalog`
   - Si hay parámetro `?next=` → redirige a la URL solicitada.

**Salidas:**
- ✅ Éxito: Sesión activa, mensaje `"¡Bienvenido {nombre}!"`.
- ❌ Error: Mensaje genérico "Email o contraseña incorrectos".

---

#### RF-03: Cierre de sesión

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RF-03 |
| **Nombre de requisito** | Cierre de sesión seguro |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Cliente / Administrador |
| **Prioridad del requisito** | ✅ Alta / Esencial |

**Descripción:**
Ruta `GET /auth/logout` protegida con `@login_required`. Destruye la sesión activa del usuario.

**Proceso:**
1. `logout_user()` invalida la sesión de Flask-Login.
2. Redirige al catálogo.

**Salidas:**
- ✅ Éxito: Mensaje "Sesión cerrada correctamente", redirección a `/catalog`.

---

#### RF-04: Catálogo de productos con búsqueda

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RF-04 |
| **Nombre de requisito** | Catálogo de productos con búsqueda por texto |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Cliente |
| **Prioridad del requisito** | ✅ Alta / Esencial |

**Descripción:**
Ruta pública `GET /catalog` (accesible sin autenticación). Implementado en `app/routes/shop.py` → `catalog()`.

**Entradas:**
- Parámetro URL `?q=texto` (opcional).

**Proceso:**
- Con `?q=`: `product_service.buscar_productos(query)` — búsqueda regex insensible a mayúsculas en `nombre` y `descripcion`.
- Sin `?q=`: `product_service.get_all_products(solo_activos=True)` — todos los productos con `activo = True`.

**Salidas:**
- Grid responsivo con imagen (o placeholder), nombre y precio COP.
- Sin resultados: Mensaje informativo.

---

#### RF-05: Detalle de producto

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RF-05 |
| **Nombre de requisito** | Vista detallada de producto |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Cliente |
| **Prioridad del requisito** | ✅ Alta / Esencial |

**Descripción:**
Ruta pública `GET /product/<product_id>`. Implementado en `app/routes/shop.py` → `product_detail()`.

**Proceso:**
1. Busca producto por `ObjectId` en MongoDB.
2. Verifica que exista y `activo = True`.
3. Calcula tallas disponibles (solo las que tienen `stock > 0`).

**Salidas:**
- Imagen, nombre, descripción, precio COP.
- Selectores de talla (solo con stock disponible), color y cantidad.
- Botón "Agregar al Carrito".
- Enlace de consulta por WhatsApp.
- ❌ Producto inactivo/inexistente: Redirección al catálogo con mensaje.

---

#### RF-06: Agregar producto al carrito

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RF-06 |
| **Nombre de requisito** | Agregar producto al carrito de compras |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Cliente |
| **Prioridad del requisito** | ✅ Alta / Esencial |

**Descripción:**
Ruta `POST /cart/add`. Disponible para usuarios no autenticados. Implementado en `app/routes/shop.py` → `add_to_cart()`.

**Entradas:** `product_id`, `talla`, `color`, `cantidad`.

**Proceso:**
1. Obtiene el producto de MongoDB.
2. Verifica stock con `product.tiene_stock(talla, cantidad)`.
3. Inicializa `session['cart'] = []` si no existe.
4. Crea el item: `{product_id, nombre, talla, color, cantidad, precio_unitario, subtotal, imagen}`.
5. Si ya existe el mismo `product_id + talla + color`: suma la cantidad.
6. Marca `session.modified = True`.

**Salidas:**
- ✅ Éxito: Flash "Producto agregado al carrito", redirección al carrito.
- ❌ Sin stock: Flash "Stock insuficiente para talla {talla}".
- ❌ Producto no encontrado: Redirección al catálogo.

---

#### RF-07: Visualización y gestión del carrito

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RF-07 |
| **Nombre de requisito** | Visualización y gestión del carrito de compras |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Cliente |
| **Prioridad del requisito** | ✅ Alta / Esencial |

**Descripción:**
Rutas `GET /cart` y `GET /cart/remove/<index>`. Implementado en `app/routes/shop.py`.

**Funcionalidades:**
- Lista todos los items con imagen, nombre, talla, color, cantidad, precio unitario y subtotal.
- Total general calculado: `sum(item['subtotal'] for item in cart_items)`.
- Eliminar items por índice con `remove_from_cart(index)`.
- Actualizar cantidades con `update_cart()`.
- Botón "Vaciar Carrito" y "Proceder al Pago".
- Contador dinámico en navbar inyectado globalmente por `context_processor`.

**Salidas:**
- Tabla de items con total en COP.
- Carrito vacío: Mensaje y botón para ir al catálogo.

---

#### RF-08: Proceso de checkout (realizar pedido)

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RF-08 |
| **Nombre de requisito** | Proceso de checkout y creación de pedido |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Cliente |
| **Prioridad del requisito** | ✅ Alta / Esencial |

**Descripción:**
Ruta `GET/POST /checkout` protegida con `@login_required`. Implementado en `app/routes/shop.py` → `checkout()`.

**Entradas (formulario):**
- `nombre`, `telefono`, `direccion`, `ciudad` (pre-cargados con datos del usuario), `notas` (opcional).

**Proceso:**
1. Verifica que el carrito no esté vacío.
2. Valida stock de cada item nuevamente con `product.tiene_stock()`.
3. `order_service.create_order(user_id, items, direccion_envio)` crea el pedido en MongoDB.
4. `product_service.reducir_stock(product_id, talla, cantidad)` descuenta el stock.
5. Vacía el carrito con `session.pop('cart', None)`.
6. Genera enlace WhatsApp con `WhatsAppService.generar_enlace_whatsapp(order, user)`.
7. Renderiza `order_success.html` con número de pedido y botón WhatsApp.

**Validaciones en `order_service.create_order()`:**
- Items no vacíos.
- Campos requeridos: `nombre`, `telefono`, `direccion`, `ciudad`.

**Salidas:**
- ✅ Éxito: Página con resumen de pedido, número único y botón WhatsApp verde.
- ❌ Stock insuficiente: Flash error + redirección al carrito.
- ❌ Sin sesión: Redirección a login.

---

#### RF-09: Confirmación de pedido por WhatsApp

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RF-09 |
| **Nombre de requisito** | Integración con WhatsApp para confirmación de pedido |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Cliente / Administrador |
| **Prioridad del requisito** | ✅ Alta / Esencial |

**Descripción:**
Servicio en `app/services/whatsapp_service.py` → clase `WhatsAppService`.

**Métodos:**
- `generar_mensaje_pedido(order, user)`: Genera mensaje con emoji con número de pedido, datos del cliente, lista de ítems (`nombre, talla, color, cantidad, subtotal`) y total COP.
- `generar_enlace_whatsapp(order, user)`: Codifica el mensaje con `urllib.parse.quote()` y retorna URL `https://wa.me/{numero}?text={mensaje_encoded}`.
- `generar_mensaje_consulta(producto, user)`: Genera enlace de consulta sobre un producto.

**Configuración:**
- Número en `.env` → `WHATSAPP_NUMBER` con prefijo `57` (Colombia).
- Botón en `order_success.html` abre en nueva pestaña (`target="_blank"`).

---

#### RF-10: Historial de pedidos del cliente

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RF-10 |
| **Nombre de requisito** | Historial y detalle de pedidos del cliente |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Cliente |
| **Prioridad del requisito** | ✅ Alta / Esencial |

**Descripción:**
Rutas `GET /user/orders` y `GET /user/orders/<order_id>` en `app/routes/user.py`, protegidas con `@login_required`.

**Proceso:**
1. `order_service.get_orders_by_user(user_id)`: Pedidos del usuario ordenados por fecha descendente.
2. `order_detail()`: Verifica que `str(order.user_id) == current_user.get_id()` antes de mostrar el detalle.

**Salidas:**
- Lista de pedidos con: número, fecha, total COP, badge de estado.
- Detalle: ítems comprados, datos de envío, historial completo de estados con fechas.
- ❌ Pedido ajeno: Flash "No tienes permiso para ver este pedido" + redirección.

---

#### RF-11: Edición de perfil de usuario

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RF-11 |
| **Nombre de requisito** | Edición del perfil personal del usuario |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Cliente |
| **Prioridad del requisito** | ⚪ Media / Deseado |

**Descripción:**
Ruta `GET/POST /user/profile` en `app/routes/user.py`, protegida con `@login_required`.

**Entradas:**
- Nombre, teléfono, dirección, ciudad.
- Cambio de contraseña (opcional): requiere contraseña actual + nueva (mínimo 6 caracteres).

**Proceso:**
- Actualiza campos con `auth_service.update_user(user_id, **updates)`.
- Si se provee nueva contraseña: verifica la actual con `current_user.check_password()`. Solo actualiza si es correcta.

**Salidas:**
- ✅ Éxito: Flash "Perfil actualizado exitosamente", redirección al perfil.
- ❌ Contraseña incorrecta: Flash "Contraseña actual incorrecta".

---

#### RF-12: Dashboard administrativo

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RF-12 |
| **Nombre de requisito** | Panel de control con estadísticas del negocio |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Administrador |
| **Prioridad del requisito** | ✅ Alta / Esencial |

**Descripción:**
Ruta `GET /admin/dashboard` protegida con `@login_required` + `@admin_required`. Implementado en `app/routes/admin.py` → `dashboard()`.

**Métricas mostradas:**
- Total de pedidos (todos los estados).
- Ventas totales acumuladas en COP (aggregation pipeline de MongoDB).
- Conteo de pedidos por cada estado válido.
- Productos con `stock_total < 10` unidades (alerta de bajo stock).
- Últimos 10 pedidos recientes.

---

#### RF-13: CRUD de productos (Administrador)

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RF-13 |
| **Nombre de requisito** | Gestión completa de productos (CRUD) |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Administrador |
| **Prioridad del requisito** | ✅ Alta / Esencial |

**Descripción:**
Rutas en `app/routes/admin.py`, todas protegidas con `@login_required` + `@admin_required`.

| Ruta | Método | Función |
|------|--------|---------|
| `GET /admin/products` | GET | Lista todos con filtros `?q=` y `?inactive=true` |
| `GET/POST /admin/products/new` | GET/POST | Crear nuevo producto |
| `GET/POST /admin/products/<id>/edit` | GET/POST | Editar producto existente |
| `GET /admin/products/<id>/delete` | GET | Desactivar producto (soft delete) |
| `GET /admin/products/<id>/restore` | GET | Restaurar producto desactivado |

**Servicios:** `ProductService` → `create_product()`, `update_product()`, `delete_product()` (soft), `restore_product()`.

**Imágenes:** `save_image()` de `helpers.py` con `secure_filename()` y nombres únicos con contador.

---

#### RF-14: Gestión de pedidos (Administrador)

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RF-14 |
| **Nombre de requisito** | Gestión y cambio de estado de pedidos |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Administrador |
| **Prioridad del requisito** | ✅ Alta / Esencial |

**Descripción:**
Rutas en `app/routes/admin.py`, todas protegidas con `@login_required` + `@admin_required`.

| Ruta | Método | Función |
|------|--------|---------|
| `GET /admin/orders` | GET | Lista todos con filtro `?estado=` |
| `GET /admin/orders/<id>` | GET | Detalle del pedido con info del cliente |
| `POST /admin/orders/<id>/change-status` | POST | Cambiar estado del pedido |

**Estados válidos** (`Order.ESTADOS_VALIDOS`):

| Estado | Significado |
|--------|-------------|
| `RECIBIDO` | Pedido recibido, pendiente confirmación |
| `ALISTAMIENTO` | Confirmado, preparando productos |
| `ENVIO` | Enviado, en camino al cliente |
| `ENTREGADO` | Entregado exitosamente |

**Proceso de cambio:** `order_service.cambiar_estado(order_id, nuevo_estado, admin_id)` registra el cambio en `historial_estados` con fecha y `cambiado_por`.

---

#### RF-15: Exportación de pedidos a CSV

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RF-15 |
| **Nombre de requisito** | Exportar pedidos en formato CSV |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Administrador |
| **Prioridad del requisito** | ⚪ Media / Deseado |

**Descripción:**
Ruta `GET /admin/orders/export` con filtro `?estado=`. Implementado en `app/routes/admin.py` → `orders_export()`.

**Proceso:**
1. `order_service.exportar_pedidos_csv(estado_filtro)` retorna datos formateados.
2. `csv.DictWriter` escribe en buffer `StringIO`.
3. Respuesta con `Content-Disposition: attachment; filename=pedidos.csv`.

**Salidas:** Archivo descargable `pedidos.csv` con columnas: Número Pedido, Fecha, Cliente, Teléfono, Ciudad, Total, Estado.

---

#### RF-16: Control automático de stock

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RF-16 |
| **Nombre de requisito** | Control automático de inventario por talla |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Sistema |
| **Prioridad del requisito** | ✅ Alta / Esencial |

**Descripción:**
Implementado en `app/services/product_service.py` y `app/models/product.py`.

**Funciones:**
- `reducir_stock(product_id, talla, cantidad)`: Descuenta stock al confirmar pedido. Valida disponibilidad antes de descontar.
- `aumentar_stock(product_id, talla, cantidad)`: Incrementa stock (uso administrativo).
- `product.tiene_stock(talla, cantidad)`: Verificación previa al agregar al carrito y al checkout.
- `product.get_stock_total()`: Suma stock de todas las tallas para alertas de bajo stock (umbral < 10).

---

#### RF-17: Búsqueda y filtrado de productos

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RF-17 |
| **Nombre de requisito** | Búsqueda y filtrado de productos |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Cliente / Administrador |
| **Prioridad del requisito** | ⚪ Media / Deseado |

**Descripción:**
Implementado en `app/services/product_service.py`.

- `buscar_productos(query)`: Regex insensible a mayúsculas sobre `nombre` y `descripcion` con `activo = True`.
- `get_all_products(solo_activos)`: Listado completo o solo activos.
- `filtrar_productos(**filtros)`: Combinación de múltiples filtros dinámicos.
- Panel admin: `?inactive=true` para ver productos desactivados, `?q=texto` para búsqueda administrativa.

---

#### RF-18: Generación de número de pedido único

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RF-18 |
| **Nombre de requisito** | Generación de número de pedido único garantizado |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Sistema |
| **Prioridad del requisito** | ✅ Alta / Esencial |

**Descripción:**
Implementado en `app/models/order.py` → `generar_numero_pedido()` y `app/services/order_service.py` → `_generar_numero_pedido_unico()`.

**Proceso:**
1. Formato: `ORD-{YYYY}-{NNNNNN}` (año actual + 6 dígitos aleatorios).
2. `_generar_numero_pedido_unico()` verifica en MongoDB que el número no exista.
3. Reintenta si hay colisión (bucle `while True`).
4. El campo tiene índice `unique=True` en MongoDB (definido en `setup_indexes.py`).

---

#### RF-19: Control de acceso a pedidos por propietario

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RF-19 |
| **Nombre de requisito** | Verificación de propiedad en acceso a pedidos |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Sistema / Seguridad |
| **Prioridad del requisito** | ✅ Alta / Esencial |

**Descripción:**
Implementado en `app/routes/user.py` → `order_detail()`. Previene que un usuario vea pedidos ajenos.

**Proceso:**
```python
if str(order.user_id) != current_user.get_id():
    flash('No tienes permiso para ver este pedido', 'danger')
    return redirect(url_for('user.orders'))
```

**Salidas:**
- ❌ Acceso no autorizado: Flash de error + redirección.
- ✅ Autorizado: Muestra detalle completo del pedido.

---

#### RF-20: Estadísticas del negocio

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RF-20 |
| **Nombre de requisito** | Generación de estadísticas del negocio para el dashboard |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Administrador |
| **Prioridad del requisito** | ⚪ Media / Deseado |

**Descripción:**
Implementado en `app/services/order_service.py` → `get_estadisticas()`.

**Métricas:**
- `total_pedidos`: `count_documents({})`.
- `pedidos_por_estado`: `count_documents({'estado': estado})` por cada estado.
- `total_ventas`: Aggregation pipeline `$group → $sum $total`.
- Últimos 10 pedidos: `get_all_orders()[:10]`.
- Productos bajo stock: Filtrado en ruta por `stock_total < 10`.

---

### 3.3 Requisitos No Funcionales

---

### 3.3.1 Requisitos de rendimiento

#### RNF-01: Tiempos de respuesta

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RNF-01 |
| **Nombre de requisito** | Tiempos de respuesta del sistema |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Especificación técnica |
| **Prioridad del requisito** | ✅ Alta / Esencial |

- El **95%** de las páginas deben cargar en menos de **2 segundos**.
- Búsquedas de productos en menos de **1 segundo**.
- Índices MongoDB definidos en `setup_indexes.py`: `email` (único), `rol`, `nombre`, `activo`, `precio`, `numero_pedido` (único), `user_id`, `estado`, `created_at` (desc).
- Imágenes limitadas a **5MB** (`MAX_CONTENT_LENGTH = 5 * 1024 * 1024` en `config.py`).
- Sistema soporta mínimo **10 usuarios simultáneos** sin degradación perceptible.

---

#### RNF-02: Escalabilidad y paginación

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RNF-02 |
| **Nombre de requisito** | Escalabilidad mediante paginación configurable |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Especificación técnica |
| **Prioridad del requisito** | ⚪ Media / Deseado |

- `PRODUCTS_PER_PAGE = 12` y `ORDERS_PER_PAGE = 20` en `app/config.py`.
- Valores configurables mediante variables de entorno sin modificar código.
- MongoDB Atlas permite escalado horizontal en tiers superiores.

---

### 3.3.2 Seguridad

#### RNF-03: Control de acceso basado en roles (RBAC)

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RNF-03 |
| **Nombre de requisito** | Control de acceso basado en roles |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Especificación técnica |
| **Prioridad del requisito** | ✅ Alta / Esencial |

- `@admin_required` en `app/utils/decorators.py`: Verifica `current_user.is_admin()` en cada request a `/admin/*`.
- `@logout_required`: Bloquea acceso a login/registro si ya hay sesión activa.
- Las verificaciones ocurren en **cada request**, no solo al iniciar sesión.
- Redirección automática con mensaje de error para accesos no autorizados.

---

#### RNF-04: Almacenamiento seguro de contraseñas

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RNF-04 |
| **Nombre de requisito** | Hashing seguro de contraseñas |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Especificación técnica |
| **Prioridad del requisito** | ✅ Alta / Esencial |

- Contraseñas almacenadas exclusivamente con hash `PBKDF2-SHA256` (Werkzeug).
- `set_password()` y `check_password()` en `app/models/user.py`.
- `SECRET_KEY` desde variable de entorno, nunca hardcodeada.
- Las contraseñas no aparecen en respuestas HTTP ni en logs.

---

#### RNF-05: Gestión segura de sesiones

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RNF-05 |
| **Nombre de requisito** | Gestión segura de sesiones de usuario |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Especificación técnica |
| **Prioridad del requisito** | ✅ Alta / Esencial |

- `SESSION_TYPE = 'filesystem'`, `SESSION_PERMANENT = True`, `PERMANENT_SESSION_LIFETIME = timedelta(days=7)` en `app/config.py`.
- Sesiones firmadas criptográficamente con `SECRET_KEY`.
- `login_manager.login_view = 'auth.login'` redirige a login si la sesión expira.

---

#### RNF-06: Seguridad en carga de archivos

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RNF-06 |
| **Nombre de requisito** | Validación y seguridad en carga de imágenes |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Especificación técnica |
| **Prioridad del requisito** | ✅ Alta / Esencial |

- `allowed_file()`: Valida extensión contra `{'png', 'jpg', 'jpeg', 'gif', 'webp'}`.
- `save_image()`: Usa `secure_filename()` para sanitizar nombres y prevenir path traversal.
- Genera nombres únicos con contador incremental si ya existe el archivo.
- Almacenamiento en `app/static/uploads/`, aislado del código ejecutable.

---

### 3.3.3 Fiabilidad

#### RNF-07: Manejo robusto de errores

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RNF-07 |
| **Nombre de requisito** | Manejo robusto de errores del sistema |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Especificación técnica |
| **Prioridad del requisito** | ⚪ Media / Deseado |

- Errores de conexión MongoDB capturados con `ConnectionFailure` en `test_mongo_connection()`.
- Todas las operaciones críticas de BD usan `try/except`.
- Errores registrados con `app.logger.error()` sin exponer detalles al usuario.
- MTBF estimado: **720 horas** (30 días) de operación continua sin intervención.

---

#### RNF-08: Trazabilidad del historial de pedidos

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RNF-08 |
| **Nombre de requisito** | Trazabilidad completa del historial de pedidos |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Administrador / Cliente |
| **Prioridad del requisito** | ✅ Alta / Esencial |

- Cada cambio de estado registra en `historial_estados`: estado, fecha/hora, `cambiado_por` (ObjectId del admin).
- Historial inmutable: solo se agregan entradas, nunca se eliminan.
- Los pedidos nunca se eliminan físicamente de MongoDB.
- Consultable por cliente (`/user/orders/<id>`) y por admin (`/admin/orders/<id>`).

---

### 3.3.4 Disponibilidad

#### RNF-09: Disponibilidad del sistema

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RNF-09 |
| **Nombre de requisito** | Disponibilidad del sistema en producción |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Especificación técnica |
| **Prioridad del requisito** | ⚪ Media / Deseado |

- Desarrollo: **100%** durante horas de trabajo activo.
- Producción: Mínimo **99%** anual (~7.2 horas de inactividad permitidas).
- MongoDB Atlas: Sujeto a disponibilidad garantizada por el servicio.
- Verificación de conexión al iniciar con `test_mongo_connection()`.
- Producción: Uso de `gunicorn` con múltiples workers para tolerancia a fallos.

---

#### RNF-10: Separación de entornos desarrollo/producción

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RNF-10 |
| **Nombre de requisito** | Separación de entornos mediante configuración |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Especificación técnica |
| **Prioridad del requisito** | ✅ Alta / Esencial |

- `DevelopmentConfig`: `DEBUG = True`, `TESTING = False`.
- `ProductionConfig`: `DEBUG = False`, `TESTING = False`.
- Selección mediante `FLASK_ENV` sin modificar código fuente.
- `create_app(config_name)` en `run.py`: `config_name = os.getenv('FLASK_ENV', 'development')`.

---

### 3.3.5 Mantenibilidad

#### RNF-11: Arquitectura modular y mantenible

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RNF-11 |
| **Nombre de requisito** | Mantenibilidad mediante arquitectura modular |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Especificación técnica |
| **Prioridad del requisito** | ✅ Alta / Esencial |

- 5 capas bien definidas: `models/`, `services/`, `routes/`, `utils/`, `templates/`.
- 4 Blueprints independientes: `auth`, `shop`, `admin`, `user`.
- 4 Servicios desacoplados: `AuthService`, `ProductService`, `OrderService`, `WhatsAppService`.
- Factory Pattern (`create_app()`) para instanciación configurable.
- Docstrings en todas las funciones con descripción, `Args` y `Returns`.
- Dependencias en `requirements.txt`, revisión trimestral recomendada.

---

#### RNF-12: Testabilidad (pruebas unitarias)

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RNF-12 |
| **Nombre de requisito** | Capacidad de pruebas unitarias |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Especificación técnica |
| **Prioridad del requisito** | ⚪ Media / Deseado |

- Carpeta `tests/` con 3 módulos: `test_auth.py`, `test_products.py`, `test_orders.py`.
- Factory Pattern permite crear instancia de app en modo test con BD aislada.
- Servicios inyectados con la conexión DB, facilitando el uso de mocks.
- Ejecución: `python -m pytest tests/`

---

#### RNF-13: Control de versiones con Git y GitHub

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RNF-13 |
| **Nombre de requisito** | Gestión de código fuente con Git y GitHub |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Especificación técnica |
| **Prioridad del requisito** | ✅ Alta / Esencial |

- Repositorio: `https://github.com/DjKiller07FT/hoodie-shop`.
- `.gitignore` excluye `venv/`, `.env`, `__pycache__/`, `app/static/uploads/*`.
- `.env.example` como plantilla documentada para nuevos despliegues.
- Convención de commits semánticos: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`.
- Composición: Python 49.5%, HTML 46.4%, JavaScript 2.8%, CSS 1.3%.

---

### 3.3.6 Portabilidad

#### RNF-14: Portabilidad entre sistemas operativos

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RNF-14 |
| **Nombre de requisito** | Portabilidad entre plataformas |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Especificación técnica |
| **Prioridad del requisito** | ⚪ Media / Deseado |

- Compatible con Windows 10+, Ubuntu 20.04+ y macOS 12+ sin modificaciones.
- Python es multiplataforma por diseño.
- MongoDB Atlas elimina dependencia de motor de BD local.
- `requirements.txt` garantiza replicabilidad exacta del entorno.
- ~5% del código puede requerir ajustes por rutas de archivos en diferentes SO.

---

#### RNF-15: Configurabilidad por variables de entorno

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RNF-15 |
| **Nombre de requisito** | Configurabilidad total mediante variables de entorno |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Especificación técnica |
| **Prioridad del requisito** | ✅ Alta / Esencial |

- `python-dotenv` carga el archivo `.env` en `app/config.py` y `seed_admin.py`.
- Variables configurables: `SECRET_KEY`, `MONGO_URI`, `UPLOAD_FOLDER`, `MAX_CONTENT_LENGTH`, `WHATSAPP_NUMBER`, `PRODUCTS_PER_PAGE`, `ORDERS_PER_PAGE`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `ADMIN_NOMBRE`, `PORT`, `FLASK_DEBUG`.
- Ninguna credencial sensible está hardcodeada en el código fuente.
- `.env.example` documenta todas las variables para nuevos despliegues.

---

#### RNF-16: Preparado para despliegue en la nube

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RNF-16 |
| **Nombre de requisito** | Preparado para despliegue en plataformas cloud |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Especificación técnica |
| **Prioridad del requisito** | ⚪ Media / Deseado |

- Despliegue posible sin modificaciones en: Render, Railway, PythonAnywhere, Heroku.
- `run.py` configura host `0.0.0.0` y puerto desde variable `PORT` para compatibilidad con plataformas cloud.
- `os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)` crea carpeta `uploads/` automáticamente.
- `README.md` incluye instrucciones completas de instalación y despliegue.

---

#### RNF-17: Usabilidad e interfaz responsiva

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RNF-17 |
| **Nombre de requisito** | Usabilidad e interfaz web responsiva |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Cliente / Usuario final |
| **Prioridad del requisito** | ✅ Alta / Esencial |

- Bootstrap 5.3: Responsivo en móvil (320px+), tablet (768px+), escritorio (1200px+).
- `app/static/js/main.js`: Validación de contraseñas en tiempo real, formateo de precios, preview de imagen antes de subir.
- `app/static/css/custom.css`: Animación `fadeIn` para alertas flash, hover en tablas.
- Navbar fija con contador dinámico de items del carrito (inyectado por `context_processor`).

---

#### RNF-18: Localización para el mercado colombiano

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RNF-18 |
| **Nombre de requisito** | Localización para Colombia |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Cliente |
| **Prioridad del requisito** | ⚪ Media / Deseado |

- Idioma: Español colombiano en toda la interfaz, mensajes y validaciones.
- Moneda: COP con `formato_moneda_cop()` en `app/utils/helpers.py`.
- Teléfonos: `validar_telefono()` para formato colombiano (10 dígitos).
- WhatsApp: Número con prefijo `57` (Colombia), mensajes en español colombiano.
- Sin i18n: Diseñado exclusivamente para operación en Colombia.

---

#### RNF-19: Inyección de contexto global en templates

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RNF-19 |
| **Nombre de requisito** | Variables globales inyectadas en todos los templates |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Especificación técnica |
| **Prioridad del requisito** | ⚪ Media / Deseado |

- `@app.context_processor` → `inject_globals()` en `app/__init__.py`.
- Inyecta `cart_count` (conteo del carrito) disponible en todos los templates automáticamente.
- La navbar en `base.html` muestra el contador actualizado sin código adicional en cada ruta.
- Centraliza datos comunes para evitar duplicación en cada función de vista.

---

#### RNF-20: Gestión eficiente de conexiones a MongoDB

| Campo | Detalle |
|-------|---------|
| **Número de requisito** | RNF-20 |
| **Nombre de requisito** | Gestión eficiente de conexiones a base de datos |
| **Tipo** | ✅ Requisito |
| **Fuente del requisito** | Especificación técnica |
| **Prioridad del requisito** | ✅ Alta / Esencial |

- `get_db()`: Crea la conexión MongoDB y la almacena en el objeto `g` de Flask (una conexión por request).
- `close_db(e=None)`: Registrada con `app.teardown_appcontext(close_db)`, cierra la conexión al finalizar cada request.
- Previene agotamiento del pool de conexiones en producción.
- Evita conexiones zombie que acumulan memoria en MongoDB Atlas.

---

### 3.4 Otros requisitos

#### Requisitos culturales y regionales

- El sistema usa **español colombiano** como único idioma. Sin soporte de i18n en esta versión.
- Los precios se expresan en **pesos colombianos (COP)**: formato `$X.XXX.XXX COP`.
- Los números de teléfono siguen el formato colombiano (10 dígitos, comenzando con `3` para celulares).
- Los mensajes de WhatsApp están redactados en español colombiano con emojis de contexto.
- El formato de número de pedido incluye el año actual: `ORD-2026-NNNNNN`.

#### Requisitos legales

- El sistema **no almacena** datos de tarjetas de crédito ni información bancaria.
- Los datos personales (nombre, email, teléfono, dirección) se almacenan conforme a principios básicos de privacidad.
- Se recomienda en una versión futura agregar política de privacidad y términos y condiciones según la **Ley 1581 de 2012** (Protección de Datos Personales en Colombia) y el **Decreto 1074 de 2015**.
- Las imágenes subidas por el administrador son responsabilidad del propietario del sistema.

---

## 4. Apéndices

### Apéndice A: Modelo de datos MongoDB

#### Colección: `users`
```json
{
  "_id": "ObjectId",
  "nombre": "String (requerido)",
  "email": "String (requerido, único, índice)",
  "telefono": "String (requerido)",
  "direccion": "String (requerido)",
  "ciudad": "String (requerido)",
  "password_hash": "String (PBKDF2-SHA256)",
  "rol": "String ('user' | 'admin')",
  "created_at": "DateTime",
  "updated_at": "DateTime"
}
```

#### Colección: `products`
```json
{
  "_id": "ObjectId",
  "nombre": "String (requerido, índice)",
  "descripcion": "String (requerido)",
  "precio": "Number (> 0, índice)",
  "stock": {
    "S": "Number (>= 0)",
    "M": "Number (>= 0)",
    "L": "Number (>= 0)",
    "XL": "Number (>= 0)"
  },
  "colores": ["String"],
  "imagen": "String (ruta relativa /static/uploads/ o URL)",
  "activo": "Boolean (índice)",
  "created_at": "DateTime",
  "updated_at": "DateTime"
}
```

#### Colección: `orders`
```json
{
  "_id": "ObjectId",
  "numero_pedido": "String (único, índice, formato ORD-YYYY-NNNNNN)",
  "user_id": "ObjectId (ref users, índice)",
  "items": [
    {
      "product_id": "ObjectId",
      "nombre": "String",
      "talla": "String (S|M|L|XL)",
      "color": "String",
      "cantidad": "Number",
      "precio_unitario": "Number",
      "subtotal": "Number",
      "imagen": "String"
    }
  ],
  "total": "Number",
  "direccion_envio": {
    "nombre": "String",
    "telefono": "String",
    "direccion": "String",
    "ciudad": "String",
    "notas": "String (opcional)"
  },
  "estado": "String (RECIBIDO|ALISTAMIENTO|ENVIO|ENTREGADO, índice)",
  "historial_estados": [
    {
      "estado": "String",
      "fecha": "DateTime",
      "cambiado_por": "ObjectId"
    }
  ],
  "created_at": "DateTime (índice desc)",
  "updated_at": "DateTime"
}
```

---

### Apéndice B: Estructura del proyecto

```
hoodie-shop/
├── app/
│   ├── __init__.py          # Factory Pattern: create_app(), get_db(), close_db()
│   ├── config.py            # DevelopmentConfig, ProductionConfig
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # Modelo User + Flask-Login
│   │   ├── product.py       # Modelo Product + lógica de stock
│   │   └── order.py         # Modelo Order + estados + historial
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py          # Blueprint auth: /auth/*
│   │   ├── shop.py          # Blueprint shop: /catalog, /product, /cart, /checkout
│   │   ├── admin.py         # Blueprint admin: /admin/*
│   │   └── user.py          # Blueprint user: /user/*
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py      # AuthService: registro, login, update
│   │   ├── product_service.py   # ProductService: CRUD, stock, búsqueda
│   │   ├── order_service.py     # OrderService: crear, cambiar estado, CSV
│   │   └── whatsapp_service.py  # WhatsAppService: mensajes y enlaces
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── decorators.py    # @admin_required, @logout_required
│   │   └── helpers.py       # formato_moneda_cop, allowed_file, save_image
│   ├── templates/
│   │   ├── base.html        # Template base con navbar y flash messages
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── shop/
│   │   │   ├── catalog.html
│   │   │   ├── product_detail.html
│   │   │   ├── cart.html
│   │   │   ├── checkout.html
│   │   │   └── order_success.html
│   │   ├── admin/
│   │   │   ├── dashboard.html
│   │   │   ├── products.html
│   │   │   ├── product_form.html
│   │   │   ├── orders.html
│   │   │   └── order_detail.html
│   │   └── user/
│   │       ├── profile.html
│   │       ├── my_orders.html
│   │       └── order_detail.html
│   └── static/
│       ├── css/
│       │   └── custom.css
│       ├── js/
│       │   └── main.js
│       ├── img/
│       │   └── placeholder.jpg
│       └── uploads/         # Imágenes subidas por admin
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_products.py
│   └── test_orders.py
├── .env                     # Variables de entorno (NO en Git)
├── .env.example             # Plantilla documentada
├── .gitignore
├── requirements.txt         # 10 dependencias de producción + 2 de testing
├── run.py                   # Punto de entrada: create_app() + app.run()
├── seed_admin.py            # Script: crear usuario administrador inicial
├── setup_indexes.py         # Script: configurar índices MongoDB
└── README.md
```

---

### Apéndice C: Tecnologías y versiones (requirements.txt)

```
# Framework web
Flask==3.0.0
Werkzeug==3.0.1

# Autenticación
Flask-Login==0.6.3

# Base de datos
pymongo==4.6.1
dnspython==2.4.2

# Variables de entorno
python-dotenv==1.0.0

# Formularios y validación
email-validator==2.1.0

# Utilidades
python-dateutil==2.8.2

# Testing
pytest==7.4.3
pytest-flask==1.3.0

# Desarrollo
flask-cors==4.0.0
```

---

### Apéndice D: Casos de uso principales

#### CU-01: Comprar un producto (Cliente)
```
Actor: Cliente autenticado
Precondición: Sesión activa, productos disponibles

Flujo principal:
1. Cliente navega al catálogo (/catalog)
2. Cliente busca un producto (opcional, ?q=texto)
3. Cliente hace clic en "Ver Detalle"
4. Cliente selecciona talla, color y cantidad
5. Cliente hace clic en "Agregar al Carrito"
6. Sistema verifica stock disponible
7. Cliente accede al carrito (/cart)
8. Cliente hace clic en "Proceder al Pago"
9. Sistema verifica sesión activa
10. Cliente revisa/edita datos de envío
11. Cliente confirma el pedido
12. Sistema crea el pedido, reduce stock, vacía carrito
13. Sistema muestra página de éxito con botón WhatsApp
14. Cliente envía confirmación por WhatsApp

Flujo alternativo 6a (sin stock):
   Sistema muestra "Stock insuficiente para talla X"
   Cliente selecciona otra talla

Flujo alternativo 9a (sin sesión):
   Sistema redirige al login con ?next=/checkout
   Cliente inicia sesión → regresa al checkout
```

#### CU-02: Gestionar estado de pedido (Administrador)
```
Actor: Administrador autenticado
Precondición: Sesión activa con rol=admin

Flujo principal:
1. Admin accede a /admin/dashboard
2. Admin navega a /admin/orders
3. Admin filtra pedidos por estado (opcional)
4. Admin hace clic en un pedido
5. Admin selecciona nuevo estado del formulario
6. Admin confirma el cambio
7. Sistema actualiza estado y registra historial
8. Sistema muestra flash de confirmación
```

#### CU-03: Crear producto (Administrador)
```
Actor: Administrador autenticado
Precondición: Sesión activa con rol=admin

Flujo principal:
1. Admin accede a /admin/products/new
2. Admin completa el formulario (nombre, descripción, precio, stock por talla, colores)
3. Admin sube imagen (opcional)
4. Admin hace clic en "Crear Producto"
5. Sistema valida los datos
6. Sistema guarda imagen con nombre único seguro
7. Sistema crea el producto en MongoDB con activo=True
8. Sistema redirige a la lista de productos con mensaje de éxito
```

---

### Apéndice E: Matriz de trazabilidad de requisitos

| Requisito | Archivo fuente | Función / Clase | Ruta HTTP |
|-----------|---------------|-----------------|-----------|
| RF-01 | `routes/auth.py` | `register()` | `POST /auth/register` |
| RF-02 | `routes/auth.py` | `login()` | `POST /auth/login` |
| RF-03 | `routes/auth.py` | `logout()` | `GET /auth/logout` |
| RF-04 | `routes/shop.py` | `catalog()` | `GET /catalog` |
| RF-05 | `routes/shop.py` | `product_detail()` | `GET /product/<id>` |
| RF-06 | `routes/shop.py` | `add_to_cart()` | `POST /cart/add` |
| RF-07 | `routes/shop.py` | `cart()`, `remove_from_cart()` | `GET /cart` |
| RF-08 | `routes/shop.py` | `checkout()` | `POST /checkout` |
| RF-09 | `services/whatsapp_service.py` | `WhatsAppService` | N/A (servicio) |
| RF-10 | `routes/user.py` | `orders()`, `order_detail()` | `GET /user/orders` |
| RF-11 | `routes/user.py` | `profile()` | `POST /user/profile` |
| RF-12 | `routes/admin.py` | `dashboard()` | `GET /admin/dashboard` |
| RF-13 | `routes/admin.py` | `product_new()`, `product_edit()` | `POST /admin/products/*` |
| RF-14 | `routes/admin.py` | `order_change_status()` | `POST /admin/orders/<id>/change-status` |
| RF-15 | `routes/admin.py` | `orders_export()` | `GET /admin/orders/export` |
| RF-16 | `services/product_service.py` | `reducir_stock()`, `aumentar_stock()` | N/A (servicio) |
| RF-17 | `services/product_service.py` | `buscar_productos()`, `filtrar_productos()` | N/A (servicio) |
| RF-18 | `models/order.py` | `generar_numero_pedido()` | N/A (modelo) |
| RF-19 | `routes/user.py` | `order_detail()` | `GET /user/orders/<id>` |
| RF-20 | `services/order_service.py` | `get_estadisticas()` | N/A (servicio) |
| RNF-01 | `setup_indexes.py` | Índices MongoDB | N/A |
| RNF-02 | `config.py` | `PRODUCTS_PER_PAGE`, `ORDERS_PER_PAGE` | N/A |
| RNF-03 | `utils/decorators.py` | `admin_required`, `logout_required` | N/A |
| RNF-04 | `models/user.py` | `set_password()`, `check_password()` | N/A |
| RNF-05 | `config.py` | `SESSION_*`, `PERMANENT_SESSION_LIFETIME` | N/A |
| RNF-06 | `utils/helpers.py` | `allowed_file()`, `save_image()` | N/A |
| RNF-07 | `__init__.py` | `test_mongo_connection()`, `try/except` | N/A |
| RNF-08 | `models/order.py` | `historial_estados` | N/A |
| RNF-09 | `__init__.py` | `test_mongo_connection()` | N/A |
| RNF-10 | `config.py` | `DevelopmentConfig`, `ProductionConfig` | N/A |
| RNF-11 | Toda la arquitectura | Blueprints + Services | N/A |
| RNF-12 | `tests/` | `test_auth.py`, `test_products.py`, `test_orders.py` | N/A |
| RNF-13 | `.gitignore`, `.env.example` | Control de versiones Git | N/A |
| RNF-14 | `requirements.txt` | Python multiplataforma | N/A |
| RNF-15 | `config.py` | `load_dotenv()`, variables de entorno | N/A |
| RNF-16 | `run.py` | `host='0.0.0.0'`, `PORT` env var | N/A |
| RNF-17 | `static/js/main.js` | Validaciones cliente + Bootstrap 5 | N/A |
| RNF-18 | `utils/helpers.py` | `formato_moneda_cop()`, `validar_telefono()` | N/A |
| RNF-19 | `__init__.py` | `inject_globals()` context_processor | N/A |
| RNF-20 | `__init__.py` | `get_db()`, `close_db()`, `teardown_appcontext` | N/A |

---

**Documento elaborado por:** Nicolas Camilo Bocanegra Vaca
**GitHub:** [@DjKiller07FT](https://github.com/DjKiller07FT)
**Repositorio:** https://github.com/DjKiller07FT/hoodie-shop
**Fecha:** 02 de Marzo de 2026
**Versión:** 1.0
**Estándar:** IEEE Std 830-1998