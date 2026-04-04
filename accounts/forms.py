from django import forms
from .models import Gym, Perfil_usuario, User, Invitacion, Membership
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })


class inicio_sesion_form(AuthenticationForm):
    username = forms.EmailField(label="Email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

        
class perfil_form(BaseForm):
    class Meta():
        model = Perfil_usuario
        fields = "__all__"
        exclude = ["usuario", "gym_activo"]


class registro_form(BaseForm):

    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise ValidationError("Las contraseñas no coinciden")

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user
    

class gym_form(BaseForm):

    class Meta:
        model = Gym
        exclude = ['slug']


class invitacion_form(BaseForm):
    EXPIRACION_CHOICES = [
        ("1h", "1 hora"),
        ("24h", "24 horas"),
        ("7d", "7 días"),
    ]

    expiracion = forms.ChoiceField(choices=EXPIRACION_CHOICES)

    class Meta:
        model = Invitacion
        exclude = ['codigo', 'gym', 'usos_actuales', 'activa', 'creado_por', 'expira_en']
