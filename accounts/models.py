from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.core.exceptions import ValidationError
import random, string


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("El usuario debe tener un email")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save(using=self._db)

        return user


    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)
# Create your models here.

class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Gym(BaseModel):

    nombre = models.CharField(max_length=50, blank=True)

    slug = models.SlugField(unique=True, blank=True)

    direccion = models.CharField(max_length=50, blank=True)

    telefono = models.CharField(max_length=20, blank= True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nombre)
            slug = base_slug
            contador = 1
            while Gym.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{contador}"
                contador += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre}"



class Perfil_usuario(BaseModel):

    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil")

    nombre = models.CharField(max_length=40, blank=True)

    apellido = models.CharField(max_length=40, blank=True)

    gym_activo = models.ForeignKey(Gym, null=True, on_delete=models.SET_NULL)

    dni = models.CharField(max_length=9, blank=True)

    celular = models.CharField(max_length=20, blank=True)

    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre}"
    
class User(AbstractUser):

    username = None

    email = models.EmailField(unique=True)

    fecha_registro = models.DateField(auto_now_add=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = UserManager()






class Invitacion(BaseModel):
    ROLES = [
            ("Admin_Gym", "Administrador"),
            ("profesor", "Profesor"),
    ]

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)

    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    codigo = models.CharField(max_length=20, unique=True)

    rol = models.CharField(max_length=20, choices=ROLES)

    activa = models.BooleanField(default=True)

    usos_maximos = models.IntegerField(default=1)

    usos_actuales = models.IntegerField(default=0)

    expira_en = models.DateTimeField(null=True, blank=True)

    def esta_expirada(self):
        return self.expira_en and timezone.now() > self.expira_en

    def puede_usarse(self):
        return self.activa and self.usos_actuales < self.usos_maximos and not self.esta_expirada()
    
    def registrar_uso(self):

        if not self.puede_usarse():
            raise ValueError("Invitacion no valida")
        
        self.usos_actuales += 1

        if self.usos_maximos >= self.usos_actuales:
            self.activa = False

        self.save()

    def generar_codigo_legible(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def estado(self):
        if self.esta_expirada():
            return "expirada"
        elif self.usos_actuales >= self.usos_maximos:
            return "sin_usos"
        elif self.activa:
            return "activa"
        return "inactiva"

    def save(self, *args, **kwargs):
        if not self.codigo:
            while True:
                try:
                    self.codigo = self.generar_codigo_legible()
                    super().save(*args, **kwargs)
                    break
                except IntegrityError:
                    continue
        else:
            super().save(*args, **kwargs)


class Membership(BaseModel):

    ROLES = [
            ("owner", "Dueño"),
            ("Admin_Gym", "Administrador"),
            ("profesor", "Profesor"),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)

    rol = models.CharField(max_length=20, choices=ROLES)

    activo = models.BooleanField(default=True)

    fecha_union = models.DateTimeField(auto_now_add=True)

    invitacion = models.ForeignKey(Invitacion, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.perfil_usuario.nombre} {self.usuario.perfil_usuario.apellido} - {self.rol}"

    class Meta:
        unique_together = ["usuario", "gym"]

    def clean(self):
        if self.Invitacion and self.invitacion.gym != self.gym:
            raise ValidationError("Esta invitacion no pertenece a este gym")
