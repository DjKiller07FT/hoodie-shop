# MATRIZ DE TRAZABILIDAD – WEB
## Parcial de Testing de Software – Ingeniería de Software II

**Estudiante:** Nicolas Camilo Bocanegra Vaca
**Fecha:** Marzo 2026
**Proyecto:** Hoodie Shop – E-commerce
**Módulo:** Gestión de Usuarios y Autenticación
**Repositorio:** https://github.com/DjKiller07FT/hoodie-shop

---

## 1. Requisitos Funcionales identificados

| ID | Descripción del Requisito |
|----|--------------------------|
| RF-01 | El sistema debe permitir el login con credenciales válidas |
| RF-02 | El sistema debe rechazar el login con contraseña incorrecta |
| RF-03 | El sistema debe rechazar el registro con email ya existente |
| RF-04 | El sistema debe rechazar el registro con contraseñas que no coinciden |
| RF-05 | El sistema debe proteger rutas privadas redirigiendo a login si no hay sesión |
| RF-06 | El sistema debe validar campos vacíos en el login |
| RF-07 | El sistema debe rechazar emails con formato inválido en el registro |
| RF-08 | El sistema debe rechazar contraseñas menores a 6 caracteres |
| RF-09 | El sistema debe redirigir a login si el usuario ya está autenticado |
| RF-10 | El sistema debe persistir la sesión del usuario tras el login (Flask-Login) |
| RF-11 | El sistema debe controlar el acceso por roles (RBAC) — usuario vs admin |
| RF-12 | El sistema debe almacenar la contraseña como hash PBKDF2-SHA256 (nunca texto plano) |
| RF-13 | El sistema debe normalizar el email a minúsculas antes de guardarlo |
| RF-14 | El sistema debe reducir el stock del producto tras un checkout exitoso |
| RF-15 | El sistema debe registrar el pedido en la colección `orders` con estado `RECIBIDO` |

---

## 2. Requisitos No Funcionales identificados

| ID | Categoría | Descripción |
|----|-----------|-------------|
| RNF-01 | Seguridad | Las contraseñas deben almacenarse con hash PBKDF2-SHA256 (nunca en texto plano) |
| RNF-02 | Seguridad | El sistema debe controlar el acceso por roles (RBAC): `user` y `admin` |
| RNF-03 | Seguridad | Todas las rutas privadas deben estar protegidas con autenticación obligatoria (`@login_required`) |
| RNF-04 | Rendimiento | El login debe responder en menos de 2 segundos bajo condiciones normales |
| RNF-05 | Persistencia | La sesión debe mantenerse activa durante 7 días (`SESSION_PERMANENT = True`) |
| RNF-06 | Integridad de datos | El email debe normalizarse a minúsculas antes de guardarse en MongoDB |
| RNF-07 | Consistencia | El stock debe actualizarse correctamente tras cada checkout exitoso |
| RNF-08 | Usabilidad | El sistema debe mostrar mensajes flash descriptivos ante errores de validación |

---

## 3. Matriz de Trazabilidad – Requisitos Funcionales

| Caso de Prueba | RF-01 | RF-02 | RF-03 | RF-04 | RF-05 | RF-06 | RF-07 | RF-08 | RF-09 | RF-10 | RF-11 | RF-12 | RF-13 | RF-14 | RF-15 |
|----------------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| **WEB-CN-01** | ✅ | | | | | | | | | | | | | | |
| **WEB-CN-02** | | ✅ | | | | | | | | | | | | | |
| **WEB-CN-03** | | | ✅ | | | | | | | | | | | | |
| **WEB-CN-04** | | | | ✅ | | | | | | | | | | | |
| **WEB-CN-05** | | | | | ✅ | | | | | | | | | | |
| **WEB-CB-01** | ✅ | | | | | | | | | | | | | | |
| **WEB-CB-02** | | | | | | ✅ | | | | | | | | | |
| **WEB-CB-03** | | ✅ | | | | | | | | | | | | | |
| **WEB-CB-04** | | | | | | | ✅ | | | | | | | | |
| **WEB-CB-05** | | | | | | | | ✅ | | | | | | | |
| **WEB-CB-06** | | | | | | | | | ✅ | | | | | | |
| **WEB-CB-07** | | | ✅ | | | | | | | | | | | | |
| **WEB-CG-01** | ✅ | | | | | | | | | ✅ | | | ✅ | | |
| **WEB-CG-02** | | | | | | | | | | | ✅ | | | | |
| **WEB-CG-03** | | | | | | | | | | | | ✅ | ✅ | | |
| **WEB-CG-04** | | | | | | | | | | | | | | ✅ | ✅ |

---

## 4. Matriz de Trazabilidad – Requisitos No Funcionales

| Caso de Prueba | RNF-01 | RNF-02 | RNF-03 | RNF-04 | RNF-05 | RNF-06 | RNF-07 | RNF-08 |
|----------------|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|
| **WEB-CN-01** | | | | ✅ | ✅ | | | ✅ |
| **WEB-CN-02** | | | | ✅ | | | | ✅ |
| **WEB-CN-03** | | | | | | | | ✅ |
| **WEB-CN-04** | | | | | | | | ✅ |
| **WEB-CN-05** | | | ✅ | | | | | ✅ |
| **WEB-CB-01** | | | | ✅ | ✅ | | | |
| **WEB-CB-02** | | | | | | | | ✅ |
| **WEB-CB-03** | | | | ✅ | | | | ✅ |
| **WEB-CB-04** | | | | | | | | ✅ |
| **WEB-CB-05** | | | | | | | | ✅ |
| **WEB-CB-06** | | ✅ | ✅ | | | | | ✅ |
| **WEB-CB-07** | | | | | | | | |
| **WEB-CG-01** | | | | | ✅ | ✅ | | |
| **WEB-CG-02** | | ✅ | ✅ | | | | | ✅ |
| **WEB-CG-03** | ✅ | | | | | ✅ | | |
| **WEB-CG-04** | | | | | | | ✅ | |

**Cobertura RNF total: 8/8 → 100% ✅**

---

## 5. Cobertura por Requisito Funcional

| ID | Descripción (resumen) | Casos que lo cubren | Cobertura |
|----|-----------------------|---------------------|-----------|
| RF-01 | Login con credenciales válidas | WEB-CN-01, WEB-CB-01, WEB-CG-01 | ✅ |
| RF-02 | Login con contraseña incorrecta | WEB-CN-02, WEB-CB-03 | ✅ |
| RF-03 | Registro con email ya existente | WEB-CN-03, WEB-CB-07 | ✅ |
| RF-04 | Registro con contraseñas que no coinciden | WEB-CN-04 | ✅ |
| RF-05 | Ruta protegida sin sesión activa | WEB-CN-05 | ✅ |
| RF-06 | Campos vacíos en login | WEB-CB-02 | ✅ |
| RF-07 | Email con formato inválido | WEB-CB-04 | ✅ |
| RF-08 | Contraseña menor a 6 caracteres | WEB-CB-05 | ✅ |
| RF-09 | Usuario autenticado redirigido desde login | WEB-CB-06 | ✅ |
| RF-10 | Persistencia de sesión Flask-Login | WEB-CG-01 | ✅ |
| RF-11 | Control RBAC (user vs admin) | WEB-CG-02 | ✅ |
| RF-12 | Hash PBKDF2-SHA256 en MongoDB | WEB-CG-03 | ✅ |
| RF-13 | Normalización de email a minúsculas | WEB-CG-01, WEB-CG-03 | ✅ |
| RF-14 | Reducción de stock tras checkout | WEB-CG-04 | ✅ |
| RF-15 | Pedido registrado en `orders` con estado RECIBIDO | WEB-CG-04 | ✅ |

**Cobertura RF total: 15/15 → 100% ✅**

---

## 6. Cobertura por Requisito No Funcional

| ID | Categoría | Descripción (resumen) | Casos que lo cubren | Cobertura |
|----|-----------|-----------------------|---------------------|-----------|
| RNF-01 | Seguridad | Hash PBKDF2-SHA256 en almacenamiento | WEB-CG-03 | ✅ |
| RNF-02 | Seguridad | Control de acceso por roles (RBAC) | WEB-CB-06, WEB-CG-02 | ✅ |
| RNF-03 | Seguridad | Rutas privadas protegidas con `@login_required` | WEB-CN-05, WEB-CB-06, WEB-CG-02 | ✅ |
| RNF-04 | Rendimiento | Login responde en < 2 segundos | WEB-CN-01, WEB-CN-02, WEB-CB-01, WEB-CB-03 | ✅ |
| RNF-05 | Persistencia | Sesión activa 7 días | WEB-CN-01, WEB-CB-01, WEB-CG-01 | ✅ |
| RNF-06 | Integridad de datos | Email normalizado a minúsculas | WEB-CG-01, WEB-CG-03 | ✅ |
| RNF-07 | Consistencia | Stock actualizado tras checkout | WEB-CG-04 | ✅ |
| RNF-08 | Usabilidad | Mensajes flash descriptivos ante errores | WEB-CN-01~05, WEB-CB-01~06 | ✅ |

**Cobertura RNF total: 8/8 → 100% ✅**

---

## 7. Cobertura por Caso de Prueba

| Caso de Prueba | Técnica | RF cubiertos | RNF cubiertos | Estado |
|----------------|---------|--------------|---------------|--------|
| WEB-CN-01 | Caja Negra | RF-01 | RNF-04, RNF-05, RNF-08 | ⏳ Pendiente |
| WEB-CN-02 | Caja Negra | RF-02 | RNF-04, RNF-08 | ⏳ Pendiente |
| WEB-CN-03 | Caja Negra | RF-03 | RNF-08 | ⏳ Pendiente |
| WEB-CN-04 | Caja Negra | RF-04 | RNF-08 | ⏳ Pendiente |
| WEB-CN-05 | Caja Negra | RF-05 | RNF-03, RNF-08 | ⏳ Pendiente |
| WEB-CB-01 | Caja Blanca | RF-01 | RNF-04, RNF-05 | ⏳ Pendiente |
| WEB-CB-02 | Caja Blanca | RF-06 | RNF-08 | ⏳ Pendiente |
| WEB-CB-03 | Caja Blanca | RF-02 | RNF-04, RNF-08 | ⏳ Pendiente |
| WEB-CB-04 | Caja Blanca | RF-07 | RNF-08 | ⏳ Pendiente |
| WEB-CB-05 | Caja Blanca | RF-08 | RNF-08 | ⏳ Pendiente |
| WEB-CB-06 | Caja Blanca | RF-09 | RNF-02, RNF-03, RNF-08 | ⏳ Pendiente |
| WEB-CB-07 | Caja Blanca | RF-03 | — | ⏳ Pendiente |
| WEB-CG-01 | Caja Gris | RF-01, RF-10, RF-13 | RNF-05, RNF-06 | ⏳ Pendiente |
| WEB-CG-02 | Caja Gris | RF-11 | RNF-02, RNF-03, RNF-08 | ⏳ Pendiente |
| WEB-CG-03 | Caja Gris | RF-12, RF-13 | RNF-01, RNF-06 | ⏳ Pendiente |
| WEB-CG-04 | Caja Gris | RF-14, RF-15 | RNF-07 | ⏳ Pendiente |

**Casos huérfanos (sin requisito asignado): 0 ✅**

---

## 8. Distribución por técnica de prueba

| Técnica | Cantidad de casos | IDs |
|---------|:-----------------:|-----|
| Caja Negra | 5 | WEB-CN-01 al WEB-CN-05 |
| Caja Blanca | 7 | WEB-CB-01 al WEB-CB-07 |
| Caja Gris | 4 | WEB-CG-01 al WEB-CG-04 |
| **Total** | **16** | |

---

## 9. Resumen ejecutivo

| Métrica | Valor |
|---------|-------|
| Total de requisitos funcionales (RF) | 15 |
| RF cubiertos | 15 |
| RF sin cobertura | 0 |
| Total de requisitos no funcionales (RNF) | 8 |
| RNF cubiertos | 8 |
| RNF sin cobertura | 0 |
| Total de casos de prueba | 16 |
| Casos huérfanos | 0 |
| Cobertura RF | **100%** |
| Cobertura RNF | **100%** |

---

## 10. Referencias

| Archivo | Descripción |
|---------|-------------|
| `parcial/3_Casos_CajaNegra_Web.md` | Casos WEB-CN-01 a WEB-CN-05 |
| `parcial/4_Casos_CajaBlanca_Web.md` | Casos WEB-CB-01 a WEB-CB-07 |
| `parcial/5_Casos_CajaGris_Web.md` | Casos WEB-CG-01 a WEB-CG-04 |