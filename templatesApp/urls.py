from django.urls import path
from . import views

urlpatterns = [
    # Vista principal
    path('', views.index, name='index'),
    path('login/', views.login1, name='login'),
    
    # CRUD Trabajadores
    path('trabajadores/', views.trabajadores_list, name='trabajadores_list'),
    path('trabajadores/<int:pk>/', views.trabajador_detalle, name='trabajador_detalle'),
    path('trabajadores/crear/', views.trabajador_crear, name='trabajador_crear'),
    path('trabajadores/<int:pk>/editar/', views.trabajador_editar, name='trabajador_editar'),
    path('trabajadores/<int:pk>/eliminar/', views.trabajador_eliminar, name='trabajador_eliminar'),
    
    # CRUD Roles
    path('roles/', views.roles_list, name='roles_list'),
    path('roles/<int:pk>/', views.rol_detalle, name='rol_detalle'),
    path('roles/crear/', views.rol_crear, name='rol_crear'),
    path('roles/<int:pk>/editar/', views.rol_editar, name='rol_editar'),
    path('roles/<int:pk>/eliminar/', views.rol_eliminar, name='rol_eliminar'),
    
    # CRUD Buses
    path('buses/', views.buses_list, name='buses_list'),
    path('buses/<int:pk>/', views.bus_detalle, name='bus_detalle'),
    path('buses/crear/', views.bus_crear, name='bus_crear'),
    path('buses/<int:pk>/editar/', views.bus_editar, name='bus_editar'),
    path('buses/<int:pk>/eliminar/', views.bus_eliminar, name='bus_eliminar'),
    
    # CRUD Estado Bus
    path('estados-bus/', views.estados_bus_list, name='estados_bus_list'),
    path('estados-bus/<int:pk>/', views.estado_bus_detalle, name='estado_bus_detalle'),
    path('estados-bus/crear/', views.estado_bus_crear, name='estado_bus_crear'),
    path('estados-bus/<int:pk>/editar/', views.estado_bus_editar, name='estado_bus_editar'),
    path('estados-bus/<int:pk>/eliminar/', views.estado_bus_eliminar, name='estado_bus_eliminar'),
    
    # CRUD Asignación Rol
    path('asignaciones-rol/', views.asignaciones_rol_list, name='asignaciones_rol_list'),
    path('asignaciones-rol/<int:pk>/', views.asignacion_rol_detalle, name='asignacion_rol_detalle'),
    path('asignaciones-rol/crear/', views.asignacion_rol_crear, name='asignacion_rol_crear'),
    path('asignaciones-rol/<int:pk>/editar/', views.asignacion_rol_editar, name='asignacion_rol_editar'),
    path('asignaciones-rol/<int:pk>/eliminar/', views.asignacion_rol_eliminar, name='asignacion_rol_eliminar'),
    
    # CRUD Asignación Bus
    path('asignaciones-bus/', views.asignaciones_bus_list, name='asignaciones_bus_list'),
    path('asignaciones-bus/<int:pk>/', views.asignacion_bus_detalle, name='asignacion_bus_detalle'),
    path('asignaciones-bus/crear/', views.asignacion_bus_crear, name='asignacion_bus_crear'),
    path('asignaciones-bus/<int:pk>/editar/', views.asignacion_bus_editar, name='asignacion_bus_editar'),
    path('asignaciones-bus/<int:pk>/eliminar/', views.asignacion_bus_eliminar, name='asignacion_bus_eliminar'),
]