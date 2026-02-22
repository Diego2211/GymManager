from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Profesores(models.Model):

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    nombre = models.CharField(max_length=40)

    apellido = models.CharField(max_length=40)

    dni = models.CharField(max_length=9)

    celular = models.CharField(max_length=20)

    fecha_alta = models.DateField(auto_now_add=True)



class Alumnos(models.Model):

    nombre = models.CharField(max_length=40)

    apellido = models.CharField(max_length=40)

    dni = models.CharField(max_length=9)

    celular = models.CharField(max_length=20)

    fecha_alta = models.DateField(auto_now_add=True)



class Clases(models.Model):

    clase = models.CharField(max_length=30)

    slug = models.SlugField(unique=True, blank=True)

    horario = models.CharField(max_length=50)

    profesor = models.ForeignKey(Profesores, on_delete=models.CASCADE)

    cuota_mensual = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.clase)
            slug = base_slug
            contador = 1
            while Clases.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{contador}"
                contador += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Inscripciones(models.Model):

    clase = models.ForeignKey(Clases, on_delete=models.CASCADE)

    alumno = models.ForeignKey(Alumnos, on_delete=models.CASCADE)

    fecha_inscripcion = models.DateField(auto_now_add=True)
    
    activo = models.BooleanField(default=True)



class Pagos(models.Model):

    Inscripcion = models.ForeignKey(Inscripciones, on_delete=models.CASCADE)

    fecha_pago = models.DateField()

    monto = models.DecimalField(max_digits=10, decimal_places=2)

    mes_correspondiente = models.CharField(max_length=20)


class Avisos(models.Model):
    inscripcion = models.ForeignKey(Inscripciones, on_delete=models.CASCADE)

    tipo = models.CharField(
        max_length=20,
        choices=[
            ('vencimiento', 'Próximo a vencer'),
            ('impago', 'Cuota impaga')
        ]
    )

    mensaje = models.TextField()

    fecha_generado = models.DateTimeField(auto_now_add=True)

    visto_por_profesor = models.BooleanField(default=False)

    fecha_visto = models.DateTimeField(null=True, blank=True)