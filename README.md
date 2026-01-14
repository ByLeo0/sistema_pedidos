# Sistema de Gestión de Pedidos - Versión Web

## 🚀 Características Principales

- **🌐 Interfaz Web Moderna**: Diseño responsivo con Bootstrap 5
- **👥 Sistema de Autenticación**: Login y gestión de usuarios con roles
- **🔐 Control de Acceso por Roles**: 
  - **Administrador**: Acceso completo a todas las funciones
  - **Vendedor**: Gestión limitada a productos, distribuidoras y pedidos
- **📊 Panel Administrativo**: Estadísticas y reportes en tiempo real
- **💾 Base de Datos SQLAlchemy**: Persistencia robusta de datos
- **🎨 Diseño Profesional**: Interfaz moderna con gradientes y animaciones

## 📋 Estructura del Proyecto

```
sistema_pedidos/
├── app.py                    # Aplicación principal Flask
├── models.py                 # Modelos de datos SQLAlchemy
├── forms.py                  # Formularios WTForms
├── decorators.py             # Decoradores de permisos
├── config/                   # Configuración de la aplicación
├── auth/                     # Módulo de autenticación
├── main/                     # Módulo principal (vendedor)
├── admin/                    # Módulo administrativo
├── templates/                # Plantillas HTML
│   ├── base.html            # Plantilla base
│   ├── auth/                # Login y registro
│   ├── main/                # Dashboard vendedor
│   ├── admin/               # Panel administrativo
│   ├── distribuidoras/      # Gestión de distribuidoras
│   ├── productos/          # Gestión de productos
│   └── pedidos/            # Gestión de pedidos
├── static/                  # Archivos estáticos
│   └── css/style.css       # Estilos personalizados
└── requirements.txt         # Dependencias
```

## 🔧 Instalación y Configuración

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar la Aplicación
```bash
python app.py
```

### 3. Acceder al Sistema
- **URL**: http://localhost:5000
- **Usuario Administrador**: admin / admin123
- **Usuario Vendedor**: (crear desde panel admin)

## 👤 Roles y Permisos

### 🛡️ Administrador
- ✅ Gestión completa de usuarios
- ✅ Acceso a panel administrativo
- ✅ Estadísticas y reportes
- ✅ Todas las funciones de vendedor
- ✅ Configuración del sistema

### 🏪 Vendedor
- ✅ Gestión de distribuidoras
- ✅ Gestión de productos
- ✅ Creación y gestión de pedidos
- ✅ Dashboard con estadísticas básicas
- ❌ No puede gestionar usuarios
- ❌ No accede al panel administrativo

## 🎯 Funcionalidades

### 📋 Gestión de Distribuidoras
- Registro de nuevas distribuidoras
- Edición de información existente
- Listado con búsqueda y paginación
- Control de estado (activa/inactiva)

### 📦 Gestión de Productos
- Registro de productos con precio y stock
- Actualización de inventario
- Búsqueda y filtrado
- Control de estado (activo/inactivo)

### 🛒 Gestión de Pedidos
- Creación de pedidos por distribuidora
- Agregado de items individualmente
- Cambio de estado (pendiente → enviado → recibido → cancelado)
- Detalles completos con totales
- Historial y seguimiento

### 👥 Gestión de Usuarios (Solo Admin)
- Registro de nuevos usuarios
- Asignación de roles
- Activación/desactivación
- Listado con estadísticas

### 📊 Dashboards y Reportes
- **Dashboard Vendedor**: Estadísticas de sus pedidos y productos
- **Dashboard Admin**: Estadísticas completas del sistema
- Gráficos y métricas en tiempo real
- Reportes por estado y período

## 🎨 Características de Diseño

- **Interfaz Moderna**: Bootstrap 5 con gradientes
- **Diseño Responsivo**: Adaptable a móviles y tablets
- **Sidebar Navegación**: Menú lateral intuitivo
- **Animaciones**: Transiciones suaves y efectos hover
- **Notificaciones**: Sistema de alertas y mensajes
- **Tablas Interactivas**: DataTables con búsqueda y paginación

## 🔒 Seguridad

- **Autenticación**: Login seguro con Flask-Login
- **Control de Acceso**: Decoradores por rol
- **Protección CSRF**: Formularios seguros con WTForms
- **Sesiones**: Gestión segura de sesiones de usuario
- **Validación**: Validación de datos en frontend y backend

## 📈 Estadísticas y Métricas

- Totales de distribuidoras, productos y pedidos
- Pedidos por estado
- Usuarios por rol
- Actividad reciente
- Gráficos visuales con progreso

## 🔄 Flujo de Trabajo

1. **Login**: Usuario inicia sesión según su rol
2. **Dashboard**: Vista principal con estadísticas
3. **Gestión**: Acceso a módulos según permisos
4. **Operaciones**: CRUD completo en cada módulo
5. **Reportes**: Visualización de datos y métricas

## 🚀 Extensiones Futuras

- 📧 Notificaciones por email
- 📄 Reportes PDF/Excel
- 🔄 Integración con APIs externas
- 📱 Aplicación móvil
- 🌐 Multi-idioma
- 💳 Pagos online
- 📦 Control de inventario avanzado

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask 2.3.3
- **Base de Datos**: SQLAlchemy + SQLite
- **Frontend**: Bootstrap 5 + jQuery
- **Autenticación**: Flask-Login
- **Formularios**: Flask-WTF + WTForms
- **Tablas**: DataTables
- **Iconos**: Font Awesome

## 📞 Soporte

El sistema incluye documentación en línea y mensajes de ayuda para guiar al usuario en cada proceso.