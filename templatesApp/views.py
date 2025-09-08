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