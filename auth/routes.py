from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from auth import auth_bp
from models import db, User, Rol
from forms import LoginForm, RegistroForm
from decorators import administrador_requerido

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data) and user.activo:
            login_user(user, remember=form.remember_me.data)
            from datetime import datetime
            user.ultimo_login = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            if user.is_administrador():
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('main.dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/registro', methods=['GET', 'POST'])
@login_required
@administrador_requerido
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        # Verificar si el usuario ya existe
        if User.query.filter_by(username=form.username.data).first():
            flash('El usuario ya existe', 'danger')
            return render_template('auth/registro.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('El email ya está registrado', 'danger')
            return render_template('auth/registro.html', form=form)
        
        # Crear nuevo usuario
        user = User(
            username=form.username.data,
            email=form.email.data,
            nombre=form.nombre.data,
            rol=Rol(form.rol.data)
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Usuario {form.username.data} creado exitosamente', 'success')
        return redirect(url_for('admin.usuarios'))
    
    return render_template('auth/registro.html', form=form)