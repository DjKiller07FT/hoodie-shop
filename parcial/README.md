# PARCIAL – TESTING DE SOFTWARE
## Ingeniería de Software II

**Estudiante:** Nicolas Camilo Bocanegra Vaca

**Fecha:** Marzo 2026

**Proyecto:** Hoodie Shop – E-commerce

**Módulo:** Gestión de Usuarios y Autenticación

**Repositorio:** https://github.com/DjKiller07FT/hoodie-shop

---

## Descripción

Este directorio contiene todos los entregables del parcial de Testing de Software aplicado sobre el proyecto **Hoodie Shop**, un e-commerce desarrollado con Flask y MongoDB Atlas. Las pruebas cubren el módulo de **Gestión de Usuarios y Autenticación** utilizando tres técnicas: Caja Negra, Caja Blanca y Caja Gris.

---

## Estructura del directorio

```
parcial/
├── README.md                            ← Este archivo
├── 1_Respuestas_Test.md                 ← Sección A: 10 preguntas teóricas
├── 2_Componente_Seleccionado.md         ← Ficha técnica del componente analizado
├── 3_Casos_CajaNegra_Web.md             ← 5 casos de prueba – Caja Negra
├── 4_Casos_CajaBlanca_Web.md            ← Código + rutas de ejecución + 7 casos
├── 5_Casos_CajaGris_Web.md              ← 4 casos de prueba – Caja Gris
├── 6_Evidencias_Ejecucion/              ← Capturas de pantalla (.png)
│   ├── CN_01_login_exitoso.png
│   ├── CN_02_password_incorrecto.png
│   ├── CN_03_email_duplicado.png
│   ├── CN_04_passwords_distintas.png
│   ├── CN_05_sin_sesion.png
│   ├── CB_pytest_output.png
│   ├── CB_coverage_report.png
│   ├── CG_01a_login_postman.png
│   ├── CG_02a_rbac_postman.png
│   ├── CG_02b_rol_compass.png
│   ├── CG_03a_registro_postman.png
│   ├── CG_03b_hash_compass.png
│   ├── CG_04a_stock_antes.png
│   ├── CG_04b_confirmacion.png
│   ├── CG_04c_stock_despues.png
│   └── CG_04d_orden_compass.png
├── 7_Matriz_Trazabilidad_Web.md         ← RF → caso → técnica → estado
├── 8_Reporte_Defectos.md                ← Defectos encontrados
└── 9_Reflexion_Critica_Web.md           ← Reflexión crítica (~200 palabras)
```

---

## Resumen de casos de prueba

| Técnica | Casos | IDs |
|---------|:-----:|-----|
| Caja Negra | 5 | WEB-CN-01 al WEB-CN-05 |
| Caja Blanca | 7 | WEB-CB-01 al WEB-CB-07 |
| Caja Gris | 4 | WEB-CG-01 al WEB-CG-04 |
| **Total** | **16** | |

---

## Cómo ejecutar las pruebas automatizadas

### Requisitos previos

```bash
# Clonar el repositorio
git clone https://github.com/DjKiller07FT/hoodie-shop.git
cd hoodie-shop

# Crear entorno virtual e instalar dependencias
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

pip install -r requirements.txt
pip install pytest pytest-cov
```

### Pruebas de Caja Blanca (pytest)

```bash
# Ejecutar los 7 casos de caja blanca
python -m pytest tests/test_cajaBlanca_auth.py -v

# Con reporte de cobertura
python -m pytest tests/test_cajaBlanca_auth.py -v \
  --cov=app/services/auth_service \
  --cov-report=term-missing
```

**Output esperado:**
```
tests/test_cajaBlanca_auth.py::test_WEB_CB_01_login_exitoso             PASSED
tests/test_cajaBlanca_auth.py::test_WEB_CB_02_login_campos_vacios       PASSED
tests/test_cajaBlanca_auth.py::test_WEB_CB_03_login_password_incorrecto PASSED
tests/test_cajaBlanca_auth.py::test_WEB_CB_04_registro_email_invalido   PASSED
tests/test_cajaBlanca_auth.py::test_WEB_CB_05_registro_password_corto   PASSED
tests/test_cajaBlanca_auth.py::test_WEB_CB_06_registro_email_duplicado  PASSED
tests/test_cajaBlanca_auth.py::test_WEB_CB_07_registro_exitoso          PASSED

7 passed in 0.45s — Coverage: 92%
```

Ver capturas: `6_Evidencias_Ejecucion/CB_pytest_output.png` y `CB_coverage_report.png`

### Pruebas de Caja Negra (manual — navegador)

1. Iniciar el servidor Flask:
```bash
python run.py
```
2. Abrir navegador en `http://localhost:5000`
3. Ejecutar casos WEB-CN-01 a WEB-CN-05 siguiendo los pasos en `3_Casos_CajaNegra_Web.md`

Ver capturas: `6_Evidencias_Ejecucion/CN_01_*.png` a `CN_05_*.png`

### Pruebas de Caja Gris (Postman + MongoDB Compass)

1. Importar colección en Postman y ejecutar los endpoints indicados en `5_Casos_CajaGris_Web.md`
2. Verificar resultados en MongoDB Atlas o MongoDB Compass

Ver capturas: `6_Evidencias_Ejecucion/CG_0*.png`

---

## Cobertura alcanzada

| Métrica | Valor |
|---------|-------|
| Requisitos funcionales cubiertos | 15/15 — **100%** |
| Cobertura de ramas (pytest-cov) | **92%** |
| Casos aprobados | 16/16 |
| Defectos encontrados | 3 |

---

## Defectos destacados

| ID | Severidad | Título |
|----|-----------|--------|
| DEF-02 | 🔴 Alta | Sin límite de intentos de login (fuerza bruta) |
| DEF-04 | 🟠 Media | `confirm_password` no validado en `AuthService` |
| DEF-03 | 🟡 Baja | Mensaje Flask-Login en inglés |

Ver detalle completo en `8_Reporte_Defectos.md`.

---

## Archivos de prueba

| Archivo | Descripción |
|---------|-------------|
| `tests/test_cajaBlanca_auth.py` | Script pytest con los 7 casos de Caja Blanca |
| `app/services/auth_service.py` | Servicio analizado en Caja Blanca |
| `app/utils/decorators.py` | Decorador `logout_required` analizado |