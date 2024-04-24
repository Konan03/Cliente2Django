from django import forms
from .models import Usuario
from .models import Videojuego

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'estatura', 'fecha_nacimiento', 'es_premium']  # Asumiendo que manejas videojuegos de otra manera
        widgets = {
            'fecha_nacimiento': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'es_premium': forms.Select(choices=[(True, 'Sí'), (False, 'No')]),
        }

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.fields['fecha_nacimiento'].input_formats = ('%Y-%m-%dT%H:%M',)

class VideojuegoForm(forms.ModelForm):
    id = forms.IntegerField(label='ID', required=False)  # Campo para el ID del videojuego

    class Meta:
        model = Videojuego
        fields = ['id', 'nombre', 'precio', 'multijugador', 'fechaLanzamiento']
        widgets = {
            'multijugador': forms.Select(choices=[(True, 'Sí'), (False, 'No')]),
            'fechaLanzamiento': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super(VideojuegoForm, self).__init__(*args, **kwargs)
        self.fields['fechaLanzamiento'].input_formats = ('%Y-%m-%dT%H:%M',)

