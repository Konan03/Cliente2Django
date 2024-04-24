from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    id = forms.IntegerField(label='ID', required=False)
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
