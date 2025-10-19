# Gestión de Transporte - Sistema de Administración de Buses

## Descripción
Aplicación Django para la gestión integral de empresas de transporte, incluyendo administración de trabajadores, roles, buses, asignaciones de roles y asignaciones de buses a conductores.

## Características Principales
- **Gestión de Trabajadores**: Crear, editar, eliminar y listar trabajadores con validaciones
- **Gestión de Roles**: Asignar roles con niveles de acceso
- **Gestión de Buses**: Registro de buses con capacidad y especificaciones
- **Estado de Buses**: Seguimiento del estado operativo de cada bus
- **Asignaciones de Roles**: Vincular trabajadores con roles específicos
- **Asignaciones de Buses**: Asignar buses a conductores por turno
- **Búsqueda y Filtros**: En todos los listados
- **Paginación**: Listados con paginación de 10 registros por página
- **Panel de Administración Django**: Interfaz completa para gestionar datos

## Tecnologías Utilizadas
- **Python 3.8+**
- **Django 5.2.6**
- **MySQL 8.0+**
- **Bootstrap 5** (para estilos)

## Requisitos Previos
- Python 3.8 o superior
- MySQL Server instalado y ejecutándose
- pip (gestor de paquetes de Python)

## Instalación

### 1. Clonar el repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd projectoFrontEnd
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos MySQL
Editar `projectoFrontEnd/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'projectoFrontEnd',
        'USER': 'root',
        'PASSWORD': 'tu_contraseña',  # Cambiar
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5. Ejecutar migraciones
```bash
python manage.py migrate
```

### 6. Crear superusuario (admin)
```bash
python manage.py createsuperuser
```
Ingresa:
- Username: `admin`
- Email: `admin@example.com`
- Password: tu contraseña

### 7. Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

La aplicación estará disponible en: `http://127.0.0.1:8000`

## Uso

### Acceder a la Aplicación
- **Sitio Principal**: `http://127.0.0.1:8000/`
- **Panel Admin**: `http://127.0.0.1:8000/admin/`

### Operaciones CRUD

#### Trabajadores
- Listar: `/trabajadores/`
- Crear: `/trabajadores/crear/`
- Editar: `/trabajadores/<id>/editar/`
- Eliminar: `/trabajadores/<id>/eliminar/`

#### Roles
- Listar: `/roles/`
- Crear: `/roles/crear/`
- Editar: `/roles/<id>/editar/`
- Eliminar: `/roles/<id>/eliminar/`

#### Buses
- Listar: `/buses/`
- Crear: `/buses/crear/`
- Editar: `/buses/<id>/editar/`
- Eliminar: `/buses/<id>/eliminar/`

#### Estados de Buses
- Listar: `/estados-bus/`
- Crear: `/estados-bus/crear/`
- Editar: `/estados-bus/<id>/editar/`

#### Asignaciones de Roles
- Listar: `/asignaciones-rol/`
- Crear: `/asignaciones-rol/crear/`

#### Asignaciones de Buses
- Listar: `/asignaciones-bus/`
- Crear: `/asignaciones-bus/crear/`

## Validaciones Implementadas

### Trabajador
- Nombre y apellido: solo letras, mínimo 2 caracteres
- Edad: entre 18 y 70 años
- Contacto: formato de teléfono válido (8-15 dígitos)
- El nombre y apellido no pueden ser iguales

### Rol
- Nombre: único, solo letras, mínimo 3 caracteres
- Nivel de acceso: 1-5
- Descripción: máximo 500 caracteres

### Bus
- Patente: formato válido (ABC-123)
- Año: entre 1990 y año actual
- Capacidad: entre 10 y 80 pasajeros
- Validación: buses anteriores a 2000 no pueden tener capacidad > 60

### EstadoBus
- Kilometraje: no negativo, máximo 2,000,000 km
- Estados en mantenimiento requieren observaciones (mínimo 10 caracteres)

## Estructura del Proyecto

```
projectoFrontEnd/
├── projectoFrontEnd/
│   ├── settings.py          # Configuración de Django
│   ├── urls.py              # URLs principales
│   ├── wsgi.py
│   └── asgi.py
├── templatesApp/
│   ├── models.py            # Modelos de datos
│   ├── views.py             # Vistas
│   ├── forms.py             # Formularios
│   ├── admin.py             # Configuración Admin
│   ├── urls.py              # URLs de la app
│   └── migrations/          # Migraciones de BD
├── templates/               # Templates HTML
├── static/
│   └── css/
│       └── index.css        # Estilos
├── manage.py
├── requirements.txt         # Dependencias
└── README.md
```

## Funcionalidades Destacadas

### Búsqueda y Filtros
Todos los listados incluyen:
- Campo de búsqueda por nombre/patente/contacto
- Filtros por estado (activo/inactivo)
- Filtros adicionales por turno (en asignaciones)

### Paginación
- 10 registros por página
- Navegación entre páginas
- Información del total de registros

### Validaciones
- A nivel de modelo (validators de Django)
- A nivel de formulario (métodos clean())
- A nivel de vista (manejo de excepciones)

### Seguridad
- Token CSRF en todos los formularios
- Protección contra acceso no autorizado
- Validación de datos en formularios

## Desarrollo

### Ejecutar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### Acceder a la shell interactiva
```bash
python manage.py shell
```

### Crear datos de prueba
```python
from templatesApp.models import Trabajador, Rol
# Crear trabajador
t = Trabajador.objects.create(nombre="Juan", apellido="Pérez", edad=30, contacto="+56912345678", direccion="Calle 123")
# Crear rol
r = Rol.objects.create(nombre="Conductor", descripcion="Operador de bus", nivel_acceso=2)
```

## Troubleshooting

### Error de conexión a MySQL
```bash
# Verificar que MySQL esté corriendo
# En Windows: Services
# En Linux: sudo systemctl status mysql
# Cambiar credenciales en settings.py
```

### Migraciones con error
```bash
# Eliminar migraciones problemáticas y reintentar
python manage.py migrate templatesApp zero
python manage.py makemigrations
python manage.py migrate
```

### Puerto 8000 en uso
```bash
python manage.py runserver 8001
```

## Notas de Desarrollo

- Sin relaciones ForeignKey: todos los datos relacionales se almacenan como campos de texto/números
- Validaciones personalizadas en formularios
- Sistema de mensajes Django para feedback del usuario
- Interfaz Admin completamente configurada con filtros y búsqueda

## Autor
[Tu nombre]

## Licencia
MIT License