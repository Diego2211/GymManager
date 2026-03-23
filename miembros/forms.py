from django import forms
from .models import Alumnos, Inscripciones, Clases
from accounts.models import Membership


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })


class ingreso_usuario(BaseForm):
    class Meta:
        model = Alumnos
        fields = ["nombre", "apellido", "dni", "celular"]


class inscripcion_form(BaseForm):
    class Meta:
        model = Inscripciones
        fields = ["alumno", "clase"]

    def __init__(self, *args, **kwargs):
        gym = kwargs.pop("gym", None)
        super().__init__(*args, **kwargs)

        if gym:
            self.fields["alumno"].queryset = Alumnos.objects.filter(gym=gym)
            self.fields["clase"].queryset = Clases.objects.filter(gym=gym)


class crear_clase_form(BaseForm):
    
    class Meta:
        model = Clases
        fields = ["clase", "profesor", "dia", "cuota_mensual"]
        exclude = ['slug']

    def __init__(self, *args, **kwargs):
        gym = kwargs.pop("gym", None)
        super().__init__(*args, **kwargs)

        if gym:
            self.fields["profesor"].queryset = Membership.objects.filter(gym=gym, activo=True)