# REPORTE DE DEFECTOS – WEB
## Parcial de Testing de Software – Ingeniería de Software II

**Estudiante:** Nicolas Camilo Bocanegra Vaca

**Fecha:** Marzo 2026

**Proyecto:** Hoodie Shop – E-commerce

**Módulo:** Gestión de Usuarios y Autenticación

**Repositorio:** https://github.com/DjKiller07FT/hoodie-shop

---

## Descripción

Durante la ejecución de los 16 casos de prueba (Caja Negra, Caja Blanca y Caja Gris), no se encontraron defectos críticos que impidieran el funcionamiento del sistema. Todos los casos fueron aprobados satisfactoriamente.

Sin embargo, se documentan a continuación **observaciones y mejoras potenciales** identificadas durante el proceso de testing, clasificadas por severidad.

---

## Registro de Defectos

### DEF-01

| Campo | Detalle |
|-------|---------|
| **ID** | DEF-01 |
| **Título** | Mensaje de error genérico para email no registrado y contraseña incorrecta |
| **Caso relacionado** | WEB-CN-02, WEB-CB-03 |
| **Técnica** | Caja Negra / Caja Blanca |
| **Severidad** | 🟡 Baja |
| **Prioridad** | Baja |
| **Tipo** | Observación de seguridad |

**Descripción:**
El sistema retorna el mismo mensaje `"Email o contraseña incorrectos"` tanto cuando el email no existe en la base de datos (RAMA 3) como cuando la contraseña es incorrecta (RAMA 4). Esto es un comportamiento **intencional y correcto** desde el punto de vista de seguridad (evita enumeración de usuarios), pero no está documentado explícitamente en los requisitos.

**Pasos para reproducir:**
1. Intentar login con email no registrado
2. Intentar login con email válido pero contraseña incorrecta
3. Observar que ambos casos retornan el mismo mensaje

**Resultado obtenido:** `"Email o contraseña incorrectos"` en ambos casos
**Resultado esperado:** Comportamiento correcto — mensaje genérico intencional ✅

**Estado:** ✅ No es defecto — comportamiento esperado de seguridad
**Recomendación:** Documentar explícitamente en los requisitos que el mensaje es genérico por diseño.

---

### DEF-02

| Campo | Detalle |
|-------|---------|
| **ID** | DEF-02 |
| **Título** | No hay límite de intentos de login (sin protección contra fuerza bruta) |
| **Caso relacionado** | WEB-CN-02, WEB-CB-03 |
| **Técnica** | Caja Negra |
| **Severidad** | 🔴 Alta |
| **Prioridad** | Alta |
| **Tipo** | Defecto de seguridad |

**Descripción:**
El endpoint `POST /auth/login` no implementa ningún mecanismo de limitación de intentos fallidos (rate limiting). Un atacante podría realizar múltiples intentos de login sin ser bloqueado, facilitando ataques de fuerza bruta contra cuentas de usuario.

**Pasos para reproducir:**
1. Enviar múltiples peticiones `POST /auth/login` con contraseñas incorrectas consecutivas
2. Observar que el sistema responde normalmente en cada intento sin bloqueo

**Resultado obtenido:** El sistema responde `200 OK` con mensaje de error en cada intento, sin límite
**Resultado esperado:** Después de N intentos fallidos, bloquear temporalmente la IP o la cuenta

**Estado:** ❌ Defecto confirmado
**Recomendación:** Implementar `Flask-Limiter` para restringir intentos por IP (ej: máximo 5 intentos por minuto).

---

### DEF-03

| Campo | Detalle |
|-------|---------|
| **ID** | DEF-03 |
| **Título** | Mensaje flash de Flask-Login en inglés al acceder a ruta protegida sin sesión |
| **Caso relacionado** | WEB-CN-05 |
| **Técnica** | Caja Negra |
| **Severidad** | 🟡 Baja |
| **Prioridad** | Baja |
| **Tipo** | Defecto de internacionalización (i18n) |

**Descripción:**
Al intentar acceder a una ruta protegida sin sesión activa, Flask-Login muestra el mensaje `"Please log in to access this page"` en inglés. Dado que toda la interfaz del sistema está en español, este mensaje rompe la consistencia del idioma de la aplicación.

**Pasos para reproducir:**
1. Abrir navegador sin sesión activa
2. Intentar acceder a `http://localhost:5000/user/profile`
3. Observar el mensaje flash en la página de login

**Resultado obtenido:** `"Please log in to access this page"` (en inglés)
**Resultado esperado:** `"Debes iniciar sesión para acceder a esta página."` (en español)

**Estado:** ❌ Defecto confirmado
**Recomendación:** Personalizar el mensaje de Flask-Login en la configuración de la app:
```python
login_manager.login_message = "Debes iniciar sesión para acceder a esta página."
login_manager.login_message_category = "warning"
```

---

### DEF-04

| Campo | Detalle |
|-------|---------|
| **ID** | DEF-04 |
| **Título** | El campo `confirm_password` no es validado en el servicio `AuthService` — solo en el controlador |
| **Caso relacionado** | WEB-CN-04 |
| **Técnica** | Caja Negra / Caja Blanca |
| **Severidad** | 🟠 Media |
| **Prioridad** | Media |
| **Tipo** | Defecto de arquitectura / validación |

**Descripción:**
La validación de que `password == confirm_password` se realiza únicamente en el controlador (blueprint `auth`), no en el servicio `AuthService.register_user()`. Esto significa que si se llama directamente al servicio (por API o por pruebas unitarias), dicha validación no se ejecuta, dejando una brecha en la capa de lógica de negocio.

**Pasos para reproducir:**
1. Llamar directamente a `auth_service.register_user(...)` con `password="Pass1234"` (sin pasar `confirm_password`)
2. Observar que el servicio no valida la confirmación de contraseña

**Resultado obtenido:** El servicio acepta el registro sin validar confirmación de contraseña
**Resultado esperado:** La validación debería existir también en la capa de servicio

**Estado:** ❌ Defecto confirmado
**Recomendación:** Agregar el parámetro `confirm_password` a `register_user()` y validar internamente:
```python
if password != confirm_password:
    return False, "Las contraseñas no coinciden", None
```

---

## Resumen de Defectos

| ID | Título (resumen) | Severidad | Estado |
|----|-----------------|-----------|--------|
| DEF-01 | Mensaje genérico login — comportamiento intencional | 🟡 Baja | ✅ No es defecto |
| DEF-02 | Sin límite de intentos de login (fuerza bruta) | 🔴 Alta | ❌ Defecto confirmado |
| DEF-03 | Mensaje Flask-Login en inglés | 🟡 Baja | ❌ Defecto confirmado |
| DEF-04 | `confirm_password` no validado en servicio | 🟠 Media | ❌ Defecto confirmado |

---

## Métricas de defectos

| Métrica | Valor |
|---------|-------|
| Total de defectos encontrados | 3 |
| Defectos críticos (Alta severidad) | 1 |
| Defectos de severidad media | 1 |
| Defectos de severidad baja | 1 |
| Observaciones (no defectos) | 1 |
| Defectos corregidos en este ciclo | 0 |
| Defectos pendientes de corrección | 3 |

---

## Referencias

| Archivo | Descripción |
|---------|-------------|
| `parcial/3_Casos_CajaNegra_Web.md` | Casos WEB-CN-01 a WEB-CN-05 |
| `parcial/4_Casos_CajaBlanca_Web.md` | Casos WEB-CB-01 a WEB-CB-07 |
| `parcial/5_Casos_CajaGris_Web.md` | Casos WEB-CG-01 a WEB-CG-04 |
| `parcial/7_Matriz_Trazabilidad_Web.md` | Matriz de trazabilidad |