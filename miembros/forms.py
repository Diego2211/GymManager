from django import forms
from .models import Alumnos, Inscripciones, Clases


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


class inscripcion_form(forms.ModelForm):
    class Meta:
        model = Inscripciones
        fields = ["alumno", "clase"]


class crear_clase_form(forms.ModelForm):
    
    class Meta:
        model = Clases
        fields = '__all__'
        exclude = ['slug']