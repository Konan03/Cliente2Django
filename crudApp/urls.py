from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),  # La URL base ahora apunta a la vista 'home'
]