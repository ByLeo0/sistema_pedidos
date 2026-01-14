#!/usr/bin/env python
# -*- coding: utf-8 -*-

print("Iniciando diagnóstico...")

try:
    print("1. Importando Flask...")
    from flask import Flask
    print("   ✓ Flask importado")
    
    print("2. Importando extensiones...")
    from flask_login import LoginManager
    from flask_sqlalchemy import SQLAlchemy
    print("   ✓ Extensiones importadas")
    
    print("3. Importando modelos...")
    from models import db, User, Rol
    print("   ✓ Modelos importados")
    
    print("4. Importando configuración...")
    from config import config
    print("   ✓ Configuración importada")
    
    print("5. Creando aplicación...")
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    print("6. Inicializando extensiones...")
    db.init_app(app)
    print("   ✓ Base de datos inicializada")
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    print("   ✓ Login Manager inicializado")
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    print("7. Creando ruta de prueba...")
    @app.route('/')
    def index():
        return '<h1>¡Funciona!</h1><a href="/login">Login</a>'
    
    @app.route('/login')
    def login():
        return '<h1>Login</h1>'
    
    print("8. Iniciando servidor...")
    print("   URL: http://127.0.0.1:5000")
    print("   Presiona CTRL+C para detener")
    
    app.run(host='127.0.0.1', port=5000, debug=True)
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()