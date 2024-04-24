from django.db import models

# Create your models here.
import datetime


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    estatura = models.FloatField()
    fechaNacimiento = models.DateTimeField(default=datetime.datetime.now)
    esPremium = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class Videojuego(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    multijugador = models.BooleanField(default=False)
    fecha_lanzamiento = models.DateTimeField(default=datetime.datetime.now)
    usuario = models.ForeignKey(Usuario, related_name='videojuegos', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
