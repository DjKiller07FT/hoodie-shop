# SECCIÓN A: TEST DE CONOCIMIENTOS
## Parcial de Testing de Software – Ingeniería de Software II

**Estudiante:** Nicolas Camilo Bocanegra Vaca
**Fecha:** Marzo 2026
**Institución:** Politécnico Internacional

---

| # | Pregunta | Respuesta |
|---|----------|-----------|
| 1 | En el contexto de una aplicación web, ¿cuál corresponde MEJOR a una prueba de caja negra? | **b)** Comprobar que al hacer clic en "Registrarse", el usuario recibe un correo de confirmación en menos de 2 minutos. |
| 2 | Validar que un endpoint REST `/api/users/{id}` retorna 404 cuando el ID es inexistente. ¿Qué técnica es la MÁS apropiada? | **a)** Caja negra, porque solo evalúa la respuesta HTTP sin conocer la implementación. |
| 3 | ¿Cuál de los siguientes NO es un objetivo típico de las pruebas de caja gris en una web app? | **d)** Evaluar la cobertura de ramas en una función de cálculo de descuentos. |
| 4 | En una aplicación web con React + Node.js, ¿qué herramienta sería MÁS útil para pruebas de caja blanca del backend? | **b)** Jest + Supertest |
| 5 | Tester conoce la estructura de BD pero no el código del backend, y diseña pruebas para validar integridad de datos. Está aplicando: | **c)** Caja gris |
| 6 | ¿Cuál de las siguientes afirmaciones sobre pruebas en aplicaciones web es VERDADERA? | **b)** Validar que un formulario muestra mensajes de error amigables es una prueba de caja negra. |
| 7 | Para probar que un componente React renderiza condicionalmente un botón según el rol del usuario, la técnica MÁS eficiente sería: | **b)** Caja blanca: usar React Testing Library con mocks de contexto de autenticación. |
| 8 | ¿Qué tipo de prueba es MÁS adecuada para detectar que una función de formato de fecha en JavaScript no maneja correctamente zonas horarias? | **b)** Caja blanca |
| 9 | En el contexto de seguridad web, ¿cuál escenario representa una prueba de caja gris? | **c)** Conocer que la app usa Helmet.js y probar headers de seguridad específicos en las respuestas HTTP. |
| 10 | "En una aplicación web, las pruebas de regresión automatizadas del frontend son siempre de caja negra". | **b)** Falso, pueden ser de caja blanca si se prueban componentes unitariamente con acceso al código. |

---