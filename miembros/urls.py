from miembros.views import index, miembros, profesores, clases, clase, ingreso_miembro, ingreso_prof, inscribir_alumno, iniciar_sesion, crear_clase
from django.urls import path

urlpatterns = [
    path('', index),
    path('miembros/', miembros),
    path('profesores/', profesores),
    path('clases/', clases),
    path('clases/<slug:slug>/', clase, name="clase"),
    path('ingreso-alumnos/', ingreso_miembro,),
    path('ingreso-profesor/', ingreso_prof),
    path('iniciar-sesion/', iniciar_sesion),
    path('inscribir-alumno/', inscribir_alumno),
    path('crear-clase/', crear_clase)
]