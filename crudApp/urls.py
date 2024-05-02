from django.urls import path
from .views import lista_usuarios, home, UserView, VideogameView, AboutView, delete_usuario, view_usuario, \
    update_usuario, SearchView, buscar_usuario
from .views import add_usuario



urlpatterns = [
    path('', home, name='home'),  # La URL base para la página de inicio
    path('usuarios/', lista_usuarios, name='lista_usuarios'),  # Para mostrar la lista de usuarios
    path('usuario/', UserView.as_view(), name='usuario'),  # Para la página general de usuario donde estarán los botones de CRUD
    path('videojuego/', VideogameView.as_view(), name='videojuego'),  # Para la sección de videojuegos
    path('about/', AboutView.as_view(), name='about'),  # Para la página de "Acerca de"
    path('search/', buscar_usuario, name='buscar_usuario'),
    path('usuario/crear/', add_usuario, name='add_usuario'),
    path('usuario/eliminar/', delete_usuario, name='delete_usuario'),
    path('usuario/verUsuarios/', view_usuario, name='view_usuario'),
    path('usuario/ActualizarUsuarios/', update_usuario, name='update_usuario'),
]
