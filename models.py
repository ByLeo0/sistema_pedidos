from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

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
    ultimo_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_administrador(self):
        return self.rol == Rol.ADMINISTRADOR
    
    def is_vendedor(self):
        return self.rol == Rol.VENDEDOR
    
    def __repr__(self):
        return f'<User {self.username}>'

class EstadoPedido(Enum):
    PENDIENTE = "pendiente"
    ENVIADO = "enviado"
    RECIBIDO = "recibido"
    CANCELADO = "cancelado"

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
    
    pedidos = db.relationship('Pedido', backref='distribuidora', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Distribuidora {self.nombre}>'

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
    
    items_pedido = db.relationship('ItemPedido', backref='producto', lazy=True)
    
    def __repr__(self):
        return f'<Producto {self.nombre}>'

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.String(50), unique=True, nullable=False)
    distribuidora_id = db.Column(db.Integer, db.ForeignKey('distribuidoras.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_entrega = db.Column(db.DateTime)
    estado = db.Column(db.Enum(EstadoPedido), default=EstadoPedido.PENDIENTE)
    observaciones = db.Column(db.Text)
    
    items = db.relationship('ItemPedido', backref='pedido', lazy=True, cascade='all, delete-orphan')
    usuario = db.relationship('User', backref='pedidos_creados')
    
    @property
    def total(self):
        return sum(item.subtotal for item in self.items)
    
    @property
    def total_items(self):
        return sum(item.cantidad for item in self.items)
    
    def __repr__(self):
        return f'<Pedido {self.id_pedido}>'

class ItemPedido(db.Model):
    __tablename__ = 'items_pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    
    @property
    def subtotal(self):
        return float(self.cantidad * self.precio_unitario)
    
    def __repr__(self):
        return f'<ItemPedido {self.producto.nombre} x{self.cantidad}>'