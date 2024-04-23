from django.http import HttpResponse
from django.views.decorators.cache import never_cache
import requests
from django.shortcuts import render
from .models import Usuario
from django.views import View
@never_cache
def lista_usuarios(request):
    response = requests.get('http://localhost:8080/usuarios')
    if response.ok:
        usuarios = response.json()
        return render(request, 'crudApp/lista_usuarios.html', {'usuarios': usuarios})
    else:
        return HttpResponse('Error al obtener los usuarios: ' + str(response.status_code))

from django.shortcuts import render

@never_cache
def home(request):
    # Aquí puedes agregar cualquier contexto que desees pasar a tu plantilla
    context = {
        # Por ejemplo, si quieres mostrar un mensaje de bienvenida dinámico
        'welcome_message': '¡Bienvenido a nuestra aplicación!',
        # Otros datos necesarios para la página de inicio
    }
    return render(request, 'crudApp/home.html', context)

class UserView(View):
    def get(self, request):
        return render(request, 'usuario.html')

class VideogameView(View):
    def get(self, request):
        return render(request, 'videojuego.html')

class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')