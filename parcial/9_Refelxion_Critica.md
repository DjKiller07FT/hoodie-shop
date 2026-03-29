# REFLEXIÓN CRÍTICA – WEB
## Parcial de Testing de Software – Ingeniería de Software II

**Estudiante:** Nicolas Camilo Bocanegra Vaca
**Fecha:** Marzo 2026
**Proyecto:** Hoodie Shop – E-commerce
**Módulo:** Gestión de Usuarios y Autenticación
**Repositorio:** https://github.com/DjKiller07FT/hoodie-shop

---

## Reflexión

La aplicación de las tres técnicas de prueba sobre el módulo de autenticación de **Hoodie Shop** permitió obtener una visión completa del comportamiento del sistema desde perspectivas complementarias.

Las pruebas de **caja negra** fueron las más intuitivas: evaluar entradas y salidas sin conocer el código interno obliga al tester a pensar como un usuario real, identificando casos límite visibles como el acceso a rutas protegidas sin sesión activa (WEB-CN-05) o el rechazo de credenciales inválidas (WEB-CN-02).

Las pruebas de **caja blanca** resultaron las más rigurosas técnicamente. Al analizar cada rama condicional de `login_user()` y `register_user()`, fue posible identificar que la validación de `confirm_password` no existe en la capa de servicio (DEF-04), un defecto que solo es visible con acceso al código fuente y que pasaría desapercibido con caja negra.

Las pruebas de **caja gris** demostraron ser las más valiosas para un sistema con arquitectura multicapa como este. Conocer el esquema de MongoDB permitió verificar directamente que las contraseñas se almacenan como hash `PBKDF2-SHA256` y que el email se normaliza a minúsculas, garantizando integridad de datos más allá de lo que muestra la interfaz.

El defecto más relevante encontrado fue **DEF-02**: la ausencia de limitación de intentos de login, un riesgo de seguridad real que ninguna de las tres técnicas detectó directamente hasta ser explorado con criterio de seguridad. Esto evidencia que las técnicas de prueba funcional deben complementarse con pruebas de seguridad específicas.

En conclusión, ninguna técnica por sí sola es suficiente. La combinación de caja negra, caja blanca y caja gris permitió alcanzar una cobertura del **100% de los requisitos funcionales y no funcionales**, demostrando que un enfoque diversificado de testing es esencial para garantizar la calidad de un sistema de e-commerce.

---