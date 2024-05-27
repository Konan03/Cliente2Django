from django import forms
from .models import Usuario, Videojuego


class UsuarioForm(forms.ModelForm):
    id = forms.IntegerField(label='ID', required=False)  # Campo para el ID del usuario
    class Meta:
        model = Usuario
        fields = ['id','nombre', 'estatura', 'fechaNacimiento', 'esPremium']  # Asumiendo que manejas videojuegos de otra manera
        widgets = {
            'fechaNacimiento': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'esPremium':  forms.Select(choices=[(True, 'Sí'), (False, 'No')]),
        }

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.fields['fechaNacimiento'].input_formats = ('%Y-%m-%dT%H:%M',)


class VideojuegoCreateForm(forms.ModelForm):
    usuario_id = forms.IntegerField(widget=forms.HiddenInput(), required=True)
    id = forms.IntegerField(required=True)  # Campo editable para la creación

    class Meta:
        model = Videojuego
        fields = ['id', 'nombre', 'precio', 'multijugador', 'fechaLanzamiento', 'usuario_id']
        widgets = {
            'multijugador': forms.Select(choices=[(True, 'Sí'), (False, 'No')]),
            'fechaLanzamiento': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super(VideojuegoCreateForm, self).__init__(*args, **kwargs)
        self.fields['fechaLanzamiento'].input_formats = ('%Y-%m-%dT%H:%M',)



class VideojuegoUpdateForm(forms.ModelForm):
    usuario_id = forms.IntegerField(widget=forms.HiddenInput(), required=True)
    id = forms.IntegerField(widget=forms.HiddenInput(), required=True)  # Campo oculto para la actualización

    class Meta:
        model = Videojuego
        fields = ['id', 'nombre', 'precio', 'multijugador', 'fechaLanzamiento', 'usuario_id']
        widgets = {
            'multijugador': forms.Select(choices=[(True, 'Sí'), (False, 'No')]),
            'fechaLanzamiento': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super(VideojuegoUpdateForm, self).__init__(*args, **kwargs)
        self.fields['fechaLanzamiento'].input_formats = ('%Y-%m-%dT%H:%M',)
