from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'templatesApp/index.html')

def rol(request):
    return render(request, 'templatesApp/rol.html')

def login1(request):
    return render(request, 'templatesApp/login.html')

def buses1(request):
    data = {
        "patente" : "A1 P2 23",
        "modelo" : "volvo",
        "año" : 2003,
        "capacidad" : 40,
    }
    return render(request, 'templatesApp/buses.html', data)

def ingresot(request):
    return render(request, 'templatesApp/ingresoT.html')


def data1(request):
    data = {
        "id" : "1",
        "nombre" : "juan",
        "apellido" : "saravia",
        "direccion" : "amadeo de lar 1736",
        "contacto" : "+56957980694",
        "edad" : 18  
            }
    return render(request, 'templatesApp/trabajadores.html', data)

def buses(request):
    return render(request, 'templatesApp/ingresobus.html')


def rol (request):
    data = {
        "id" : "1",
        "rol" : "conductor"
    }
    return render(request, 'templatesApp/rol.html', data)

def ingresoR(request):
    return render(request, 'templatesApp/ingresoR.html')

def estadoB(request):
    data = {
        "patente" : "A1 P2 23",
        "estado" : "en servicio"
    }
    return render(request, 'templatesApp/estado_bus.html', data)

def cambiarestado(request):
    return render(request, 'templatesApp/cambioestado.html')

def asignarR(request):
    data = {
        "id_trabajador" : "1",
        "nombre" : "juan",
        "apellido" : "saravia",
        "rol_asignado" : "conductor"
    }
    return render(request, 'templatesApp/asignarol.html', data)

def asignarB(request):
    data = {
        "id_trabajador" : "1",
        "nombre" : "juan",
        "apellido" : "saravia",
        "bus_asignado" : "A1 P2 23"
    }
    return render(request, 'templatesApp/asignarbus.html', data)

def cambiarol(request):
    return render(request, 'templatesApp/cambiarol.html')

def asignarbus(request):
    data = {
        "id_trabajador" : "1",
        "nombre" : "juan",
        "apellido" : "saravia",
        "bus_asignado" : "A1 P2 23"
    }
    return render(request, 'templatesApp/asignarbus.html', data)

def cambiarbus(request):
    return render(request, 'templatesApp/cambiarbus.html')