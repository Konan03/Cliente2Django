<<<<<<< HEAD
"""
URL configuration for Cliente2Django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crudApp.urls')),
]

=======
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # La URL base ahora apunta a la vista 'home'
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
]
>>>>>>> 06b1a376af08a6721e7b7d4a4a90177d4238fbfe
