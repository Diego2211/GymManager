from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.conf import settings

# Create your models here.

class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Gym(models.Model):

    nombre = models.CharField(max_length=50)

    slug = models.SlugField(unique=True, blank=True)

    direccion = models.CharField(max_length=50)

    telefono = models.CharField(max_length=20)

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gym_propietario"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.clase)
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

    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    nombre = models.CharField(max_length=40, blank=True)

    apellido = models.CharField(max_length=40, blank=True)

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


class Membership(BaseModel):

    ROLES = [
        ("admin", "Admin Gym"),
        ("profesor", "Profesor"),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)

    rol = models.CharField(max_length=20, choices=ROLES)

    activo = models.BooleanField(default=True)

    fecha_union = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["usuario", "gym"]

