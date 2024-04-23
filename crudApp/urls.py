# Cliente2Django/urls.py
from django.contrib import admin
from django.urls import path, include
from crudApp import views  # Importa la vista

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('crudApp.urls')),  # Incluye las URLs de la aplicación crudApp
    path('', views.lista_usuarios, name='home'),  # Redirige la ruta raíz directamente a la vista lista_usuarios
]
