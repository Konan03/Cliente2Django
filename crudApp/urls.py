# crudApp/urls.py
from django.urls import path
from .views import lista_usuarios  # Asegúrate de que estás importando la vista correctamente

urlpatterns = [
    path('', lista_usuarios, name='lista_usuarios.html'),  # Esto manejará la ruta 'usuarios/'
]
