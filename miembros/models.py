from django.db import models
from accounts.models import Gym, Membership
from django.utils.text import slugify
from django.conf import settings
from datetime import date

# Create your models here.
class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Alumnos(BaseModel):
    
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)

    nombre = models.CharField(max_length=40)

    apellido = models.CharField(max_length=40)

    dni = models.CharField(max_length=9, unique=True)

    celular = models.CharField(max_length=20)

    fecha_alta = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"



class Clases(BaseModel):

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)

    clase = models.CharField(max_length=30)

    slug = models.SlugField()

    profesor = models.ForeignKey(Membership, on_delete=models.CASCADE)

    cuota_mensual = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.clase)
            slug = base_slug
            contador = 1
            while Clases.objects.filter(slug=slug, gym=self.gym).exists():
                slug = f"{base_slug}-{contador}"
                contador += 1
            self.slug = slug
        super().save(*args, **kwargs)
    

    def __str__(self):
        prof = self.profesor.usuario.perfil
        return f"{self.clase} - {prof.nombre} {prof.apellido}"
    
    class Meta:
        unique_together = ["gym", "slug"]


class Horario(BaseModel):
    DIAS = [
        ("lunes", "Lunes"),
        ("martes", "Martes"),
        ("miercoles", "Miércoles"),
        ("jueves", "Jueves"),
        ("viernes", "Viernes"),
        ("sabado", "Sábado"),
        ("domingo", "Domingo"),
    ]

    clase = models.ForeignKey(Clases, on_delete=models.CASCADE, related_name="horarios")

    dia = models.CharField(max_length=20, choices=DIAS)

    hora_inicio = models.TimeField()
    
    hora_fin = models.TimeField()


class Inscripciones(BaseModel):

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)

    clase = models.ForeignKey(Clases, on_delete=models.CASCADE)

    alumno = models.ForeignKey(Alumnos, on_delete=models.CASCADE)

    fecha_inscripcion = models.DateField(auto_now_add=True)

    fecha_vencimiento = models.DateField(db_index=True, null=True)

    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.SET_NULL,
                                   null=True)
    
    activo = models.BooleanField(default=True)

    @property
    def esta_al_dia(self):
        hoy = date.today()

        return Pagos.objects.filter(
            inscripcion=self,
            fecha_fin__gte=hoy
            ).exists()
    
    def deuda(self):

        hoy = date.today()
    
        # Buscar si hay un pago vigente (fecha_fin >= hoy)
        pagos_periodo = Pagos.objects.filter(
            inscripcion=self,
            fecha_fin__gte=hoy
            )
    
        if not pagos_periodo.exists():
            return None  # No hay pago reciente, no mostramos deuda parcial
    
        # Sumar todos los pagos del período vigente
        from django.db.models import Sum
        total_pagado = pagos_periodo.aggregate(Sum('monto'))['monto__sum'] or 0
    
        diferencia = self.clase.cuota_mensual - total_pagado
        return diferencia if diferencia > 0 else None

    class Meta:
        unique_together = ["clase", "alumno"]



class Pagos(models.Model):

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    inscripcion = models.ForeignKey(Inscripciones, on_delete=models.CASCADE)

    fecha_pago = models.DateField(auto_now_add=True)

    fecha_inicio = models.DateField(default= None)
    fecha_fin = models.DateField(default=None)

    monto = models.DecimalField(max_digits=10, decimal_places=2)

    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.inscripcion} ({self.fecha_inicio} - {self.fecha_fin})"
    


class Avisos(BaseModel):

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)

    inscripcion = models.ForeignKey(Inscripciones, on_delete=models.CASCADE)

    tipo = models.CharField(max_length=50)

    mensaje = models.TextField()

    fecha_generado = models.DateTimeField(auto_now_add=True)

    visto_por_profesor = models.BooleanField(default=False)

    fecha_visto = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["inscripcion", "tipo"]