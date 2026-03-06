# INFORME FINAL DE PROYECTO DE SOFTWARE

## TABLA DE CONTENIDO

1. [Análisis de la Aplicación](#1-análisis-de-la-aplicación)
2. [Diseño – Metodología de Desarrollo](#2-diseño--metodología-de-desarrollo)
3. [Desarrollo – Justificación de Tecnologías](#3-desarrollo--justificación-de-tecnologías)
4. [Ciclo de Vida del Software](#4-ciclo-de-vida-del-software)
5. [Requisitos IEEE 830](#5-requisitos-ieee-830)
6. [Historias de Usuario](#6-historias-de-usuario)
7. [Diagramas de Casos de Uso](#7-diagramas-de-casos-de-uso)
8. [Implementación – Despliegue y Código Fuente](#8-implementación--despliegue-y-código-fuente)
9. [Checklist de Pruebas](#9-checklist-de-pruebas)
10. [Plan de Capacitación](#10-plan-de-capacitación)
11. [Conclusiones](#11-conclusiones)
12. [Referencias](#12-referencias)

---

## 1. Análisis de la Aplicación

### 1.1 Objetivo General

Desarrollar una aplicación web de comercio electrónico denominada **Hoodie Shop**, que permita la venta en línea de hoodies mediante una plataforma accesible desde cualquier dispositivo con navegador web, integrando gestión de inventario, procesamiento de pedidos con pago contraentrega y confirmación de compras a través de WhatsApp.

### 1.2 Objetivos Específicos

- Implementar un sistema de autenticación seguro con roles diferenciados para clientes y administradores.
- Desarrollar un catálogo de productos con búsqueda, filtrado y gestión de stock por talla.
- Crear un flujo completo de compra: catálogo → carrito → checkout → confirmación por WhatsApp.
- Construir un panel de administración para gestionar productos, pedidos y visualizar estadísticas del negocio.
- Garantizar la seguridad de los datos mediante hashing de contraseñas, control de acceso por roles y validación de entradas.
- Desplegar el código fuente en un repositorio público en GitHub para su auditoría.

### 1.3 Justificación

En el contexto actual del comercio digital en Colombia, el comercio electrónico ha crecido de manera sostenida, especialmente en la venta de productos de moda y ropa. Sin embargo, muchos emprendedores del sector textil aún dependen de catálogos por redes sociales y ventas informales por WhatsApp, lo que dificulta el control del inventario, la gestión de pedidos y el seguimiento de ventas.

**Hoodie Shop** surge como solución a esta problemática, ofreciendo:

- **Para el cliente:** Una experiencia de compra ordenada, transparente y cómoda desde cualquier dispositivo, con seguimiento en tiempo real del estado de su pedido.
- **Para el administrador:** Un panel centralizado que reemplaza las hojas de cálculo y los chats desorganizados, permitiendo controlar el inventario, gestionar pedidos y analizar ventas desde un solo lugar.
- **Para el negocio:** Una plataforma escalable construida sobre tecnologías modernas y gratuitas (Python, Flask, MongoDB Atlas) que minimiza costos de operación sin sacrificar funcionalidad.

La integración con WhatsApp como canal de confirmación responde a la realidad del mercado colombiano, donde esta aplicación es el principal medio de comunicación entre compradores y vendedores informales, facilitando una transición natural hacia el comercio digital sin romper los hábitos del usuario.

### 1.4 Alcance del Sistema

**El sistema incluye:**
- Registro e inicio de sesión con dos roles: cliente y administrador.
- Catálogo público de productos con búsqueda por texto.
- Carrito de compras persistente en sesión del servidor.
- Proceso de checkout con validación de stock en tiempo real.
- Generación automática de número de pedido único (`ORD-YYYY-NNNNNN`).
- Confirmación de pedidos vía enlace de WhatsApp con mensaje prellenado.
- Historial de pedidos del cliente con seguimiento de estado.
- Panel administrativo: CRUD de productos, gestión de pedidos, dashboard con estadísticas y exportación a CSV.

**El sistema NO incluye en esta versión:**
- Pasarelas de pago en línea (tarjetas, PSE, Nequi).
- Notificaciones automáticas por correo electrónico.
- Aplicación móvil nativa.
- Integración con sistemas de logística externos.

---

## 2. Diseño – Metodología de Desarrollo

### 2.1 Metodología seleccionada: SCRUM (adaptado)

Para el desarrollo de **Hoodie Shop** se seleccionó la metodología ágil **SCRUM** en su versión adaptada para equipos de un solo desarrollador (Solo Scrum / Personal Scrum).

### 2.2 Justificación de la elección

Se evaluaron tres metodologías antes de tomar la decisión:

| Metodología | Por qué NO se eligió |
|-------------|----------------------|
| **Cascada** | Requiere requisitos 100% definidos desde el inicio. No permite cambios durante el desarrollo. Genera software funcional solo al final, retrasando la detección de errores. |
| **Espiral** | Más apropiada para proyectos grandes con alto nivel de incertidumbre técnica. Su overhead de gestión es excesivo para un proyecto individual. |
| **SCRUM ✅** | **Elegida** — Permite entregas incrementales, es flexible ante cambios, organiza el desarrollo por módulos funcionales y es adaptable para un solo desarrollador. |

**Razones concretas para elegir SCRUM:**

1. **Entregas incrementales:** Cada sprint genera un módulo funcional y probado del sistema.
2. **Flexibilidad:** Los requisitos pueden ajustarse entre sprints sin comprometer el proyecto.
3. **Organización clara:** Cada sprint se enfocó en un módulo completo del sistema.
4. **Adaptable al trabajo individual:** Las ceremonias SCRUM pueden simplificarse sin perder su esencia iterativa.
5. **Evidencia de avance:** Los sprints generan entregables concretos y verificables.

### 2.3 Sprints ejecutados

| Sprint | Módulo desarrollado | Funcionalidades |
|--------|--------------------|--------------------|
| Sprint 1 | Autenticación | Registro, login, logout, roles |
| Sprint 2 | Catálogo | Listado, búsqueda, detalle de producto |
| Sprint 3 | Carrito | Agregar, ver, actualizar, vaciar |
| Sprint 4 | Pedidos | Checkout, WhatsApp, historial de pedidos |
| Sprint 5 | Perfil | Edición de datos y cambio de contraseña |
| Sprint 6 | Admin – Productos | CRUD completo con imágenes |
| Sprint 7 | Admin – Pedidos | Gestión, cambio de estado, exportar CSV |
| Sprint 8 | Transversal | Control de stock, estadísticas, pruebas, documentación |

### 2.4 Arquitectura de diseño: MVC + Servicios

Se implementó el patrón **MVC (Modelo – Vista – Controlador)** con una capa adicional de **Servicios**:

```
MODELO      → app/models/     (User, Product, Order)
VISTA       → app/templates/  (HTML + Jinja2 + Bootstrap)
CONTROLADOR → app/routes/     (Blueprints Flask)
SERVICIOS   → app/services/   (AuthService, ProductService, OrderService, WhatsAppService)
```

---

## 3. Desarrollo – Justificación de Tecnologías

### 3.1 Lenguaje de programación: Python 3.14

Python fue seleccionado como lenguaje principal por:

- **Legibilidad y productividad:** Sintaxis limpia que reduce el tiempo de desarrollo y facilita la comprensión del código.
- **Ecosistema robusto:** Librerías maduras para web (Flask), base de datos (PyMongo) y seguridad (Werkzeug).
- **Orientado a objetos:** Permite implementar el patrón MVC con clases bien definidas.
- **Multiplataforma:** El mismo código funciona en Windows, Linux y macOS sin modificaciones.

### 3.2 Framework web: Flask 3.0

Flask fue elegido sobre Django y FastAPI por:

- **Microframework:** Proporciona solo lo esencial sin imponer estructuras rígidas.
- **Blueprints:** Organiza el código en módulos independientes (`auth`, `shop`, `admin`, `user`).
- **Jinja2 integrado:** Motor de templates que separa la lógica del HTML elegantemente.
- **Flask-Login:** Extensión madura para gestión de sesiones con mínima configuración.

| Framework | Desventaja para este proyecto |
|-----------|-------------------------------|
| Django | ORM incompatible con MongoDB; excesivamente complejo para el alcance |
| FastAPI | Orientado a APIs REST, no a renderizado HTML con templates |
| **Flask ✅** | Ninguna para este caso de uso |

### 3.3 Base de datos: MongoDB Atlas

MongoDB fue elegido sobre MySQL y PostgreSQL por:

- **Modelo de datos flexible:** Los documentos JSON/BSON se adaptan al campo `stock` por tallas y al array `items` de un pedido, estructuras difíciles de representar en tablas relacionales.
- **Sin esquema fijo:** Permite agregar campos sin migraciones, agilizando el desarrollo iterativo con SCRUM.
- **Atlas (cloud):** Instancia gratuita M0 en la nube, sin necesidad de instalar un servidor local.
- **Escalabilidad:** Permite escalar horizontalmente sin cambiar el código de la aplicación.

| Base de datos | Desventaja para este proyecto |
|--------------|-------------------------------|
| MySQL | Esquema rígido; dificultad para arrays y objetos anidados |
| PostgreSQL | Más complejo de configurar; JSONB tiene limitaciones vs. documentos nativos |
| **MongoDB ✅** | Sin transacciones ACID complejas (no necesarias para este alcance) |

### 3.4 Frontend: HTML5 + Bootstrap 5.3 + JavaScript

- **Bootstrap 5.3:** Diseño responsivo automático para móvil, tablet y escritorio.
- **Jinja2 Templates:** Reutilización de componentes HTML sin duplicación de código.
- **JavaScript vanilla:** Validaciones del lado del cliente sin frameworks pesados innecesarios.

### 3.5 Resumen del stack tecnológico

```
Frontend:   HTML5 + Bootstrap 5.3 + JavaScript
Templates:  Jinja2 (integrado en Flask)
Backend:    Python 3.14 + Flask 3.0
Seguridad:  Werkzeug (PBKDF2) + Flask-Login
Base datos: MongoDB Atlas (NoSQL, Cloud M0)
Driver BD:  PyMongo 4.6.1
Entorno:    python-dotenv + venv
Pruebas:    pytest 7.4.3 + pytest-flask
Versiones:  Git + GitHub
```

---

## 4. Ciclo de Vida del Software

### 4.1 Modelo aplicado: SCRUM iterativo

```
┌─────────────────────────────────────────────────────────────┐
│                  CICLO DE VIDA HOODIE SHOP                  │
│                                                             │
│   ANÁLISIS ──▶ DISEÑO ──▶ DESARROLLO ──▶ IMPLEMENTACIÓN    │
│                                               │             │
│                                          IMPLANTACIÓN       │
└─────────────────────────────────────────────────────────────┘
```

---

### FASE 1 – ANÁLISIS ✅

**Objetivo:** Entender qué debe hacer el sistema.

**Actividades realizadas:**
- Identificación de usuarios: cliente y administrador.
- Levantamiento de 20 Requisitos Funcionales (RF).
- Definición de 20 Requisitos No Funcionales (RNF).
- Redacción del SRS bajo la norma IEEE 830.
- Creación de 20 Historias de Usuario con criterios de aceptación.

**Entregable:** `docs/SRS_IEEE830.md` + PDF

---

### FASE 2 – DISEÑO ✅

**Objetivo:** Definir cómo se construirá el sistema.

**Actividades realizadas:**
- Diseño de arquitectura 3 capas: Presentación, Aplicación, Datos.
- Selección del patrón MVC con capa de servicios.
- Diseño del modelo de datos MongoDB (3 colecciones).
- Definición de la estructura de carpetas del proyecto.
- Definición de Blueprints: `auth`, `shop`, `admin`, `user`.
- Elaboración de diagramas de casos de uso.

**Entregable:** `docs/Docuemento_Tecnico.md`

---

### FASE 3 – DESARROLLO ✅

**Objetivo:** Escribir el código funcional del sistema.

**Actividades realizadas:**
- Implementación de 3 modelos: `User`, `Product`, `Order`.
- Implementación de 4 servicios: `AuthService`, `ProductService`, `OrderService`, `WhatsAppService`.
- Implementación de 4 Blueprints con 29 endpoints HTTP.
- Desarrollo de 14 templates HTML con Bootstrap 5.3.
- Implementación de seguridad: hashing, decoradores, control de acceso.
- Escritura de pruebas unitarias en `tests/`.
- Control de versiones con Git y GitHub.

**Métricas del desarrollo:**

| Métrica | Valor |
|---------|-------|
| Archivos de código | 48 archivos |
| Líneas de código | 4,563 líneas |
| Python | 49.5% |
| HTML (Jinja2) | 46.4% |
| JavaScript | 2.8% |
| CSS | 1.3% |

**Entregable:** https://github.com/DjKiller07FT/hoodie-shop

---

### FASE 4 – IMPLEMENTACIÓN (PRUEBAS) ✅

**Objetivo:** Verificar que el sistema cumple todos los requisitos.

**Actividades realizadas:**
- Ejecución de pruebas unitarias con pytest.
- Pruebas funcionales manuales de todos los flujos principales.
- Verificación del cumplimiento de los 20 RF mediante checklist.
- Corrección de errores encontrados durante las pruebas.
- Verificación del sistema en múltiples navegadores y dispositivos.

**Entregable:** Checklist de pruebas (sección 9 de este documento)

---

### FASE 5 – IMPLANTACIÓN ⏳

**Objetivo:** Poner el sistema en producción para uso real.

**Estado actual:** Sistema funcional en entorno de desarrollo local (`localhost:5000`).

**Actividades para producción:**
- Despliegue en plataforma cloud (Render.com o Railway.app).
- Configuración de variables de entorno de producción.
- Capacitación a usuarios finales.
- Entrega de manual de usuario y administrador.

---

## 5. Requisitos IEEE 830

### 5.1 Requisitos Funcionales (20 RF)

---

#### RF-01: Registro de usuario

| Campo | Detalle |
|-------|---------|
| **Número** | RF-01 |
| **Nombre** | Registro de nuevo usuario cliente |
| **Prioridad** | Alta / Esencial |
| **Fuente** | Cliente / Usuario final |

**Descripción:** El sistema permite a cualquier visitante crear una cuenta proporcionando nombre, email, teléfono, dirección, ciudad y contraseña. La contraseña se almacena con hash PBKDF2-SHA256. Al registrarse, la sesión se inicia automáticamente y se redirige al catálogo.

---

#### RF-02: Inicio de sesión

| Campo | Detalle |
|-------|---------|
| **Número** | RF-02 |
| **Nombre** | Inicio de sesión de usuario |
| **Prioridad** | Alta / Esencial |
| **Fuente** | Cliente / Administrador |

**Descripción:** Ruta `POST /auth/login` protegida con `@logout_required`. El sistema autentica al usuario con email y contraseña. Según el rol (`user` o `admin`), redirige al catálogo o al dashboard. Soporta la opción "Recordarme" con sesión de 7 días.

---

#### RF-03: Cierre de sesión

| Campo | Detalle |
|-------|---------|
| **Número** | RF-03 |
| **Nombre** | Cierre de sesión seguro |
| **Prioridad** | Alta / Esencial |
| **Fuente** | Cliente / Administrador |

**Descripción:** Ruta `GET /auth/logout` protegida con `@login_required`. Destruye la sesión activa mediante `logout_user()` de Flask-Login y redirige al catálogo.

---

#### RF-04: Catálogo de productos con búsqueda

| Campo | Detalle |
|-------|---------|
| **Número** | RF-04 |
| **Nombre** | Catálogo público con búsqueda por texto |
| **Prioridad** | Alta / Esencial |
| **Fuente** | Cliente |

**Descripción:** Ruta pública `GET /catalog`. Muestra todos los productos activos. Soporta búsqueda por nombre o descripción con el parámetro `?q=texto` mediante expresiones regulares insensibles a mayúsculas/minúsculas.

---

#### RF-05: Detalle de producto

| Campo | Detalle |
|-------|---------|
| **Número** | RF-05 |
| **Nombre** | Vista detallada de producto |
| **Prioridad** | Alta / Esencial |
| **Fuente** | Cliente |

**Descripción:** Ruta pública `GET /product/<product_id>`. Muestra imagen, nombre, descripción, precio COP, tallas disponibles (solo con stock > 0), colores y selector de cantidad. Productos desactivados o inexistentes redirigen al catálogo.

---

#### RF-06: Agregar producto al carrito

| Campo | Detalle |
|-------|---------|
| **Número** | RF-06 |
| **Nombre** | Agregar producto al carrito de compras |
| **Prioridad** | Alta / Esencial |
| **Fuente** | Cliente |

**Descripción:** Ruta `POST /cart/add`. Disponible sin autenticación. Verifica stock con `product.tiene_stock(talla, cantidad)`, crea el ítem en sesión del servidor. Si el mismo producto con igual talla y color ya existe en el carrito, suma la cantidad.

---

#### RF-07: Visualización y gestión del carrito

| Campo | Detalle |
|-------|---------|
| **Número** | RF-07 |
| **Nombre** | Visualización y gestión del carrito |
| **Prioridad** | Alta / Esencial |
| **Fuente** | Cliente |

**Descripción:** Rutas `GET /cart`, `GET /cart/remove/<index>`, `POST /cart/update`, `GET /cart/clear`. Muestra todos los ítems con imagen, nombre, talla, color, cantidad, subtotal y total general en COP. Permite eliminar ítems, actualizar cantidades y vaciar el carrito completo.

---

#### RF-08: Proceso de checkout y creación de pedido

| Campo | Detalle |
|-------|---------|
| **Número** | RF-08 |
| **Nombre** | Checkout con validación de stock y creación de pedido |
| **Prioridad** | Alta / Esencial |
| **Fuente** | Cliente |

**Descripción:** Ruta `POST /checkout` protegida con `@login_required`. Pre-carga datos del usuario, valida stock de cada ítem, crea el pedido con `order_service.create_order()`, genera número único `ORD-YYYY-NNNNNN`, descuenta el stock, vacía el carrito y muestra la página de confirmación.

---

#### RF-09: Confirmación de pedido por WhatsApp

| Campo | Detalle |
|-------|---------|
| **Número** | RF-09 |
| **Nombre** | Integración con WhatsApp para confirmación de pedido |
| **Prioridad** | Alta / Esencial |
| **Fuente** | Cliente / Administrador |

**Descripción:** Servicio `WhatsAppService` en `app/services/whatsapp_service.py`. Genera mensaje prellenado con número de pedido, datos del cliente, productos (talla/color/cantidad/subtotal) y total COP. Enlace `https://wa.me/{numero}?text={mensaje_encoded}` abre en nueva pestaña.

---

#### RF-10: Historial de pedidos del cliente

| Campo | Detalle |
|-------|---------|
| **Número** | RF-10 |
| **Nombre** | Historial y detalle de pedidos del cliente |
| **Prioridad** | Alta / Esencial |
| **Fuente** | Cliente |

**Descripción:** Rutas `GET /user/orders` y `GET /user/orders/<order_id>` protegidas con `@login_required`. Lista pedidos del usuario ordenados por fecha descendente. En el detalle verifica que `str(order.user_id) == current_user.get_id()` para prevenir acceso no autorizado.

---

#### RF-11: Edición de perfil de usuario

| Campo | Detalle |
|-------|---------|
| **Número** | RF-11 |
| **Nombre** | Edición del perfil personal del usuario |
| **Prioridad** | Media / Deseado |
| **Fuente** | Cliente |

**Descripción:** Ruta `POST /user/profile` protegida con `@login_required`. Permite actualizar nombre, teléfono, dirección y ciudad. El cambio de contraseña es opcional y requiere verificar la contraseña actual con `check_password()` antes de actualizar.

---

#### RF-12: Dashboard administrativo

| Campo | Detalle |
|-------|---------|
| **Número** | RF-12 |
| **Nombre** | Panel de control con estadísticas del negocio |
| **Prioridad** | Alta / Esencial |
| **Fuente** | Administrador |

**Descripción:** Ruta `GET /admin/dashboard` protegida con `@login_required` + `@admin_required`. Muestra total de pedidos, ventas acumuladas en COP, conteo por estado, productos con `stock_total < 10` (alerta de bajo stock) y últimos 10 pedidos recientes.

---

#### RF-13: CRUD de productos (Administrador)

| Campo | Detalle |
|-------|---------|
| **Número** | RF-13 |
| **Nombre** | Gestión completa de productos (CRUD) |
| **Prioridad** | Alta / Esencial |
| **Fuente** | Administrador |

**Descripción:** Rutas `/admin/products/*` protegidas con doble decorador. Permite crear, editar, desactivar (soft delete: `activo=False`) y restaurar productos. Incluye carga de imágenes con `allowed_file()`, `secure_filename()` y límite de 5MB.

---

#### RF-14: Gestión de pedidos (Administrador)

| Campo | Detalle |
|-------|---------|
| **Número** | RF-14 |
| **Nombre** | Gestión y cambio de estado de pedidos |
| **Prioridad** | Alta / Esencial |
| **Fuente** | Administrador |

**Descripción:** Rutas `/admin/orders/*`. Lista todos los pedidos con filtro `?estado=`. Permite cambiar el estado (`RECIBIDO → ALISTAMIENTO → ENVIO → ENTREGADO`) mediante `order_service.cambiar_estado()`, que registra el cambio en `historial_estados` con fecha y admin responsable.

---

#### RF-15: Exportación de pedidos a CSV

| Campo | Detalle |
|-------|---------|
| **Número** | RF-15 |
| **Nombre** | Exportar pedidos en formato CSV |
| **Prioridad** | Media / Deseado |
| **Fuente** | Administrador |

**Descripción:** Ruta `GET /admin/orders/export` con filtro `?estado=`. Usa `csv.DictWriter` y `StringIO` para generar el archivo. Respuesta con `Content-Disposition: attachment; filename=pedidos.csv` con columnas: Número Pedido, Fecha, Cliente, Teléfono, Ciudad, Total, Estado.

---

#### RF-16: Control automático de stock

| Campo | Detalle |
|-------|---------|
| **Número** | RF-16 |
| **Nombre** | Control automático de inventario por talla |
| **Prioridad** | Alta / Esencial |
| **Fuente** | Sistema |

**Descripción:** `ProductService` implementa `reducir_stock()`, `aumentar_stock()`. El modelo `Product` implementa `tiene_stock(talla, cantidad)` y `get_stock_total()`. La verificación se realiza dos veces: al agregar al carrito y en el momento del checkout para evitar race conditions.

---

#### RF-17: Búsqueda y filtrado de productos

| Campo | Detalle |
|-------|---------|
| **Número** | RF-17 |
| **Nombre** | Búsqueda y filtrado de productos |
| **Prioridad** | Media / Deseado |
| **Fuente** | Cliente / Administrador |

**Descripción:** `ProductService.buscar_productos(query)` usa regex MongoDB insensible a mayúsculas sobre `nombre` y `descripcion`. `filtrar_productos(**filtros)` permite combinaciones dinámicas. En el admin: `?inactive=true` para ver desactivados y `?q=` para búsqueda administrativa.

---

#### RF-18: Generación de número de pedido único

| Campo | Detalle |
|-------|---------|
| **Número** | RF-18 |
| **Nombre** | Generación de número de pedido único garantizado |
| **Prioridad** | Alta / Esencial |
| **Fuente** | Sistema |

**Descripción:** `Order.generar_numero_pedido()` genera formato `ORD-{YYYY}-{NNNNNN}`. `OrderService._generar_numero_pedido_unico()` verifica en MongoDB que no exista colisión (bucle `while True`). El campo tiene índice `unique=True` en MongoDB definido en `setup_indexes.py`.

---

#### RF-19: Control de acceso a pedidos por propietario

| Campo | Detalle |
|-------|---------|
| **Número** | RF-19 |
| **Nombre** | Verificación de propiedad en acceso a pedidos |
| **Prioridad** | Alta / Esencial |
| **Fuente** | Sistema / Seguridad |

**Descripción:** En `routes/user.py → order_detail()` se verifica `str(order.user_id) != current_user.get_id()` antes de mostrar el detalle. Si no coincide, muestra "No tienes permiso para ver este pedido" y redirige a "Mis Pedidos".

---

#### RF-20: Estadísticas del negocio

| Campo | Detalle |
|-------|---------|
| **Número** | RF-20 |
| **Nombre** | Generación de estadísticas del negocio |
| **Prioridad** | Media / Deseado |
| **Fuente** | Administrador |

**Descripción:** `OrderService.get_estadisticas()` retorna: `total_pedidos` con `count_documents({})`, `pedidos_por_estado` por cada estado válido, `total_ventas` mediante aggregation pipeline `$group → $sum $total`. Consumido por el dashboard administrativo.

---

### 5.2 Requisitos No Funcionales (20 RNF)

---

#### RNF-01: Tiempos de respuesta

| Campo | Detalle |
|-------|---------|
| **Número** | RNF-01 |
| **Categoría** | Rendimiento |
| **Prioridad** | Alta / Esencial |

**Descripción:** El 95% de las páginas deben cargar en menos de 2 segundos. Las búsquedas en menos de 1 segundo. Índices MongoDB definidos en `setup_indexes.py`: `email` (único), `rol`, `nombre`, `activo`, `precio`, `numero_pedido` (único), `user_id`, `estado`, `created_at` (desc). Imágenes limitadas a 5MB.

---

#### RNF-02: Escalabilidad y paginación

| Campo | Detalle |
|-------|---------|
| **Número** | RNF-02 |
| **Categoría** | Rendimiento |
| **Prioridad** | Media / Deseado |

**Descripción:** `PRODUCTS_PER_PAGE = 12` y `ORDERS_PER_PAGE = 20` configurables en `app/config.py` sin modificar código. MongoDB Atlas permite escalado horizontal mediante sharding en tiers superiores.

---

#### RNF-03: Control de acceso basado en roles (RBAC)

| Campo | Detalle |
|-------|---------|
| **Número** | RNF-03 |
| **Categoría** | Seguridad |
| **Prioridad** | Alta / Esencial |

**Descripción:** Decoradores en `app/utils/decorators.py`: `@admin_required` verifica `current_user.is_admin()` en cada request a `/admin/*`. `@logout_required` bloquea login/registro si hay sesión activa. Las verificaciones ocurren en cada request, no solo al iniciar sesión.

---

#### RNF-04: Almacenamiento seguro de contraseñas

| Campo | Detalle |
|-------|---------|
| **Número** | RNF-04 |
| **Categoría** | Seguridad |
| **Prioridad** | Alta / Esencial |

**Descripción:** Contraseñas almacenadas exclusivamente con hash `PBKDF2-SHA256` mediante Werkzeug. Métodos `set_password()` y `check_password()` en `app/models/user.py`. `SECRET_KEY` cargada desde variable de entorno. Las contraseñas nunca aparecen en respuestas HTTP ni en logs.

---

#### RNF-05: Gestión segura de sesiones

| Campo | Detalle |
|-------|---------|
| **Número** | RNF-05 |
| **Categoría** | Seguridad |
| **Prioridad** | Alta / Esencial |

**Descripción:** `SESSION_TYPE = 'filesystem'`, `SESSION_PERMANENT = True`, `PERMANENT_SESSION_LIFETIME = timedelta(days=7)` en `app/config.py`. Sesiones firmadas criptográficamente con `SECRET_KEY`. `login_manager.login_view = 'auth.login'` redirige si la sesión expira.

---

#### RNF-06: Seguridad en carga de archivos

| Campo | Detalle |
|-------|---------|
| **Número** | RNF-06 |
| **Categoría** | Seguridad |
| **Prioridad** | Alta / Esencial |

**Descripción:** `allowed_file()` valida extensiones contra `{'png', 'jpg', 'jpeg', 'gif', 'webp'}`. `save_image()` usa `secure_filename()` de Werkzeug para sanitizar nombres y prevenir path traversal. Genera nombres únicos con contador si existe colisión. Almacenamiento en `app/static/uploads/`, aislado del código.

---

#### RNF-07: Manejo robusto de errores

| Campo | Detalle |
|-------|---------|
| **Número** | RNF-07 |
| **Categoría** | Fiabilidad |
| **Prioridad** | Media / Deseado |

**Descripción:** Errores de conexión MongoDB capturados con `ConnectionFailure` en `test_mongo_connection()`. Todas las operaciones críticas de BD usan `try/except`. Errores registrados con `app.logger.error()` sin exponer detalles técnicos al usuario. MTBF estimado: 720 horas (30 días).

---

#### RNF-08: Trazabilidad del historial de pedidos

| Campo | Detalle |
|-------|---------|
| **Número** | RNF-08 |
| **Categoría** | Fiabilidad |
| **Prioridad** | Alta / Esencial |

**Descripción:** Cada cambio de estado registra en `historial_estados`: estado, fecha/hora (`DateTime`) y `cambiado_por` (ObjectId del admin). El historial es inmutable (solo se agregan entradas). Los pedidos no se eliminan físicamente de MongoDB.

---

#### RNF-09: Disponibilidad del sistema

| Campo | Detalle |
|-------|---------|
| **Número** | RNF-09 |
| **Categoría** | Disponibilidad |
| **Prioridad** | Media / Deseado |

**Descripción:** Desarrollo: 100% durante horas activas. Producción: mínimo 99% anual (~7.2 horas de inactividad permitidas). Verificación de conexión al iniciar con `test_mongo_connection()`. En producción: `gunicorn` con múltiples workers para tolerancia a fallos.

---

#### RNF-10: Separación de entornos desarrollo/producción

| Campo | Detalle |
|-------|---------|
| **Número** | RNF-10 |
| **Categoría** | Disponibilidad |
| **Prioridad** | Alta / Esencial |

**Descripción:** `DevelopmentConfig`: `DEBUG = True`. `ProductionConfig`: `DEBUG = False`. Selección mediante variable de entorno `FLASK_ENV` sin modificar código fuente. `create_app(config_name)` en `run.py`: `config_name = os.getenv('FLASK_ENV', 'development')`.

---

#### RNF-11: Arquitectura modular y mantenible

| Campo | Detalle |
|-------|---------|
| **Número** | RNF-11 |
| **Categoría** | Mantenibilidad |
| **Prioridad** | Alta / Esencial |

**Descripción:** 5 capas bien definidas: `models/`, `services/`, `routes/`, `utils/`, `templates/`. 4 Blueprints independientes. 4 Servicios desacoplados. Factory Pattern (`create_app()`). Docstrings en todas las funciones con descripción, `Args` y `Returns`.

---

#### RNF-12: Testabilidad

| Campo | Detalle |
|-------|---------|
| **Número** | RNF-12 |
| **Categoría** | Mantenibilidad |
| **Prioridad** | Media / Deseado |

**Descripción:** Carpeta `tests/` con 3 módulos: `test_auth.py`, `test_products.py`, `test_orders.py`. Factory Pattern permite crear instancia de app en modo test con BD aislada. Servicios inyectados con la conexión DB, facilitando el uso de mocks. Ejecución: `python -m pytest tests/`.

---

#### RNF-13: Control de versiones con Git y GitHub

| Campo | Detalle |
|-------|---------|
| **Número** | RNF-13 |
| **Categoría** | Mantenibilidad |
| **Prioridad** | Alta / Esencial |

**Descripción:** Repositorio: `https://github.com/DjKiller07FT/hoodie-shop` (público). `.gitignore` excluye `venv/`, `.env`, `__pycache__/`, `app/static/uploads/*`. `.env.example` como plantilla documentada. Commits semánticos: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`.

---

#### RNF-14: Portabilidad entre plataformas

| Campo | Detalle |
|-------|---------|
| **Número** | RNF-14 |
| **Categoría** | Portabilidad |
| **Prioridad** | Media / Deseado |

**Descripción:** Compatible con Windows 10+, Ubuntu 20.04+ y macOS 12+ sin modificaciones. Python es multiplataforma por diseño. MongoDB Atlas elimina dependencia de instalación local de motor de BD. `requirements.txt` garantiza replicabilidad exacta del entorno.

---

#### RNF-15: Configurabilidad por variables de entorno

| Campo | Detalle |
|-------|---------|
| **Número** | RNF-15 |
| **Categoría** | Portabilidad |
| **Prioridad** | Alta / Esencial |

**Descripción:** `python-dotenv` carga `.env`. Variables configurables: `SECRET_KEY`, `MONGO_URI`, `UPLOAD_FOLDER`, `MAX_CONTENT_LENGTH`, `WHATSAPP_NUMBER`, `PRODUCTS_PER_PAGE`, `ORDERS_PER_PAGE`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `PORT`. Ninguna credencial hardcodeada en el código.

---

#### RNF-16: Preparado para despliegue en la nube

| Campo | Detalle |
|-------|---------|
| **Número** | RNF-16 |
| **Categoría** | Portabilidad |
| **Prioridad** | Media / Deseado |

**Descripción:** Compatible sin modificaciones con Render, Railway, PythonAnywhere y Heroku. `run.py` configura `host='0.0.0.0'` y puerto desde variable `PORT`. `os.makedirs(UPLOAD_FOLDER, exist_ok=True)` crea la carpeta de uploads automáticamente en cualquier entorno.

---

#### RNF-17: Interfaz responsiva y usable

| Campo | Detalle |
|-------|---------|
| **Número** | RNF-17 |
| **Categoría** | Usabilidad |
| **Prioridad** | Alta / Esencial |

**Descripción:** Bootstrap 5.3 adaptable a móvil (320px+), tablet (768px+) y escritorio (1200px+). `main.js`: validación de contraseñas en tiempo real, formateo de precios y preview de imagen. `custom.css`: animación `fadeIn` para alertas flash. Navbar fija con contador dinámico del carrito.

---

#### RNF-18: Localización para el mercado colombiano

| Campo | Detalle |
|-------|---------|
| **Número** | RNF-18 |
| **Categoría** | Usabilidad |
| **Prioridad** | Media / Deseado |

**Descripción:** Idioma: español colombiano en toda la interfaz. Moneda: COP con `formato_moneda_cop()` en `helpers.py`. Teléfonos: `validar_telefono()` para formato colombiano (10 dígitos). WhatsApp: prefijo `57` (Colombia). Sin i18n: diseñado exclusivamente para Colombia.

---

#### RNF-19: Inyección de contexto global en templates

| Campo | Detalle |
|-------|---------|
| **Número** | RNF-19 |
| **Categoría** | Técnico |
| **Prioridad** | Media / Deseado |

**Descripción:** `@app.context_processor → inject_globals()` en `app/__init__.py` inyecta `cart_count` en todos los templates automáticamente. La navbar en `base.html` muestra el contador actualizado sin código adicional en cada ruta. Centraliza datos comunes evitando duplicación.

---

#### RNF-20: Gestión eficiente de conexiones a MongoDB

| Campo | Detalle |
|-------|---------|
| **Número** | RNF-20 |
| **Categoría** | Técnico |
| **Prioridad** | Alta / Esencial |

**Descripción:** `get_db()` crea la conexión MongoDB y la almacena en el objeto `g` de Flask (una conexión por request). `close_db(e=None)` registrada con `app.teardown_appcontext(close_db)` cierra la conexión al finalizar cada request. Previene agotamiento del pool y conexiones zombie en Atlas.

---

## 6. Historias de Usuario

### HU-01 – Registro de nuevo usuario

| Campo | Detalle |
|-------|---------|
| **Título** | REGISTRO DE NUEVO USUARIO |
| **Nro Sprint** | 1 |
| **Responsable** | Nicolas Camilo Bocanegra Vaca |

**Como:** visitante del sitio web
**Quiero:** registrarme con mis datos personales y una contraseña
**Para:** crear una cuenta y poder realizar compras en la tienda.

**Criterios de Aceptación:**
- **Dado que** el visitante ingresa todos los datos obligatorios válidos, **cuando** presione "Registrarse", **entonces** el sistema creará la cuenta, iniciará sesión automáticamente y redirigirá al catálogo.
- **Dado que** el visitante ingresa un email ya registrado, **cuando** intente registrarse, **entonces** el sistema mostrará "El email ya está registrado".
- **Dado que** las contraseñas no coinciden, **cuando** intente registrarse, **entonces** el sistema mostrará "Las contraseñas no coinciden".
- **Dado que** el visitante deja campos obligatorios vacíos, **cuando** intente registrarse, **entonces** el sistema mostrará los mensajes de validación correspondientes.

---

### HU-02 – Inicio de sesión

| Campo | Detalle |
|-------|---------|
| **Título** | INICIO DE SESIÓN |
| **Nro Sprint** | 1 |
| **Responsable** | Nicolas Camilo Bocanegra Vaca |

**Como:** usuario registrado
**Quiero:** iniciar sesión con mi email y contraseña
**Para:** acceder a las funcionalidades según mi perfil.

**Criterios de Aceptación:**
- **Dado que** el usuario ingresa credenciales válidas, **cuando** presione "Iniciar Sesión", **entonces** el sistema lo autenticará y redirigirá al catálogo (cliente) o dashboard (admin).
- **Dado que** el usuario ingresa credenciales incorrectas, **cuando** intente iniciar sesión, **entonces** el sistema mostrará "Email o contraseña incorrectos".
- **Dado que** el usuario marca "Recordarme", **cuando** inicie sesión, **entonces** la sesión se mantendrá activa por 7 días.
- **Dado que** el usuario ya está autenticado, **cuando** acceda a `/auth/login`, **entonces** el sistema lo redirigirá al catálogo.

---

### HU-03 – Cierre de sesión

| Campo | Detalle |
|-------|---------|
| **Título** | CIERRE DE SESIÓN |
| **Nro Sprint** | 1 |
| **Responsable** | Nicolas Camilo Bocanegra Vaca |

**Como:** usuario autenticado
**Quiero:** cerrar mi sesión de forma segura
**Para:** proteger mi cuenta cuando termine de usar la aplicación.

**Criterios de Aceptación:**
- **Dado que** el usuario hace clic en "Cerrar Sesión", **cuando** se procese, **entonces** el sistema destruirá la sesión y redirigirá al catálogo.
- **Dado que** la sesión está cerrada, **cuando** el usuario acceda a una ruta protegida, **entonces** el sistema lo redirigirá al login.

---

### HU-04 – Catálogo de productos

| Campo | Detalle |
|-------|---------|
| **Título** | VISUALIZACIÓN DEL CATÁLOGO |
| **Nro Sprint** | 2 |
| **Responsable** | Nicolas Camilo Bocanegra Vaca |

**Como:** visitante o usuario registrado
**Quiero:** ver todos los hoodies disponibles
**Para:** explorar los productos y encontrar el que deseo comprar.

**Criterios de Aceptación:**
- **Dado que** cualquier persona accede a `/catalog`, **cuando** cargue la página, **entonces** el sistema mostrará todos los productos activos con imagen, nombre y precio COP.
- **Dado que** el usuario escribe en la búsqueda, **cuando** presione buscar, **entonces** el sistema mostrará solo los productos que coincidan con el texto.
- **Dado que** no hay resultados, **cuando** se procese la búsqueda, **entonces** el sistema mostrará "No se encontraron productos".

---

### HU-05 – Detalle de producto

| Campo | Detalle |
|-------|---------|
| **Título** | VER DETALLE DE PRODUCTO |
| **Nro Sprint** | 2 |
| **Responsable** | Nicolas Camilo Bocanegra Vaca |

**Como:** visitante o usuario registrado
**Quiero:** ver la información completa de un hoodie
**Para:** conocer su descripción, precio, tallas y colores antes de comprar.

**Criterios de Aceptación:**
- **Dado que** el usuario hace clic en un producto, **cuando** cargue el detalle, **entonces** verá imagen, descripción, precio, tallas con stock y colores disponibles.
- **Dado que** una talla no tiene stock, **cuando** cargue el detalle, **entonces** esa talla no aparecerá como opción seleccionable.
- **Dado que** el usuario accede a un producto desactivado, **cuando** cargue la URL, **entonces** el sistema lo redirigirá al catálogo con mensaje de error.

---

### HU-06 – Agregar al carrito

| Campo | Detalle |
|-------|---------|
| **Título** | AGREGAR PRODUCTO AL CARRITO |
| **Nro Sprint** | 3 |
| **Responsable** | Nicolas Camilo Bocanegra Vaca |

**Como:** visitante o usuario registrado
**Quiero:** agregar un hoodie al carrito seleccionando talla, color y cantidad
**Para:** acumular los productos que deseo comprar.

**Criterios de Aceptación:**
- **Dado que** el usuario selecciona talla, color y cantidad válidos, **cuando** presione "Agregar al Carrito" con stock suficiente, **entonces** el producto se agregará al carrito y el contador del menú se actualizará.
- **Dado que** ya existe el mismo producto con igual talla y color en el carrito, **cuando** se agregue de nuevo, **entonces** el sistema sumará la cantidad al ítem existente.
- **Dado que** no hay stock suficiente, **cuando** intente agregar, **entonces** el sistema mostrará "Stock insuficiente para talla {talla}".

---

### HU-07 – Gestión del carrito

| Campo | Detalle |
|-------|---------|
| **Título** | VER Y GESTIONAR EL CARRITO |
| **Nro Sprint** | 3 |
| **Responsable** | Nicolas Camilo Bocanegra Vaca |

**Como:** visitante o usuario registrado
**Quiero:** ver y gestionar los productos en mi carrito
**Para:** revisar mi selección antes de pagar.

**Criterios de Aceptación:**
- **Dado que** el usuario accede al carrito, **cuando** cargue la página, **entonces** verá todos los ítems con subtotales y el total general en COP.
- **Dado que** el usuario elimina un ítem, **cuando** se procese, **entonces** el sistema lo eliminará y recalculará el total.
- **Dado que** el carrito está vacío, **cuando** el usuario acceda, **entonces** el sistema mostrará "Tu carrito está vacío".

---

### HU-08 – Realizar pedido (Checkout)

| Campo | Detalle |
|-------|---------|
| **Título** | REALIZAR PEDIDO (CHECKOUT) |
| **Nro Sprint** | 4 |
| **Responsable** | Nicolas Camilo Bocanegra Vaca |

**Como:** usuario registrado con productos en el carrito
**Quiero:** confirmar mi pedido con mis datos de envío
**Para:** formalizar mi compra con pago contraentrega.

**Criterios de Aceptación:**
- **Dado que** el usuario completa el formulario y confirma, **cuando** haya stock disponible, **entonces** el sistema creará el pedido, reducirá el stock, vaciará el carrito y mostrará la confirmación con número de pedido.
- **Dado que** el stock se agotó durante el checkout, **cuando** el usuario confirme, **entonces** el sistema mostrará "Stock insuficiente para {producto} talla {talla}".
- **Dado que** el usuario no está autenticado, **cuando** intente acceder al checkout, **entonces** el sistema lo redirigirá al login.

---

### HU-09 – Confirmación por WhatsApp

| Campo | Detalle |
|-------|---------|
| **Título** | CONFIRMACIÓN DE PEDIDO POR WHATSAPP |
| **Nro Sprint** | 4 |
| **Responsable** | Nicolas Camilo Bocanegra Vaca |

**Como:** cliente que acaba de realizar un pedido
**Quiero:** enviar la confirmación por WhatsApp al vendedor
**Para:** notificar mi compra con todos los detalles.

**Criterios de Aceptación:**
- **Dado que** el pedido fue creado, **cuando** se muestre la confirmación, **entonces** aparecerá un botón verde de WhatsApp con mensaje prellenado (número de pedido, productos, total COP).
- **Dado que** el usuario hace clic en el botón WhatsApp, **cuando** se abra el enlace, **entonces** redirigirá a WhatsApp con el mensaje listo para enviar.

---

### HU-10 – Historial de pedidos

| Campo | Detalle |
|-------|---------|
| **Título** | HISTORIAL DE PEDIDOS DEL CLIENTE |
| **Nro Sprint** | 4 |
| **Responsable** | Nicolas Camilo Bocanegra Vaca |

**Como:** cliente registrado
**Quiero:** ver el listado de todos mis pedidos y el detalle de cada uno
**Para:** hacer seguimiento a mis compras.

**Criterios de Aceptación:**
- **Dado que** el usuario accede a "Mis Pedidos", **cuando** cargue la página, **entonces** verá sus pedidos con número, fecha, total y estado.
- **Dado que** el usuario hace clic en un pedido, **cuando** cargue el detalle, **entonces** verá los productos, datos de envío e historial completo de estados con fechas.
- **Dado que** un usuario intenta ver un pedido ajeno, **cuando** acceda a la URL, **entonces** el sistema mostrará "No tienes permiso para ver este pedido".

---

### HU-11 – Edición de perfil

| Campo | Detalle |
|-------|---------|
| **Título** | EDICIÓN DE PERFIL DE USUARIO |
| **Nro Sprint** | 5 |
| **Responsable** | Nicolas Camilo Bocanegra Vaca |

**Como:** usuario registrado
**Quiero:** editar mis datos personales y cambiar mi contraseña
**Para:** mantener mi información actualizada para futuros pedidos.

**Criterios de Aceptación:**
- **Dado que** el usuario modifica sus datos y guarda, **cuando** se procese, **entonces** el sistema actualizará los datos y mostrará "Perfil actualizado exitosamente".
- **Dado que** el usuario ingresa la contraseña actual correcta y una nueva, **cuando** guarde, **entonces** el sistema actualizará la contraseña.
- **Dado que** el usuario ingresa la contraseña actual incorrecta, **cuando** intente cambiarla, **entonces** el sistema mostrará "Contraseña actual incorrecta".

---

### HU-12 – Dashboard administrativo

| Campo | Detalle |
|-------|---------|
| **Título** | DASHBOARD ADMINISTRATIVO |
| **Nro Sprint** | 6 |
| **Responsable** | Nicolas Camilo Bocanegra Vaca |

**Como:** administrador
**Quiero:** ver un panel de control con las estadísticas del negocio
**Para:** tomar decisiones sobre inventario, ventas y pedidos.

**Criterios de Aceptación:**
- **Dado que** el administrador accede al dashboard, **cuando** cargue, **entonces** verá: total pedidos, ventas totales COP, pedidos por estado, bajo stock y últimos 10 pedidos.
- **Dado que** un cliente intenta acceder a `/admin/dashboard`, **cuando** ingrese la URL, **entonces** el sistema negará el acceso y lo redirigirá al catálogo.

---

### HU-13 – Crear producto

| Campo | Detalle |
|-------|---------|
| **Título** | CREAR PRODUCTO |
| **Nro Sprint** | 6 |
| **Responsable** | Nicolas Camilo Bocanegra Vaca |

**Como:** administrador
**Quiero:** crear nuevos hoodies con información completa y foto
**Para:** agregarlos al catálogo para que los clientes puedan comprarlos.

**Criterios de Aceptación:**
- **Dado que** el administrador completa el formulario con todos los campos válidos, **cuando** presione "Crear Producto", **entonces** el sistema guardará el producto con `activo=True` y lo publicará en el catálogo.
- **Dado que** el administrador sube una imagen con extensión no permitida, **cuando** intente crear el producto, **entonces** el sistema mostrará el error de formato.
- **Dado que** la imagen supera 5MB, **cuando** intente enviar el formulario, **entonces** el sistema mostrará el error de tamaño excedido.

---

### HU-14 – Editar producto

| Campo | Detalle |
|-------|---------|
| **Título** | EDITAR PRODUCTO |
| **Nro Sprint** | 6 |
| **Responsable** | Nicolas Camilo Bocanegra Vaca |

**Como:** administrador
**Quiero:** editar la información de un producto existente
**Para:** actualizar precios, descripciones, stock o imágenes.

**Criterios de Aceptación:**
- **Dado que** el administrador modifica algún campo y guarda, **cuando** se procese, **entonces** el sistema actualizará los datos y mostrará "Producto actualizado exitosamente".
- **Dado que** el administrador sube nueva imagen, **cuando** guarde, **entonces** el sistema reemplazará la imagen anterior.
- **Dado que** no se sube nueva imagen, **cuando** guarde, **entonces** el sistema conservará la imagen anterior.

---

### HU-15 – Desactivar y restaurar producto

| Campo | Detalle |
|-------|---------|
| **Título** | DESACTIVAR Y RESTAURAR PRODUCTO |
| **Nro Sprint** | 6 |
| **Responsable** | Nicolas Camilo Bocanegra Vaca |

**Como:** administrador
**Quiero:** desactivar productos sin eliminarlos y poder reactivarlos
**Para:** ocultar temporalmente un producto sin perder su historial.

**Criterios de Aceptación:**
- **Dado que** el administrador desactiva un producto, **cuando** confirme, **entonces** el producto dejará de aparecer en el catálogo de clientes.
- **Dado que** el administrador restaura un producto, **cuando** confirme, **entonces** el producto volverá a ser visible en el catálogo.

---

### HU-16 – Gestión de pedidos (admin)

| Campo | Detalle |
|-------|---------|
| **Título** | GESTIÓN DE PEDIDOS (ADMINISTRADOR) |
| **Nro Sprint** | 7 |
| **Responsable** | Nicolas Camilo Bocanegra Vaca |

**Como:** administrador
**Quiero:** ver todos los pedidos y filtrarlos por estado
**Para:** hacer seguimiento de las ventas y atender pedidos pendientes.

**Criterios de Aceptación:**
- **Dado que** el administrador accede a `/admin/orders`, **cuando** cargue, **entonces** verá todos los pedidos con número, cliente, fecha, total y estado.
- **Dado que** el administrador filtra por estado, **cuando** aplique el filtro, **entonces** el sistema mostrará solo los pedidos de ese estado.
- **Dado que** el administrador hace clic en un pedido, **cuando** cargue el detalle, **entonces** verá los productos, datos de envío e historial completo de estados.

---

### HU-17 – Cambiar estado de pedido

| Campo | Detalle |
|-------|---------|
| **Título** | CAMBIAR ESTADO DE PEDIDO |
| **Nro Sprint** | 7 |
| **Responsable** | Nicolas Camilo Bocanegra Vaca |

**Como:** administrador
**Quiero:** cambiar el estado de un pedido a lo largo de su ciclo de vida
**Para:** informar al cliente el progreso de su compra.

**Criterios de Aceptación:**
- **Dado que** el administrador selecciona un nuevo estado válido y confirma, **cuando** se procese, **entonces** el sistema actualizará el estado y registrará en el historial la fecha y el admin responsable.
- **Dado que** el administrador intenta asignar el mismo estado actual, **cuando** envíe, **entonces** el sistema mostrará "El pedido ya está en ese estado".

---

### HU-18 – Exportar pedidos a CSV

| Campo | Detalle |
|-------|---------|
| **Título** | EXPORTAR PEDIDOS A CSV |
| **Nro Sprint** | 7 |
| **Responsable** | Nicolas Camilo Bocanegra Vaca |

**Como:** administrador
**Quiero:** exportar el listado de pedidos en formato CSV
**Para:** analizar las ventas en Excel o Google Sheets.

**Criterios de Aceptación:**
- **Dado que** el administrador hace clic en "Exportar CSV", **cuando** se descargue, **entonces** generará `pedidos.csv` con columnas: Número Pedido, Fecha, Cliente, Teléfono, Ciudad, Total y Estado.
- **Dado que** el administrador filtra por estado antes de exportar, **cuando** descargue el CSV, **entonces** el archivo contendrá solo los pedidos de ese estado.

---

### HU-19 – Control automático de stock

| Campo | Detalle |
|-------|---------|
| **Título** | CONTROL AUTOMÁTICO DE STOCK |
| **Nro Sprint** | 8 |
| **Responsable** | Nicolas Camilo Bocanegra Vaca |

**Como:** sistema
**Quiero:** actualizar automáticamente el stock al confirmar un pedido
**Para:** garantizar que no se venda más inventario del disponible.

**Criterios de Aceptación:**
- **Dado que** se confirma un pedido, **cuando** el sistema lo procese, **entonces** reducirá el stock de cada ítem por talla de manera inmediata.
- **Dado que** el stock de una talla queda en 0, **cuando** otro cliente vea el detalle, **entonces** esa talla no aparecerá disponible.
- **Dado que** el stock total cae por debajo de 10, **cuando** el admin acceda al dashboard, **entonces** el producto aparecerá en la alerta de bajo stock.

---

### HU-20 – Número de pedido único

| Campo | Detalle |
|-------|---------|
| **Título** | GENERACIÓN DE NÚMERO DE PEDIDO ÚNICO |
| **Nro Sprint** | 8 |
| **Responsable** | Nicolas Camilo Bocanegra Vaca |

**Como:** sistema
**Quiero:** generar un número de pedido único para cada compra
**Para:** identificar inequívocamente cada pedido y facilitar su seguimiento.

**Criterios de Aceptación:**
- **Dado que** se crea un pedido, **cuando** el sistema lo procese, **entonces** generará un número con formato `ORD-YYYY-NNNNNN` que no exista previamente en la base de datos.
- **Dado que** hay una colisión de número, **cuando** el sistema lo detecte, **entonces** reintentará la generación hasta obtener un número único.
- **Dado que** el número fue generado, **cuando** el cliente lo vea, **entonces** aparecerá en la página de confirmación y en el mensaje de WhatsApp.

---

## 7. Diagramas de Casos de Uso

### 7.1 Diagrama General del Sistema

```
                    ┌────────────────────────────────────────────────────┐
                    │               SISTEMA HOODIE SHOP                  │
                    │                                                    │
  ┌──────────┐      │  ┌──────────────────────────────────────────────┐  │
  │          │      │  │         MÓDULO DE AUTENTICACIÓN              │  │
  │VISITANTE │─────▶│  │  ○ Registrarse                               │  │
  │          │      │  │  ○ Iniciar Sesión                             │  │
  └──────────┘      │  └──────────────────────────────────────────────┘  │
       │            │                                                    │
       ▼            │  ┌──────────────────────────────────────────────┐  │
  ┌──────────┐      │  │         MÓDULO DE CATÁLOGO                   │  │
  │          │      │  │  ○ Ver Catálogo                               │  │
  │ CLIENTE  │─────▶│  │  ○ Buscar Productos                           │  │
  │          │      │  │  ○ Ver Detalle de Producto                    │  │
  └──────────┘      │  └──────────────────────────────────────────────┘  │
       │            │                                                    │
       │            │  ┌──────────────────────────────────────────────┐  │
       │            │  │         MÓDULO DE CARRITO                    │  │
       │            │  │  ○ Agregar al Carrito                         │  │
       │            │  │  ○ Ver Carrito                                │  │
       │            │  │  ○ Eliminar Ítem / Vaciar Carrito             │  │
       │            │  └──────────────────────────────────────────────┘  │
       │            │                                                    │
       └───────────▶│  ┌────────────────────────���─────────────────────┐  │
                    │  │         MÓDULO DE PEDIDOS                    │  │
                    │  │  ○ Realizar Pedido (Checkout)                 │  │
                    │  │  ○ Confirmar por WhatsApp                     │  │
                    │  │  ○ Ver Mis Pedidos / Detalle de Pedido        │  │
                    │  └──────────────────────────────────────────────┘  │
                    │                                                    │
  ┌──────────────┐  │  ┌──────────────────────────────────────────────┐  │
  │              │  │  │        MÓDULO ADMINISTRATIVO                 │  │
  │ADMINISTRADOR │─▶│  │  ○ Ver Dashboard con Estadísticas            │  │
  │              │  │  │  ○ Crear / Editar / Desactivar Producto      │  │
  └──────────────┘  │  │  ○ Ver / Filtrar / Gestionar Pedidos         │  │
                    │  │  ○ Cambiar Estado de Pedido                  │  │
                    │  │  ○ Exportar Pedidos CSV                      │  │
                    │  └──────────────────────────────────────────────┘  │
                    └────────────────────────────────────────────────────┘
```

---

### 7.2 CU-RF01 y RF02 y RF03: Autenticación

```
┌──────────────────────────────────────────────────────┐
│     CU-RF01/RF02/RF03: AUTENTICACIÓN DE USUARIOS     │
│                                                      │
│  VISITANTE ──▶ ○ Registrarse                         │
│                      │ «include»                     │
│                      ▼                               │
│               ○ Validar email único,                 │
│                 contraseña y campos                  │
│                                                      │
│  USUARIO   ──▶ ○ Iniciar Sesión                      │
│  REGISTRADO          │ «extend»                      │
│                      ▼                               │
│               ○ Redirigir según rol                  │
│                 (admin → dashboard                   │
│                  user  → catálogo)                   │
│                                                      │
│  USUARIO   ──▶ ○ Cerrar Sesión                       │
│  AUTENTICADO         │ «include»                     │
│                      ▼                               │
│               ○ Destruir sesión Flask-Login          │
└──────────────────────────────────────────────────────┘
```

---

### 7.3 CU-RF04 y RF17: Catálogo y Búsqueda

```
┌──────────────────────────────────────────────────────┐
│     CU-RF04/RF17: CATÁLOGO Y BÚSQUEDA                │
│                                                      │
│  VISITANTE /  ──▶ ○ Ver Catálogo GET /catalog        │
│  CLIENTE              │ «extend»                     │
│                       ▼                              │
│                ○ Buscar productos ?q=texto           │
│                  (regex insensible a                 │
│                   mayúsculas en nombre               │
│                   y descripción)                     │
│                                                      │
│  VISITANTE /  ──▶ ○ Ver Detalle                      │
│  CLIENTE           GET /product/<id>                 │
│                       │ «include»                    │
│                       ▼                              │
│                ○ Verificar producto                  │
│                  activo en MongoDB                   │
└──────────────────────────────────────────────────────┘
```

---

### 7.4 CU-RF06 y RF07 y RF16: Carrito y Stock

```
┌──────────────────────────────────────────────────────┐
│     CU-RF06/RF07/RF16: CARRITO Y CONTROL DE STOCK    │
│                                                      │
│  VISITANTE /  ──▶ ○ Agregar al Carrito               │
│  CLIENTE           POST /cart/add                    │
│                       │ «include»                    │
│                       ▼                              │
│                ○ Verificar stock                     │
│                  tiene_stock(talla, cantidad)         │
│                                                      │
│               ──▶ ○ Ver Carrito GET /cart            │
│                                                      │
│               ──▶ ○ Eliminar Ítem                    │
│                    GET /cart/remove/<index>          │
│                                                      │
│               ──▶ ○ Actualizar Cantidades            │
│                    POST /cart/update                 │
│                                                      │
│               ──▶ ○ Vaciar Carrito                   │
│                    GET /cart/clear                   │
└──────────────────────────────────────────────────────┘
```

---

### 7.5 CU-RF05 y RF08 y RF09 y RF18: Pedidos

```
┌──────────────────────────────────────────────────────┐
│     CU-RF05/RF08/RF09/RF18: PEDIDOS Y WHATSAPP       │
│                                                      │
│  CLIENTE   ──▶ ○ Realizar Pedido                     │
│ (autenticado)   POST /checkout                       │
│                       │ «include»                    │
│                       ▼                              │
│                ○ Validar stock + crear               │
│                  pedido + generar número             │
│                  ORD-YYYY-NNNNNN (único)             │
│                       │ «include»                    │
│                       ▼                              │
│                ○ Reducir stock                       │
│                  por talla en MongoDB                │
│                       │ «include»                    │
│                       ▼                              │
│                ○ Generar enlace WhatsApp             │
│                  wa.me con mensaje                   │
│                  prellenado                          │
└──────────────────────────────────────────────────────┘
```

---

### 7.6 CU-RF10 y RF19: Historial de Pedidos del Cliente

```
┌──────────────────────────────────────────────────────┐
│     CU-RF10/RF19: HISTORIAL Y SEGURIDAD DE PEDIDOS   │
│                                                      │
│  CLIENTE   ──▶ ○ Ver Mis Pedidos                     │
│                  GET /user/orders                    │
│                       │ «extend»                     │
│                       ▼                              │
│                ○ Ver Detalle de Pedido               │
│                  GET /user/orders/<id>               │
│                       │ «include»                    │
│                       ▼                              │
│                ○ Verificar propiedad                 │
│                  order.user_id ==                    │
│                  current_user.get_id()               │
│                  (previene acceso ajeno)             │
└──────────────────────────────────────────────────────┘
```

---

### 7.7 CU-RF11: Perfil de Usuario

```
┌──────────────────────────────────────────────────────┐
│     CU-RF11: PERFIL DE USUARIO                       │
│                                                      │
│  CLIENTE   ──▶ ○ Ver / Editar Perfil                 │
│                  GET/POST /user/profile               │
│                       │ «extend»                     │
│                       ▼                              │
│                ○ Cambiar contraseña                  │
│                  (opcional)                          │
│                       │ «include»                    │
│                       ▼                              │
│                ○ Verificar contraseña                │
│                  actual con check_password()         │
└──────────────────────────────────────────────────────┘
```

---

### 7.8 CU-RF12 y RF20: Dashboard Administrativo

```
┌──────────────────────────────────────────────────────┐
│     CU-RF12/RF20: DASHBOARD Y ESTADÍSTICAS           │
│                                                      │
│  ADMIN     ──▶ ○ Ver Dashboard                       │
│                  GET /admin/dashboard                │
│                       │ «include»                    │
│                       ▼                              │
│                ○ Obtener estadísticas                │
│                  total pedidos, ventas COP,          │
│                  pedidos por estado,                 │
│                  bajo stock (<10 unidades)           │
│                                                      │
│  ADMIN     ──▶ ○ Exportar CSV                        │
│                  GET /admin/orders/export            │
│                       │ «extend»                     │
│                       ▼                              │
│                ○ Filtrar por estado                  │
│                  antes de exportar                   │
└──────────────────────────────────────────────────────┘
```

---

### 7.9 CU-RF13: CRUD de Productos (Admin)

```
┌──────────────────────────────────────────────────────┐
│     CU-RF13: GESTIÓN DE PRODUCTOS                    │
│                                                      │
│  ADMIN     ──▶ ○ Crear Producto                      │
│                  POST /admin/products/new            │
│                       │ «include»                    │
│                       ▼                              │
│                ○ Validar imagen                      │
│                  (extensión + tamaño)                │
│                  + secure_filename()                 │
│                                                      │
│  ADMIN     ──▶ ��� Editar Producto                     │
│                  POST /admin/products/<id>/edit      │
│                                                      │
│  ADMIN     ──▶ ○ Desactivar Producto                 │
│                  GET /admin/products/<id>/delete     │
│                  (soft delete: activo=False)         │
│                                                      │
│  ADMIN     ──▶ ○ Restaurar Producto                  │
│                  GET /admin/products/<id>/restore    │
└──────────────────────────────────────────────────────┘
```

---

### 7.10 CU-RF14 y RF15: Gestión de Pedidos (Admin)

```
┌──────────────────────────────────────────────────────┐
│     CU-RF14/RF15: GESTIÓN DE PEDIDOS ADMIN           │
│                                                      │
│  ADMIN     ──▶ ○ Ver Todos los Pedidos               │
│                  GET /admin/orders                   │
│                       │ «extend»                     │
│                       ▼                              │
│                ○ Filtrar por estado ?estado=         │
│                                                      │
│  ADMIN     ──▶ ○ Ver Detalle de Pedido               │
│                  GET /admin/orders/<id>              │
│                                                      │
│  ADMIN     ──▶ ○ Cambiar Estado                      │
│                  POST /admin/orders/<id>/            │
│                  change-status                       │
│                       │ «include»                    │
│                       ▼                              │
│                ○ Registrar en historial_estados      │
│                  (estado + fecha + admin_id)         │
│                                                      │
│  ADMIN     ──▶ ○ Exportar CSV                        │
│                  GET /admin/orders/export            │
└──────────────────────────────────────────────────────┘
```

---

## 8. Implementación – Despliegue y Código Fuente

### 8.1 Repositorio público en GitHub

| Campo | Detalle |
|-------|---------|
| **URL del repositorio** | https://github.com/DjKiller07FT/hoodie-shop |
| **Visibilidad** | 🌐 Público (auditable) |
| **Rama principal** | `main` |
| **Descripción** | E-commerce para venta de hoodies con Flask y MongoDB |

### 8.2 Composición del código fuente

| Lenguaje | Porcentaje | Uso |
|----------|-----------|-----|
| Python | 49.5% | Backend: modelos, servicios, rutas, configuración |
| HTML (Jinja2) | 46.4% | Templates: todas las vistas del sistema |
| JavaScript | 2.8% | Validaciones cliente, preview de imágenes |
| CSS | 1.3% | Estilos personalizados sobre Bootstrap |

### 8.3 Estructura del código fuente

```
hoodie-shop/
├── app/
│   ├── __init__.py        → Factory Pattern, conexión BD
│   ├── config.py          → Configuración por entorno
│   ├── models/            → User, Product, Order
│   ├── routes/            → auth, shop, admin, user (Blueprints)
│   ├── services/          → AuthService, ProductService, OrderService, WhatsAppService
│   ├── utils/             → decoradores, helpers
│   ├── templates/         → 14 templates HTML
│   └── static/            → CSS, JS, imágenes
├── tests/                 → test_auth.py, test_products.py, test_orders.py
├── docs/                  → SRS, Documento Técnico, HU, Informe Final
├── .env.example           → Plantilla de variables de entorno
├── requirements.txt       → Dependencias del proyecto
├── run.py                 → Punto de entrada
├── seed_admin.py          → Script crear administrador
└── setup_indexes.py       → Script crear índices MongoDB
```

### 8.4 Instrucciones de instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/DjKiller07FT/hoodie-shop.git
cd hoodie-shop

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate          # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
copy .env.example .env
# (Editar .env con los valores reales)

# 5. Crear administrador inicial
python seed_admin.py

# 6. Ejecutar la aplicación
python run.py
# Abrir: http://localhost:5000
```

### 8.5 Variables de entorno requeridas

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=clave-secreta-segura
MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net/hoodie_shop
UPLOAD_FOLDER=app/static/uploads
MAX_CONTENT_LENGTH=5242880
PRODUCTS_PER_PAGE=12
ORDERS_PER_PAGE=20
ADMIN_EMAIL=admin@hoodieshop.com
ADMIN_PASSWORD=admin123
ADMIN_NOMBRE=Administrador
WHATSAPP_NUMBER=57XXXXXXXXXX
PORT=5000
```

---

## 9. Checklist de Pruebas

### 9.1 Pruebas Funcionales – Verificación de los 20 RF

| # | RF | Caso de prueba | Resultado esperado | ¿Cumple? |
|---|-----|---------------|-------------------|---------|
| 1 | RF-01 | Registrar usuario con todos los datos válidos | Cuenta creada, sesión iniciada, redirección al catálogo | ✅ SÍ CUMPLE |
| 2 | RF-01 | Registrar con email duplicado | Mensaje "El email ya está registrado" | ✅ SÍ CUMPLE |
| 3 | RF-01 | Registrar con contraseñas distintas | Mensaje "Las contraseñas no coinciden" | ✅ SÍ CUMPLE |
| 4 | RF-02 | Login con credenciales correctas (cliente) | Sesión activa, redirección al catálogo | ✅ SÍ CUMPLE |
| 5 | RF-02 | Login con credenciales correctas (admin) | Sesión activa, redirección al dashboard | ✅ SÍ CUMPLE |
| 6 | RF-02 | Login con contraseña incorrecta | Mensaje "Email o contraseña incorrectos" | ✅ SÍ CUMPLE |
| 7 | RF-03 | Cerrar sesión | Sesión destruida, redirección al catálogo | ✅ SÍ CUMPLE |
| 8 | RF-04 | Ver catálogo sin autenticación | Todos los productos activos visibles | ✅ SÍ CUMPLE |
| 9 | RF-04 | Buscar producto existente `?q=hoodie` | Productos que coincidan con el texto | ✅ SÍ CUMPLE |
| 10 | RF-04 | Buscar producto inexistente | Mensaje informativo sin resultados | ✅ SÍ CUMPLE |
| 11 | RF-05 | Ver detalle de producto activo | Imagen, nombre, precio, tallas, colores visibles | ✅ SÍ CUMPLE |
| 12 | RF-05 | Acceder a producto desactivado | Redirección al catálogo con mensaje de error | ✅ SÍ CUMPLE |
| 13 | RF-06 | Agregar producto al carrito con stock disponible | Producto en carrito, contador actualizado | ✅ SÍ CUMPLE |
| 14 | RF-06 | Agregar mismo producto (talla+color) ya en carrito | Suma la cantidad al ítem existente | ✅ SÍ CUMPLE |
| 15 | RF-07 | Ver carrito con ítems | Lista completa con subtotales y total en COP | ✅ SÍ CUMPLE |
| 16 | RF-07 | Eliminar ítem del carrito | Ítem eliminado, total recalculado | ✅ SÍ CUMPLE |
| 17 | RF-07 | Acceder a carrito vacío | Mensaje "Tu carrito está vacío" | ✅ SÍ CUMPLE |
| 18 | RF-08 | Checkout con carrito lleno y sesión activa | Pedido creado, stock reducido, carrito vaciado | ✅ SÍ CUMPLE |
| 19 | RF-08 | Checkout sin autenticación | Redirección a login con parámetro `?next=/checkout` | ✅ SÍ CUMPLE |
| 20 | RF-08 | Checkout con stock agotado | Mensaje "Stock insuficiente para {producto}" | ✅ SÍ CUMPLE |
| 21 | RF-09 | Botón WhatsApp en confirmación de pedido | Enlace `wa.me` con mensaje prellenado en español | ✅ SÍ CUMPLE |
| 22 | RF-09 | Mensaje WhatsApp incluye número de pedido y total | Formato `ORD-YYYY-NNNNNN` y `$XXX.XXX COP` | ✅ SÍ CUMPLE |
| 23 | RF-10 | Ver historial de pedidos propios | Lista con estado y total en COP | ✅ SÍ CUMPLE |
| 24 | RF-10 | Intentar ver pedido ajeno | Mensaje "No tienes permiso" + redirección | ✅ SÍ CUMPLE |
| 25 | RF-11 | Editar datos de perfil | Datos actualizados, mensaje de éxito | ✅ SÍ CUMPLE |
| 26 | RF-11 | Cambiar contraseña con contraseña actual correcta | Contraseña actualizada exitosamente | ✅ SÍ CUMPLE |
| 27 | RF-11 | Cambiar contraseña con contraseña actual incorrecta | Mensaje "Contraseña actual incorrecta" | ✅ SÍ CUMPLE |
| 28 | RF-12 | Ver dashboard como administrador | Estadísticas, bajo stock y pedidos recientes visibles | ✅ SÍ CUMPLE |
| 29 | RF-12 | Cliente intenta acceder a `/admin/dashboard` | Acceso denegado, redirección al catálogo | ✅ SÍ CUMPLE |
| 30 | RF-13 | Crear producto con imagen válida | Producto visible en catálogo con imagen | ✅ SÍ CUMPLE |
| 31 | RF-13 | Editar precio de producto | Precio actualizado en catálogo y detalle | ✅ SÍ CUMPLE |
| 32 | RF-13 | Desactivar producto | Producto desaparece del catálogo de clientes | ✅ SÍ CUMPLE |
| 33 | RF-13 | Restaurar producto desactivado | Producto vuelve a aparecer en el catálogo | ✅ SÍ CUMPLE |
| 34 | RF-14 | Cambiar estado de pedido a ALISTAMIENTO | Estado actualizado, historial registrado con fecha | ✅ SÍ CUMPLE |
| 35 | RF-14 | Filtrar pedidos por estado RECIBIDO | Solo pedidos con ese estado visibles | ✅ SÍ CUMPLE |
| 36 | RF-15 | Exportar todos los pedidos a CSV | Archivo `pedidos.csv` descargado con columnas correctas | ✅ SÍ CUMPLE |
| 37 | RF-16 | Stock se reduce al confirmar pedido | Stock decrementado correctamente por talla | ✅ SÍ CUMPLE |
| 38 | RF-17 | Buscar producto en panel admin con `?q=` | Resultados filtrados en la lista administrativa | ✅ SÍ CUMPLE |
| 39 | RF-18 | Número de pedido generado con formato correcto | Formato `ORD-2026-NNNNNN` único en cada pedido | ✅ SÍ CUMPLE |
| 40 | RF-19 | Verificación de propiedad en acceso a pedido | Acceso bloqueado para pedidos de otros usuarios | ✅ SÍ CUMPLE |
| 41 | RF-20 | Estadísticas del dashboard correctas | Total pedidos, ventas y pedidos por estado precisos | ✅ SÍ CUMPLE |

---

### 9.2 Pruebas de Seguridad

| # | Caso de prueba | Resultado esperado | ¿Cumple? |
|---|---------------|-------------------|---------|
| 42 | Subir imagen con extensión `.exe` | Mensaje de formato no permitido | ✅ SÍ CUMPLE |
| 43 | Subir imagen mayor a 5MB | Mensaje de tamaño excedido | ✅ SÍ CUMPLE |
| 44 | Contraseñas no expuestas en HTML ni logs | No hay texto plano de contraseña en respuestas | ✅ SÍ CUMPLE |
| 45 | Usuario no autenticado accede a `/user/profile` | Redirección al login | ✅ SÍ CUMPLE |

---

### 9.3 Pruebas de Interfaz (Responsividad)

| # | Caso de prueba | Resultado esperado | ¿Cumple? |
|---|---------------|-------------------|---------|
| 46 | Ver catálogo en móvil (320px) | Grid de 1 columna, imágenes adaptadas | ✅ SÍ CUMPLE |
| 47 | Ver catálogo en tablet (768px) | Grid de 2 columnas | ✅ SÍ CUMPLE |
| 48 | Ver catálogo en escritorio (1200px) | Grid de 3-4 columnas | ✅ SÍ CUMPLE |
| 49 | Mensajes flash visibles y cerrables | Alertas Bootstrap con botón X | ✅ SÍ CUMPLE |
| 50 | Contador del carrito actualizado en navbar | Badge con número de ítems correcto | ✅ SÍ CUMPLE |

---

### 9.4 Resumen del checklist

| Categoría | Total | Cumple | No cumple |
|-----------|-------|--------|-----------|
| Pruebas funcionales (20 RF) | 41 | **41** | 0 |
| Pruebas de seguridad | 4 | **4** | 0 |
| Pruebas de interfaz | 5 | **5** | 0 |
| **TOTAL** | **50** | **50 ✅** | **0** |

> **Resultado:** El 100% de los casos de prueba documentados se cumplen satisfactoriamente.

---

## 10. Plan de Capacitación

### 10.1 Objetivos del plan

Garantizar que los usuarios del sistema **Hoodie Shop** puedan utilizar todas las funcionalidades de manera autónoma, eficiente y segura, minimizando errores operativos.

### 10.2 Usuarios a capacitar

| Tipo de usuario | Módulos a capacitar |
|----------------|----------------------|
| **Administrador (1 persona)** | Todos los módulos (completo) |
| **Clientes (variable)** | Catálogo, carrito, pedidos, perfil |

### 10.3 Plan de capacitación: Administrador

| Sesión | Duración | Tema | Contenido |
|--------|----------|------|-----------|
| 1 | 30 min | Acceso al sistema | Login con credenciales admin, navegación por el menú, cierre de sesión seguro |
| 2 | 45 min | Gestión de productos | Crear, editar, subir imágenes, desactivar y restaurar productos. Gestión de stock por talla |
| 3 | 30 min | Dashboard | Interpretación de estadísticas, identificación de productos con bajo stock, lectura de métricas |
| 4 | 45 min | Gestión de pedidos | Ver y filtrar pedidos, cambiar estado, interpretar historial de estados |
| 5 | 20 min | Exportar CSV | Exportar pedidos, filtrar por estado, interpretar el archivo en Excel |
| 6 | 20 min | Seguridad | Cambio periódico de contraseña, no compartir credenciales, cierre de sesión en dispositivos compartidos |

**Total: 3 horas**

---

### 10.4 Plan de capacitación: Cliente

| Sesión | Duración | Tema | Contenido |
|--------|----------|------|-----------|
| 1 | 20 min | Registro e inicio de sesión | Crear cuenta, iniciar sesión, opción "Recordarme", cerrar sesión |
| 2 | 20 min | Explorar el catálogo | Navegar por productos, usar la búsqueda, ver detalle de un producto |
| 3 | 25 min | Comprar un producto | Seleccionar talla y color, agregar al carrito, modificar carrito, proceder al pago |
| 4 | 20 min | Confirmar pedido por WhatsApp | Proceso de checkout, página de confirmación, botón WhatsApp |
| 5 | 15 min | Seguimiento de pedidos | Acceder a "Mis Pedidos", interpretar los estados, ver el historial |

**Total: 1 hora 40 minutos**

---

### 10.5 Modalidades de capacitación

| Modalidad | Descripción |
|-----------|-------------|
| **Presencial** | Sesión práctica frente al computador con el sistema en funcionamiento |
| **Video tutorial** | Grabación de las sesiones para consulta posterior |
| **Manual de usuario** | Documento PDF con capturas de pantalla paso a paso |
| **Soporte WhatsApp** | Canal de soporte para dudas durante los primeros 30 días |

### 10.6 Indicadores de éxito

| Indicador | Meta |
|-----------|------|
| Administrador realiza CRUD de productos sin ayuda | 100% |
| Administrador cambia estado de pedido correctamente | 100% |
| Cliente completa proceso de compra de inicio a fin | 100% |
| Cliente confirma pedido por WhatsApp correctamente | 100% |
| Reducción de consultas de soporte tras capacitación | > 80% en 30 días |

---

## 11. Conclusiones

El desarrollo de **Hoodie Shop** permitió aplicar de forma integral los conocimientos adquiridos durante el proceso de formación, abarcando todas las fases del ciclo de vida del software:

1. **Análisis:** Se identificaron y documentaron 20 requisitos funcionales y 20 no funcionales bajo la norma IEEE 830, garantizando que el sistema cubre las necesidades reales del negocio.

2. **Diseño:** La arquitectura MVC con capa de servicios y el patrón Factory, combinados con MongoDB como base de datos NoSQL, demostraron ser las elecciones correctas para un sistema de e-commerce flexible y escalable.

3. **Desarrollo:** El stack Python + Flask + MongoDB Atlas permitió construir un sistema robusto con 4,563 líneas de código en 48 archivos, cumpliendo todos los requisitos en 8 sprints bajo metodología SCRUM adaptada.

4. **Pruebas:** Los 50 casos de prueba documentados fueron ejecutados satisfactoriamente, con un cumplimiento del 100% de los requisitos funcionales, de seguridad e interfaz.

5. **Implantación:** El sistema está preparado para desplegarse en producción y cuenta con un plan de capacitación estructurado para garantizar la adopción exitosa por parte de los usuarios.

El proyecto demuestra que es posible construir una solución de comercio electrónico completa, segura y funcional utilizando exclusivamente herramientas gratuitas y de código abierto, lo que lo convierte en una propuesta viable para emprendedores del sector textil en Colombia.

---

## 12. Referencias

| Recurso | URL |
|---------|-----|
| Repositorio GitHub | https://github.com/DjKiller07FT/hoodie-shop |
| Flask 3.0 | https://flask.palletsprojects.com/ |
| MongoDB Atlas | https://docs.mongodb.com/ |
| Flask-Login | https://flask-login.readthedocs.io/ |
| PyMongo 4.6.1 | https://pymongo.readthedocs.io/ |
| Bootstrap 5.3 | https://getbootstrap.com/docs/5.3/ |
| Norma IEEE 830 | https://ieeexplore.ieee.org/document/720574 |
| Python 3.14 | https://docs.python.org/3/ |
| Werkzeug 3.0.1 | https://werkzeug.palletsprojects.com/ |
| WhatsApp API | https://faq.whatsapp.com/425247423114725 |

---

**Documento elaborado por:** Nicolas Camilo Bocanegra Vaca
**Email:** nicolas.bocanegra@pi.edu.co
**GitHub:** [@DjKiller07FT](https://github.com/DjKiller07FT)
**Repositorio:** https://github.com/DjKiller07FT/hoodie-shop
**Fecha:** Marzo 2026
**Versión:** 1.0