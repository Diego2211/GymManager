from django import forms
from .models import Gym, Perfil_usuario
from django.contrib.auth.forms import AuthenticationForm

class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

class registro_form(BaseForm):
    class Meta():
        model = Gym

        
class login_form(BaseForm):
    class Meta():
        model = Perfil_usuario