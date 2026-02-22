from django.contrib import admin
from .models import Alumnos, Profesores, Pagos, Clases, Inscripciones, Avisos
# Register your models here.

admin.site.register(Alumnos)
admin.site.register(Profesores)
admin.site.register(Pagos)
admin.site.register(Clases)
admin.site.register(Inscripciones)
admin.site.register(Avisos)