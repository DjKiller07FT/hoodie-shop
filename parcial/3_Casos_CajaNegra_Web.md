# CASOS DE PRUEBA – CAJA NEGRA
## Parcial de Testing de Software – Ingeniería de Software II

**Estudiante:** Nicolas Camilo Bocanegra Vaca
**Fecha:** Marzo 2026
**Proyecto:** Hoodie Shop – E-commerce
**Módulo:** Gestión de Usuarios y Autenticación
**Técnica:** Caja Negra
**Repositorio:** https://github.com/DjKiller07FT/hoodie-shop

---

## Descripción de la técnica aplicada

Las pruebas de **caja negra** evalúan el comportamiento externo del sistema sin conocer ni acceder a su implementación interna. El tester solo interactúa con las **entradas** (formularios, peticiones HTTP) y verifica las **salidas** (respuestas HTTP, mensajes en pantalla, redirecciones), tratando el sistema como una caja opaca.

En **Hoodie Shop**, esta técnica se aplica sobre los endpoints de autenticación evaluando únicamente lo que el usuario ve y recibe: códigos de estado HTTP, mensajes flash, redirecciones y comportamiento del formulario.

---

## Casos de Prueba

---

### WEB-CN-01

| Campo | Detalle |
|-------|---------|
| **ID** | WEB-CN-01 |
| **Título** | Login exitoso con credenciales válidas |
| **Técnica** | Caja Negra |
| **Capa** | Frontend + API |
| **Prioridad** | Alta |
| **Tipo** | Normal / Camino feliz |

**🌐 Contexto Web**
- URL/Endpoint: `POST /auth/login`
- Método: `POST`
- Headers: `Content-Type: application/x-www-form-urlencoded`

**✅ Precondiciones**
- [ ] Usuario registrado en el sistema con email `ftcamilo07@gmail.com`
- [ ] Contraseña correcta conocida
- [ ] Servidor Flask corriendo en `localhost:5000`

**🔁 Pasos de ejecución**
1. Abrir navegador en `http://localhost:5000/auth/login`
2. Ingresar email: `ftcamilo07@gmail.com`
3. Ingresar contraseña correcta
4. Hacer clic en "Iniciar Sesión"

**📥 Datos de entrada**
```
email=ftcamilo07@gmail.com
password=<contraseña_correcta>
remember=on
```

**📤 Resultado esperado**
- Status HTTP: `302 Found` → redirección
- Redirección a: `/catalog` (cliente) o `/admin/dashboard` (admin)
- Mensaje flash: `"¡Bienvenido {nombre}!"`
- Sesión activa en el navegador

**📋 Resultado obtenido**
- Status: ______
- Redirección: ______
- Mensaje: ______

**🟢 Estado:** ✅ Aprobado / ❌ Fallido / ⚠️ Bloqueado

---

### WEB-CN-02

| Campo | Detalle |
|-------|---------|
| **ID** | WEB-CN-02 |
| **Título** | Login con contraseña incorrecta |
| **Técnica** | Caja Negra |
| **Capa** | Frontend + API |
| **Prioridad** | Alta |
| **Tipo** | Error / Negativo |

**🌐 Contexto Web**
- URL/Endpoint: `POST /auth/login`
- Método: `POST`

**✅ Precondiciones**
- [ ] Usuario registrado con email `ftcamilo07@gmail.com`
- [ ] Contraseña incorrecta a proporcionar

**🔁 Pasos de ejecución**
1. Abrir `http://localhost:5000/auth/login`
2. Ingresar email: `ftcamilo07@gmail.com`
3. Ingresar contraseña: `wrongpassword123`
4. Hacer clic en "Iniciar Sesión"

**📥 Datos de entrada**
```
email=ftcamilo07@gmail.com
password=wrongpassword123
```

**📤 Resultado esperado**
- Status HTTP: `200 OK` (re-renderiza el formulario)
- Permanece en `/auth/login`
- Mensaje flash: `"Email o contraseña incorrectos"`
- No se crea sesión activa

**📋 Resultado obtenido**
- Status: ______
- Página actual: ______
- Mensaje: ______

**🟢 Estado:** ✅ Aprobado / ❌ Fallido / ⚠️ Bloqueado

---

### WEB-CN-03

| Campo | Detalle |
|-------|---------|
| **ID** | WEB-CN-03 |
| **Título** | Registro con email ya existente |
| **Técnica** | Caja Negra |
| **Capa** | Frontend + API |
| **Prioridad** | Alta |
| **Tipo** | Error / Borde |

**🌐 Contexto Web**
- URL/Endpoint: `POST /auth/register`
- Método: `POST`

**✅ Precondiciones**
- [ ] Existe un usuario registrado con el email `ftcamilo07@gmail.com`
- [ ] Servidor corriendo

**🔁 Pasos de ejecución**
1. Abrir `http://localhost:5000/auth/register`
2. Completar formulario con email `ftcamilo07@gmail.com` (ya registrado)
3. Completar los demás campos con datos válidos
4. Hacer clic en "Registrarse"

**📥 Datos de entrada**
```
nombre=Usuario Prueba
email=ftcamilo07@gmail.com
telefono=3001234567
direccion=Calle 10 # 20-30
ciudad=Bogotá
password=pass123
confirm_password=pass123
```

**📤 Resultado esperado**
- Status HTTP: `200 OK` (re-renderiza el formulario)
- Permanece en `/auth/register`
- Mensaje flash: `"Este email ya está registrado"`
- No se crea nuevo usuario en base de datos

**📋 Resultado obtenido**
- Status: ______
- Página actual: ______
- Mensaje: ______

**🟢 Estado:** ✅ Aprobado / ❌ Fallido / ⚠️ Bloqueado

---

### WEB-CN-04

| Campo | Detalle |
|-------|---------|
| **ID** | WEB-CN-04 |
| **Título** | Registro con contraseñas que no coinciden |
| **Técnica** | Caja Negra |
| **Capa** | Frontend + API |
| **Prioridad** | Media |
| **Tipo** | Error / Validación |

**🌐 Contexto Web**
- URL/Endpoint: `POST /auth/register`
- Método: `POST`

**✅ Precondiciones**
- [ ] Servidor corriendo
- [ ] Email no registrado previamente

**🔁 Pasos de ejecución**
1. Abrir `http://localhost:5000/auth/register`
2. Ingresar email nuevo válido
3. Ingresar `password=Pass1234` y `confirm_password=Pass9999`
4. Hacer clic en "Registrarse"

**📥 Datos de entrada**
```
nombre=Nuevo Usuario
email=nuevo@correo.com
telefono=3009876543
direccion=Carrera 5 # 10-20
ciudad=Medellín
password=Pass1234
confirm_password=Pass9999
```

**📤 Resultado esperado**
- Status HTTP: `200 OK` (re-renderiza el formulario)
- Permanece en `/auth/register`
- Mensaje flash: `"Las contraseñas no coinciden"`
- No se crea usuario en base de datos

**📋 Resultado obtenido**
- Status: ______
- Página actual: ______
- Mensaje: ______

**🟢 Estado:** ✅ Aprobado / ❌ Fallido / ⚠️ Bloqueado

---

### WEB-CN-05

| Campo | Detalle |
|-------|---------|
| **ID** | WEB-CN-05 |
| **Título** | Acceso a ruta protegida sin sesión activa |
| **Técnica** | Caja Negra |
| **Capa** | Frontend + API |
| **Prioridad** | Alta |
| **Tipo** | Seguridad / Borde |

**🌐 Contexto Web**
- URL/Endpoint: `GET /user/profile`
- Método: `GET`

**✅ Precondiciones**
- [ ] Usuario NO autenticado (sin sesión activa)
- [ ] Servidor corriendo

**🔁 Pasos de ejecución**
1. Abrir navegador sin sesión activa (o en modo incógnito)
2. Intentar acceder directamente a `http://localhost:5000/user/profile`
3. Observar la respuesta del sistema

**📥 Datos de entrada**
```
URL: http://localhost:5000/user/profile
Sin cookies de sesión
```

**📤 Resultado esperado**
- Status HTTP: `302 Found` → redirección
- Redirección a: `/auth/login?next=%2Fuser%2Fprofile`
- Página de login visible en el navegador
- Mensaje flash: `"Please log in to access this page"` (Flask-Login)
- Después de login exitoso → redirige automáticamente a `/user/profile`

**📋 Resultado obtenido**
- Status: ______
- Redirección: ______
- Parámetro `?next=`: ______

**🟢 Estado:** ✅ Aprobado / ❌ Fallido / ⚠️ Bloqueado

---

## Resumen de Casos de Prueba – Caja Negra

| ID | Título | Tipo | Prioridad | Estado |
|----|--------|------|-----------|--------|
| WEB-CN-01 | Login exitoso con credenciales válidas | Normal | Alta | ⏳ Pendiente |
| WEB-CN-02 | Login con contraseña incorrecta | Error | Alta | ⏳ Pendiente |
| WEB-CN-03 | Registro con email ya existente | Error / Borde | Alta | ⏳ Pendiente |
| WEB-CN-04 | Registro con contraseñas que no coinciden | Error / Validación | Media | ⏳ Pendiente |
| WEB-CN-05 | Acceso a ruta protegida sin sesión activa | Seguridad / Borde | Alta | ⏳ Pendiente |

---

## Herramienta de ejecución

Estos casos pueden ejecutarse con:
- **Manual:** Navegador web en `http://localhost:5000`
- **Postman:** Colección con peticiones HTTP directas a los endpoints
- **pytest + requests:** Script automatizado (ver `tests/test_auth.py`)

```bash
# Ejecutar pruebas automatizadas del módulo auth
python -m pytest tests/test_auth.py -v
```