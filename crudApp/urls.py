from django.urls import path
from .views import lista_usuarios, home, UserView, VideogameView, AboutView
from .views import add_usuario
from .views import seleccionar_usuario,add_videojuego,read_videojuegos,update_videojuego




urlpatterns = [
    path('', home, name='home'),  # La URL base para la página de inicio
    path('usuarios/', lista_usuarios, name='lista_usuarios'),  # Para mostrar la lista de usuarios
    path('usuario/', UserView.as_view(), name='usuario'),  # Para la página general de usuario donde estarán los botones de CRUD
    path('videojuego/', VideogameView.as_view(), name='videojuego'),  # Para la sección de videojuegos
    path('about/', AboutView.as_view(), name='about'),  # Para la página de "Acerca de"
    path('usuario/crear/', add_usuario, name='add_usuario'),
    path('usuarios/seleccionar/', seleccionar_usuario, name='seleccionar_usuario'),
    path('videojuego/add/<int:usuario_id>/', add_videojuego, name='add_videojuego'),
    path('videojuego/read/', read_videojuegos, name='read_videojuegos'),
    path('videojuego/update/', update_videojuego, name='update_videojuego'),


]
