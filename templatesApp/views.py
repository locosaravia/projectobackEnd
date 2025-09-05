from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'templatesApp/index.html')

def trabajadores(request):
    return render(request, 'templatesApp/trabajadores.html')

def login1(request):
    return render(request, 'templatesApp/login.html')