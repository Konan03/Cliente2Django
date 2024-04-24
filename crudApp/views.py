from datetime import datetime, timezone
from decimal import Decimal

from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.views import View
from django.contrib import messages  # Importa el módulo de mensajes
from .forms import UsuarioForm
import requests
from django.shortcuts import render, redirect
from .forms import VideojuegoForm
from django.core.serializers import serialize

from .models import Videojuego, Usuario


@never_cache
def lista_usuarios(request):
    response = requests.get('http://localhost:8080/usuarios')
    if response.ok:
        usuarios = response.json()
        return render(request, 'crudApp/lista_usuarios.html', {'usuarios': usuarios})
    else:
        return HttpResponse('Error al obtener los usuarios: ' + str(response.status_code))


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
        return render(request, 'crudApp/videojuego.html')

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

def seleccionar_usuario(request):
    response = requests.get('http://localhost:8080/usuarios')  # Asume que esta es la URL de tu API
    if response.ok:
        usuarios = response.json()
        return render(request, 'crudApp/seleccionar_usuario.html', {'usuarios': usuarios})
    return render(request, 'error.html', {'mensaje': 'No se pudieron cargar los usuarios.'})


def add_videojuego(request, usuario_id):
    if request.method == 'POST':
        form = VideojuegoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Convertir cualquier objeto Decimal a float
            if isinstance(data['precio'], Decimal):
                data['precio'] = float(data['precio'])

            # Asegurarse de que la fecha de lanzamiento está presente y es válida
            if data['fechaLanzamiento']:
                data['fechaLanzamiento'] = data['fechaLanzamiento'].strftime('%Y-%m-%dT%H:%M')
            else:
                messages.error(request, 'La fecha de lanzamiento es requerida.')
                return render(request, 'crudApp/CrudVideojuego/CreateV.html', {'form': form, 'usuario_id': usuario_id})

            # Enviar los datos del videojuego al servidor externo
            response = requests.post(f'http://localhost:8080/videojuegos/{usuario_id}', json=data)
            if response.status_code == 201:
                videojuego_creado = response.json()
                videojuego_id = videojuego_creado.get('id')
                messages.success(request, f'El videojuego con ID {videojuego_id} se ha creado exitosamente.')
            else:
                messages.error(request, 'Hubo un error al crear el videojuego en el servidor externo.')

            return redirect('add_videojuego', usuario_id=usuario_id)
    else:
        form = VideojuegoForm()
    return render(request, 'crudApp/CrudVideojuego/CreateV.html', {'form': form, 'usuario_id': usuario_id})


def read_videojuegos(request):
    url = 'http://localhost:8080/videojuegos'  # Cambia esto según tu configuración
    response = requests.get(url)
    if response.status_code == 200:
        videojuegos = response.json()
        return render(request, 'crudApp/CrudVideojuego/ReadV.html', {'videojuegos': videojuegos})
    else:
        return HttpResponse('No se pudo obtener los videojuegos', status=response.status_code)

# Vista corregida
# views.py

def update_videojuego(request):
    usuario_id = request.GET.get('usuario_id')
    usuario = None
    videojuegos = None
    form = None

    if usuario_id:
        # Obtener detalles del usuario
        user_response = requests.get(f'http://localhost:8080/usuarios', params={'id': usuario_id})
        if user_response.ok:
            usuario = user_response.json()

            # Obtener videojuegos asociados al usuario
            games_response = requests.get(f'http://localhost:8080/videojuegos/{usuario_id}')
            if games_response.ok:
                videojuegos = games_response.json()

                # Si se selecciona un juego, cargar los datos del juego en el formulario
                selected_game_id = request.GET.get('videojuego_id')
                if selected_game_id:
                    selected_game_response = requests.get(f'http://localhost:8080/videojuegos/{usuario_id}/{selected_game_id}')
                    if selected_game_response.ok:
                        selected_game_data = selected_game_response.json()
                        form = VideojuegoForm(initial=selected_game_data)

    return render(request, 'crudApp/CrudVideojuego/UpdateV.html', {
        'form': form, 'videojuegos': videojuegos, 'usuario': usuario, 'usuario_id': usuario_id
    })
















