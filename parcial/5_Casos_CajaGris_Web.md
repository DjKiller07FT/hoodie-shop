# CASOS DE PRUEBA – CAJA GRIS
## Parcial de Testing de Software – Ingeniería de Software II

**Estudiante:** Nicolas Camilo Bocanegra Vaca
**Fecha:** Marzo 2026
**Proyecto:** Hoodie Shop – E-commerce
**Módulo:** Gestión de Usuarios y Autenticación
**Técnica:** Caja Gris
**Repositorio:** https://github.com/DjKiller07FT/hoodie-shop

---

## Descripción de la técnica aplicada

Las pruebas de **caja gris** combinan elementos de caja negra y caja blanca. El tester tiene **conocimiento parcial** de la arquitectura interna del sistema (estructura de base de datos, esquemas de datos, tecnologías usadas, flujos generales) pero **no accede al código fuente línea por línea**. Se validan las **interacciones entre capas**: frontend ↔ backend ↔ base de datos.

En **Hoodie Shop**, el tester conoce:
- La estructura de la colección `users` en MongoDB Atlas
- Que las contraseñas se almacenan con hash `PBKDF2-SHA256`
- Que las sesiones usan `Flask-Login` con `SESSION_TYPE=filesystem`
- Que el rol del usuario se almacena como campo `rol: 'user' | 'admin'`
- Que el decorador `@admin_required` protege todas las rutas `/admin/*`
- Que el email se normaliza a minúsculas antes de guardarse

Pero **no conoce** la implementación exacta de cada función ni los detalles internos del servicio.

---

## Casos de Prueba

---

### WEB-CG-01

| Campo | Detalle |
|-------|---------|
| **ID** | WEB-CG-01 |
| **Título** | Login exitoso verifica persistencia real de sesión en MongoDB + Flask-Login |
| **Técnica** | Caja Gris |
| **Capa** | Frontend → Backend → Base de Datos → Sesión |
| **Prioridad** | Alta |

**🌐 Contexto Web**
- URL/Endpoint: `POST /auth/login` → `GET /user/profile`
- Método: `POST` seguido de `GET`
- Conocimiento arquitectónico utilizado:
  - Sé que Flask-Login almacena el `user_id` en la sesión del servidor
  - Sé que el campo `_id` de MongoDB se convierte a string con `get_id()`
  - Sé que `SESSION_PERMANENT = True` con duración de 7 días

**✅ Precondiciones**
- [ ] Usuario registrado con `email=ftcamilo07@gmail.com` y contraseña conocida
- [ ] Servidor Flask corriendo en `localhost:5000`
- [ ] Acceso a MongoDB Atlas para verificar el documento del usuario

**🔁 Pasos de ejecución**
1. Enviar `POST /auth/login` con credenciales válidas
2. Verificar que la respuesta incluye cookie de sesión (`Set-Cookie: session=...`)
3. Usar la cookie obtenida para hacer `GET /user/profile`
4. Verificar que el perfil cargado corresponde exactamente al usuario en MongoDB
5. Consultar directamente en MongoDB Atlas que el campo `email` coincide (normalizado en minúsculas)

**📥 Datos de entrada**
```json
POST /auth/login
{
  "email": "FTCAMILO07@GMAIL.COM",
  "password": "password_correcto"
}
```
> ⚠️ Email en mayúsculas deliberadamente — se conoce que el sistema normaliza a minúsculas

**📤 Resultado esperado**
- `POST /auth/login` → Status `302` + cookie de sesión activa
- `GET /user/profile` → Status `200` + datos del usuario visibles
- En MongoDB: documento con `email: "ftcamilo07@gmail.com"` (minúsculas)
- El `_id` del documento MongoDB coincide con el `user_id` de la sesión Flask-Login
- Campo `rol: "user"` — no puede acceder a `/admin/dashboard`

**📋 Resultado obtenido**
- Status login: ______
- Cookie de sesión presente: ______
- Perfil cargado: ______
- Email en MongoDB (minúsculas): ______

**🟢 Estado:** ✅ Aprobado / ❌ Fallido / ⚠️ Bloqueado

---

### WEB-CG-02

| Campo | Detalle |
|-------|---------|
| **ID** | WEB-CG-02 |
| **Título** | Usuario con rol `user` intenta acceder a rutas `/admin/*` — control RBAC |
| **Técnica** | Caja Gris |
| **Capa** | Frontend → Backend → Decorador `@admin_required` → Base de Datos |
| **Prioridad** | Alta |

**🌐 Contexto Web**
- URL/Endpoint: `GET /admin/dashboard`
- Método: `GET`
- Conocimiento arquitectónico utilizado:
  - Sé que el campo `rol` en MongoDB es `'user'` o `'admin'`
  - Sé que el decorador `@admin_required` verifica `current_user.is_admin()`
  - Sé que `is_admin()` compara `self.rol == 'admin'`
  - Sé que un usuario con `rol='user'` debe recibir redirección a `/catalog`

**✅ Precondiciones**
- [ ] Usuario registrado con `rol='user'` (cliente estándar) y sesión activa
- [ ] Servidor corriendo

**🔁 Pasos de ejecución**
1. Iniciar sesión con un usuario de rol `'user'`
2. Intentar acceder directamente a `GET /admin/dashboard`
3. Observar la respuesta HTTP y el destino de la redirección
4. Verificar en MongoDB que el campo `rol` del usuario es efectivamente `'user'`
5. Intentar también con `GET /admin/products` y `GET /admin/orders`

**📥 Datos de entrada**
```
GET /admin/dashboard
Cookie: session=<sesion_de_usuario_rol_user>
```

**📤 Resultado esperado**
- Status HTTP: `302 Found`
- Redirección a: `/catalog`
- Mensaje flash: `"No tienes permisos para acceder a esta página."`
- En MongoDB: campo `rol: "user"` confirmado
- Ninguna ruta `/admin/*` accesible con rol `'user'`

**📋 Resultado obtenido**
- Status: ______
- Redirección a: ______
- Mensaje flash: ______
- `rol` en MongoDB: ______

**🟢 Estado:** ✅ Aprobado / ❌ Fallido / ⚠️ Bloqueado

---

### WEB-CG-03

| Campo | Detalle |
|-------|---------|
| **ID** | WEB-CG-03 |
| **Título** | Registro de usuario verifica integridad del hash de contraseña en MongoDB |
| **Técnica** | Caja Gris |
| **Capa** | Frontend → Backend → Base de Datos |
| **Prioridad** | Alta |

**🌐 Contexto Web**
- URL/Endpoint: `POST /auth/register`
- Método: `POST`
- Conocimiento arquitectónico utilizado:
  - Sé que las contraseñas se almacenan con `PBKDF2-SHA256` mediante Werkzeug
  - Sé que el campo en MongoDB es `password_hash` (nunca texto plano)
  - Sé que el hash tiene el formato `pbkdf2:sha256:...`
  - Sé que `created_at` y `updated_at` se generan automáticamente como `datetime.utcnow()`

**✅ Precondiciones**
- [ ] Email nuevo no registrado previamente
- [ ] Acceso a MongoDB Atlas para inspeccionar el documento creado
- [ ] Servidor corriendo

**🔁 Pasos de ejecución**
1. Enviar `POST /auth/register` con datos válidos y un email nuevo
2. Verificar que la respuesta es `302` con redirección a `/catalog`
3. Consultar directamente en MongoDB Atlas la colección `users`
4. Localizar el documento del usuario recién creado por email
5. Verificar los campos del documento en MongoDB

**📥 Datos de entrada**
```json
POST /auth/register
{
  "nombre": "Usuario Prueba Gris",
  "email": "pruebagris@test.com",
  "telefono": "3001234567",
  "direccion": "Calle 100 # 10-20",
  "ciudad": "Bogotá",
  "password": "MiPass123",
  "confirm_password": "MiPass123"
}
```

**📤 Resultado esperado**
- Status HTTP: `302 Found` → redirección a `/catalog`
- Sesión activa (login automático post-registro)
- En MongoDB, el documento creado debe tener:

```json
{
  "_id": "ObjectId(...)",
  "nombre": "Usuario Prueba Gris",
  "email": "pruebagris@test.com",
  "telefono": "3001234567",
  "direccion": "Calle 100 # 10-20",
  "ciudad": "Bogotá",
  "password_hash": "pbkdf2:sha256:...",
  "rol": "user",
  "created_at": "ISODate(...)",
  "updated_at": "ISODate(...)"
}
```

- Campo `password_hash` comienza con `pbkdf2:sha256:` ✅
- Campo `password` **NO existe** en el documento (nunca texto plano) ✅
- Campo `rol` es `"user"` (nunca `"admin"`) ✅
- Campo `email` en minúsculas ✅

**📋 Resultado obtenido**
- Status registro: ______
- Redirección a: ______
- `password_hash` inicia con `pbkdf2:sha256:`: ______
- Campo `password` (texto plano) existe en BD: ______
- `rol` en MongoDB: ______

**🟢 Estado:** ✅ Aprobado / ❌ Fallido / ⚠️ Bloqueado

---

### WEB-CG-04

| Campo | Detalle |
|-------|---------|
| **ID** | WEB-CG-04 |
| **Título** | Checkout completo verifica reducción de stock en MongoDB tras pedido |
| **Técnica** | Caja Gris |
| **Capa** | Frontend → Backend → Base de Datos (colecciones `orders` + `products`) |
| **Prioridad** | Alta |

**🌐 Contexto Web**
- URL/Endpoint: `POST /checkout`
- Método: `POST`
- Conocimiento arquitectónico utilizado:
  - Sé que el stock se almacena como `stock: {S: int, M: int, L: int, XL: int}` en MongoDB
  - Sé que `reducir_stock()` en `ProductService` decrementa el valor del campo `stock.<talla>`
  - Sé que el pedido se guarda en colección `orders` con número `ORD-YYYY-NNNNNN`
  - Sé que el carrito se vacía con `session.pop('cart', None)` tras el checkout

**✅ Precondiciones**
- [ ] Usuario autenticado con sesión activa
- [ ] Producto con stock `M: 5` disponible en MongoDB
- [ ] Carrito con 2 unidades del producto en talla M

**🔁 Pasos de ejecución**
1. Consultar en MongoDB el stock actual del producto: `stock.M = 5`
2. Agregar 2 unidades talla M al carrito (`POST /cart/add`)
3. Completar el checkout (`POST /checkout`) con datos de envío válidos
4. Verificar la respuesta: página de confirmación con número de pedido
5. Consultar en MongoDB Atlas:
   - Colección `products`: verificar que `stock.M` se redujo de `5` a `3`
   - Colección `orders`: verificar que existe el nuevo pedido con estado `RECIBIDO`

**📥 Datos de entrada**
```json
POST /checkout
{
  "nombre": "Nicolas Bocanegra",
  "telefono": "3001234567",
  "direccion": "Calle 10 # 20-30",
  "ciudad": "Bogotá",
  "notas": "Entregar en la tarde"
}
```

**📤 Resultado esperado**
- Status HTTP: `200 OK` → página de confirmación
- Número de pedido generado: `ORD-2026-XXXXXX`
- En MongoDB colección `products`:
  - `stock.M` cambió de `5` → `3` ✅
- En MongoDB colección `orders`:
  - Nuevo documento con `estado: "RECIBIDO"` ✅
  - Campo `items` contiene el producto con `talla: "M"`, `cantidad: 2` ✅
- Carrito vacío tras el checkout ✅
- Botón WhatsApp visible en la página de confirmación ✅

**📋 Resultado obtenido**
- Status checkout: ______
- Número de pedido generado: ______
- `stock.M` antes: 5 → después: ______
- Pedido en MongoDB con estado: ______
- Carrito vacío: ______

**🟢 Estado:** ✅ Aprobado / ❌ Fallido / ⚠️ Bloqueado

---

## Resumen de Casos de Prueba – Caja Gris

| ID | Título | Capas involucradas | Conocimiento usado | Prioridad | Estado |
|----|--------|--------------------|--------------------|-----------|--------|
| WEB-CG-01 | Login + persistencia de sesión en MongoDB | Frontend → Backend → BD → Sesión | Normalización email, Flask-Login, `_id` MongoDB | Alta | ⏳ Pendiente |
| WEB-CG-02 | Control RBAC: usuario `user` vs rutas `/admin/*` | Frontend → Decorador → BD | Campo `rol` en MongoDB, `@admin_required` | Alta | ⏳ Pendiente |
| WEB-CG-03 | Registro + integridad hash en MongoDB | Frontend → Backend → BD | `PBKDF2-SHA256`, esquema `users`, `created_at` | Alta | ⏳ Pendiente |
| WEB-CG-04 | Checkout + reducción de stock en MongoDB | Frontend → Backend → BD (2 colecciones) | Esquema `stock.<talla>`, colección `orders` | Alta | ⏳ Pendiente |

---

## Diferencia entre técnicas aplicadas en este módulo

| Aspecto | Caja Negra | Caja Blanca | Caja Gris |
|---------|-----------|-------------|-----------|
| **Acceso al código** | ❌ Sin acceso | ✅ Acceso total | ⚠️ Conocimiento parcial |
| **Qué se evalúa** | Entradas/salidas visibles | Rutas de código internas | Interacción entre capas |
| **Conocimiento de BD** | ❌ No | ❌ No aplica directamente | ✅ Conoce el esquema |
| **Ejemplo en Hoodie Shop** | Login exitoso desde el navegador | Ramas de `login_user()` en `auth_service.py` | Verificar que el hash se guardó en MongoDB |
| **Herramienta sugerida** | Navegador / Postman | pytest + MagicMock | Postman + MongoDB Compass |

---

## Herramientas de ejecución

```bash
# Verificar directamente en MongoDB (MongoDB Shell)
use hoodie_shop
db.users.findOne({email: "ftcamilo07@gmail.com"})

# Verificar stock después del checkout
db.products.findOne({_id: ObjectId("<id_producto>")}, {stock: 1})

# Verificar pedido creado
db.orders.findOne({}, {sort: {created_at: -1}})
```

```bash
# Ejecutar pruebas con Postman + Newman (CLI)
newman run parcial/6_Evidencias_Ejecucion/postman_collection.json
```