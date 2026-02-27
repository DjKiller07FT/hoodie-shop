"""
Blueprint de Usuario.
Rutas: perfil, mis pedidos.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import get_db
from app.services.auth_service import AuthService
from app.services.order_service import OrderService

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Perfil del usuario"""
    if request.method == 'POST':
        # Actualizar datos
        updates = {
            'nombre': request.form.get('nombre', '').strip(),
            'telefono': request.form.get('telefono', '').strip(),
            'direccion': request.form.get('direccion', '').strip(),
            'ciudad': request.form.get('ciudad', '').strip()
        }
        
        # Cambiar contraseña (opcional)
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        
        if new_password:
            if not current_password:
                flash('Debes ingresar tu contraseña actual', 'danger')
                return render_template('user/profile.html')
            
            if not current_user.check_password(current_password):
                flash('Contraseña actual incorrecta', 'danger')
                return render_template('user/profile.html')
            
            # Actualizar contraseña
            from werkzeug.security import generate_password_hash
            updates['password_hash'] = generate_password_hash(new_password)
            flash('Contraseña actualizada exitosamente', 'success')
        
        # Guardar cambios
        db = get_db()
        auth_service = AuthService(db)
        
        if auth_service.update_user(current_user.get_id(), **updates):
            flash('Perfil actualizado exitosamente', 'success')
            return redirect(url_for('user.profile'))
        else:
            flash('Error al actualizar perfil', 'danger')
    
    return render_template('user/profile.html')


@bp.route('/orders')
@login_required
def orders():
    """Mis pedidos"""
    db = get_db()
    order_service = OrderService(db)
    
    user_orders = order_service.get_orders_by_user(current_user.get_id())
    
    return render_template('user/my_orders.html', orders=user_orders)


@bp.route('/orders/<order_id>')
@login_required
def order_detail(order_id):
    """Detalle de mi pedido"""
    db = get_db()
    order_service = OrderService(db)
    
    order = order_service.get_order_by_id(order_id)
    
    if not order:
        flash('Pedido no encontrado', 'danger')
        return redirect(url_for('user.orders'))
    
    # Verificar que el pedido pertenece al usuario actual
    if str(order.user_id) != current_user.get_id():
        flash('No tienes permiso para ver este pedido', 'danger')
        return redirect(url_for('user.orders'))
    
    return render_template('user/order_detail.html', order=order)