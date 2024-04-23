from django.urls import path
from .views import lista_usuarios, home, UserView, VideogameView, AboutView
from .views import add_usuario



urlpatterns = [
    path('', home, name='home'),  # La URL base para la página de inicio
    path('usuarios/', lista_usuarios, name='lista_usuarios'),  # Para mostrar la lista de usuarios
    path('usuario/', UserView.as_view(), name='usuario'),  # Para la página general de usuario donde estarán los botones de CRUD
    path('videojuego/', VideogameView.as_view(), name='videojuego'),  # Para la sección de videojuegos
    path('about/', AboutView.as_view(), name='about'),  # Para la página de "Acerca de"
    path('usuario/crear/', add_usuario, name='add_usuario'),
]
