from django import forms
from .models import Usuario, Videojuego


class UsuarioForm(forms.ModelForm):
    id = forms.IntegerField(label='ID', required=False)  # Campo para el ID del usuario
    class Meta:
        model = Usuario
        fields = ['id','nombre', 'estatura', 'fechaNacimiento', 'esPremium']  # Asumiendo que manejas videojuegos de otra manera
        widgets = {
            'fechaNacimiento': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'esPremium': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.fields['fechaNacimiento'].input_formats = ('%Y-%m-%dT%H:%M',)


class VideojuegoForm(forms.ModelForm):
    usuario_id = forms.IntegerField(widget=forms.HiddenInput(), required=True)
    id = forms.IntegerField(required=True)

    class Meta:
        model = Videojuego
        fields = ['id', 'nombre', 'precio', 'multijugador', 'fechaLanzamiento', 'usuario_id']
        widgets = {
            'multijugador': forms.Select(choices=[(True, 'Sí'), (False, 'No')]),
            'fechaLanzamiento': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super(VideojuegoForm, self).__init__(*args, **kwargs)
        self.fields['fechaLanzamiento'].input_formats = ('%Y-%m-%dT%H:%M',)
