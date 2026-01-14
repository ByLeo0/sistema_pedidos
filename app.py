from flask import Flask
from flask_login import LoginManager
from config import config
from models import db, User, Rol
import os

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Configurar Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Debes iniciar sesión para acceder a esta página.'
    login_manager.login_message_category = 'warning'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Registrar blueprints
    from auth import auth_bp
    from main import main_bp
    from admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    # Crear tablas de la base de datos
    with app.app_context():
        db.create_all()
        
        # Crear usuario administrador por defecto si no existe
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@sistema.com',
                nombre='Administrador del Sistema',
                rol=Rol.ADMINISTRADOR
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("Usuario administrador creado: admin / admin123")
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Iniciando aplicación Flask...")
    print("📡 El servidor estará disponible en: http://localhost:5000")
    print("👤 Usuario admin: admin / admin123")
    print("="*50)
    app.run(debug=True, host='127.0.0.1', port=5000, threaded=True)