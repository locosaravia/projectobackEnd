from django.shortcuts import render
from .models import Trabajador

# Create your views here.

def index(request):
    return render(request, 'templatesApp/index.html')

def login1(request):
    return render(request, 'templatesApp/login.html')

def buses(request):
    data = {
        "patente": "A1 P2 23",
        "modelo": "chevrolet",
        "año": 2003,
        "capacidad": 40,
    }
    return render(request, 'templatesApp/buses.html', data)

def ingresot(request):
    return render(request, 'templatesApp/ingresoT.html')

def trabajadores_list(request):
    trabajadores_data = Trabajador.objects.all()
    data = {
        'trabajadores': trabajadores_data
    }
    return render(request, 'templatesApp/trabajadores.html', data)

def rol(request):
    data = {
        "id": 1,
        "rol": "conductor"
    }
    return render(request, 'templatesApp/rol.html', data)

def ingresoR(request):
    return render(request, 'templatesApp/ingresoR.html')

def estadoB(request):
    data = {
        "patente": "A1 P2 23",
        "estado": "en servicio"
    }
    return render(request, 'templatesApp/estado_bus.html', data)

def cambiarestado(request):
    return render(request, 'templatesApp/cambioestado.html')

def asignarR(request):
    data = {
        "id_trabajador": 1,
        "nombre": "juan",
        "apellido": "saravia",
        "rol_asignado": "conductor"
    }
    return render(request, 'templatesApp/asignarol.html', data)

def asignarbus(request):
    data = {
        "id_trabajador": 1,
        "nombre": "juan",
        "apellido": "saravia",
        "bus_asignado": "A1 P2 23"
    }
    return render(request, 'templatesApp/asignarbus.html', data)

def cambiarbus(request):
    return render(request, 'templatesApp/cambiarbus.html')
