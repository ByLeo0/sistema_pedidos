# Sistema de Pedidos - Versión Visual Studio Code

## 🚀 **Instrucciones para VS Code**

### 1. **Abrir el proyecto en VS Code**
```bash
cd /d/sistema_pedidos
code .
```

### 2. **Ejecutar el servidor**
En la terminal de VS Code, ejecuta:
```bash
python vscode_app.py
```

### 3. **Acceder al sistema**
- **URL**: http://localhost:5000
- **Usuario Administrador**: `admin` / `admin123`
- **Usuario Vendedor**: `vendedor` / `vendedor123`

## 🌟 **Características de esta versión**

### ✨ **Interfaz Web Completa**
- 🎨 Diseño moderno con Bootstrap 5
- 📱 Totalmente responsivo
- 🌈 Gradientes y animaciones
- 📊 Dashboard interactivo

### 👥 **Sistema de Roles**
- 🛡️ **Administrador**: Acceso completo
- 🏪 **Vendedor**: Gestión limitada
- 🔐 Control de acceso por permisos

### 📋 **Módulos Implementados**
- **Dashboard**: Estadísticas en tiempo real
- **Distribuidoras**: Listado y gestión
- **Productos**: Catálogo con stock
- **Pedidos**: Sistema completo de pedidos
- **Usuarios**: Gestión (solo admin)

### 🎯 **Funcionalidades Web**
- ✅ Login seguro con sesión
- ✅ Navegación con tabs
- ✅ Tablas interactivas
- ✅ Badges de estado
- ✅ Acciones rápidas
- ✅ Diseño profesional

## 💡 **Ventajas de esta versión**

1. **🔥 Servidor estable**: No se detiene inesperadamente
2. **🎯 Todo en un archivo**: Fácil de gestionar
3. **📱 Diseño responsivo**: Funciona en móviles
4. **🔐 Roles funcionales**: Permiso por tipo de usuario
5. **📊 Dashboard real**: Estadísticas dinámicas
6. **🎨 Interfaz moderna**: Bootstrap 5 + gradientes

## 🔄 **Flujo de trabajo en VS Code**

1. **Abrir terminal**: Ctrl + ` (o View → Terminal)
2. **Navegar al proyecto**: `cd sistema_pedidos`
3. **Ejecutar servidor**: `python vscode_app.py`
4. **Ver mensaje**: "🚀 Iniciando servidor web..."
5. **Abrir navegador**: http://localhost:5000
6. **Iniciar sesión**: con los usuarios de prueba

## 📱 **Acceso Móvil**

El sistema es totalmente responsivo, puedes acceder desde:
- 📱 Teléfono móvil
- 💻 Tablet
- 🖥️ Computadora

## 🎮 **Probando el sistema**

### Como Administrador (admin/admin123):
- ✅ Ver dashboard completo
- ✅ Gestionar usuarios
- ✅ Todas las funciones de vendedor
- ✅ Acceso a todos los módulos

### Como Vendedor (vendedor/vendedor123):
- ✅ Ver dashboard limitado
- ✅ Gestionar distribuidoras
- ✅ Gestionar productos
- ✅ Gestionar pedidos
- ❌ No puede gestionar usuarios

## 🔧 **Si tienes problemas**

1. **Verificar que el puerto 5000 esté libre**
2. **Instalar Flask**: `pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF`
3. **Verificar que estás en el directorio correcto**
4. **Ejecutar con Python 3.7+**

## 🎉 **¡Listo para usar!**

El sistema está completamente funcional con:
- Base de datos SQLite integrada
- Datos de ejemplo precargados
- Interfaz web moderna
- Sistema de autenticación
- Control de roles
- Dashboard interactivo

¡Simplemente ejecuta `python vscode_app.py` y comienza a usar!