from django import forms
from .models import Alumnos, Profesores, Inscripciones, Clases
from django.contrib.auth.forms import AuthenticationForm


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


class login_usuario(AuthenticationForm):
    username = forms.CharField(label="usuario")
    password = forms.CharField(label="contraseña", widget=forms.PasswordInput)


class inscripcion_form(forms.ModelForm):
    class Meta:
        model = Inscripciones
        fields = ["alumno", "clase"]


class crear_clase_form(forms.ModelForm):
    
    class Meta:
        model = Clases
        fields = '__all__'
        exclude = ['slug']