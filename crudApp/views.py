from django.shortcuts import render, redirect
import requests
from django.contrib import messages


def lista_usuarios(request):
    response = requests.get('http://localhost:8080/usuarios')
    usuarios = response.json()
    return render(request, 'miApp/lista_usuarios.html', {'usuarios': usuarios})

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def user(request):
    # Aquí iría la lógica para obtener la información del usuario de Spring Boot
    return render(request, 'user.html')

def crear_usuario(request):
    if request.method == 'POST':
        # Recuperar los datos del formulario enviado por el usuario
        nombre = request.POST.get('nombre')
        estatura = request.POST.get('estatura')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        es_premium = request.POST.get('es_premium')

        # Validar los datos del formulario (puedes hacerlo aquí o en un formulario Django separado)

        # Crear un diccionario con los datos del usuario
        nuevo_usuario = {
            'nombre': nombre,
            'estatura': float(estatura),
            'fechaNacimiento': fecha_nacimiento,
            'esPremium': es_premium == 'on'  # Convertir el valor de 'es_premium' a booleano
        }

        # Enviar una solicitud POST al endpoint correspondiente en tu servidor Spring Boot
        try:
            response = requests.post('URL_DEL_ENDPOINT_PARA_CREAR_USUARIO', json=nuevo_usuario)

            # Verificar si la solicitud fue exitosa (código de estado HTTP 201)
            if response.status_code == 201:
                # Mostrar un mensaje de éxito al usuario
                messages.success(request, '¡Usuario creado exitosamente!')
                return redirect('nombre_de_la_url_a_la_que_redirigir_después_de_crear_el_usuario')
            else:
                # Mostrar un mensaje de error al usuario
                messages.error(request, 'Error al crear el usuario. Por favor, inténtelo de nuevo.')
        except requests.exceptions.RequestException as e:
            # Si ocurre un error de conexión, mostrar un mensaje de error al usuario
            messages.error(request, 'Error de conexión. Por favor, inténtelo de nuevo más tarde.')

    # Si la solicitud no es POST o si hay errores, renderizar el formulario para crear un usuario
    return render(request, 'crear_usuario.html')

def videogame(request):
    # Aquí iría la lógica para obtener la información de videojuegos de Spring Boot
    return render(request, 'videogame.html')

def about(request):
    return render(request, 'about.html')

