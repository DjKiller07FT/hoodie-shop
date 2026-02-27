"""
Blueprint de Autenticación.
Rutas: login, registro, logout.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app import get_db
from app.services.auth_service import AuthService
from app.utils.decorators import logout_required

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
@logout_required
def register():
    """Registro de nuevos usuarios"""
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        telefono = request.form.get('telefono', '').strip()
        direccion = request.form.get('direccion', '').strip()
        ciudad = request.form.get('ciudad', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validar que las contraseñas coincidan
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return render_template('auth/register.html')
        
        # Registrar usuario
        db = get_db()
        auth_service = AuthService(db)
        success, message, user = auth_service.register_user(
            nombre, email, telefono, direccion, ciudad, password
        )
        
        if success:
            flash(message, 'success')
            # Login automático después de registro
            login_user(user, remember=True)
            return redirect(url_for('shop.catalog'))
        else:
            flash(message, 'danger')
    
    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    """Login de usuarios"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        # Autenticar usuario
        db = get_db()
        auth_service = AuthService(db)
        success, message, user = auth_service.login_user(email, password)
        
        if success:
            login_user(user, remember=remember)
            flash(f'¡Bienvenido {user.nombre}!', 'success')
            
            # Redirigir según el rol
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            elif user.is_admin():
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('shop.catalog'))
        else:
            flash(message, 'danger')
    
    return render_template('auth/login.html')


@bp.route('/logout')
@login_required
def logout():
    """Logout de usuarios"""
    logout_user()
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('shop.catalog'))