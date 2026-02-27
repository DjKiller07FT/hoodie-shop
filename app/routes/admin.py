"""
Blueprint de Administración.
Rutas: dashboard, CRUD productos, gestión pedidos.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from bson import ObjectId
import os
import csv
from io import StringIO
from flask import make_response

from app import get_db
from app.services.product_service import ProductService
from app.services.order_service import OrderService
from app.utils.decorators import admin_required
from app.utils.helpers import save_image
from app.models.order import Order

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Dashboard principal del administrador"""
    db = get_db()
    order_service = OrderService(db)
    product_service = ProductService(db)
    
    # Obtener estadísticas
    stats = order_service.get_estadisticas()
    
    # Productos con bajo stock
    products = product_service.get_all_products(solo_activos=True)
    low_stock_products = [p for p in products if p.get_stock_total() < 10]
    
    # Últimos pedidos
    recent_orders = order_service.get_all_orders()[:10]
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         low_stock_products=low_stock_products,
                         recent_orders=recent_orders)


# ==================== CRUD PRODUCTOS ====================

@bp.route('/products')
@login_required
@admin_required
def products():
    """Lista de productos (todos)"""
    db = get_db()
    product_service = ProductService(db)
    
    search = request.args.get('q', '').strip()
    show_inactive = request.args.get('inactive', 'false') == 'true'
    
    if search:
        all_products = product_service.buscar_productos(search)
    else:
        all_products = product_service.get_all_products(solo_activos=not show_inactive)
    
    return render_template('admin/products.html', 
                         products=all_products,
                         search=search,
                         show_inactive=show_inactive)


@bp.route('/products/new', methods=['GET', 'POST'])
@login_required
@admin_required
def product_new():
    """Crear nuevo producto"""
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        precio = request.form.get('precio', 0)
        
        # Stock por talla
        stock = {
            'S': int(request.form.get('stock_s', 0)),
            'M': int(request.form.get('stock_m', 0)),
            'L': int(request.form.get('stock_l', 0)),
            'XL': int(request.form.get('stock_xl', 0))
        }
        
        # Colores (separados por coma)
        colores_input = request.form.get('colores', '')
        colores = [c.strip() for c in colores_input.split(',') if c.strip()]
        
        # Imagen
        imagen = None
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and file.filename:
                imagen = save_image(file)
        
        # Crear producto
        db = get_db()
        product_service = ProductService(db)
        success, message, product_id = product_service.create_product(
            nombre, descripcion, precio, stock, colores, imagen
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('admin.products'))
        else:
            flash(message, 'danger')
    
    return render_template('admin/product_form.html', product=None, action='Crear')


@bp.route('/products/<product_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def product_edit(product_id):
    """Editar producto existente"""
    db = get_db()
    product_service = ProductService(db)
    product = product_service.get_product_by_id(product_id)
    
    if not product:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('admin.products'))
    
    if request.method == 'POST':
        updates = {
            'nombre': request.form.get('nombre', '').strip(),
            'descripcion': request.form.get('descripcion', '').strip(),
            'precio': float(request.form.get('precio', 0)),
            'stock': {
                'S': int(request.form.get('stock_s', 0)),
                'M': int(request.form.get('stock_m', 0)),
                'L': int(request.form.get('stock_l', 0)),
                'XL': int(request.form.get('stock_xl', 0))
            }
        }
        
        # Colores
        colores_input = request.form.get('colores', '')
        updates['colores'] = [c.strip() for c in colores_input.split(',') if c.strip()]
        
        # Imagen nueva (opcional)
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and file.filename:
                nueva_imagen = save_image(file)
                if nueva_imagen:
                    updates['imagen'] = nueva_imagen
        
        success, message = product_service.update_product(product_id, **updates)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('admin.products'))
        else:
            flash(message, 'danger')
    
    return render_template('admin/product_form.html', product=product, action='Editar')


@bp.route('/products/<product_id>/delete')
@login_required
@admin_required
def product_delete(product_id):
    """Eliminar (desactivar) producto"""
    db = get_db()
    product_service = ProductService(db)
    
    success, message = product_service.delete_product(product_id)
    
    if success:
        flash('Producto desactivado exitosamente', 'success')
    else:
        flash(message, 'danger')
    
    return redirect(url_for('admin.products'))


@bp.route('/products/<product_id>/restore')
@login_required
@admin_required
def product_restore(product_id):
    """Restaurar producto desactivado"""
    db = get_db()
    product_service = ProductService(db)
    
    success, message = product_service.restore_product(product_id)
    
    if success:
        flash('Producto restaurado exitosamente', 'success')
    else:
        flash(message, 'danger')
    
    return redirect(url_for('admin.products'))


# ==================== GESTIÓN DE PEDIDOS ====================

@bp.route('/orders')
@login_required
@admin_required
def orders():
    """Lista de todos los pedidos"""
    db = get_db()
    order_service = OrderService(db)
    
    # Filtro por estado
    estado_filtro = request.args.get('estado', None)
    
    all_orders = order_service.get_all_orders(filtro_estado=estado_filtro)
    
    return render_template('admin/orders.html', 
                         orders=all_orders,
                         estados=Order.ESTADOS_VALIDOS,
                         estado_filtro=estado_filtro)


@bp.route('/orders/<order_id>')
@login_required
@admin_required
def order_detail(order_id):
    """Detalle de un pedido"""
    db = get_db()
    order_service = OrderService(db)
    
    order = order_service.get_order_by_id(order_id)
    
    if not order:
        flash('Pedido no encontrado', 'danger')
        return redirect(url_for('admin.orders'))
    
    # Obtener info del usuario
    from app.services.auth_service import AuthService
    auth_service = AuthService(db)
    user = auth_service.get_user_by_id(order.user_id)
    
    return render_template('admin/order_detail.html', order=order, user=user)


@bp.route('/orders/<order_id>/change-status', methods=['POST'])
@login_required
@admin_required
def order_change_status(order_id):
    """Cambiar estado de un pedido"""
    nuevo_estado = request.form.get('estado')
    
    db = get_db()
    order_service = OrderService(db)
    
    success, message = order_service.cambiar_estado(
        order_id, 
        nuevo_estado, 
        current_user.get_id()
    )
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
    
    return redirect(url_for('admin.order_detail', order_id=order_id))


@bp.route('/orders/export')
@login_required
@admin_required
def orders_export():
    """Exportar pedidos a CSV"""
    db = get_db()
    order_service = OrderService(db)
    
    estado_filtro = request.args.get('estado', None)
    csv_data = order_service.exportar_pedidos_csv(estado_filtro)
    
    # Crear CSV
    si = StringIO()
    writer = csv.DictWriter(si, fieldnames=csv_data[0].keys() if csv_data else [])
    writer.writeheader()
    writer.writerows(csv_data)
    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=pedidos.csv"
    output.headers["Content-type"] = "text/csv"
    
    return output