from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # La URL base ahora apunta a la vista 'home'
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
]