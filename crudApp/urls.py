from django.urls import path
from . import views
from .views import UserView, VideogameView, AboutView  # Importar las vistas desde el módulo actual

urlpatterns = [
    path('', views.home, name='home'),  # La URL base ahora apunta a la vista 'home'
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuario/', UserView.as_view(), name='usuario'),  # Usar las vistas importadas directamente
    path('videojuego/', VideogameView.as_view(), name='videojuego'),
    path('about/', AboutView.as_view(), name='about'),
]