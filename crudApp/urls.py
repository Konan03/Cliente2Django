from django.urls import path
from .views import  home, UserView, VideogameView, AboutView, delete_usuario, view_usuario, \
    update_usuario
from .views import add_usuario
from .views import seleccionar_usuario,add_videojuego,read_videojuegos,update_videojuego, delete_videojuego, search_videojuegos

urlpatterns = [
    path('', home, name='home'),  # La URL base para la página de inicio
    path('usuario/', UserView.as_view(), name='usuario'),  # Para la página general de usuario donde estarán los botones de CRUD
    path('videojuego/', VideogameView.as_view(), name='videojuego'),  # Para la sección de videojuegos
    path('about/', AboutView.as_view(), name='about'),  # Para la página de "Acerca de"
    path('usuario/crear/', add_usuario, name='add_usuario'),
    path('usuarios/seleccionar/', seleccionar_usuario, name='seleccionar_usuario'),
    path('videojuego/add/<int:usuario_id>/', add_videojuego, name='add_videojuego'),
    path('videojuego/read/', read_videojuegos, name='read_videojuegos'),
    path('videojuego/update/', update_videojuego, name='update_videojuego'),
    path('videojuego/delete/', delete_videojuego, name='delete_videojuego'),
    path('videojuego/search/', search_videojuegos, name='search_videojuegos'),
    path('usuario/eliminar/', delete_usuario, name='delete_usuario'),
    path('usuario/verUsuarios/', view_usuario, name='view_usuario'),
    path('usuario/ActualizarUsuarios/', update_usuario, name='update_usuario'),
]
