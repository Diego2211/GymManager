from django import forms
from .models import Alumnos, Inscripciones, Clases, Horario
from accounts.models import Membership
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.core.exceptions import ValidationError


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
        fields = ["clase", "profesor", "cuota_mensual"]
        exclude = ['slug']

    def __init__(self, *args, **kwargs):
        gym = kwargs.pop("gym", None)
        super().__init__(*args, **kwargs)

        if gym:
            self.fields["profesor"].queryset = Membership.objects.filter(gym=gym, activo=True)


class Horario_Form(forms.ModelForm):


    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get("hora_inicio")
        fin = cleaned_data.get("hora_fin")

        if inicio and fin and inicio >= fin:
            raise forms.ValidationError("La hora de fin debe ser mayor a la de inicio")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hora_inicio'].input_formats = ['%H:%M']
        self.fields['hora_fin'].input_formats = ['%H:%M']


    class Meta:
        model = Horario
        fields = ['dia', 'hora_inicio', 'hora_fin']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'},format='%H:%M'),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        }

    
    
class BaseHorarioFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        count = 0

        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                count += 1

        if count < 1:
            raise ValidationError("Debe existir al menos un horario")

Horario_FormSet = inlineformset_factory(
    Clases,
    Horario,
    form=Horario_Form,
    formset=BaseHorarioFormSet,
    extra=1,
    can_delete=True
)