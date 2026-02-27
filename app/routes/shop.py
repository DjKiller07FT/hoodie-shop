"""
Blueprint de Tienda.
Rutas: catálogo, detalle producto, carrito, checkout.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from bson import ObjectId
from app import get_db
from app.services.product_service import ProductService
from app.services.order_service import OrderService
from app.services.whatsapp_service import WhatsAppService
from flask import current_app

bp = Blueprint('shop', __name__)


@bp.route('/')
@bp.route('/catalog')
def catalog():
    """Catálogo de productos"""
    db = get_db()
    product_service = ProductService(db)
    
    # Obtener parámetros de búsqueda/filtro
    search_query = request.args.get('q', '').strip()
    
    if search_query:
        products = product_service.buscar_productos(search_query)
    else:
        products = product_service.get_all_products(solo_activos=True)
    
    return render_template('shop/catalog.html', products=products, search_query=search_query)


@bp.route('/product/<product_id>')
def product_detail(product_id):
    """Detalle de un producto"""
    db = get_db()
    product_service = ProductService(db)
    
    product = product_service.get_product_by_id(product_id)
    
    if not product or not product.activo:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('shop.catalog'))
    
    return render_template('shop/product_detail.html', product=product)


@bp.route('/cart')
def cart():
    """Ver carrito de compras"""
    cart_items = session.get('cart', [])
    
    # Calcular total
    total = sum(item['subtotal'] for item in cart_items)
    
    return render_template('shop/cart.html', cart_items=cart_items, total=total)


@bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    """Agregar producto al carrito"""
    product_id = request.form.get('product_id')
    talla = request.form.get('talla')
    color = request.form.get('color')
    cantidad = int(request.form.get('cantidad', 1))
    
    db = get_db()
    product_service = ProductService(db)
    product = product_service.get_product_by_id(product_id)
    
    if not product:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('shop.catalog'))
    
    # Verificar stock
    if not product.tiene_stock(talla, cantidad):
        flash(f'Stock insuficiente para talla {talla}', 'warning')
        return redirect(url_for('shop.product_detail', product_id=product_id))
    
    # Inicializar carrito si no existe
    if 'cart' not in session:
        session['cart'] = []
    
    # Crear item del carrito
    cart_item = {
        'product_id': str(product._id),
        'nombre': product.nombre,
        'talla': talla,
        'color': color,
        'cantidad': cantidad,
        'precio_unitario': product.precio,
        'subtotal': product.precio * cantidad,
        'imagen': product.imagen
    }
    
    # Verificar si ya existe el mismo producto con misma talla y color
    cart = session['cart']
    item_existente = None
    for i, item in enumerate(cart):
        if (item['product_id'] == cart_item['product_id'] and 
            item['talla'] == talla and 
            item['color'] == color):
            item_existente = i
            break
    
    if item_existente is not None:
        # Actualizar cantidad
        cart[item_existente]['cantidad'] += cantidad
        cart[item_existente]['subtotal'] = cart[item_existente]['cantidad'] * cart[item_existente]['precio_unitario']
    else:
        # Agregar nuevo item
        cart.append(cart_item)
    
    session['cart'] = cart
    session.modified = True
    
    flash(f'{product.nombre} agregado al carrito', 'success')
    return redirect(url_for('shop.cart'))


@bp.route('/cart/remove/<int:index>')
def remove_from_cart(index):
    """Eliminar item del carrito"""
    cart = session.get('cart', [])
    
    if 0 <= index < len(cart):
        removed_item = cart.pop(index)
        session['cart'] = cart
        session.modified = True
        flash(f'{removed_item["nombre"]} eliminado del carrito', 'info')
    
    return redirect(url_for('shop.cart'))


@bp.route('/cart/update', methods=['POST'])
def update_cart():
    """Actualizar cantidades en el carrito"""
    cart = session.get('cart', [])
    
    for i, item in enumerate(cart):
        new_quantity = request.form.get(f'cantidad_{i}')
        if new_quantity:
            cart[i]['cantidad'] = int(new_quantity)
            cart[i]['subtotal'] = cart[i]['cantidad'] * cart[i]['precio_unitario']
    
    session['cart'] = cart
    session.modified = True
    flash('Carrito actualizado', 'success')
    
    return redirect(url_for('shop.cart'))


@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout - confirmar pedido"""
    cart = session.get('cart', [])
    
    if not cart:
        flash('Tu carrito está vacío', 'warning')
        return redirect(url_for('shop.catalog'))
    
    if request.method == 'POST':
        # Obtener datos de envío
        direccion_envio = {
            'nombre': request.form.get('nombre', current_user.nombre),
            'telefono': request.form.get('telefono', current_user.telefono),
            'direccion': request.form.get('direccion', current_user.direccion),
            'ciudad': request.form.get('ciudad', current_user.ciudad),
            'notas': request.form.get('notas', '')
        }
        
        # Crear pedido
        db = get_db()
        order_service = OrderService(db)
        product_service = ProductService(db)
        
        # Verificar stock antes de crear pedido
        for item in cart:
            product = product_service.get_product_by_id(item['product_id'])
            if not product.tiene_stock(item['talla'], item['cantidad']):
                flash(f'Stock insuficiente para {item["nombre"]} talla {item["talla"]}', 'danger')
                return redirect(url_for('shop.cart'))
        
        success, message, order = order_service.create_order(
            user_id=current_user.get_id(),
            items=cart,
            direccion_envio=direccion_envio
        )
        
        if success:
            # Reducir stock de productos
            for item in cart:
                product_service.reducir_stock(
                    item['product_id'],
                    item['talla'],
                    item['cantidad']
                )
            
            # Limpiar carrito
            session.pop('cart', None)
            session.modified = True
            
            # Generar enlace de WhatsApp
            whatsapp_service = WhatsAppService(current_app.config['WHATSAPP_NUMBER'])
            whatsapp_link = whatsapp_service.generar_enlace_whatsapp(order, current_user)
            
            flash('¡Pedido creado exitosamente!', 'success')
            return render_template('shop/order_success.html', order=order, whatsapp_link=whatsapp_link)
        else:
            flash(message, 'danger')
    
    # Calcular total
    total = sum(item['subtotal'] for item in cart)
    
    return render_template('shop/checkout.html', cart=cart, total=total, user=current_user)