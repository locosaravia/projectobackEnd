# templatesApp/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Trabajador, Rol, Bus, EstadoBus, AsignacionRol, AsignacionBus
from .forms import (
    TrabajadorForm, RolForm, BusForm, EstadoBusForm, 
    AsignacionRolForm, AsignacionBusForm
)

# ==================== VISTAS GENERALES ====================

def index(request):
    # Dashboard con estadísticas
    context = {
        'total_trabajadores': Trabajador.objects.filter(activo=True).count(),
        'total_buses': Bus.objects.filter(activo=True).count(),
        'total_roles': Rol.objects.filter(activo=True).count(),
        'buses_operativos': EstadoBus.objects.filter(estado='OPERATIVO').count(),
        'asignaciones_activas': AsignacionBus.objects.filter(activo=True).count(),
    }
    return render(request, 'templatesApp/index.html', context)

def login1(request):
    return render(request, 'templatesApp/login.html')


# ==================== CRUD TRABAJADORES ====================

def trabajadores_list(request):
    # Búsqueda
    search_query = request.GET.get('search', '')
    trabajadores_data = Trabajador.objects.all()
    
    if search_query:
        trabajadores_data = trabajadores_data.filter(
            Q(nombre__icontains=search_query) |
            Q(apellido__icontains=search_query) |
            Q(contacto__icontains=search_query)
        )
    
    # Filtro por activo/inactivo
    estado_filter = request.GET.get('estado', '')
    if estado_filter == 'activo':
        trabajadores_data = trabajadores_data.filter(activo=True)
    elif estado_filter == 'inactivo':
        trabajadores_data = trabajadores_data.filter(activo=False)
    
    # Ordenamiento
    trabajadores_data = trabajadores_data.order_by('apellido', 'nombre')
    
    # Paginación
    paginator = Paginator(trabajadores_data, 10)  # 10 por página
    page = request.GET.get('page')
    
    try:
        trabajadores = paginator.page(page)
    except PageNotAnInteger:
        trabajadores = paginator.page(1)
    except EmptyPage:
        trabajadores = paginator.page(paginator.num_pages)
    
    context = {
        'trabajadores': trabajadores,
        'search_query': search_query,
        'estado_filter': estado_filter,
    }
    return render(request, 'templatesApp/trabajadores.html', context)


def trabajador_detalle(request, pk):
    trabajador = get_object_or_404(Trabajador, pk=pk)
    # Obtener asignaciones del trabajador
    asignaciones_rol = AsignacionRol.objects.filter(trabajador_id=pk)
    asignaciones_bus = AsignacionBus.objects.filter(trabajador_id=pk)
    
    context = {
        'trabajador': trabajador,
        'asignaciones_rol': asignaciones_rol,
        'asignaciones_bus': asignaciones_bus,
    }
    return render(request, 'templatesApp/trabajador_detalle.html', context)


def trabajador_crear(request):
    if request.method == 'POST':
        form = TrabajadorForm(request.POST)
        if form.is_valid():
            trabajador = form.save()
            messages.success(request, f'Trabajador {trabajador.nombre} {trabajador.apellido} creado exitosamente.')
            return redirect('trabajadores_list')
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = TrabajadorForm()
    
    return render(request, 'templatesApp/trabajador_form.html', {'form': form, 'accion': 'Crear'})


def trabajador_editar(request, pk):
    trabajador = get_object_or_404(Trabajador, pk=pk)
    
    if request.method == 'POST':
        form = TrabajadorForm(request.POST, instance=trabajador)
        if form.is_valid():
            trabajador = form.save()
            messages.success(request, f'Trabajador {trabajador.nombre} {trabajador.apellido} actualizado exitosamente.')
            return redirect('trabajador_detalle', pk=trabajador.pk)
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = TrabajadorForm(instance=trabajador)
    
    return render(request, 'templatesApp/trabajador_form.html', {
        'form': form, 
        'accion': 'Editar',
        'trabajador': trabajador
    })


def trabajador_eliminar(request, pk):
    trabajador = get_object_or_404(Trabajador, pk=pk)
    
    if request.method == 'POST':
        nombre_completo = f"{trabajador.nombre} {trabajador.apellido}"
        trabajador.delete()
        messages.success(request, f'Trabajador {nombre_completo} eliminado exitosamente.')
        return redirect('trabajadores_list')
    
    return render(request, 'templatesApp/trabajador_confirm_delete.html', {'trabajador': trabajador})


# ==================== CRUD ROLES ====================

def roles_list(request):
    search_query = request.GET.get('search', '')
    roles_data = Rol.objects.all()
    
    if search_query:
        roles_data = roles_data.filter(nombre__icontains=search_query)
    
    estado_filter = request.GET.get('estado', '')
    if estado_filter == 'activo':
        roles_data = roles_data.filter(activo=True)
    elif estado_filter == 'inactivo':
        roles_data = roles_data.filter(activo=False)
    
    roles_data = roles_data.order_by('nombre')
    
    paginator = Paginator(roles_data, 10)
    page = request.GET.get('page')
    
    try:
        roles = paginator.page(page)
    except PageNotAnInteger:
        roles = paginator.page(1)
    except EmptyPage:
        roles = paginator.page(paginator.num_pages)
    
    context = {
        'roles': roles,
        'search_query': search_query,
        'estado_filter': estado_filter,
    }
    return render(request, 'templatesApp/roles.html', context)


def rol_detalle(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    asignaciones = AsignacionRol.objects.filter(rol_id=pk)
    
    context = {
        'rol': rol,
        'asignaciones': asignaciones,
    }
    return render(request, 'templatesApp/rol_detalle.html', context)


def rol_crear(request):
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            rol = form.save()
            messages.success(request, f'Rol "{rol.nombre}" creado exitosamente.')
            return redirect('roles_list')
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = RolForm()
    
    return render(request, 'templatesApp/rol_form.html', {'form': form, 'accion': 'Crear'})


def rol_editar(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    
    if request.method == 'POST':
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            rol = form.save()
            messages.success(request, f'Rol "{rol.nombre}" actualizado exitosamente.')
            return redirect('rol_detalle', pk=rol.pk)
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = RolForm(instance=rol)
    
    return render(request, 'templatesApp/rol_form.html', {
        'form': form, 
        'accion': 'Editar',
        'rol': rol
    })


def rol_eliminar(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    
    if request.method == 'POST':
        nombre = rol.nombre
        rol.delete()
        messages.success(request, f'Rol "{nombre}" eliminado exitosamente.')
        return redirect('roles_list')
    
    return render(request, 'templatesApp/rol_confirm_delete.html', {'rol': rol})


# ==================== CRUD BUSES ====================

def buses_list(request):
    search_query = request.GET.get('search', '')
    buses_data = Bus.objects.all()
    
    if search_query:
        buses_data = buses_data.filter(
            Q(patente__icontains=search_query) |
            Q(modelo__icontains=search_query) |
            Q(marca__icontains=search_query)
        )
    
    estado_filter = request.GET.get('estado', '')
    if estado_filter == 'activo':
        buses_data = buses_data.filter(activo=True)
    elif estado_filter == 'inactivo':
        buses_data = buses_data.filter(activo=False)
    
    buses_data = buses_data.order_by('patente')
    
    paginator = Paginator(buses_data, 10)
    page = request.GET.get('page')
    
    try:
        buses = paginator.page(page)
    except PageNotAnInteger:
        buses = paginator.page(1)
    except EmptyPage:
        buses = paginator.page(paginator.num_pages)
    
    context = {
        'buses': buses,
        'search_query': search_query,
        'estado_filter': estado_filter,
    }
    return render(request, 'templatesApp/buses.html', context)


def bus_detalle(request, pk):
    bus = get_object_or_404(Bus, pk=pk)
    try:
        estado = EstadoBus.objects.get(bus_patente=bus.patente)
    except EstadoBus.DoesNotExist:
        estado = None
    
    asignaciones = AsignacionBus.objects.filter(bus_id=pk)
    
    context = {
        'bus': bus,
        'estado': estado,
        'asignaciones': asignaciones,
    }
    return render(request, 'templatesApp/bus_detalle.html', context)


def bus_crear(request):
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            bus = form.save()
            messages.success(request, f'Bus {bus.patente} creado exitosamente.')
            return redirect('buses_list')
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = BusForm()
    
    return render(request, 'templatesApp/bus_form.html', {'form': form, 'accion': 'Crear'})


def bus_editar(request, pk):
    bus = get_object_or_404(Bus, pk=pk)
    
    if request.method == 'POST':
        form = BusForm(request.POST, instance=bus)
        if form.is_valid():
            bus = form.save()
            messages.success(request, f'Bus {bus.patente} actualizado exitosamente.')
            return redirect('bus_detalle', pk=bus.pk)
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = BusForm(instance=bus)
    
    return render(request, 'templatesApp/bus_form.html', {
        'form': form, 
        'accion': 'Editar',
        'bus': bus
    })


def bus_eliminar(request, pk):
    bus = get_object_or_404(Bus, pk=pk)
    
    if request.method == 'POST':
        patente = bus.patente
        bus.delete()
        messages.success(request, f'Bus {patente} eliminado exitosamente.')
        return redirect('buses_list')
    
    return render(request, 'templatesApp/bus_confirm_delete.html', {'bus': bus})


# ==================== CRUD ESTADO BUS ====================

def estados_bus_list(request):
    search_query = request.GET.get('search', '')
    estados_data = EstadoBus.objects.all()
    
    if search_query:
        estados_data = estados_data.filter(
            Q(bus_patente__icontains=search_query) |
            Q(bus_modelo__icontains=search_query)
        )
    
    estado_filter = request.GET.get('estado', '')
    if estado_filter:
        estados_data = estados_data.filter(estado=estado_filter)
    
    estados_data = estados_data.order_by('-fecha_cambio')
    
    paginator = Paginator(estados_data, 10)
    page = request.GET.get('page')
    
    try:
        estados = paginator.page(page)
    except PageNotAnInteger:
        estados = paginator.page(1)
    except EmptyPage:
        estados = paginator.page(paginator.num_pages)
    
    context = {
        'estados': estados,
        'search_query': search_query,
        'estado_filter': estado_filter,
    }
    return render(request, 'templatesApp/estados_bus.html', context)


def estado_bus_detalle(request, pk):
    estado = get_object_or_404(EstadoBus, pk=pk)
    return render(request, 'templatesApp/estado_bus_detalle.html', {'estado': estado})


def estado_bus_crear(request):
    if request.method == 'POST':
        form = EstadoBusForm(request.POST)
        if form.is_valid():
            estado = form.save()
            messages.success(request, f'Estado del bus {estado.bus_patente} registrado exitosamente.')
            return redirect('estados_bus_list')
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = EstadoBusForm()
    
    return render(request, 'templatesApp/estado_bus_form.html', {'form': form, 'accion': 'Crear'})


def estado_bus_editar(request, pk):
    estado = get_object_or_404(EstadoBus, pk=pk)
    
    if request.method == 'POST':
        form = EstadoBusForm(request.POST, instance=estado)
        if form.is_valid():
            estado = form.save()
            messages.success(request, f'Estado del bus {estado.bus_patente} actualizado exitosamente.')
            return redirect('estado_bus_detalle', pk=estado.pk)
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = EstadoBusForm(instance=estado)
    
    return render(request, 'templatesApp/estado_bus_form.html', {
        'form': form, 
        'accion': 'Editar',
        'estado': estado
    })


def estado_bus_eliminar(request, pk):
    estado = get_object_or_404(EstadoBus, pk=pk)
    
    if request.method == 'POST':
        patente = estado.bus_patente
        estado.delete()
        messages.success(request, f'Estado del bus {patente} eliminado exitosamente.')
        return redirect('estados_bus_list')
    
    return render(request, 'templatesApp/estado_bus_confirm_delete.html', {'estado': estado})


# ==================== CRUD ASIGNACIÓN ROL ====================

def asignaciones_rol_list(request):
    search_query = request.GET.get('search', '')
    asignaciones_data = AsignacionRol.objects.all()
    
    if search_query:
        asignaciones_data = asignaciones_data.filter(
            Q(trabajador_nombre__icontains=search_query) |
            Q(trabajador_apellido__icontains=search_query) |
            Q(rol_nombre__icontains=search_query)
        )
    
    estado_filter = request.GET.get('estado', '')
    if estado_filter == 'activo':
        asignaciones_data = asignaciones_data.filter(activo=True)
    elif estado_filter == 'inactivo':
        asignaciones_data = asignaciones_data.filter(activo=False)
    
    asignaciones_data = asignaciones_data.order_by('-fecha_asignacion')
    
    paginator = Paginator(asignaciones_data, 10)
    page = request.GET.get('page')
    
    try:
        asignaciones = paginator.page(page)
    except PageNotAnInteger:
        asignaciones = paginator.page(1)
    except EmptyPage:
        asignaciones = paginator.page(paginator.num_pages)
    
    context = {
        'asignaciones': asignaciones,
        'search_query': search_query,
        'estado_filter': estado_filter,
    }
    return render(request, 'templatesApp/asignaciones_rol.html', context)


def asignacion_rol_detalle(request, pk):
    asignacion = get_object_or_404(AsignacionRol, pk=pk)
    return render(request, 'templatesApp/asignacion_rol_detalle.html', {'asignacion': asignacion})


def asignacion_rol_crear(request):
    if request.method == 'POST':
        form = AsignacionRolForm(request.POST)
        if form.is_valid():
            asignacion = form.save()
            messages.success(request, f'Rol asignado exitosamente a {asignacion.trabajador_nombre}.')
            return redirect('asignaciones_rol_list')
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = AsignacionRolForm()
    
    # Pasar listas de trabajadores y roles para ayudar al usuario
    context = {
        'form': form,
        'accion': 'Crear',
        'trabajadores': Trabajador.objects.filter(activo=True),
        'roles': Rol.objects.filter(activo=True),
    }
    return render(request, 'templatesApp/asignacion_rol_form.html', context)


def asignacion_rol_editar(request, pk):
    asignacion = get_object_or_404(AsignacionRol, pk=pk)
    
    if request.method == 'POST':
        form = AsignacionRolForm(request.POST, instance=asignacion)
        if form.is_valid():
            asignacion = form.save()
            messages.success(request, 'Asignación de rol actualizada exitosamente.')
            return redirect('asignacion_rol_detalle', pk=asignacion.pk)
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = AsignacionRolForm(instance=asignacion)
    
    context = {
        'form': form,
        'accion': 'Editar',
        'asignacion': asignacion,
        'trabajadores': Trabajador.objects.filter(activo=True),
        'roles': Rol.objects.filter(activo=True),
    }
    return render(request, 'templatesApp/asignacion_rol_form.html', context)


def asignacion_rol_eliminar(request, pk):
    asignacion = get_object_or_404(AsignacionRol, pk=pk)
    
    if request.method == 'POST':
        asignacion.delete()
        messages.success(request, 'Asignación de rol eliminada exitosamente.')
        return redirect('asignaciones_rol_list')
    
    return render(request, 'templatesApp/asignacion_rol_confirm_delete.html', {'asignacion': asignacion})


# ==================== CRUD ASIGNACIÓN BUS ====================

def asignaciones_bus_list(request):
    search_query = request.GET.get('search', '')
    asignaciones_data = AsignacionBus.objects.all()
    
    if search_query:
        asignaciones_data = asignaciones_data.filter(
            Q(trabajador_nombre__icontains=search_query) |
            Q(trabajador_apellido__icontains=search_query) |
            Q(bus_patente__icontains=search_query)
        )
    
    estado_filter = request.GET.get('estado', '')
    if estado_filter == 'activo':
        asignaciones_data = asignaciones_data.filter(activo=True)
    elif estado_filter == 'inactivo':
        asignaciones_data = asignaciones_data.filter(activo=False)
    
    turno_filter = request.GET.get('turno', '')
    if turno_filter:
        asignaciones_data = asignaciones_data.filter(turno=turno_filter)
    
    asignaciones_data = asignaciones_data.order_by('-fecha_asignacion')
    
    paginator = Paginator(asignaciones_data, 10)
    page = request.GET.get('page')
    
    try:
        asignaciones = paginator.page(page)
    except PageNotAnInteger:
        asignaciones = paginator.page(1)
    except EmptyPage:
        asignaciones = paginator.page(paginator.num_pages)
    
    context = {
        'asignaciones': asignaciones,
        'search_query': search_query,
        'estado_filter': estado_filter,
        'turno_filter': turno_filter,
    }
    return render(request, 'templatesApp/asignaciones_bus.html', context)


def asignacion_bus_detalle(request, pk):
    asignacion = get_object_or_404(AsignacionBus, pk=pk)
    return render(request, 'templatesApp/asignacion_bus_detalle.html', {'asignacion': asignacion})


def asignacion_bus_crear(request):
    if request.method == 'POST':
        form = AsignacionBusForm(request.POST)
        if form.is_valid():
            asignacion = form.save()
            messages.success(request, f'Bus {asignacion.bus_patente} asignado exitosamente a {asignacion.trabajador_nombre}.')
            return redirect('asignaciones_bus_list')
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = AsignacionBusForm()
    
    context = {
        'form': form,
        'accion': 'Crear',
        'trabajadores': Trabajador.objects.filter(activo=True),
        'buses': Bus.objects.filter(activo=True),
    }
    return render(request, 'templatesApp/asignacion_bus_form.html', context)


def asignacion_bus_editar(request, pk):
    asignacion = get_object_or_404(AsignacionBus, pk=pk)
    
    if request.method == 'POST':
        form = AsignacionBusForm(request.POST, instance=asignacion)
        if form.is_valid():
            asignacion = form.save()
            messages.success(request, 'Asignación de bus actualizada exitosamente.')
            return redirect('asignacion_bus_detalle', pk=asignacion.pk)
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = AsignacionBusForm(instance=asignacion)
    
    context = {
        'form': form,
        'accion': 'Editar',
        'asignacion': asignacion,
        'trabajadores': Trabajador.objects.filter(activo=True),
        'buses': Bus.objects.filter(activo=True),
    }
    return render(request, 'templatesApp/asignacion_bus_form.html', context)


def asignacion_bus_eliminar(request, pk):
    asignacion = get_object_or_404(AsignacionBus, pk=pk)
    
    if request.method == 'POST':
        asignacion.delete()
        messages.success(request, 'Asignación de bus eliminada exitosamente.')
        return redirect('asignaciones_bus_list')
    
    return render(request, 'templatesApp/asignacion_bus_confirm_delete.html', {'asignacion': asignacion})