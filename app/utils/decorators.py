"""
Decoradores personalizados para proteger rutas.
"""

from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(f):
    """
    Decorador para restringir acceso solo a administradores.
    Debe usarse después de @login_required.
    
    Usage:
        @app.route('/admin')
        @login_required
        @admin_required
        def admin_panel():
            return 'Admin panel'
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Debes iniciar sesión para acceder.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_admin():
            flash('No tienes permisos para acceder a esta página.', 'danger')
            return redirect(url_for('shop.catalog'))
        
        return f(*args, **kwargs)
    return decorated_function


def logout_required(f):
    """
    Decorador para restringir acceso solo a usuarios NO autenticados.
    Útil para páginas de login/registro.
    
    Usage:
        @app.route('/login')
        @logout_required
        def login():
            return 'Login page'
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash('Ya has iniciado sesión.', 'info')
            return redirect(url_for('shop.catalog'))
        
        return f(*args, **kwargs)
    return decorated_function