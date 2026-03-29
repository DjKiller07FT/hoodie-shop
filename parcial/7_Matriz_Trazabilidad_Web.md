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

## 2. Matriz de Trazabilidad

| Requisito | RF-01 | RF-02 | RF-03 | RF-04 | RF-05 | RF-06 | RF-07 | RF-08 | RF-09 | RF-10 | RF-11 | RF-12 | RF-13 | RF-14 | RF-15 |
|-----------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| **WEB-CN-01** | ✅ | | | | | | | | | | | | | | |
| **WEB-CN-02** | | ✅ | | | | | | | | | | | | | |
| **WEB-CN-03** | | | ✅ | | | | | | | | | | | | |
| **WEB-CN-04** | | | | ✅ | | | | | | | | | | | |
| **WEB-CN-05** | | | | | ✅ | | | | | | | | | | |
| **WEB-CB-01** | ✅ | | | | | | | | | | | | | | |
| **WEB-CB-02** | | | | | | ✅ | | | | | | | | | |
| **WEB-CB-03** | | ✅ | | | | | | | | | | | | | |
| **WEB-CB-04** | | | | | | | ✅ | | | | | | | | |
| **WEB-CB-05** | | | | | | | | ✅ | | | | | | |
| **WEB-CB-06** | | | | | | | | | ✅ | | | | | | |
| **WEB-CB-07** | | | ✅ | | | | | | | | | | | | |
| **WEB-CG-01** | ✅ | | | | | | | | | ✅ | | | ✅ | | |
| **WEB-CG-02** | | | | | | | | | | | ✅ | | | | |
| **WEB-CG-03** | | | | | | | | | | | | ✅ | ✅ | | |
| **WEB-CG-04** | | | | | | | | | | | | | | ✅ | ✅ |

---

## 3. Cobertura por Requisito

| ID Requisito | Descripción (resumen) | Casos que lo cubren | Cobertura |
|---|---|---|---|
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

**Cobertura total: 15/15 requisitos cubiertos → 100% ✅**

---

## 4. Cobertura por Caso de Prueba

| Caso de Prueba | Técnica | Requisitos cubiertos | Estado |
|---|---|---|---|
| WEB-CN-01 | Caja Negra | RF-01 | ⏳ Pendiente |
| WEB-CN-02 | Caja Negra | RF-02 | ⏳ Pendiente |
| WEB-CN-03 | Caja Negra | RF-03 | ⏳ Pendiente |
| WEB-CN-04 | Caja Negra | RF-04 | ⏳ Pendiente |
| WEB-CN-05 | Caja Negra | RF-05 | ⏳ Pendiente |
| WEB-CB-01 | Caja Blanca | RF-01 | ⏳ Pendiente |
| WEB-CB-02 | Caja Blanca | RF-06 | ⏳ Pendiente |
| WEB-CB-03 | Caja Blanca | RF-02 | ⏳ Pendiente |
| WEB-CB-04 | Caja Blanca | RF-07 | ⏳ Pendiente |
| WEB-CB-05 | Caja Blanca | RF-08 | ⏳ Pendiente |
| WEB-CB-06 | Caja Blanca | RF-09 | ⏳ Pendiente |
| WEB-CB-07 | Caja Blanca | RF-03 | ⏳ Pendiente |
| WEB-CG-01 | Caja Gris | RF-01, RF-10, RF-13 | ⏳ Pendiente |
| WEB-CG-02 | Caja Gris | RF-11 | ⏳ Pendiente |
| WEB-CG-03 | Caja Gris | RF-12, RF-13 | ⏳ Pendiente |
| WEB-CG-04 | Caja Gris | RF-14, RF-15 | ⏳ Pendiente |

**Casos huérfanos (sin requisito asignado): 0 ✅**

---

## 5. Distribución por técnica de prueba

| Técnica | Cantidad de casos | IDs |
|---------|:-----------------:|-----|
| Caja Negra | 5 | WEB-CN-01 al WEB-CN-05 |
| Caja Blanca | 7 | WEB-CB-01 al WEB-CB-07 |
| Caja Gris | 4 | WEB-CG-01 al WEB-CG-04 |
| **Total** | **16** | |

---

## 6. Resumen ejecutivo

| Métrica | Valor |
|---------|-------|
| Total de requisitos funcionales | 15 |
| Requisitos cubiertos | 15 |
| Requisitos sin cobertura | 0 |
| Total de casos de prueba | 16 |
| Casos con requisito asignado | 16 |
| Casos huérfanos | 0 |
| Cobertura de requisitos | **100%** |

---

## 7. Referencias

| Archivo | Descripción |
|---------|-------------|
| `parcial/3_Casos_CajaNegra_Web.md` | Casos WEB-CN-01 a WEB-CN-05 |
| `parcial/4_Casos_CajaBlanca_Web.md` | Casos WEB-CB-01 a WEB-CB-07 |
| `parcial/5_Casos_CajaGris_Web.md` | Casos WEB-CG-01 a WEB-CG-04 |