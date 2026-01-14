from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from main import main_bp
from models import db, Distribuidora, Producto, Pedido, ItemPedido, EstadoPedido
from forms import DistribuidoraForm, ProductoForm, PedidoForm, ItemPedidoForm, CambiarEstadoPedidoForm, BusquedaForm
from decorators import vendedor_requerido, rol_permitido
from datetime import datetime
import uuid

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Estadísticas básicas
    total_distribuidoras = Distribuidora.query.filter_by(activa=True).count()
    total_productos = Producto.query.filter_by(activo=True).count()
    total_pedidos = Pedido.query.count()
    
    # Pedidos por estado
    pedidos_pendientes = Pedido.query.filter_by(estado=EstadoPedido.PENDIENTE).count()
    pedidos_enviados = Pedido.query.filter_by(estado=EstadoPedido.ENVIADO).count()
    pedidos_recibidos = Pedido.query.filter_by(estado=EstadoPedido.RECIBIDO).count()
    
    # Pedidos recientes
    pedidos_recientes = Pedido.query.order_by(Pedido.fecha_creacion.desc()).limit(5).all()
    
    return render_template('main/dashboard.html',
                         total_distribuidoras=total_distribuidoras,
                         total_productos=total_productos,
                         total_pedidos=total_pedidos,
                         pedidos_pendientes=pedidos_pendientes,
                         pedidos_enviados=pedidos_enviados,
                         pedidos_recibidos=pedidos_recibidos,
                         pedidos_recientes=pedidos_recientes)

# DISTRIBUIDORAS
@main_bp.route('/distribuidoras')
@login_required
@vendedor_requerido
def distribuidoras():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = Distribuidora.query.filter_by(activa=True)
    
    if search:
        query = query.filter(Distribuidora.nombre.contains(search) | 
                           Distribuidora.codigo.contains(search))
    
    distribuidoras = query.paginate(page=page, per_page=10, error_out=False)
    
    return render_template('distribuidoras/lista.html', 
                         distribuidoras=distribuidoras, 
                         search=search)

@main_bp.route('/distribuidoras/nueva', methods=['GET', 'POST'])
@login_required
@vendedor_requerido
def nueva_distribuidora():
    form = DistribuidoraForm()
    
    if form.validate_on_submit():
        # Verificar si el código ya existe
        if Distribuidora.query.filter_by(codigo=form.codigo.data).first():
            flash('El código de distribuidora ya existe', 'danger')
            return render_template('distribuidoras/formulario.html', form=form)
        
        distribuidora = Distribuidora(
            nombre=form.nombre.data,
            codigo=form.codigo.data,
            contacto=form.contacto.data,
            telefono=form.telefono.data,
            email=form.email.data,
            direccion=form.direccion.data,
            activa=form.activa.data
        )
        
        db.session.add(distribuidora)
        db.session.commit()
        
        flash('Distribuidora creada exitosamente', 'success')
        return redirect(url_for('main.distribuidoras'))
    
    return render_template('distribuidoras/formulario.html', form=form)

@main_bp.route('/distribuidoras/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@vendedor_requerido
def editar_distribuidora(id):
    distribuidora = Distribuidora.query.get_or_404(id)
    form = DistribuidoraForm(obj=distribuidora)
    
    if form.validate_on_submit():
        # Verificar si el código ya existe (excluyendo el actual)
        existente = Distribuidora.query.filter(Distribuidora.codigo == form.codigo.data, 
                                              Distribuidora.id != id).first()
        if existente:
            flash('El código de distribuidora ya existe', 'danger')
            return render_template('distribuidoras/formulario.html', form=form)
        
        form.populate_obj(distribuidora)
        db.session.commit()
        
        flash('Distribuidora actualizada exitosamente', 'success')
        return redirect(url_for('main.distribuidoras'))
    
    return render_template('distribuidoras/formulario.html', form=form, distribuidora=distribuidora)

# PRODUCTOS
@main_bp.route('/productos')
@login_required
@vendedor_requerido
def productos():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = Producto.query.filter_by(activo=True)
    
    if search:
        query = query.filter(Producto.nombre.contains(search) | 
                           Producto.codigo.contains(search))
    
    productos = query.paginate(page=page, per_page=10, error_out=False)
    
    return render_template('productos/lista.html', 
                         productos=productos, 
                         search=search)

@main_bp.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
@vendedor_requerido
def nuevo_producto():
    form = ProductoForm()
    
    if form.validate_on_submit():
        # Verificar si el código ya existe
        if Producto.query.filter_by(codigo=form.codigo.data).first():
            flash('El código de producto ya existe', 'danger')
            return render_template('productos/formulario.html', form=form)
        
        producto = Producto(
            nombre=form.nombre.data,
            codigo=form.codigo.data,
            precio=float(form.precio.data),
            stock=form.stock.data,
            descripcion=form.descripcion.data,
            activo=form.activo.data
        )
        
        db.session.add(producto)
        db.session.commit()
        
        flash('Producto creado exitosamente', 'success')
        return redirect(url_for('main.productos'))
    
    return render_template('productos/formulario.html', form=form)

@main_bp.route('/productos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@vendedor_requerido
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    form = ProductoForm(obj=producto)
    
    if form.validate_on_submit():
        # Verificar si el código ya existe (excluyendo el actual)
        existente = Producto.query.filter(Producto.codigo == form.codigo.data, 
                                         Producto.id != id).first()
        if existente:
            flash('El código de producto ya existe', 'danger')
            return render_template('productos/formulario.html', form=form)
        
        form.populate_obj(producto)
        db.session.commit()
        
        flash('Producto actualizado exitosamente', 'success')
        return redirect(url_for('main.productos'))
    
    return render_template('productos/formulario.html', form=form, producto=producto)

# PEDIDOS
@main_bp.route('/pedidos')
@login_required
@vendedor_requerido
def pedidos():
    page = request.args.get('page', 1, type=int)
    estado_filter = request.args.get('estado', '', type=str)
    distribuidora_filter = request.args.get('distribuidora', '', type=str)
    
    query = Pedido.query
    
    if estado_filter:
        query = query.filter(Pedido.estado == EstadoPedido(estado_filter))
    
    if distribuidora_filter:
        query = query.join(Distribuidora).filter(Distribuidora.nombre.contains(distribuidora_filter))
    
    # Si es vendedor, solo ver sus pedidos
    if current_user.is_vendedor():
        query = query.filter(Pedido.usuario_id == current_user.id)
    
    pedidos = query.order_by(Pedido.fecha_creacion.desc()).paginate(page=page, per_page=10, error_out=False)
    
    return render_template('pedidos/lista.html', 
                         pedidos=pedidos,
                         estado_filter=estado_filter,
                         distribuidora_filter=distribuidora_filter,
                         estados=EstadoPedido)

@main_bp.route('/pedidos/nuevo', methods=['GET', 'POST'])
@login_required
@vendedor_requerido
def nuevo_pedido():
    form = PedidoForm()
    form.distribuidora_id.choices = [(d.id, f"{d.nombre} ({d.codigo})") 
                                   for d in Distribuidora.query.filter_by(activa=True).all()]
    
    if form.validate_on_submit():
        # Generar ID único
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_uuid = str(uuid.uuid4())[:8].upper()
        id_pedido = f"PED-{timestamp}-{random_uuid}"
        
        pedido = Pedido(
            id_pedido=id_pedido,
            distribuidora_id=form.distribuidora_id.data,
            usuario_id=current_user.id,
            observaciones=form.observaciones.data
        )
        
        db.session.add(pedido)
        db.session.commit()
        
        flash(f'Pedido {id_pedido} creado exitosamente', 'success')
        return redirect(url_for('main.detalle_pedido', id=pedido.id))
    
    return render_template('pedidos/formulario.html', form=form)

@main_bp.route('/pedidos/<int:id>')
@login_required
@vendedor_requerido
def detalle_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    
    # Verificar permisos
    if current_user.is_vendedor() and pedido.usuario_id != current_user.id:
        flash('No tienes permisos para ver este pedido', 'danger')
        return redirect(url_for('main.pedidos'))
    
    form_item = ItemPedidoForm()
    form_item.producto_id.choices = [(p.id, f"{p.nombre} ({p.codigo}) - ${p.precio}") 
                                    for p in Producto.query.filter_by(activo=True).all()]
    
    form_estado = CambiarEstadoPedidoForm()
    
    return render_template('pedidos/detalle.html', 
                         pedido=pedido, 
                         form_item=form_item,
                         form_estado=form_estado)

@main_bp.route('/pedidos/<int:id>/agregar-item', methods=['POST'])
@login_required
@vendedor_requerido
def agregar_item_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    
    # Verificar permisos
    if current_user.is_vendedor() and pedido.usuario_id != current_user.id:
        flash('No tienes permisos para modificar este pedido', 'danger')
        return redirect(url_for('main.pedidos'))
    
    form = ItemPedidoForm()
    form.producto_id.choices = [(p.id, f"{p.nombre} ({p.codigo})") 
                               for p in Producto.query.filter_by(activo=True).all()]
    
    if form.validate_on_submit():
        producto = Producto.query.get(form.producto_id.data)
        
        item = ItemPedido(
            pedido_id=pedido.id,
            producto_id=producto.id,
            cantidad=form.cantidad.data,
            precio_unitario=float(form.precio_unitario.data)
        )
        
        db.session.add(item)
        db.session.commit()
        
        flash('Item agregado exitosamente', 'success')
    
    return redirect(url_for('main.detalle_pedido', id=id))

@main_bp.route('/pedidos/<int:id>/cambiar-estado', methods=['POST'])
@login_required
@vendedor_requerido
def cambiar_estado_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    
    # Verificar permisos
    if current_user.is_vendedor() and pedido.usuario_id != current_user.id:
        flash('No tienes permisos para modificar este pedido', 'danger')
        return redirect(url_for('main.pedidos'))
    
    form = CambiarEstadoPedidoForm()
    
    if form.validate_on_submit():
        pedido.estado = EstadoPedido(form.estado.data)
        
        if pedido.estado == EstadoPedido.RECIBIDO and not pedido.fecha_entrega:
            pedido.fecha_entrega = datetime.utcnow()
        
        db.session.commit()
        
        flash('Estado del pedido actualizado exitosamente', 'success')
    
    return redirect(url_for('main.detalle_pedido', id=id))

@main_bp.route('/pedidos/<int:id>/eliminar-item/<int:item_id>', methods=['POST'])
@login_required
@vendedor_requerido
def eliminar_item_pedido(id, item_id):
    pedido = Pedido.query.get_or_404(id)
    item = ItemPedido.query.get_or_404(item_id)
    
    # Verificar permisos
    if current_user.is_vendedor() and pedido.usuario_id != current_user.id:
        flash('No tienes permisos para modificar este pedido', 'danger')
        return redirect(url_for('main.pedidos'))
    
    if item.pedido_id != pedido.id:
        flash('Item no pertenece a este pedido', 'danger')
        return redirect(url_for('main.detalle_pedido', id=id))
    
    db.session.delete(item)
    db.session.commit()
    
    flash('Item eliminado exitosamente', 'success')
    return redirect(url_for('main.detalle_pedido', id=id))