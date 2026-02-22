from django import forms

class ingreso_usuario(forms.Form):
    nombre = forms.CharField(max_length=40, label="Ingrese el nombre o nombres",)

    apellido = forms.CharField(max_length=40, label="ingrese el apellido o apellidos")

    dni = forms.CharField(max_length=9, label="ingrese el dni, sin puntos ni comas")

    celular = forms.CharField(max_length=20, label="ingrese el nro de celular sin guiones ni espacios")