from django.contrib import admin
from django.utils.html import format_html
from .models import Trabajador, Rol, Bus, EstadoBus, AsignacionRol, AsignacionBus


@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'edad', 'contacto', 'estado_badge', 'fecha_registro')
    list_filter = ('activo', 'edad', 'fecha_registro')
    search_fields = ('nombre', 'apellido', 'contacto', 'direccion')
    ordering = ('apellido', 'nombre')
    date_hierarchy = 'fecha_registro'
    list_per_page = 20
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'edad'),
            'description': 'Datos personales del trabajador'
        }),
        ('Contacto', {
            'fields': ('contacto', 'direccion'),
            'classes': ('wide',)
        }),
        ('Estado', {
            'fields': ('activo',),
            'description': 'Marque si el trabajador está activo en el sistema'
        }),
        ('Información del Sistema', {
            'fields': ('fecha_registro',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('fecha_registro',)
    
    actions = ['activar_trabajadores', 'desactivar_trabajadores']
    
    def nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido}"
    nombre_completo.short_description = 'Nombre Completo'
    nombre_completo.admin_order_field = 'apellido'
    
    def estado_badge(self, obj):
        if obj.activo:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">Activo</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 3px;">Inactivo</span>'
        )
    estado_badge.short_description = 'Estado'
    
    def activar_trabajadores(self, request, queryset):
        updated = queryset.update(activo=True)
        self.message_user(request, f'{updated} trabajadores activados exitosamente.')
    activar_trabajadores.short_description = 'Activar trabajadores seleccionados'
    
    def desactivar_trabajadores(self, request, queryset):
        updated = queryset.update(activo=False)
        self.message_user(request, f'{updated} trabajadores desactivados exitosamente.')
    desactivar_trabajadores.short_description = 'Desactivar trabajadores seleccionados'


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nivel_acceso', 'estado_badge', 'cantidad_asignaciones', 'fecha_creacion')
    list_filter = ('activo', 'nivel_acceso', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)
    date_hierarchy = 'fecha_creacion'
    list_per_page = 20
    
    fieldsets = (
        ('Información del Rol', {
            'fields': ('nombre', 'descripcion', 'nivel_acceso'),
            'description': 'Defina el rol y su nivel de acceso'
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Información del Sistema', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('fecha_creacion',)
    
    actions = ['activar_roles', 'desactivar_roles']
    
    def estado_badge(self, obj):
        if obj.activo:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">Activo</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 3px;">Inactivo</span>'
        )
    estado_badge.short_description = 'Estado'
    
    def cantidad_asignaciones(self, obj):
        count = obj.cantidad_asignaciones_activas()
        return format_html(
            '<span style="background-color: #007bff; color: white; padding: 3px 8px; border-radius: 50%;">{}</span>',
            count
        )
    cantidad_asignaciones.short_description = 'Asignaciones Activas'
    
    def activar_roles(self, request, queryset):
        updated = queryset.update(activo=True)
        self.message_user(request, f'{updated} roles activados exitosamente.')
    activar_roles.short_description = 'Activar roles seleccionados'
    
    def desactivar_roles(self, request, queryset):
        updated = queryset.update(activo=False)
        self.message_user(request, f'{updated} roles desactivados exitosamente.')
    desactivar_roles.short_description = 'Desactivar roles seleccionados'


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('patente', 'marca', 'modelo', 'año', 'capacidad', 'estado_badge', 'fecha_registro')
    list_filter = ('activo', 'año', 'marca', 'fecha_registro')
    search_fields = ('patente', 'modelo', 'marca')
    ordering = ('patente',)
    date_hierarchy = 'fecha_registro'
    list_per_page = 20
    
    fieldsets = (
        ('Identificación', {
            'fields': ('patente', 'marca', 'modelo'),
            'description': 'Información de identificación del bus'
        }),
        ('Especificaciones', {
            'fields': ('año', 'capacidad'),
            'classes': ('wide',)
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Información del Sistema', {
            'fields': ('fecha_registro',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('fecha_registro',)
    
    actions = ['activar_buses', 'desactivar_buses']
    
    def estado_badge(self, obj):
        if obj.activo:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">Activo</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 3px;">Inactivo</span>'
        )
    estado_badge.short_description = 'Estado'
    
    def activar_buses(self, request, queryset):
        updated = queryset.update(activo=True)
        self.message_user(request, f'{updated} buses activados exitosamente.')
    activar_buses.short_description = 'Activar buses seleccionados'
    
    def desactivar_buses(self, request, queryset):
        updated = queryset.update(activo=False)
        self.message_user(request, f'{updated} buses desactivados exitosamente.')
    desactivar_buses.short_description = 'Desactivar buses seleccionados'


@admin.register(EstadoBus)
class EstadoBusAdmin(admin.ModelAdmin):
    list_display = ('bus', 'estado_badge', 'kilometraje', 'fecha_cambio')
    list_filter = ('estado', 'fecha_cambio')
    search_fields = ('bus__patente', 'bus__modelo', 'observaciones')
    ordering = ('-fecha_cambio',)
    date_hierarchy = 'fecha_cambio'
    list_per_page = 20
    
    autocomplete_fields = ['bus']
    
    fieldsets = (
        ('Bus', {
            'fields': ('bus',),
            'description': 'Seleccione el bus al que desea asignar un estado'
        }),
        ('Estado Actual', {
            'fields': ('estado', 'observaciones', 'kilometraje'),
            'classes': ('wide',)
        }),
        ('Información Temporal', {
            'fields': ('fecha_cambio',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('fecha_cambio',)
    
    def estado_badge(self, obj):
        colores = {
            'OPERATIVO': '#28a745',
            'MANTENIMIENTO': '#ffc107',
            'REPARACION': '#fd7e14',
            'FUERA_SERVICIO': '#dc3545',
            'RESERVADO': '#17a2b8',
        }
        color = colores.get(obj.estado, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'


@admin.register(AsignacionRol)
class AsignacionRolAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'rol', 'fecha_asignacion', 'fecha_finalizacion', 'estado_badge')
    list_filter = ('activo', 'fecha_asignacion', 'fecha_finalizacion')
    search_fields = ('trabajador__nombre', 'trabajador__apellido', 'rol__nombre')
    ordering = ('-fecha_asignacion',)
    date_hierarchy = 'fecha_asignacion'
    list_per_page = 20
    
    autocomplete_fields = ['trabajador', 'rol']
    
    fieldsets = (
        ('Asignación', {
            'fields': ('trabajador', 'rol'),
            'description': 'Seleccione el trabajador y el rol a asignar'
        }),
        ('Fechas', {
            'fields': ('fecha_asignacion', 'fecha_finalizacion'),
            'classes': ('wide',)
        }),
        ('Estado y Notas', {
            'fields': ('activo', 'notas')
        }),
    )
    
    readonly_fields = ('fecha_asignacion',)
    
    actions = ['activar_asignaciones', 'desactivar_asignaciones', 'finalizar_asignaciones']
    
    def estado_badge(self, obj):
        if obj.activo:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">Activa</span>'
            )
        return format_html(
            '<span style="background-color: #6c757d; color: white; padding: 3px 10px; border-radius: 3px;">Finalizada</span>'
        )
    estado_badge.short_description = 'Estado'
    
    def activar_asignaciones(self, request, queryset):
        updated = queryset.update(activo=True)
        self.message_user(request, f'{updated} asignaciones activadas exitosamente.')
    activar_asignaciones.short_description = 'Activar asignaciones seleccionadas'
    
    def desactivar_asignaciones(self, request, queryset):
        updated = queryset.update(activo=False)
        self.message_user(request, f'{updated} asignaciones desactivadas exitosamente.')
    desactivar_asignaciones.short_description = 'Desactivar asignaciones seleccionadas'
    
    def finalizar_asignaciones(self, request, queryset):
        from django.utils import timezone
        count = 0
        for obj in queryset.filter(activo=True):
            obj.finalizar_asignacion()
            count += 1
        self.message_user(request, f'{count} asignaciones finalizadas exitosamente.')
    finalizar_asignaciones.short_description = 'Finalizar asignaciones seleccionadas'


@admin.register(AsignacionBus)
class AsignacionBusAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'bus', 'turno', 'fecha_asignacion', 'fecha_finalizacion', 'estado_badge')
    list_filter = ('activo', 'turno', 'fecha_asignacion', 'fecha_finalizacion')
    search_fields = ('trabajador__nombre', 'trabajador__apellido', 'bus__patente')
    ordering = ('-fecha_asignacion',)
    date_hierarchy = 'fecha_asignacion'
    list_per_page = 20
    
    autocomplete_fields = ['trabajador', 'bus']
    
    fieldsets = (
        ('Asignación', {
            'fields': ('trabajador', 'bus', 'turno'),
            'description': 'Seleccione el trabajador, bus y turno'
        }),
        ('Fechas', {
            'fields': ('fecha_asignacion', 'fecha_finalizacion'),
            'classes': ('wide',)
        }),
        ('Estado y Notas', {
            'fields': ('activo', 'notas')
        }),
    )
    
    readonly_fields = ('fecha_asignacion',)
    
    actions = ['activar_asignaciones', 'desactivar_asignaciones', 'finalizar_asignaciones']
    
    def estado_badge(self, obj):
        if obj.activo:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">Activa</span>'
            )
        return format_html(
            '<span style="background-color: #6c757d; color: white; padding: 3px 10px; border-radius: 3px;">Finalizada</span>'
        )
    estado_badge.short_description = 'Estado'
    
    def activar_asignaciones(self, request, queryset):
        updated = queryset.update(activo=True)
        self.message_user(request, f'{updated} asignaciones activadas exitosamente.')
    activar_asignaciones.short_description = 'Activar asignaciones seleccionadas'
    
    def desactivar_asignaciones(self, request, queryset):
        updated = queryset.update(activo=False)
        self.message_user(request, f'{updated} asignaciones desactivadas exitosamente.')
    desactivar_asignaciones.short_description = 'Desactivar asignaciones seleccionadas'
    
    def finalizar_asignaciones(self, request, queryset):
        from django.utils import timezone
        count = 0
        for obj in queryset.filter(activo=True):
            obj.finalizar_asignacion()
            count += 1
        self.message_user(request, f'{count} asignaciones finalizadas exitosamente.')
    finalizar_asignaciones.short_description = 'Finalizar asignaciones seleccionadas'


# Configuración del sitio de administración
admin.site.site_header = 'Administración de Sistema de Buses'
admin.site.site_title = 'Admin Buses'
admin.site.index_title = 'Panel de Administración'