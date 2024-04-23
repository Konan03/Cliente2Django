from django.http import HttpResponse
from django.views.decorators.cache import never_cache
import requests
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages  # Importa el módulo de mensajes
from .forms import UsuarioForm


@never_cache
def lista_usuarios(request):
    response = requests.get('http://localhost:8080/usuarios')
    if response.ok:
        usuarios = response.json()
        return render(request, 'crudApp/lista_usuarios.html', {'usuarios': usuarios})
    else:
        return HttpResponse('Error al obtener los usuarios: ' + str(response.status_code))

from django.shortcuts import render


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
        return render(request, 'crudApp/usuario.html')

class VideogameView(View):
    def get(self, request):
        return render(request, 'videojuego.html')

class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')


def add_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El usuario se ha creado con éxito.')  # Añade un mensaje de éxito
            return redirect('add_usuario')  # Redirige a la misma página para limpiar el formulario
    else:
        form = UsuarioForm()
    return render(request, 'crudApp/CrudUsuario/CreateU.html', {'form': form})

