from django import forms
from .models import Alumnos, Profesores


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })


class ingreso_usuario(forms.ModelForm):
    class Meta:
        model = Alumnos
        fields = '__all__'


class ingreso_profesor(forms.ModelForm):
    username = forms.CharField(label="usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="contraseña")
    email = forms.EmailField(label="Correo")
    class Meta:
        model = Profesores
        fields = '__all__'
        exclude = ['usuario']