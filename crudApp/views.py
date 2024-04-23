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
        return render(request, 'about.html')


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
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario_id = form.cleaned_data['id']
            form_data = form.cleaned_data
            # Eliminamos el id del formulario para que no se incluya al actualizar
            del form_data['id']
            response = requests.put(f'http://localhost:8080/usuarios/{usuario_id}', json=form_data,
                                    headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                messages.success(request, 'El usuario se ha actualizado con éxito')
                return redirect('update_usuario')
            else:
                messages.error(request, 'Error al actualizar el usuario en el backend de Spring Boot')
    else:
        # Obtener el ID del usuario desde la solicitud GET
        usuario_id = request.GET.get('search')
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
                messages.error(request, 'Error al obtener los datos del usuario del backend de Spring Boot')
                return redirect('update_usuario')
        else:
            form = UsuarioForm()
    return render(request, 'crudApp/CrudUsuario/UpdateU.html', {'form': form})



