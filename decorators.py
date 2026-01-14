from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def rol_requerido(rol):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Debes iniciar sesión para acceder a esta página.', 'warning')
                return redirect(url_for('auth.login'))
            
            if current_user.rol.value != rol:
                flash('No tienes permisos para acceder a esta página.', 'danger')
                return redirect(url_for('main.dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def administrador_requerido(f):
    return rol_requerido('administrador')(f)

def vendedor_requerido(f):
    return rol_requerido('vendedor')(f)

def rol_permitido(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Debes iniciar sesión para acceder a esta página.', 'warning')
                return redirect(url_for('auth.login'))
            
            if current_user.rol.value not in roles:
                flash('No tienes permisos para acceder a esta página.', 'danger')
                return redirect(url_for('main.dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator