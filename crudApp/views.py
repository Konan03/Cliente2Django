import json
from datetime import datetime, timezone
from decimal import Decimal

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache
from django.views import View
from django.contrib import messages  # Importa el módulo de mensajes
from .forms import UsuarioForm
from django.shortcuts import render, redirect
from .forms import VideojuegoForm
from django.shortcuts import render
import requests
from django.http import JsonResponse

from .models import Usuario


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
            form_data = form.cleaned_data
            form_data['fechaNacimiento'] = form_data['fechaNacimiento'].strftime('%Y-%m-%dT%H:%M')
            # Guarda el usuario en el backend de Spring Boot
            response = requests.post('http://localhost:8080/usuarios', json=form_data,
                                     headers={'Content-Type': 'application/json'})
            if response.status_code == 201:
                # El usuario se agregó correctamente, limpia el formulario y muestra un mensaje de éxito
                form = UsuarioForm()
                messages.success(request, 'El usuario se ha creado con éxito.')
                return render(request, 'crudApp/CrudUsuario/CreateU.html', {'form': form})
            else:
                # Hubo un error al agregar el usuario, muestra un mensaje de error
                return HttpResponse('Error al agregar el usuario al backend de Spring Boot')
    else:
        # Si no es una solicitud POST, muestra el formulario vacío
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


def update_videojuego(request):
    try:
        usuario_id = request.GET.get('usuario_id')
        videojuego_id = request.GET.get('videojuego_id')

        usuario = None
        videojuegos = []
        form = VideojuegoForm()

        if usuario_id:
            user_response = requests.get(f'http://localhost:8080/usuarios', params={'id': usuario_id})
            if user_response.ok:
                usuario = user_response.json()

                games_response = requests.get(f'http://localhost:8080/videojuegos/{usuario_id}')
                if games_response.ok:
                    videojuegos = games_response.json()

                    if videojuego_id:
                        selected_game_response = requests.get(f'http://localhost:8080/videojuegos/{usuario_id}/{videojuego_id}')
                        if selected_game_response.ok:
                            selected_game_data = selected_game_response.json()
                            form = VideojuegoForm(initial=selected_game_data)
            else:
                messages.error(request, 'No se pudo obtener el usuario.')
                return redirect('update_videojuego')

        if request.method == 'POST':
            form = VideojuegoForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                if isinstance(data['precio'], Decimal):
                    data['precio'] = float(data['precio'])

                if data.get('fechaLanzamiento'):
                    data['fechaLanzamiento'] = data['fechaLanzamiento'].strftime('%Y-%m-%dT%H:%M')
                    update_response = requests.put(f'http://localhost:8080/videojuegos/{usuario_id}/{videojuego_id}', json=data)
                    if update_response.ok:
                        messages.success(request, '¡El videojuego se ha actualizado correctamente!')
                        return redirect('update_videojuego')  # Asegúrate de usar la URL correcta para la redirección
                    else:
                        messages.error(request, 'Error al actualizar el videojuego.')
                else:
                    messages.error(request, 'La fecha de lanzamiento es requerida.')
                    return render(request, 'crudApp/CrudVideojuego/UpdateV.html', {'form': form, 'usuario_id': usuario_id})
            else:
                messages.error(request, 'El formulario no es válido. Verifique los datos ingresados.')

        return render(request, 'crudApp/CrudVideojuego/UpdateV.html', {
            'usuario': usuario,
            'videojuegos': videojuegos,
            'form': form,
            'usuario_id': usuario_id,
            'videojuego_id': videojuego_id
        })

    except Exception as e:
        messages.error(request, f'Ocurrió un error: {e}')
        return render(request, 'crudApp/CrudVideojuego/UpdateV.html')

def delete_videojuego(request):
    try:
        usuario_id = request.GET.get('usuario_id')
        videojuego_id = request.GET.get('videojuego_id')

        usuario = None
        videojuegos = []
        form = VideojuegoForm()

        if usuario_id:
            user_response = requests.get(f'http://localhost:8080/usuarios', params={'id': usuario_id})
            if user_response.ok:
                usuario = user_response.json()

                games_response = requests.get(f'http://localhost:8080/videojuegos/{usuario_id}')
                if games_response.ok:
                    videojuegos = games_response.json()

                    if videojuego_id:
                        selected_game_response = requests.get(f'http://localhost:8080/videojuegos/{usuario_id}/{videojuego_id}')
                        if selected_game_response.ok:
                            selected_game_data = selected_game_response.json()
                            form = VideojuegoForm(initial=selected_game_data)
            else:
                messages.error(request, 'No se pudo obtener el usuario.')
                return redirect('delete_videojuego')

        if request.method == 'POST':
            form = VideojuegoForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                if isinstance(data['precio'], Decimal):
                    data['precio'] = float(data['precio'])

                if data.get('fechaLanzamiento'):
                    data['fechaLanzamiento'] = data['fechaLanzamiento'].strftime('%Y-%m-%dT%H:%M')
                    update_response = requests.delete(f'http://localhost:8080/videojuegos/{usuario_id}/{videojuego_id}', json=data)
                    if update_response.ok:
                        messages.success(request, '¡El videojuego se ha actualizado correctamente!')
                        return redirect('delete_videojuego')  # Asegúrate de usar la URL correcta para la redirección
                    else:
                        messages.error(request, 'Error al actualizar el videojuego.')
                else:
                    messages.error(request, 'La fecha de lanzamiento es requerida.')
                    return render(request, 'crudApp/CrudVideojuego/DeleteV.html', {'form': form, 'usuario_id': usuario_id})
            else:
                messages.error(request, 'El formulario no es válido. Verifique los datos ingresados.')

        return render(request, 'crudApp/CrudVideojuego/DeleteV.html', {
            'usuario': usuario,
            'videojuegos': videojuegos,
            'form': form,
            'usuario_id': usuario_id,
            'videojuego_id': videojuego_id
        })

    except Exception as e:
        messages.error(request, f'Ocurrió un error: {e}')
        return render(request, 'crudApp/CrudVideojuego/DeleteV.html')





def search_videojuegos(request):
    videojuegos = []
    if request.method == 'GET' and 'usuario_id' in request.GET:
        params = {
            'id': request.GET.get('id'),
            'nombre': request.GET.get('nombre'),
            'precio': request.GET.get('precio'),
            'multijugador': request.GET.get('multijugador'),
        }
        try:
            response = requests.get(f"http://localhost:8080/usuario/{request.GET['usuario_id']}", params=params)
            if response.status_code == 200:
                videojuegos = response.json()
            else:
                messages.error(request, "No se encontraron videojuegos con los criterios proporcionados.")
        except requests.RequestException as e:
            messages.error(request, str(e))

    return render(request, 'crudApp/CrudVideojuego/Search.html', {
        'videojuegos': videojuegos
    })


def delete_usuario(request):
    if request.method == 'DELETE':
        form = UsuarioForm(request.DELETE)
        if form.is_valid():
            form.save()
            messages.success(request, 'El usuario se ha eliminado con exito')
            return redirect('delete_usuario')
    else:
        form = UsuarioForm()
    return render(request, 'crudApp/CrudUsuario/DeleteU.html', {'form': form})


def view_usuario(request):
    response = requests.get('http://localhost:8080/usuarios')
    if response.ok:
        usuarios = response.json()
        return render(request, 'crudApp/CrudUsuario/ReadU.html', {'usuarios': usuarios})
    else:
        return HttpResponse('Error al obtener los usuarios: ' + str(response.status_code))


def update_usuario(request):
    try:
        if request.method == 'POST':
            form = UsuarioForm(request.POST)
            if form.is_valid():
                usuario_id = form.cleaned_data['id']
                form_data = form.cleaned_data
                form_data['fechaNacimiento'] = form_data['fechaNacimiento'].strftime('%Y-%m-%dT%H:%M')

                print("Datos enviados a Spring Boot:", form_data)
                # Eliminamos el id del formulario para que no se incluya al actualizar
                del form_data['id']
                response = requests.put(f'http://localhost:8080/usuarios/{usuario_id}', json=form_data,
                                        headers={'Content-Type': 'application/json'})
                if response.status_code == 200:
                    messages.success(request, 'El usuario se ha actualizado con éxito')
                    return redirect('update_usuario')
                else:
                    messages.error(request, f'Error al actualizar el usuario en el backend de Spring Boot. '
                                            f'Código de estado: {response.status_code}')
        else:
            # Obtener el ID del usuario desde la solicitud GET
            usuario_id = request.GET.get('id')
            if usuario_id:
                print(f'Búsqueda de usuario con ID: {usuario_id}')
                # Realizar una solicitud GET al backend de Spring Boot para obtener los datos del usuario
                response = requests.get(f'http://localhost:8080/usuarios', params={'id': usuario_id})

                if response.status_code == 200:
                    # Si la solicitud fue exitosa, obtener los datos del usuario del cuerpo de la respuesta JSON
                    usuario_data = response.json()
                    print(usuario_data)  # Agregar esta línea para verificar los datos del usuario
                    # Inicializar el formulario con los datos del usuario y pasarlos al contexto
                    form = UsuarioForm(initial=usuario_data)
                    return render(request, 'crudApp/CrudUsuario/UpdateU.html', {'form': form, 'usuario': usuario_data})
                else:
                    messages.error(request, f'Error al obtener los datos del usuario del backend de Spring Boot. '
                                            f'Código de estado: {response.status_code}')
                    return redirect('update_usuario')
            else:
                form = UsuarioForm()
    except Exception as e:
        messages.error(request, f'Ocurrió un error: {e}')

    # Si hubo algún error o si no se proporcionó un ID de usuario válido, simplemente renderizamos el formulario vacío
    form = UsuarioForm()
    return render(request, 'crudApp/CrudUsuario/UpdateU.html', {'form': form})
