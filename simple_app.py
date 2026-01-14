from flask import Flask, render_template_string, redirect, url_for
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from enum import Enum

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sistema_pedidos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class Rol(Enum):
    ADMINISTRADOR = "administrador"
    VENDEDOR = "vendedor"

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
    
    def __repr__(self):
        return f'<User {self.username}>'

class Distribuidora(db.Model):
    __tablename__ = 'distribuidoras'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    contacto = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    activa = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Distribuidora {self.nombre}>'

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    activo = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Producto {self.nombre}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return '''
    <h1>¡SISTEMA DE GESTIÓN DE PEDIDOS WEB!</h1>
    <h2>🎉 Funcionando correctamente</h2>
    <p>Esta es una versión simplificada para demostrar que funciona.</p>
    
    <h3>👤 Usuarios de prueba:</h3>
    <ul>
        <li><strong>Administrador:</strong> admin / admin123</li>
    </ul>
    
    <h3>🔗 Enlaces:</h3>
    <ul>
        <li><a href="/login">Iniciar Sesión</a></li>
        <li><a href="/distribuidoras">Ver Distribuidoras</a></li>
        <li><a href="/productos">Ver Productos</a></li>
    </ul>
    
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        h1 { color: #667eea; }
        h2 { color: #28a745; }
        h3 { color: #17a2b8; }
        ul { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        li { margin: 5px 0; }
        a { color: #667eea; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
    '''

@app.route('/login')
def login():
    return '''
    <h1>🔐 Iniciar Sesión</h1>
    <form method="post" action="/do_login">
        <p>
            <label>Usuario:</label><br>
            <input type="text" name="username" required><br>
            <small>Prueba con: <strong>admin</strong></small>
        </p>
        <p>
            <label>Contraseña:</label><br>
            <input type="password" name="password" required><br>
            <small>Prueba con: <strong>admin123</strong></small>
        </p>
        <button type="submit" style="background: #667eea; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">Iniciar Sesión</button>
    </form>
    <p><a href="/">← Volver al inicio</a></p>
    
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        h1 { color: #667eea; }
        input { width: 200px; padding: 8px; margin: 5px 0; border: 1px solid #ddd; border-radius: 4px; }
        label { font-weight: bold; }
        form { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 300px; }
    </style>
    '''

@app.route('/do_login', methods=['POST'])
def do_login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == 'admin' and password == 'admin123':
        return '''
        <h1>✅ ¡Inicio de sesión exitoso!</h1>
        <p>Bienvenido al Sistema de Gestión de Pedidos</p>
        <h3>🎯 Características implementadas:</h3>
        <ul>
            <li>✅ Servidor Flask funcionando</li>
            <li>✅ Base de datos SQLAlchemy configurada</li>
            <li>✅ Sistema de login básico</li>
            <li>✅ Estructura de modelos creada</li>
        </ul>
        <h3>📋 Próximos pasos:</h3>
        <ul>
            <li>Implementar gestión completa de usuarios</li>
            <li>Agregar gestión de distribuidoras</li>
            <li>Agregar gestión de productos</li>
            <li>Implementar sistema de pedidos</li>
        </ul>
        <p><a href="/">← Volver al inicio</a></p>
        '''
    else:
        return '''
        <h1>❌ Error de autenticación</h1>
        <p>Usuario o contraseña incorrectos.</p>
        <p><a href="/login">← Intentar nuevamente</a></p>
        '''

@app.route('/distribuidoras')
def distribuidoras():
    return '''
    <h1>🚚 Gestión de Distribuidoras</h1>
    <p>Este módulo permitirá gestionar las distribuidoras del sistema.</p>
    <div style="background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3>📋 Funcionalidades a implementar:</h3>
        <ul>
            <li>➕ Registro de nuevas distribuidoras</li>
            <li>📝 Edición de información</li>
            <li>🔍 Búsqueda y filtrado</li>
            <li>📊 Listado con paginación</li>
        </ul>
    </div>
    <p><a href="/">← Volver al inicio</a></p>
    '''

@app.route('/productos')
def productos():
    return '''
    <h1>📦 Gestión de Productos</h1>
    <p>Este módulo permitirá gestionar el catálogo de productos.</p>
    <div style="background: #f3e5f5; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3>📋 Funcionalidades a implementar:</h3>
        <ul>
            <li>➕ Registro de nuevos productos</li>
            <li>💰 Gestión de precios y stock</li>
            <li>🏷️ Códigos y descripciones</li>
            <li>📈 Control de inventario</li>
        </ul>
    </div>
    <p><a href="/">← Volver al inicio</a></p>
    '''

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Crear usuario administrador
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
            db.session.commit()
            print("✅ Usuario administrador creado: admin / admin123")
        
        # Crear datos de ejemplo
        if Distribuidora.query.count() == 0:
            dist1 = Distribuidora(nombre='Distribuidora Central', codigo='DIST001', contacto='Juan Pérez', telefono='555-0123', email='juan@distcentral.com')
            dist2 = Distribuidora(nombre='Productos del Norte', codigo='DIST002', contacto='María García', telefono='555-0456', email='maria@prodnorte.com')
            db.session.add(dist1)
            db.session.add(dist2)
            db.session.commit()
            print("✅ Distribuidoras de ejemplo creadas")
        
        if Producto.query.count() == 0:
            prod1 = Producto(nombre='Laptop Pro 15"', codigo='LP001', precio=999.99, stock=25)
            prod2 = Producto(nombre='Mouse Wireless', codigo='MS001', precio=29.99, stock=150)
            prod3 = Producto(nombre='Teclado Mecánico', codigo='KB001', precio=79.99, stock=75)
            db.session.add(prod1)
            db.session.add(prod2)
            db.session.add(prod3)
            db.session.commit()
            print("✅ Productos de ejemplo creados")
    
    print("🚀 Iniciando aplicación Flask...")
    print("📡 URL: http://localhost:5000")
    print("👤 Usuario: admin / admin123")
    print("="*50)
    app.run(debug=True, host='127.0.0.1', port=5000, threaded=True)