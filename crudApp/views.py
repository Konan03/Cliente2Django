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

def buscar_usuarioA(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            juegos_usuario = usuario.videojuego_set.all()
            return render(request, 'crudApp/lista_videojuegosA.html', {'usuario': usuario, 'juegos_usuario': juegos_usuario})
        except Usuario.DoesNotExist:
            error_message = "El usuario con el ID proporcionado no existe."
            return render(request, 'crudApp/buscar_usuarioD.html', {'error_message': error_message})
    return render(request, 'crudApp/buscar_usuarioD.html')

def buscar_usuarioD(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            juegos_usuario = usuario.videojuego_set.all()
            return render(request, 'crudApp/lista_videojuegosD.html', {'usuario': usuario, 'juegos_usuario': juegos_usuario})
        except Usuario.DoesNotExist:
            error_message = "El usuario con el ID proporcionado no existe."
            return render(request, 'crudApp/buscar_usuarioD.html', {'error_message': error_message})
    return render(request, 'crudApp/buscar_usuarioD.html')

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

def update_videojuego(request):
    # Verificar si se está buscando un videojuego por ID para cargar el formulario
    if request.method == 'GET' and 'videojuego_id' in request.GET:
        videojuego_id = request.GET['videojuego_id']
        response = requests.get(f'http://localhost:8080/videojuegos/{videojuego_id}')
        if response.ok:
            videojuego_data = response.json()
            form = VideojuegoForm(initial=videojuego_data)
            return render(request, 'crudApp/CrudVideojuego/UpdateV.html', {
                'form': form,
                'videojuego_id': videojuego_id
            })
        else:
            messages.error(request, 'Videojuego no encontrado.')
            return redirect('update_videojuego')

    # Procesar el formulario actualizado y enviar una solicitud PUT a la API
    elif request.method == 'POST':
        form = VideojuegoForm(request.POST)
        videojuego_id = request.POST.get('videojuego_id')
        if form.is_valid():
            data = form.cleaned_data
            response = requests.put(f'http://localhost:8080/videojuegos/{videojuego_id}', json=data)
            if response.status_code == 200 or response.status_code == 204:  # Asumiendo que 200 o 204 indican éxito
                messages.success(request, 'Videojuego actualizado con éxito.')
            else:
                messages.error(request, f'Error al actualizar el videojuego: {response.text}')
            return redirect('update_videojuego')
        else:
            messages.error(request, 'Información del formulario no válida.')
            return render(request, 'crudApp/CrudVideojuego/UpdateV.html', {'form': form, 'videojuego_id': videojuego_id})
    else:
        # Si no es GET con videojuego_id ni POST, solo muestra el formulario de búsqueda
        return render(request, 'crudApp/CrudVideojuego/UpdateV.html')