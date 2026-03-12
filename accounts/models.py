from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Admin_gym(models.Model):

    nombre = models.CharField(max_length=50)

    direccion = models.CharField(max_length=50)

    telefono = models.CharField(max_length=20)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre}"

class Perfil_usuario(models.Model):

    gym = models.ForeignKey(Admin_gym, on_delete=models.CASCADE)

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    nombre = models.CharField(max_length=40)

    apellido = models.CharField(max_length=40)

    dni = models.CharField(max_length=9)

    email = models.CharField(max_length=50)

    celular = models.CharField(max_length=20)

    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre}"