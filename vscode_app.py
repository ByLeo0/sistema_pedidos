from flask import Flask, render_template_string, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from enum import Enum
import os

# Configuración
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sistema-pedidos-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sistema_pedidos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Enumeraciones
class Rol(Enum):
    ADMINISTRADOR = "administrador"
    VENDEDOR = "vendedor"

class EstadoPedido(Enum):
    PENDIENTE = "pendiente"
    ENVIADO = "enviado"
    RECIBIDO = "recibido"
    CANCELADO = "cancelado"

# Modelos
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum(Rol), nullable=False, default=Rol.VENDEDOR)
    nombre = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_administrador(self):
        return self.rol == Rol.ADMINISTRADOR
    
    def is_vendedor(self):
        return self.rol == Rol.VENDEDOR

class Distribuidora(db.Model):
    __tablename__ = 'distribuidoras'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    contacto = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    direccion = db.Column(db.Text)
    activa = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.String(50), unique=True, nullable=False)
    distribuidora_id = db.Column(db.Integer, db.ForeignKey('distribuidoras.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.Enum(EstadoPedido), default=EstadoPedido.PENDIENTE)
    observaciones = db.Column(db.Text)
    
    distribuidora = db.relationship('Distribuidora', backref='pedidos')
    usuario = db.relationship('User', backref='pedidos_creados')

# Login Manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)

# Plantillas base
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Sistema de Pedidos{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .main-container { background: white; border-radius: 1rem; box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin: 20px auto; max-width: 1200px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 1rem 1rem 0 0; }
        .nav-tabs .nav-link { color: #667eea; font-weight: 500; }
        .nav-tabs .nav-link.active { background: #667eea; color: white; border-color: #667eea; }
        .card { border: none; border-radius: 0.5rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none; }
        .stats-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .table thead th { background: #f8f9fa; border-bottom: 2px solid #667eea; }
        .badge { font-weight: 500; padding: 0.5em 1em; }
    </style>
</head>
<body>
    <div class="main-container">
        {% if current_user.is_authenticated %}
        <div class="header">
            <div class="container-fluid">
                <div class="row align-items-center">
                    <div class="col">
                        <h1><i class="fas fa-box"></i> Sistema de Pedidos</h1>
                        <p class="mb-0">Bienvenido, {{ current_user.nombre }} | 
                        <span class="badge bg-light text-dark">{{ current_user.rol.value.title() }}</span></p>
                    </div>
                    <div class="col-auto">
                        <a href="/logout" class="btn btn-light">
                            <i class="fas fa-sign-out-alt"></i> Salir
                        </a>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="container-fluid p-4">
            <!-- Navegación -->
            <ul class="nav nav-tabs mb-4">
                <li class="nav-item">
                    <a class="nav-link {% if request.endpoint == 'dashboard' %}active{% endif %}" href="/">
                        <i class="fas fa-tachometer-alt"></i> Dashboard
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link {% if request.endpoint == 'distribuidoras' %}active{% endif %}" href="/distribuidoras">
                        <i class="fas fa-truck"></i> Distribuidoras
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link {% if request.endpoint == 'productos' %}active{% endif %}" href="/productos">
                        <i class="fas fa-boxes"></i> Productos
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link {% if request.endpoint == 'pedidos' %}active{% endif %}" href="/pedidos">
                        <i class="fas fa-shopping-cart"></i> Pedidos
                    </a>
                </li>
                {% if current_user.is_administrador() %}
                <li class="nav-item">
                    <a class="nav-link {% if request.endpoint == 'usuarios' %}active{% endif %}" href="/usuarios">
                        <i class="fas fa-users"></i> Usuarios
                    </a>
                </li>
                {% endif %}
            </ul>
        {% endif %}
        
        <!-- Contenido -->
        {% block content %}{% endblock %}
        
        {% if current_user.is_authenticated %}
        </div>
        {% endif %}
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
'''

# Rutas
@app.route('/')
def dashboard():
    if not current_user.is_authenticated:
        return redirect('/login')
    
    stats = {
        'distribuidoras': Distribuidora.query.count(),
        'productos': Producto.query.count(),
        'pedidos': Pedido.query.count(),
        'pedidos_pendientes': Pedido.query.filter_by(estado=EstadoPedido.PENDIENTE).count()
    }
    
    return render_template_string(BASE_TEMPLATE, 
        title='Dashboard',
        content='''
        <div class="row g-4">
            <div class="col-md-3">
                <div class="card stats-card">
                    <div class="card-body text-center">
                        <i class="fas fa-truck fa-2x mb-3"></i>
                        <h3>''' + str(stats['distribuidoras']) + '''</h3>
                        <p>Distribuidoras</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stats-card">
                    <div class="card-body text-center">
                        <i class="fas fa-boxes fa-2x mb-3"></i>
                        <h3>''' + str(stats['productos']) + '''</h3>
                        <p>Productos</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stats-card">
                    <div class="card-body text-center">
                        <i class="fas fa-shopping-cart fa-2x mb-3"></i>
                        <h3>''' + str(stats['pedidos']) + '''</h3>
                        <p>Pedidos</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stats-card">
                    <div class="card-body text-center">
                        <i class="fas fa-clock fa-2x mb-3"></i>
                        <h3>''' + str(stats['pedidos_pendientes']) + '''</h3>
                        <p>Pendientes</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row mt-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-bolt"></i> Acciones Rápidas</h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-3 mb-2">
                                <a href="/distribuidoras/nueva" class="btn btn-primary w-100">
                                    <i class="fas fa-plus"></i> Nueva Distribuidora
                                </a>
                            </div>
                            <div class="col-md-3 mb-2">
                                <a href="/productos/nuevo" class="btn btn-primary w-100">
                                    <i class="fas fa-plus"></i> Nuevo Producto
                                </a>
                            </div>
                            <div class="col-md-3 mb-2">
                                <a href="/pedidos/nuevo" class="btn btn-primary w-100">
                                    <i class="fas fa-plus"></i> Nuevo Pedido
                                </a>
                            </div>
                            {% if current_user.is_administrador() %}
                            <div class="col-md-3 mb-2">
                                <a href="/usuarios/nuevo" class="btn btn-success w-100">
                                    <i class="fas fa-user-plus"></i> Nuevo Usuario
                                </a>
                            </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        '''
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password) and user.activo:
            login_user(user)
            return redirect('/')
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template_string(BASE_TEMPLATE,
        title='Login',
        content='''
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header text-center">
                        <h3><i class="fas fa-sign-in-alt"></i> Iniciar Sesión</h3>
                    </div>
                    <div class="card-body">
                        <form method="POST">
                            <div class="mb-3">
                                <label class="form-label">Usuario</label>
                                <input type="text" name="username" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Contraseña</label>
                                <input type="password" name="password" class="form-control" required>
                            </div>
                            <button type="submit" class="btn btn-primary w-100">
                                <i class="fas fa-sign-in-alt"></i> Iniciar Sesión
                            </button>
                        </form>
                        
                        <div class="mt-3 text-center">
                            <small class="text-muted">
                                <strong>Admin:</strong> admin / admin123<br>
                                <strong>Vendedor:</strong> vendedor / vendedor123
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        '''
    )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/distribuidoras')
@login_required
def distribuidoras():
    distribuidoras = Distribuidora.query.all()
    
    content = '''
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2><i class="fas fa-truck"></i> Distribuidoras</h2>
        <a href="/distribuidoras/nueva" class="btn btn-primary">
            <i class="fas fa-plus"></i> Nueva Distribuidora
        </a>
    </div>
    
    <div class="card">
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Código</th>
                            <th>Nombre</th>
                            <th>Contacto</th>
                            <th>Teléfono</th>
                            <th>Email</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>
    '''
    
    for d in distribuidoras:
        content += f'''
            <tr>
                <td><strong>{d.codigo}</strong></td>
                <td>{d.nombre}</td>
                <td>{d.contacto}</td>
                <td>{d.telefono}</td>
                <td>{d.email}</td>
                <td>
                    <span class="badge bg-{'success' if d.activa else 'secondary'}">
                        {'Activa' if d.activa else 'Inactiva'}
                    </span>
                </td>
            </tr>
        '''
    
    content += '''
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    '''
    
    return render_template_string(BASE_TEMPLATE, title='Distribuidoras', content=content)

@app.route('/productos')
@login_required
def productos():
    productos = Producto.query.all()
    
    content = '''
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2><i class="fas fa-boxes"></i> Productos</h2>
        <a href="/productos/nuevo" class="btn btn-primary">
            <i class="fas fa-plus"></i> Nuevo Producto
        </a>
    </div>
    
    <div class="card">
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Código</th>
                            <th>Nombre</th>
                            <th>Precio</th>
                            <th>Stock</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>
    '''
    
    for p in productos:
        stock_color = 'success' if p.stock > 10 else 'warning' if p.stock > 0 else 'danger'
        content += f'''
            <tr>
                <td><strong>{p.codigo}</strong></td>
                <td>{p.nombre}</td>
                <td>${float(p.precio):.2f}</td>
                <td>
                    <span class="badge bg-{stock_color}">
                        {p.stock} unidades
                    </span>
                </td>
                <td>
                    <span class="badge bg-{'success' if p.activo else 'secondary'}">
                        {'Activo' if p.activo else 'Inactivo'}
                    </span>
                </td>
            </tr>
        '''
    
    content += '''
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    '''
    
    return render_template_string(BASE_TEMPLATE, title='Productos', content=content)

@app.route('/pedidos')
@login_required
def pedidos():
    pedidos = Pedido.query.order_by(Pedido.fecha_creacion.desc()).all()
    
    content = '''
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2><i class="fas fa-shopping-cart"></i> Pedidos</h2>
        <a href="/pedidos/nuevo" class="btn btn-primary">
            <i class="fas fa-plus"></i> Nuevo Pedido
        </a>
    </div>
    
    <div class="card">
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>ID Pedido</th>
                            <th>Distribuidora</th>
                            <th>Estado</th>
                            <th>Fecha</th>
                            <th>Usuario</th>
                        </tr>
                    </thead>
                    <tbody>
    '''
    
    for p in pedidos:
        estado_colors = {
            'pendiente': 'warning',
            'enviado': 'info',
            'recibido': 'success',
            'cancelado': 'danger'
        }
        color = estado_colors.get(p.estado.value, 'secondary')
        
        content += f'''
            <tr>
                <td><strong>{p.id_pedido}</strong></td>
                <td>{p.distribuidora.nombre if p.distribuidora else 'N/A'}</td>
                <td>
                    <span class="badge bg-{color}">
                        {p.estado.value.title()}
                    </span>
                </td>
                <td>{p.fecha_creacion.strftime('%d/%m/%Y %H:%M')}</td>
                <td>{p.usuario.nombre if p.usuario else 'N/A'}</td>
            </tr>
        '''
    
    content += '''
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    '''
    
    return render_template_string(BASE_TEMPLATE, title='Pedidos', content=content)

@app.route('/usuarios')
@login_required
def usuarios():
    if not current_user.is_administrador():
        return redirect('/')
    
    usuarios = User.query.all()
    
    content = '''
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2><i class="fas fa-users"></i> Usuarios</h2>
        <a href="/usuarios/nuevo" class="btn btn-success">
            <i class="fas fa-user-plus"></i> Nuevo Usuario
        </a>
    </div>
    
    <div class="card">
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Usuario</th>
                            <th>Nombre</th>
                            <th>Email</th>
                            <th>Rol</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>
    '''
    
    for u in usuarios:
        rol_color = 'primary' if u.is_administrador() else 'info'
        content += f'''
            <tr>
                <td><strong>{u.username}</strong></td>
                <td>{u.nombre}</td>
                <td>{u.email}</td>
                <td>
                    <span class="badge bg-{rol_color}">
                        {u.rol.value.title()}
                    </span>
                </td>
                <td>
                    <span class="badge bg-{'success' if u.activo else 'secondary'}">
                        {'Activo' if u.activo else 'Inactivo'}
                    </span>
                </td>
            </tr>
        '''
    
    content += '''
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    '''
    
    return render_template_string(BASE_TEMPLATE, title='Usuarios', content=content)

# Rutas de formularios (placeholders para desarrollo)
@app.route('/distribuidoras/nueva')
@login_required
def nueva_distribuidora():
    return render_template_string(BASE_TEMPLATE,
        title='Nueva Distribuidora',
        content='''
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h4><i class="fas fa-truck"></i> Nueva Distribuidora</h4>
                    </div>
                    <div class="card-body">
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle"></i> 
                            Formulario de registro de distribuidora en desarrollo.
                        </div>
                        <a href="/distribuidoras" class="btn btn-secondary">
                            <i class="fas fa-arrow-left"></i> Volver
                        </a>
                    </div>
                </div>
            </div>
        </div>
        '''
    )

@app.route('/productos/nuevo')
@login_required
def nuevo_producto():
    return render_template_string(BASE_TEMPLATE,
        title='Nuevo Producto',
        content='''
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h4><i class="fas fa-box"></i> Nuevo Producto</h4>
                    </div>
                    <div class="card-body">
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle"></i> 
                            Formulario de registro de producto en desarrollo.
                        </div>
                        <a href="/productos" class="btn btn-secondary">
                            <i class="fas fa-arrow-left"></i> Volver
                        </a>
                    </div>
                </div>
            </div>
        </div>
        '''
    )

@app.route('/pedidos/nuevo')
@login_required
def nuevo_pedido():
    return render_template_string(BASE_TEMPLATE,
        title='Nuevo Pedido',
        content='''
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h4><i class="fas fa-shopping-cart"></i> Nuevo Pedido</h4>
                    </div>
                    <div class="card-body">
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle"></i> 
                            Formulario de creación de pedido en desarrollo.
                        </div>
                        <a href="/pedidos" class="btn btn-secondary">
                            <i class="fas fa-arrow-left"></i> Volver
                        </a>
                    </div>
                </div>
            </div>
        </div>
        '''
    )

@app.route('/usuarios/nuevo')
@login_required
def nuevo_usuario():
    if not current_user.is_administrador():
        return redirect('/')
    
    return render_template_string(BASE_TEMPLATE,
        title='Nuevo Usuario',
        content='''
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h4><i class="fas fa-user-plus"></i> Nuevo Usuario</h4>
                    </div>
                    <div class="card-body">
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle"></i> 
                            Formulario de registro de usuario en desarrollo.
                        </div>
                        <a href="/usuarios" class="btn btn-secondary">
                            <i class="fas fa-arrow-left"></i> Volver
                        </a>
                    </div>
                </div>
            </div>
        </div>
        '''
    )

# Inicialización
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Crear usuarios por defecto
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@sistema.com',
                nombre='Administrador del Sistema',
                rol=Rol.ADMINISTRADOR
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        vendedor = User.query.filter_by(username='vendedor').first()
        if not vendedor:
            vendedor = User(
                username='vendedor',
                email='vendedor@sistema.com',
                nombre='Vendedor Ejemplo',
                rol=Rol.VENDEDOR
            )
            vendedor.set_password('vendedor123')
            db.session.add(vendedor)
        
        # Crear datos de ejemplo
        if Distribuidora.query.count() == 0:
            dist1 = Distribuidora(
                nombre='Distribuidora Central',
                codigo='DIST001',
                contacto='Juan Pérez',
                telefono='555-0123',
                email='juan@distcentral.com'
            )
            dist2 = Distribuidora(
                nombre='Productos del Norte',
                codigo='DIST002',
                contacto='María García',
                telefono='555-0456',
                email='maria@prodnorte.com'
            )
            db.session.add(dist1)
            db.session.add(dist2)
        
        if Producto.query.count() == 0:
            prod1 = Producto(nombre='Laptop Pro 15"', codigo='LP001', precio=999.99, stock=25)
            prod2 = Producto(nombre='Mouse Wireless', codigo='MS001', precio=29.99, stock=150)
            prod3 = Producto(nombre='Teclado Mecánico', codigo='KB001', precio=79.99, stock=75)
            db.session.add(prod1)
            db.session.add(prod2)
            db.session.add(prod3)
        
        db.session.commit()
        print("✅ Base de datos inicializada")
        print("👤 Admin: admin / admin123")
        print("👤 Vendedor: vendedor / vendedor123")
    
    print("🚀 Iniciando servidor web...")
    print("📡 URL: http://localhost:5000")
    print("="*50)
    
    # Ejecutar servidor en un modo más estable
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)