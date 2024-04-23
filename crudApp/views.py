from django.shortcuts import render

# Create your views here.
import requests
from django.shortcuts import render

def lista_usuarios(request):
    response = requests.get('http://localhost:8080/usuarios')
    usuarios = response.json()
    return render(request, 'miApp/lista_usuarios.html', {'usuarios': usuarios})
