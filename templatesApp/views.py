# templatesApp/views.py - ARCHIVO COMPLETO

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from .models import Trabajador, Rol, Bus, EstadoBus, AsignacionRol, AsignacionBus
from .forms import (
    TrabajadorForm, RolForm, BusForm, EstadoBusForm, 
    AsignacionRolForm, AsignacionBusForm
)

# ==================== AUTENTICACIÓN ====================

def login_view(request):
    """Vista de login"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {username}!')
                next_page = request.GET.get('next', 'index')
                return redirect(next_page)
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'templatesApp/login.html', {'form': form})


def logout_view(request):
    """Vista de logout"""
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')


# ==================== DASHBOARD ====================

@login_required(login_url='login')
def index(request):
    """Dashboard con estadísticas"""
    context = {
        'total_trabajadores': Trabajador.objects.filter(activo=True).count(),
        'total_buses': Bus.objects.filter(activo=True).count(),
        'total_roles': Rol.objects.filter(activo=True).count(),
        'buses_operativos': EstadoBus.objects.filter(estado='OPERATIVO').count(),
        'asignaciones_activas_bus': AsignacionBus.objects.filter(activo=True).count(),
        'asignaciones_activas_rol': AsignacionRol.objects.filter(activo=True).count(),
        'user': request.user,
    }
    return render(request, 'templatesApp/index.html', context)


# ==================== CRUD TRABAJADORES ====================

@login_required(login_url='login')
def trabajadores_list(request):
    search_query = request.GET.get('search', '')
    trabajadores_data = Trabajador.objects.all()
    
    if search_query:
        trabajadores_data = trabajadores_data.filter(
            Q(nombre__icontains=search_query) |
            Q(apellido__icontains=search_query) |
            Q(contacto__icontains=search_query)
        )
    
    estado_filter = request.GET.get('estado', '')
    if estado_filter == 'activo':
        trabajadores_data = trabajadores_data.filter(activo=True)
    elif estado_filter == 'inactivo':
        trabajadores_data = trabajadores_data.filter(activo=False)
    
    trabajadores_data = trabajadores_data.order_by('apellido', 'nombre')
    
    paginator = Paginator(trabajadores_data, 10)
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


@login_required(login_url='login')
def trabajador_detalle(request, pk):
    trabajador = get_object_or_404(Trabajador, pk=pk)
    asignaciones_rol = trabajador.asignaciones_rol.all().order_by('-fecha_asignacion')
    asignaciones_bus = trabajador.asignaciones_bus.all().order_by('-fecha_asignacion')
    
    context = {
        'trabajador': trabajador,
        'asignaciones_rol': asignaciones_rol,
        'asignaciones_bus': asignaciones_bus,
    }
    return render(request, 'templatesApp/trabajador_detalle.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def trabajador_eliminar(request, pk):
    trabajador = get_object_or_404(Trabajador, pk=pk)
    
    if request.method == 'POST':
        nombre_completo = f"{trabajador.nombre} {trabajador.apellido}"
        
        asignaciones_activas = (
            trabajador.asignaciones_rol.filter(activo=True).count() +
            trabajador.asignaciones_bus.filter(activo=True).count()
        )
        
        if asignaciones_activas > 0:
            messages.warning(
                request, 
                f'No se puede eliminar a {nombre_completo} porque tiene {asignaciones_activas} asignaciones activas.'
            )
            return redirect('trabajador_detalle', pk=pk)
        
        trabajador.delete()
        messages.success(request, f'Trabajador {nombre_completo} eliminado exitosamente.')
        return redirect('trabajadores_list')
    
    asignaciones_count = (
        trabajador.asignaciones_rol.count() + trabajador.asignaciones_bus.count()
    )
    
    context = {
        'trabajador': trabajador,
        'asignaciones_count': asignaciones_count
    }
    return render(request, 'templatesApp/trabajador_confirm_delete.html', context)


# ==================== CRUD ROLES ====================

@login_required(login_url='login')
def roles_list(request):
    search_query = request.GET.get('search', '')
    roles_data = Rol.objects.annotate(
        num_asignaciones=Count('asignaciones', filter=Q(asignaciones__activo=True))
    )
    
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


@login_required(login_url='login')
def rol_detalle(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    asignaciones = rol.asignaciones.all().order_by('-fecha_asignacion')
    
    context = {
        'rol': rol,
        'asignaciones': asignaciones,
    }
    return render(request, 'templatesApp/rol_detalle.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def rol_eliminar(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    
    if request.method == 'POST':
        nombre = rol.nombre
        
        asignaciones_activas = rol.asignaciones.filter(activo=True).count()
        
        if asignaciones_activas > 0:
            messages.warning(
                request, 
                f'No se puede eliminar el rol "{nombre}" porque tiene {asignaciones_activas} asignaciones activas.'
            )
            return redirect('rol_detalle', pk=pk)
        
        rol.delete()
        messages.success(request, f'Rol "{nombre}" eliminado exitosamente.')
        return redirect('roles_list')
    
    asignaciones_count = rol.asignaciones.count()
    
    context = {
        'rol': rol,
        'asignaciones_count': asignaciones_count
    }
    return render(request, 'templatesApp/rol_confirm_delete.html', context)


# ==================== CRUD BUSES ====================

@login_required(login_url='login')
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


@login_required(login_url='login')
def bus_detalle(request, pk):
    bus = get_object_or_404(Bus, pk=pk)
    estado = bus.get_estado_actual()
    asignaciones = bus.asignaciones.all().order_by('-fecha_asignacion')
    
    context = {
        'bus': bus,
        'estado': estado,
        'asignaciones': asignaciones,
    }
    return render(request, 'templatesApp/bus_detalle.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def bus_eliminar(request, pk):
    bus = get_object_or_404(Bus, pk=pk)
    
    if request.method == 'POST':
        patente = bus.patente
        
        asignaciones_activas = bus.asignaciones.filter(activo=True).count()
        
        if asignaciones_activas > 0:
            messages.warning(
                request, 
                f'No se puede eliminar el bus {patente} porque tiene {asignaciones_activas} asignaciones activas.'
            )
            return redirect('bus_detalle', pk=pk)
        
        bus.delete()
        messages.success(request, f'Bus {patente} eliminado exitosamente.')
        return redirect('buses_list')
    
    asignaciones_count = bus.asignaciones.count()
    
    context = {
        'bus': bus,
        'asignaciones_count': asignaciones_count
    }
    return render(request, 'templatesApp/bus_confirm_delete.html', context)


# ==================== CRUD ESTADO BUS ====================

@login_required(login_url='login')
def estados_bus_list(request):
    search_query = request.GET.get('search', '')
    estados_data = EstadoBus.objects.select_related('bus')
    
    if search_query:
        estados_data = estados_data.filter(
            Q(bus__patente__icontains=search_query) |
            Q(bus__modelo__icontains=search_query)
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
        'estados_choices': EstadoBus.ESTADOS_CHOICES,
    }
    return render(request, 'templatesApp/estados_bus.html', context)


@login_required(login_url='login')
def estado_bus_detalle(request, pk):
    estado = get_object_or_404(EstadoBus.objects.select_related('bus'), pk=pk)
    return render(request, 'templatesApp/estado_bus_detalle.html', {'estado': estado})


@login_required(login_url='login')
def estado_bus_crear(request):
    if request.method == 'POST':
        form = EstadoBusForm(request.POST)
        if form.is_valid():
            estado = form.save()
            messages.success(request, f'Estado del bus {estado.bus.patente} registrado exitosamente.')
            return redirect('estados_bus_list')
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = EstadoBusForm()
    
    return render(request, 'templatesApp/estado_bus_form.html', {'form': form, 'accion': 'Crear'})


@login_required(login_url='login')
def estado_bus_editar(request, pk):
    estado = get_object_or_404(EstadoBus, pk=pk)
    
    if request.method == 'POST':
        form = EstadoBusForm(request.POST, instance=estado)
        if form.is_valid():
            estado = form.save()
            messages.success(request, f'Estado del bus {estado.bus.patente} actualizado exitosamente.')
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


@login_required(login_url='login')
def estado_bus_eliminar(request, pk):
    estado = get_object_or_404(EstadoBus, pk=pk)
    
    if request.method == 'POST':
        patente = estado.bus.patente
        estado.delete()
        messages.success(request, f'Estado del bus {patente} eliminado exitosamente.')
        return redirect('estados_bus_list')
    
    return render(request, 'templatesApp/estado_bus_confirm_delete.html', {'estado': estado})


# ==================== CRUD ASIGNACIÓN ROL ====================

@login_required(login_url='login')
def asignaciones_rol_list(request):
    search_query = request.GET.get('search', '')
    asignaciones_data = AsignacionRol.objects.select_related('trabajador', 'rol')
    
    if search_query:
        asignaciones_data = asignaciones_data.filter(
            Q(trabajador__nombre__icontains=search_query) |
            Q(trabajador__apellido__icontains=search_query) |
            Q(rol__nombre__icontains=search_query)
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


@login_required(login_url='login')
def asignacion_rol_detalle(request, pk):
    asignacion = get_object_or_404(
        AsignacionRol.objects.select_related('trabajador', 'rol'), 
        pk=pk
    )
    return render(request, 'templatesApp/asignacion_rol_detalle.html', {'asignacion': asignacion})


@login_required(login_url='login')
def asignacion_rol_crear(request):
    if request.method == 'POST':
        form = AsignacionRolForm(request.POST)
        if form.is_valid():
            asignacion = form.save()
            messages.success(request, f'Rol "{asignacion.rol.nombre}" asignado exitosamente a {asignacion.trabajador}.')
            return redirect('asignaciones_rol_list')
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = AsignacionRolForm()
    
    return render(request, 'templatesApp/asignacion_rol_form.html', {
        'form': form,
        'accion': 'Crear'
    })


@login_required(login_url='login')
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
    
    return render(request, 'templatesApp/asignacion_rol_form.html', {
        'form': form,
        'accion': 'Editar',
        'asignacion': asignacion
    })


@login_required(login_url='login')
def asignacion_rol_eliminar(request, pk):
    asignacion = get_object_or_404(AsignacionRol, pk=pk)
    
    if request.method == 'POST':
        asignacion.delete()
        messages.success(request, 'Asignación de rol eliminada exitosamente.')
        return redirect('asignaciones_rol_list')
    
    return render(request, 'templatesApp/asignacion_rol_confirm_delete.html', {'asignacion': asignacion})


# ==================== CRUD ASIGNACIÓN BUS ====================

@login_required(login_url='login')
def asignaciones_bus_list(request):
    search_query = request.GET.get('search', '')
    asignaciones_data = AsignacionBus.objects.select_related('trabajador', 'bus')
    
    if search_query:
        asignaciones_data = asignaciones_data.filter(
            Q(trabajador__nombre__icontains=search_query) |
            Q(trabajador__apellido__icontains=search_query) |
            Q(bus__patente__icontains=search_query)
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
        'turnos_choices': AsignacionBus.TURNO_CHOICES,
    }
    return render(request, 'templatesApp/asignaciones_bus.html', context)


@login_required(login_url='login')
def asignacion_bus_detalle(request, pk):
    asignacion = get_object_or_404(
        AsignacionBus.objects.select_related('trabajador', 'bus'), 
        pk=pk
    )
    return render(request, 'templatesApp/asignacion_bus_detalle.html', {'asignacion': asignacion})


@login_required(login_url='login')
def asignacion_bus_crear(request):
    if request.method == 'POST':
        form = AsignacionBusForm(request.POST)
        if form.is_valid():
            asignacion = form.save()
            messages.success(request, f'Bus {asignacion.bus.patente} asignado exitosamente a {asignacion.trabajador}.')
            return redirect('asignaciones_bus_list')
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = AsignacionBusForm()
    
    return render(request, 'templatesApp/asignacion_bus_form.html', {
        'form': form,
        'accion': 'Crear'
    })


@login_required(login_url='login')
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
    
    return render(request, 'templatesApp/asignacion_bus_form.html', {
        'form': form,
        'accion': 'Editar',
        'asignacion': asignacion
    })


@login_required(login_url='login')
def asignacion_bus_eliminar(request, pk):
    asignacion = get_object_or_404(AsignacionBus, pk=pk)
    
    if request.method == 'POST':
        asignacion.delete()
        messages.success(request, 'Asignación de bus eliminada exitosamente.')
        return redirect('asignaciones_bus_list')
    
    return render(request, 'templatesApp/asignacion_bus_confirm_delete.html', {'asignacion': asignacion})