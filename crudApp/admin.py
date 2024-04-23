from django.contrib import admin

# Register your models here.
from .models import Usuario, Videojuego

admin.site.register(Usuario)
admin.site.register(Videojuego)
