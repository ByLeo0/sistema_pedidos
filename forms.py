from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, IntegerField, DecimalField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional
from models import Rol, EstadoPedido

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class RegistroForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    nombre = StringField('Nombre Completo', validators=[DataRequired(), Length(min=2, max=100)])
    rol = SelectField('Rol', choices=[(r.value, r.value.title()) for r in Rol], validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

class DistribuidoraForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    codigo = StringField('Código', validators=[DataRequired(), Length(min=2, max=20)])
    contacto = StringField('Contacto', validators=[DataRequired(), Length(min=2, max=100)])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    direccion = TextAreaField('Dirección', validators=[Optional()])
    activa = BooleanField('Activa')
    submit = SubmitField('Guardar')

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    codigo = StringField('Código', validators=[DataRequired(), Length(min=2, max=20)])
    precio = DecimalField('Precio', validators=[DataRequired(), NumberRange(min=0)], places=2)
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    descripcion = TextAreaField('Descripción', validators=[Optional()])
    activo = BooleanField('Activo')
    submit = SubmitField('Guardar')

class PedidoForm(FlaskForm):
    distribuidora_id = SelectField('Distribuidora', coerce=int, validators=[DataRequired()])
    observaciones = TextAreaField('Observaciones', validators=[Optional()])
    submit = SubmitField('Crear Pedido')

class ItemPedidoForm(FlaskForm):
    producto_id = SelectField('Producto', coerce=int, validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1)])
    precio_unitario = DecimalField('Precio Unitario', validators=[DataRequired(), NumberRange(min=0)], places=2)
    submit = SubmitField('Agregar Item')

class CambiarEstadoPedidoForm(FlaskForm):
    estado = SelectField('Estado', choices=[(e.value, e.value.title()) for e in EstadoPedido], validators=[DataRequired()])
    submit = SubmitField('Cambiar Estado')

class BusquedaForm(FlaskForm):
    termino = StringField('Buscar', validators=[Optional()])
    submit = SubmitField('Buscar')