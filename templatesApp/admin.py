from django.contrib import admin
from .models import Trabajador, Rol, Bus, EstadoBus, AsignacionRol, AsignacionBus


@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'edad', 'contacto', 'activo')
    list_filter = ('activo', 'edad')
    search_fields = ('nombre', 'apellido', 'contacto')
    ordering = ('apellido', 'nombre')
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'edad')
        }),
        ('Contacto', {
            'fields': ('contacto', 'direccion')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )
    
    readonly_fields = ()


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nivel_acceso', 'activo')
    list_filter = ('activo', 'nivel_acceso')
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)
    
    fieldsets = (
        ('Información del Rol', {
            'fields': ('nombre', 'descripcion', 'nivel_acceso')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('patente', 'marca', 'modelo', 'año', 'capacidad', 'activo')
    list_filter = ('activo', 'año', 'marca')
    search_fields = ('patente', 'modelo', 'marca')
    ordering = ('patente',)
    
    fieldsets = (
        ('Identificación', {
            'fields': ('patente', 'marca', 'modelo')
        }),
        ('Especificaciones', {
            'fields': ('año', 'capacidad')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )


@admin.register(EstadoBus)
class EstadoBusAdmin(admin.ModelAdmin):
    list_display = ('bus_patente', 'bus_modelo', 'estado', 'kilometraje', 'fecha_cambio')
    list_filter = ('estado', 'fecha_cambio')
    search_fields = ('bus_patente', 'bus_modelo')
    ordering = ('-fecha_cambio',)
    
    fieldsets = (
        ('Identificación del Bus', {
            'fields': ('bus_patente', 'bus_modelo')
        }),
        ('Estado Actual', {
            'fields': ('estado', 'observaciones', 'kilometraje')
        }),
        ('Información Temporal', {
            'fields': ('fecha_cambio',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('fecha_cambio',)


@admin.register(AsignacionRol)
class AsignacionRolAdmin(admin.ModelAdmin):
    list_display = ('trabajador_nombre', 'trabajador_apellido', 'rol_nombre', 'fecha_asignacion', 'activo')
    list_filter = ('activo', 'fecha_asignacion')
    search_fields = ('trabajador_nombre', 'trabajador_apellido', 'rol_nombre')
    ordering = ('-fecha_asignacion',)
    
    fieldsets = (
        ('Trabajador', {
            'fields': ('trabajador_id', 'trabajador_nombre', 'trabajador_apellido')
        }),
        ('Rol Asignado', {
            'fields': ('rol_id', 'rol_nombre')
        }),
        ('Fechas', {
            'fields': ('fecha_asignacion', 'fecha_finalizacion')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )
    
    readonly_fields = ('fecha_asignacion',)


@admin.register(AsignacionBus)
class AsignacionBusAdmin(admin.ModelAdmin):
    list_display = ('trabajador_nombre', 'bus_patente', 'turno', 'fecha_asignacion', 'activo')
    list_filter = ('activo', 'turno', 'fecha_asignacion')
    search_fields = ('trabajador_nombre', 'trabajador_apellido', 'bus_patente')
    ordering = ('-fecha_asignacion',)
    
    fieldsets = (
        ('Trabajador', {
            'fields': ('trabajador_id', 'trabajador_nombre', 'trabajador_apellido')
        }),
        ('Bus Asignado', {
            'fields': ('bus_id', 'bus_patente', 'bus_modelo')
        }),
        ('Turno', {
            'fields': ('turno',)
        }),
        ('Fechas', {
            'fields': ('fecha_asignacion', 'fecha_finalizacion')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )
    
    readonly_fields = ('fecha_asignacion',)