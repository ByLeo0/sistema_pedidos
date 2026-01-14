from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from admin import admin_bp
from models import db, User, Distribuidora, Producto, Pedido, Rol, EstadoPedido
from forms import RegistroForm, DistribuidoraForm, ProductoForm
from decorators import administrador_requerido

@admin_bp.route('/dashboard')
@login_required
@administrador_requerido
def dashboard():
    # Estadísticas completas
    total_usuarios = User.query.count()
    total_distribuidoras = Distribuidora.query.count()
    total_productos = Producto.query.count()
    total_pedidos = Pedido.query.count()
    
    # Usuarios por rol
    admin_count = User.query.filter_by(rol=Rol.ADMINISTRADOR).count()
    vendedor_count = User.query.filter_by(rol=Rol.VENDEDOR).count()
    
    # Pedidos por estado
    pedidos_por_estado = {}
    for estado in EstadoPedido:
        pedidos_por_estado[estado.value] = Pedido.query.filter_by(estado=estado).count()
    
    # Usuarios recientes
    usuarios_recientes = User.query.order_by(User.fecha_creacion.desc()).limit(5).all()
    
    # Pedidos recientes
    pedidos_recientes = Pedido.query.order_by(Pedido.fecha_creacion.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_usuarios=total_usuarios,
                         total_distribuidoras=total_distribuidoras,
                         total_productos=total_productos,
                         total_pedidos=total_pedidos,
                         admin_count=admin_count,
                         vendedor_count=vendedor_count,
                         pedidos_por_estado=pedidos_por_estado,
                         usuarios_recientes=usuarios_recientes,
                         pedidos_recientes=pedidos_recientes)

@admin_bp.route('/usuarios')
@login_required
@administrador_requerido
def usuarios():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = User.query
    
    if search:
        query = query.filter(User.username.contains(search) | 
                           User.nombre.contains(search) |
                           User.email.contains(search))
    
    usuarios = query.order_by(User.fecha_creacion.desc()).paginate(page=page, per_page=10, error_out=False)
    
    return render_template('admin/usuarios.html', usuarios=usuarios, search=search)

@admin_bp.route('/usuarios/<int:id>/toggle-activo', methods=['POST'])
@login_required
@administrador_requerido
def toggle_usuario_activo(id):
    usuario = User.query.get_or_404(id)
    
    # No permitir desactivar al propio usuario
    if usuario.id == current_user.id:
        flash('No puedes desactivar tu propio usuario', 'danger')
        return redirect(url_for('admin.usuarios'))
    
    usuario.activo = not usuario.activo
    db.session.commit()
    
    estado = 'activado' if usuario.activo else 'desactivado'
    flash(f'Usuario {estado} exitosamente', 'success')
    return redirect(url_for('admin.usuarios'))

@admin_bp.route('/sistema')
@login_required
@administrador_requerido
def sistema():
    # Información del sistema
    return render_template('admin/sistema.html')