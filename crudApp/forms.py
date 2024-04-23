from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'estatura', 'fecha_nacimiento', 'es_premium']  # Asumiendo que manejas videojuegos de otra manera
        widgets = {
            'fecha_nacimiento': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'es_premium': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.fields['fecha_nacimiento'].input_formats = ('%Y-%m-%dT%H:%M',)
