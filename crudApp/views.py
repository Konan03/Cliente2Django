from django.http import HttpResponse
from django.views.decorators.cache import never_cache
import requests
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages  # Importa el módulo de mensajes
from .forms import UsuarioForm
from django.shortcuts import render
import json
from django.core.serializers.json import DjangoJSONEncoder

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
        return render(request, 'videojuego.html')

class AboutView(View):
    def get(self, request):
        return render(request, 'crudApp/about.html')

class SearchView(View):
    def get(self, request):
        return render(request, 'crudApp/search.html')


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
            response = requests.get(f'http://localhost:8080/usuarios', params={'id': usuario_id})
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
    response = requests.get('http://localhost:8080/usuarios')
    if response.ok:
        usuarios = response.json()
        return render(request, 'crudApp/CrudUsuario/ReadU.html', {'usuarios': usuarios})
    else:
        return HttpResponse('Error al obtener los usuarios: ' + str(response.status_code))


import requests
from django.http import JsonResponse

import requests
from django.shortcuts import render
from django.http import JsonResponse

import requests
from django.http import JsonResponse


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

import requests
from django.shortcuts import render

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




