from django.http import HttpResponse
from django.views.decorators.cache import never_cache
import requests
from django.shortcuts import render
from .models import Usuario



@never_cache
def lista_usuarios(request):
    response = requests.get('http://localhost:8080/usuarios')
    if response.ok:
        usuarios = response.json()
        return render(request, 'crudApp/lista_usuarios.html', {'usuarios': usuarios})
    else:
        return HttpResponse('Error al obtener los usuarios: ' + str(response.status_code))

@never_cache
def home(request):
    # El argumento de 'render' debe ser 'crudApp/home.html', no 'home.html' si sigues la convención estándar.
    return render(request, 'crudApp/home.html')