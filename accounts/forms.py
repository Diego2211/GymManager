from django import forms
from .models import Gym, Perfil_usuario, User
from django.contrib.auth.forms import AuthenticationForm

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })


class inicio_sesion_form(AuthenticationForm):
    username = forms.EmailField(label="Email")

        
class perfil_form(BaseForm):
    class Meta():
        model = Perfil_usuario
        fields = "__all__"
        exclude = ["usuario"]


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
            raise forms.ValidationError("Las contraseñas no coinciden")

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
