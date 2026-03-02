# HISTORIAS DE USUARIO
## Proyecto: Hoodie Shop – E-commerce
**Fecha:** Marzo 2026
**Responsable:** Camilo Bocanegra

---

## SPRINT 1 – AUTENTICACIÓN

---

### HU-01

| Campo | Detalle |
|-------|---------|
| **Título** | REGISTRO DE NUEVO USUARIO |
| **Nro Sprint** | 1 |
| **Responsable** | Programador – Camilo Bocanegra |

**Como:** visitante del sitio web
**Quiero:** registrarme con mis datos personales y una contraseña
**Para:** crear una cuenta y poder realizar compras en la tienda.

**Criterios de Aceptación:**
- **Dado que** el visitante ingresa todos los datos obligatorios (nombre, email, teléfono, dirección, ciudad y contraseña) de forma válida, **cuando** presione el botón "Registrarse", **entonces** el sistema creará la cuenta, iniciará sesión automáticamente y redirigirá al catálogo de productos.
- **Dado que** el visitante ingresa un email que ya está registrado, **cuando** intente registrarse, **entonces** el sistema mostrará el mensaje "El email ya está registrado" y no creará la cuenta.
- **Dado que** el visitante ingresa contraseñas que no coinciden en los campos "Contraseña" y "Confirmar contraseña", **cuando** intente registrarse, **entonces** el sistema mostrará el mensaje "Las contraseñas no coinciden" y no creará la cuenta.
- **Dado que** el visitante deja campos obligatorios vacíos, **cuando** intente registrarse, **entonces** el sistema mostrará los mensajes de validación correspondientes por cada campo incompleto.

---

### HU-02

| Campo | Detalle |
|-------|---------|
| **Título** | INICIO DE SESIÓN DE USUARIO |
| **Nro Sprint** | 1 |
| **Responsable** | Programador – Camilo Bocanegra |

**Como:** usuario registrado
**Quiero:** iniciar sesión en el sistema con mi email y contraseña
**Para:** acceder a las funcionalidades disponibles según mi perfil.

**Criterios de Aceptación:**
- **Dado que** el usuario ingresa un email y contraseña válidos, **cuando** presione el botón "Iniciar Sesión", **entonces** el sistema autenticará al usuario y lo redirigirá al catálogo si es cliente o al dashboard si es administrador.
- **Dado que** el usuario ingresa credenciales incorrectas, **cuando** intente iniciar sesión, **entonces** el sistema mostrará el mensaje "Email o contraseña incorrectos" y no permitirá el acceso.
- **Dado que** el usuario marca la opción "Recordarme", **cuando** inicie sesión correctamente, **entonces** el sistema mantendrá la sesión activa por 7 días aunque cierre el navegador.
- **Dado que** un usuario ya autenticado intenta acceder a la página de login, **cuando** ingrese la URL `/auth/login`, **entonces** el sistema lo redirigirá directamente al catálogo.

---

### HU-03

| Campo | Detalle |
|-------|---------|
| **Título** | CIERRE DE SESIÓN |
| **Nro Sprint** | 1 |
| **Responsable** | Programador – Camilo Bocanegra |

**Como:** usuario autenticado
**Quiero:** cerrar mi sesión de forma segura
**Para:** proteger mi cuenta cuando termine de usar la aplicación.

**Criterios de Aceptación:**
- **Dado que** el usuario autenticado hace clic en el botón "Cerrar Sesión" del menú, **cuando** confirme la acción, **entonces** el sistema destruirá la sesión activa, mostrará el mensaje "Sesión cerrada correctamente" y redirigirá al catálogo de productos.
- **Dado que** la sesión del usuario ha sido cerrada, **cuando** intente acceder a una ruta protegida como `/user/profile`, **entonces** el sistema lo redirigirá automáticamente a la página de login.

---

## SPRINT 2 – CATÁLOGO Y PRODUCTOS

---

### HU-04

| Campo | Detalle |
|-------|---------|
| **Título** | VISUALIZACIÓN DEL CATÁLOGO DE PRODUCTOS |
| **Nro Sprint** | 2 |
| **Responsable** | Programador – Camilo Bocanegra |

**Como:** visitante o usuario registrado
**Quiero:** ver todos los hoodies disponibles en el catálogo
**Para:** explorar los productos y encontrar el que deseo comprar.

**Criterios de Aceptación:**
- **Dado que** cualquier persona accede a la dirección principal del sitio (`/catalog`), **cuando** cargue la página, **entonces** el sistema mostrará todos los productos activos en un grid con imagen, nombre y precio en pesos colombianos (COP).
- **Dado que** no hay productos activos registrados en el sistema, **cuando** se acceda al catálogo, **entonces** el sistema mostrará un mensaje informativo indicando que no hay productos disponibles.
- **Dado que** el usuario accede desde un dispositivo móvil, **cuando** cargue el catálogo, **entonces** la interfaz se adaptará al tamaño de pantalla mostrando correctamente todas las tarjetas de producto.

---

### HU-05

| Campo | Detalle |
|-------|---------|
| **Título** | BÚSQUEDA DE PRODUCTOS |
| **Nro Sprint** | 2 |
| **Responsable** | Programador – Camilo Bocanegra |

**Como:** visitante o usuario registrado
**Quiero:** buscar productos por nombre o descripción
**Para:** encontrar rápidamente el hoodie que estoy buscando sin revisar todo el catálogo.

**Criterios de Aceptación:**
- **Dado que** el usuario escribe un texto en la barra de búsqueda y presiona Enter o el botón buscar, **cuando** se procese la búsqueda, **entonces** el sistema mostrará únicamente los productos activos cuyo nombre o descripción contenga el texto buscado (sin importar mayúsculas o minúsculas).
- **Dado que** el usuario realiza una búsqueda con un texto que no coincide con ningún producto, **cuando** se procese la búsqueda, **entonces** el sistema mostrará el mensaje "No se encontraron productos para tu búsqueda".
- **Dado que** el usuario borra el texto de búsqueda y presiona Enter, **cuando** se procese la solicitud, **entonces** el sistema mostrará nuevamente todos los productos activos del catálogo.

---

### HU-06

| Campo | Detalle |
|-------|---------|
| **Título** | VER DETALLE DE PRODUCTO |
| **Nro Sprint** | 2 |
| **Responsable** | Programador – Camilo Bocanegra |

**Como:** visitante o usuario registrado
**Quiero:** ver la información completa de un hoodie específico
**Para:** conocer su descripción, precio, tallas y colores disponibles antes de decidir comprarlo.

**Criterios de Aceptación:**
- **Dado que** el usuario hace clic en un producto del catálogo, **cuando** cargue la página de detalle, **entonces** el sistema mostrará la imagen, nombre, descripción, precio en COP, los selectores de talla (solo las que tienen stock), colores disponibles y el botón "Agregar al Carrito".
- **Dado que** una talla no tiene stock disponible, **cuando** se cargue el detalle del producto, **entonces** esa talla no aparecerá como opción seleccionable en el selector.
- **Dado que** el usuario intenta acceder al detalle de un producto desactivado o inexistente, **cuando** cargue la URL, **entonces** el sistema lo redirigirá al catálogo mostrando el mensaje "Producto no encontrado".

---

## SPRINT 3 – CARRITO DE COMPRAS

---

### HU-07

| Campo | Detalle |
|-------|---------|
| **Título** | AGREGAR PRODUCTO AL CARRITO |
| **Nro Sprint** | 3 |
| **Responsable** | Programador – Camilo Bocanegra |

**Como:** visitante o usuario registrado
**Quiero:** agregar un hoodie al carrito seleccionando talla, color y cantidad
**Para:** acumular los productos que deseo comprar antes de proceder al pago.

**Criterios de Aceptación:**
- **Dado que** el usuario selecciona una talla, un color y una cantidad válida en el detalle del producto, **cuando** presione el botón "Agregar al Carrito", **entonces** el sistema verificará el stock, agregará el producto al carrito, actualizará el contador del carrito en el menú superior y mostrará el mensaje "{nombre del producto} agregado al carrito".
- **Dado que** el usuario agrega el mismo producto con la misma talla y color que ya está en el carrito, **cuando** se procese la solicitud, **entonces** el sistema sumará la nueva cantidad al item existente en lugar de crear un duplicado.
- **Dado que** la cantidad solicitada supera el stock disponible para la talla seleccionada, **cuando** el usuario intente agregar al carrito, **entonces** el sistema mostrará el mensaje "Stock insuficiente para talla {talla}" y no modificará el carrito.

---

### HU-08

| Campo | Detalle |
|-------|---------|
| **Título** | VER Y GESTIONAR EL CARRITO |
| **Nro Sprint** | 3 |
| **Responsable** | Programador – Camilo Bocanegra |

**Como:** visitante o usuario registrado
**Quiero:** ver todos los productos que he agregado al carrito y gestionar su contenido
**Para:** revisar mi selección, modificar cantidades o eliminar productos antes de pagar.

**Criterios de Aceptación:**
- **Dado que** el usuario accede a la página del carrito (`/cart`), **cuando** cargue la página, **entonces** el sistema mostrará la lista completa de productos con imagen, nombre, talla, color, cantidad, precio unitario, subtotal por ítem y el total general en COP.
- **Dado que** el usuario hace clic en el botón eliminar de un ítem del carrito, **cuando** se procese la acción, **entonces** el sistema eliminará ese ítem, recalculará el total y mostrará el carrito actualizado.
- **Dado que** el carrito está vacío, **cuando** el usuario acceda a `/cart`, **entonces** el sistema mostrará el mensaje "Tu carrito está vacío" con un botón para ir al catálogo.
- **Dado que** el usuario hace clic en "Vaciar Carrito", **cuando** confirme la acción, **entonces** el sistema eliminará todos los ítems del carrito y mostrará el carrito vacío.

---

## SPRINT 4 – PEDIDOS Y CHECKOUT

---

### HU-09

| Campo | Detalle |
|-------|---------|
| **Título** | REALIZAR PEDIDO (CHECKOUT) |
| **Nro Sprint** | 4 |
| **Responsable** | Programador – Camilo Bocanegra |

**Como:** usuario registrado con productos en el carrito
**Quiero:** confirmar mi pedido ingresando mis datos de envío
**Para:** formalizar mi compra y recibir el hoodie en mi domicilio con pago contraentrega.

**Criterios de Aceptación:**
- **Dado que** el usuario autenticado con carrito no vacío accede al checkout, **cuando** cargue la página, **entonces** el sistema pre-cargará automáticamente los datos de envío del perfil del usuario (nombre, teléfono, dirección y ciudad) en el formulario.
- **Dado que** el usuario completa el formulario de envío y presiona "Confirmar Pedido", **cuando** se procese la solicitud, **entonces** el sistema verificará el stock de cada ítem, creará el pedido con estado "RECIBIDO", reducirá el stock, vaciará el carrito y mostrará la página de confirmación con el número de pedido y el botón de WhatsApp.
- **Dado que** el stock de algún producto se agotó entre que fue agregado al carrito y el momento del checkout, **cuando** el usuario confirme el pedido, **entonces** el sistema mostrará el mensaje "Stock insuficiente para {producto} talla {talla}" y no creará el pedido.
- **Dado que** un usuario no autenticado intenta acceder al checkout, **cuando** entre a la URL `/checkout`, **entonces** el sistema lo redirigirá a la página de login y luego de autenticarse volverá al checkout.

---

### HU-10

| Campo | Detalle |
|-------|---------|
| **Título** | CONFIRMACIÓN DE PEDIDO POR WHATSAPP |
| **Nro Sprint** | 4 |
| **Responsable** | Programador – Camilo Bocanegra |

**Como:** cliente que acaba de realizar un pedido
**Quiero:** enviar la confirmación de mi pedido por WhatsApp al vendedor
**Para:** notificar al negocio de mi compra con todos los detalles del pedido.

**Criterios de Aceptación:**
- **Dado que** el pedido fue creado exitosamente, **cuando** se muestre la página de confirmación, **entonces** el sistema generará un botón verde de WhatsApp con un mensaje prellenado que incluya: número de pedido, nombre del cliente, teléfono, dirección, lista de productos con talla, color, cantidad y subtotal, y el total en COP.
- **Dado que** el usuario hace clic en el botón "Enviar por WhatsApp", **cuando** se abra el enlace, **entonces** el sistema redirigirá a WhatsApp Web o la app de WhatsApp con el mensaje ya redactado apuntando al número de la empresa, listo para enviar.
- **Dado que** el mensaje de WhatsApp incluye el total, **cuando** se genere, **entonces** el valor aparecerá en formato pesos colombianos con la notación `$XXX.XXX COP`.

---

### HU-11

| Campo | Detalle |
|-------|---------|
| **Título** | HISTORIAL DE PEDIDOS DEL CLIENTE |
| **Nro Sprint** | 4 |
| **Responsable** | Programador – Camilo Bocanegra |

**Como:** cliente registrado
**Quiero:** ver el listado de todos mis pedidos y el detalle de cada uno
**Para:** hacer seguimiento al estado de mis compras y consultar mi historial.

**Criterios de Aceptación:**
- **Dado que** el usuario autenticado accede a "Mis Pedidos" (`/user/orders`), **cuando** cargue la página, **entonces** el sistema mostrará todos sus pedidos ordenados del más reciente al más antiguo, con número de pedido, fecha, total en COP y badge de estado.
- **Dado que** el usuario hace clic en un pedido, **cuando** cargue el detalle, **entonces** el sistema mostrará los productos comprados, los datos de envío y el historial completo de cambios de estado con sus respectivas fechas.
- **Dado que** un usuario autenticado intenta acceder al detalle de un pedido que no le pertenece, **cuando** ingrese la URL del pedido ajeno, **entonces** el sistema mostrará el mensaje "No tienes permiso para ver este pedido" y lo redirigirá a su lista de pedidos.

---

## SPRINT 5 – PERFIL DE USUARIO

---

### HU-12

| Campo | Detalle |
|-------|---------|
| **Título** | EDICIÓN DE PERFIL DE USUARIO |
| **Nro Sprint** | 5 |
| **Responsable** | Programador – Camilo Bocanegra |

**Como:** usuario registrado
**Quiero:** editar mis datos personales y cambiar mi contraseña
**Para:** mantener mi información de contacto y dirección actualizados para futuros pedidos.

**Criterios de Aceptación:**
- **Dado que** el usuario accede a su perfil (`/user/profile`) y modifica su nombre, teléfono, dirección o ciudad, **cuando** presione el botón "Guardar Cambios", **entonces** el sistema actualizará los datos en la base de datos y mostrará el mensaje "Perfil actualizado exitosamente".
- **Dado que** el usuario desea cambiar su contraseña e ingresa la contraseña actual correcta junto con una nueva contraseña, **cuando** guarde los cambios, **entonces** el sistema actualizará la contraseña y mostrará el mensaje "Contraseña actualizada exitosamente".
- **Dado que** el usuario intenta cambiar la contraseña pero ingresa una contraseña actual incorrecta, **cuando** intente guardar, **entonces** el sistema mostrará el mensaje "Contraseña actual incorrecta" y no realizará ningún cambio.
- **Dado que** el usuario deja en blanco los campos de contraseña, **cuando** guarde los cambios de otros campos, **entonces** el sistema actualizará solo los datos de perfil sin modificar la contraseña.

---

## SPRINT 6 – ADMINISTRACIÓN DE PRODUCTOS

---

### HU-13

| Campo | Detalle |
|-------|---------|
| **Título** | DASHBOARD ADMINISTRATIVO |
| **Nro Sprint** | 6 |
| **Responsable** | Programador – Camilo Bocanegra |

**Como:** administrador del sistema
**Quiero:** ver un panel de control con las estadísticas del negocio
**Para:** tomar decisiones informadas sobre el inventario, las ventas y los pedidos pendientes.

**Criterios de Aceptación:**
- **Dado que** el administrador inicia sesión con su cuenta, **cuando** sea redirigido al dashboard (`/admin/dashboard`), **entonces** el sistema mostrará: el total de pedidos, las ventas totales en COP, el conteo de pedidos por cada estado y los últimos 10 pedidos recientes.
- **Dado que** hay productos con menos de 10 unidades de stock total, **cuando** el administrador acceda al dashboard, **entonces** el sistema mostrará una sección de alerta con la lista de productos con bajo stock indicando cuántas unidades les quedan.
- **Dado que** un usuario con rol "cliente" intenta acceder a `/admin/dashboard`, **cuando** ingrese la URL directamente, **entonces** el sistema le negará el acceso, mostrará el mensaje "No tienes permisos para acceder a esta página" y lo redirigirá al catálogo.

---

### HU-14

| Campo | Detalle |
|-------|---------|
| **Título** | CREAR PRODUCTO |
| **Nro Sprint** | 6 |
| **Responsable** | Programador – Camilo Bocanegra |

**Como:** administrador
**Quiero:** crear nuevos hoodies con su información completa y foto
**Para:** agregarlos al catálogo y que los clientes puedan verlos y comprarlos.

**Criterios de Aceptación:**
- **Dado que** el administrador completa el formulario con nombre, descripción, precio, stock por talla (S, M, L, XL), colores y una imagen válida, **cuando** presione "Crear Producto", **entonces** el sistema guardará el producto con `activo=True`, lo publicará en el catálogo y mostrará el mensaje "Producto creado exitosamente".
- **Dado que** el administrador sube una imagen cuya extensión no está permitida (por ejemplo `.pdf`), **cuando** intente crear el producto, **entonces** el sistema mostrará el mensaje indicando que el formato de archivo no es válido.
- **Dado que** el administrador sube una imagen mayor a 5MB, **cuando** intente enviar el formulario, **entonces** el sistema rechazará el archivo y mostrará el mensaje de tamaño excedido.
- **Dado que** el administrador deja el campo nombre o descripción vacío, **cuando** intente crear el producto, **entonces** el sistema mostrará los mensajes de validación requeridos y no creará el producto.

---

### HU-15

| Campo | Detalle |
|-------|---------|
| **Título** | EDITAR PRODUCTO |
| **Nro Sprint** | 6 |
| **Responsable** | Programador – Camilo Bocanegra |

**Como:** administrador
**Quiero:** editar la información de un producto existente
**Para:** actualizar precios, descripciones, stock o imágenes cuando sea necesario.

**Criterios de Aceptación:**
- **Dado que** el administrador accede al formulario de edición de un producto y modifica algún campo, **cuando** presione "Guardar Cambios", **entonces** el sistema actualizará los datos en MongoDB, registrará la fecha de actualización y mostrará el mensaje "Producto actualizado exitosamente".
- **Dado que** el administrador sube una nueva imagen en la edición, **cuando** guarde los cambios, **entonces** el sistema reemplazará la imagen anterior por la nueva en el catálogo.
- **Dado que** el administrador no sube una nueva imagen durante la edición, **cuando** guarde los cambios, **entonces** el sistema conservará la imagen anterior del producto sin modificarla.

---

### HU-16

| Campo | Detalle |
|-------|---------|
| **Título** | DESACTIVAR Y RESTAURAR PRODUCTO |
| **Nro Sprint** | 6 |
| **Responsable** | Programador – Camilo Bocanegra |

**Como:** administrador
**Quiero:** desactivar productos del catálogo sin eliminarlos permanentemente y poder reactivarlos
**Para:** ocultar temporalmente un producto sin perder su información histórica.

**Criterios de Aceptación:**
- **Dado que** el administrador hace clic en "Desactivar" sobre un producto activo, **cuando** confirme la acción, **entonces** el sistema pondrá el campo `activo=False`, mostrará el mensaje "Producto desactivado exitosamente" y el producto dejará de aparecer en el catálogo de clientes.
- **Dado que** el administrador accede a la lista de productos inactivos (`?inactive=true`) y hace clic en "Restaurar", **cuando** confirme la acción, **entonces** el sistema pondrá `activo=True`, mostrará el mensaje "Producto restaurado exitosamente" y el producto volverá a ser visible en el catálogo.
- **Dado que** un producto está desactivado, **cuando** un cliente intente acceder a su URL de detalle directamente, **entonces** el sistema redirigirá al catálogo con el mensaje "Producto no encontrado".

---

## SPRINT 7 – ADMINISTRACIÓN DE PEDIDOS

---

### HU-17

| Campo | Detalle |
|-------|---------|
| **Título** | GESTIÓN DE PEDIDOS (ADMINISTRADOR) |
| **Nro Sprint** | 7 |
| **Responsable** | Programador – Camilo Bocanegra |

**Como:** administrador
**Quiero:** ver todos los pedidos del sistema con sus detalles y filtrarlos por estado
**Para:** hacer seguimiento de las ventas y saber qué pedidos debo atender primero.

**Criterios de Aceptación:**
- **Dado que** el administrador accede a `/admin/orders`, **cuando** cargue la página, **entonces** el sistema mostrará todos los pedidos ordenados del más reciente al más antiguo con: número de pedido, nombre del cliente, fecha, total en COP y badge del estado actual.
- **Dado que** el administrador selecciona un filtro de estado (por ejemplo "RECIBIDO"), **cuando** aplique el filtro con `?estado=RECIBIDO`, **entonces** el sistema mostrará únicamente los pedidos que estén en ese estado.
- **Dado que** el administrador hace clic en un pedido, **cuando** cargue el detalle, **entonces** el sistema mostrará: los productos comprados con talla, color y cantidad; los datos de envío del cliente; el historial completo de estados con fecha y hora de cada cambio.

---

### HU-18

| Campo | Detalle |
|-------|---------|
| **Título** | CAMBIAR ESTADO DE PEDIDO |
| **Nro Sprint** | 7 |
| **Responsable** | Programador – Camilo Bocanegra |

**Como:** administrador
**Quiero:** cambiar el estado de un pedido a lo largo de su ciclo de vida
**Para:** informar al cliente el progreso de su compra desde que es recibida hasta que es entregada.

**Criterios de Aceptación:**
- **Dado que** el administrador selecciona un nuevo estado válido (ALISTAMIENTO, ENVIO o ENTREGADO) desde el formulario del detalle de un pedido, **cuando** presione "Cambiar Estado", **entonces** el sistema actualizará el estado del pedido, registrará en el historial la fecha/hora del cambio y el ID del administrador que lo realizó, y mostrará el mensaje "Estado cambiado a {nuevo estado}".
- **Dado que** el administrador intenta asignar el mismo estado que ya tiene el pedido, **cuando** envíe el formulario, **entonces** el sistema mostrará el mensaje "El pedido ya está en ese estado" y no realizará ningún cambio.
- **Dado que** el pedido ha cambiado de estado, **cuando** el cliente consulte su detalle en "Mis Pedidos", **entonces** el cliente verá el nuevo estado reflejado junto con el historial completo de todos los estados anteriores y sus fechas.

---

### HU-19

| Campo | Detalle |
|-------|---------|
| **Título** | EXPORTAR PEDIDOS A CSV |
| **Nro Sprint** | 7 |
| **Responsable** | Programador – Camilo Bocanegra |

**Como:** administrador
**Quiero:** exportar el listado de pedidos en formato CSV
**Para:** analizar las ventas en herramientas externas como Excel o Google Sheets.

**Criterios de Aceptación:**
- **Dado que** el administrador hace clic en el botón "Exportar CSV" en la sección de pedidos, **cuando** se descargue el archivo, **entonces** el sistema generará un archivo `pedidos.csv` con las columnas: Número Pedido, Fecha, Cliente, Teléfono, Ciudad, Total y Estado.
- **Dado que** el administrador aplica un filtro de estado antes de exportar, **cuando** descargue el CSV, **entonces** el archivo contendrá únicamente los pedidos del estado seleccionado.
- **Dado que** el administrador exporta el CSV, **cuando** abra el archivo en Excel, **entonces** los valores de total aparecerán como números sin formato de moneda para facilitar cálculos.

---

## SPRINT 8 – CONTROL DE INVENTARIO

---

### HU-20

| Campo | Detalle |
|-------|---------|
| **Título** | CONTROL AUTOMÁTICO DE STOCK |
| **Nro Sprint** | 8 |
| **Responsable** | Programador – Camilo Bocanegra |

**Como:** sistema
**Quiero:** actualizar automáticamente el stock de cada producto al confirmar un pedido
**Para:** garantizar que no se venda más inventario del disponible y los datos de stock sean siempre precisos.

**Criterios de Aceptación:**
- **Dado que** se confirma un pedido con 2 unidades de talla M de un producto, **cuando** el sistema procese el checkout, **entonces** reducirá en 2 unidades el stock de talla M de ese producto en la base de datos de manera inmediata.
- **Dado que** el stock de una talla queda en 0 después de un pedido, **cuando** otro cliente vea el detalle de ese producto, **entonces** esa talla ya no aparecerá disponible en el selector de tallas.
- **Dado que** el stock total de un producto cae por debajo de 10 unidades, **cuando** el administrador acceda al dashboard, **entonces** ese producto aparecerá en la sección de alerta "Productos con bajo stock".