from django.http import HttpResponse
from django.views.decorators.cache import never_cache
import requests
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages  # Importa el módulo de mensajes
from .forms import UsuarioForm, VideojuegoCreateForm, VideojuegoUpdateForm
from django.shortcuts import render
import json
from django.core.serializers.json import DjangoJSONEncoder
from decimal import Decimal
from datetime import datetime  # Importa datetime

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


class SearchView(View):
    def get(self, request):
        return render(request, 'crudApp/search.html')

def add_videojuego(request):
    usuario = None
    form = VideojuegoCreateForm()
    usuario_nombre = None

    if request.method == 'GET':
        usuario_id = request.GET.get('usuario_id')
        if usuario_id:
            response = requests.get(f'http://localhost:8080/usuarios/{usuario_id}')
            if response.status_code == 200:
                usuario = response.json()
                usuario_nombre = usuario.get('nombre', '')
                form = VideojuegoCreateForm(initial={'usuario_id': usuario_id})
            else:
                messages.error(request, 'Usuario no encontrado.')

    if request.method == 'POST':
        form = VideojuegoCreateForm(request.POST)
        if form.is_valid():
            videojuego_data = form.cleaned_data

            # Convertir objetos Decimal a float y datetime a string sin zona horaria
            for key, value in videojuego_data.items():
                if isinstance(value, Decimal):
                    videojuego_data[key] = float(value)
                elif isinstance(value, datetime):
                    videojuego_data[key] = value.replace(tzinfo=None).isoformat()

            usuario_id = request.POST.get('usuario_id')
            if usuario_id:
                response = requests.post(f'http://localhost:8080/videojuegos/{usuario_id}', json=videojuego_data)

                if response.status_code == 201:
                    messages.success(request, 'Videojuego agregado con éxito.')
                    return redirect('add_videojuego', usuario_id=usuario_id)
                else:
                    try:
                        error_message = response.json().get('detail', response.text)
                    except ValueError:
                        error_message = response.text
                    messages.error(request, f'Error al agregar el videojuego: {response.status_code} - {error_message}')
            else:
                messages.error(request, 'El ID del usuario no fue proporcionado.')

        else:
            messages.error(request, 'El formulario no es válido.')

    return render(request, 'crudApp/CrudVideojuego/CreateV.html', {
        'form': form,
        'usuario': usuario,
        'usuario_nombre': usuario_nombre
    })



def read_videojuegos(request):
    filtro_multijugador = request.GET.get('multijugador')
    params = {}

    if filtro_multijugador and filtro_multijugador != 'todos':
        if filtro_multijugador == 'true':
            params['multijugador'] = True
        elif filtro_multijugador == 'false':
            params['multijugador'] = False

    response = requests.get('http://localhost:8080/videojuegos', params=params)
    if response.status_code == 200:
        videojuegos = response.json()
    else:
        messages.error(request, 'Error al obtener los videojuegos: ' + str(response.status_code))
        videojuegos = []

    return render(request, 'crudApp/CrudVideojuego/ReadV.html', {
        'videojuegos': videojuegos,
        'filter_multijugador': filtro_multijugador
    })



def update_videojuego(request):
    usuario = None
    videojuego = None
    usuario_nombre = None

    if request.method == 'GET':
        usuario_id = request.GET.get('usuario_id')
        videojuego_id = request.GET.get('videojuego_id')

        if usuario_id:
            response = requests.get(f'http://localhost:8080/usuarios/{usuario_id}')
            if response.status_code == 200:
                usuario = response.json()
                usuario_nombre = usuario.get('nombre', '')

                if videojuego_id:
                    response = requests.get(f'http://localhost:8080/videojuegos/{usuario_id}/{videojuego_id}')
                    if response.status_code == 200:
                        videojuego = response.json()
                        form = VideojuegoUpdateForm(initial=videojuego)
                    else:
                        messages.error(request, 'Videojuego no encontrado.')
                        form = None
                else:
                    form = None
            else:
                messages.error(request, 'Usuario no encontrado.')
                form = None
        else:
            form = None

    if request.method == 'POST':
        form = VideojuegoUpdateForm(request.POST)
        if form.is_valid():
            videojuego_id = form.cleaned_data['id']
            usuario_id = request.POST.get('usuario_id')
            form_data = form.cleaned_data
            form_data['fechaLanzamiento'] = form_data['fechaLanzamiento'].strftime('%Y-%m-%dT%H:%M')

            # Eliminamos el id del formulario para que no se incluya al actualizar
            del form_data['id']
            for key, value in form_data.items():
                if isinstance(value, Decimal):
                    form_data[key] = float(value)
                elif isinstance(value, datetime):
                    form_data[key] = value.replace(tzinfo=None).isoformat()

            response = requests.put(f'http://localhost:8080/videojuegos/{usuario_id}/{videojuego_id}', json=form_data,
                                    headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                messages.success(request, 'El videojuego se ha actualizado con éxito')
                return redirect('update_videojuego')
            else:
                messages.error(request, f'Error al actualizar el videojuego en el backend de Spring Boot. '
                                        f'Código de estado: {response.status_code}')
        else:
            messages.error(request, 'El formulario no es válido.')

    return render(request, 'crudApp/CrudVideojuego/UpdateV.html', {
        'form': form,
        'usuario': usuario,
        'usuario_nombre': usuario_nombre,
        'videojuego': videojuego
    })


def delete_videojuego(request):
    usuario = None
    videojuego = None
    usuario_nombre = None

    if request.method == 'GET':
        usuario_id = request.GET.get('usuario_id')
        videojuego_id = request.GET.get('videojuego_id')

        if usuario_id:
            response = requests.get(f'http://localhost:8080/usuarios/{usuario_id}')
            if response.status_code == 200:
                usuario = response.json()
                usuario_nombre = usuario.get('nombre', '')
                if videojuego_id:
                    response = requests.get(f'http://localhost:8080/videojuegos/{usuario_id}/{videojuego_id}')
                    if response.status_code == 200:
                        videojuego = response.json()
                    else:
                        messages.error(request, 'Videojuego no encontrado.')
                else:
                    messages.error(request, 'Por favor, proporcione un ID de videojuego.')
            else:
                messages.error(request, 'Usuario no encontrado.')

    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        videojuego_id = request.POST.get('id')
        if usuario_id and videojuego_id:
            response = requests.delete(f'http://localhost:8080/videojuegos/{usuario_id}/{videojuego_id}')
            if response.status_code == 200:
                messages.success(request, 'Videojuego eliminado con éxito.')
                return redirect('delete_videojuego')
            else:
                messages.error(request, f'Error al eliminar el videojuego. Código de estado: {response.status_code}')
        else:
            messages.error(request, 'ID de usuario o videojuego no proporcionado.')

    return render(request, 'crudApp/CrudVideojuego/DeleteV.html', {'usuario': usuario, 'videojuego': videojuego, 'usuario_nombre': usuario_nombre})



def search_videojuegos(request):
    usuario = None
    videojuegos = []
    usuario_id = request.GET.get('usuario_id')

    if usuario_id:
        try:
            response_usuario = requests.get(f'http://localhost:8080/usuarios/{usuario_id}')
            if response_usuario.status_code == 200:
                usuario = response_usuario.json()
            else:
                messages.error(request, 'Usuario no encontrado.')
        except requests.RequestException as e:
            messages.error(request, str(e))

    if usuario:
        params = {
            'id': request.GET.get('id'),
            'nombre': request.GET.get('nombre'),
            'precio': request.GET.get('precio'),
            'multijugador': request.GET.get('multijugador'),
        }

        params = {k: v for k, v in params.items() if v is not None and v != ""}

        try:
            response = requests.get(f'http://localhost:8080/videojuegos/usuario/{usuario_id}', params=params)
            if response.status_code == 200:
                videojuegos = response.json()
            else:
                messages.error(request, "No se encontraron videojuegos con los criterios proporcionados.")
        except requests.RequestException as e:
            messages.error(request, str(e))

    return render(request, 'crudApp/CrudVideojuego/SearchV.html', {
        'usuario': usuario,
        'videojuegos': videojuegos,
        'usuario_id': usuario_id,
    })

def add_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            form_data['fechaNacimiento'] = form_data['fechaNacimiento'].strftime('%Y-%m-%dT%H:%M')
            # Guarda el usuario en el backend de Spring Boot
            response = requests.post('http://localhost:8080/usuarios', json=form_data, headers={'Content-Type': 'application/json'})
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


def delete_usuario(request):
    form = UsuarioForm(request.POST or None)

    if request.method == 'POST':
        if 'confirm_delete' in request.POST:
            usuario_id = request.POST.get('id')
            if form.is_valid() and usuario_id:
                response = requests.delete(f'http://localhost:8080/usuarios/{usuario_id}')
                if response.status_code == 200:
                    messages.success(request, 'El usuario se ha eliminado con éxito.')
                    return redirect('delete_usuario')
                else:
                    print(f'Error al eliminar usuario: {response.status_code}')
                    messages.error(request, f'Error al eliminar el usuario en el backend de Spring Boot. '
                                            f'Código de estado: {response.status_code}')
            else:
                print('El formulario no es válido o no se proporcionó ID de usuario.')
        else:
            print('La confirmación de eliminación no se recibió.')

    # GET request: Búsqueda de usuario para mostrar en el formulario
    elif request.method == 'GET':
        usuario_id = request.GET.get('id')
        if usuario_id:
            response = requests.get(f'http://localhost:8080/usuarios/{usuario_id}')

            if response.status_code == 200:
                usuario_data = response.json()
                form = UsuarioForm(initial=usuario_data)
            else:
                messages.error(request, f'Error al obtener los datos del usuario del backend de Spring Boot. '
                                        f'Código de estado: {response.status_code}')
                print(f'Error al buscar usuario: {response.status_code}')

    # Independientemente del método, siempre renderizamos la misma plantilla.
    return render(request, 'crudApp/CrudUsuario/DeleteU.html', {'form': form})


def view_usuario(request):
    filtro_premium = request.GET.get('premium')
    params = {}

    if filtro_premium and filtro_premium != 'todos':
        if filtro_premium == 'premium':
            params['esPremium'] = True
        elif filtro_premium == 'no_premium':
            params['esPremium'] = False

    response = requests.get('http://localhost:8080/usuarios', params=params)
    if response.status_code == 200:
        usuarios = response.json()
    else:
        messages.error(request, 'Error al obtener los usuarios: ' + str(response.status_code))
        usuarios = []

    return render(request, 'crudApp/CrudUsuario/ReadU.html', {
        'usuarios': usuarios,
        'filter_premium': filtro_premium
    })

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
                #del form_data['id']
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
                response = requests.get(f'http://localhost:8080/usuarios/{usuario_id}')


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

def buscar_usuario(request):
        usuarios = []
        base_url = "http://localhost:8080/usuarios"

        if request.GET:
            params = request.GET.dict()
            if 'esPremium' in params:
                params['esPremium'] = True if params['esPremium'].lower() == 'si' else False

            response = requests.get(base_url, params=params)
            print("Respuesta de la API:", response.status_code, response.text)

            if response.status_code == 200:
                # Aquí asumimos que la respuesta podría ser un solo objeto o una lista
                data = response.json()
                if isinstance(data, dict):  # Si es un diccionario, lo convertimos en una lista
                    usuarios = [data]
                elif isinstance(data, list):
                    usuarios = data
                else:
                    print("Formato de respuesta no reconocido")
            else:
                print("Error en la solicitud API:", response.status_code, response.text)

        return render(request, 'crudApp/search.html', {'usuarios': usuarios})

def about_view(request):
    nombres_integrantes = [
        "Manuel",
        "Mariana",
        "Juan",
        "Sebastian"
    ]
    return render(request, 'crudApp/about.html', {'nombres_integrantes': nombres_integrantes})

