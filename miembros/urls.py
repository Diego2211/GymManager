from miembros.views import index, miembros, profesores, clases, clase, ingreso_miembro, inscribir_alumno, crear_clase
from django.urls import path

urlpatterns = [
    path('', index),
    path('miembros/', miembros),
    path('profesores/', profesores),
    path('clases/', clases),
    path('clases/<slug:slug>/', clase, name="clase"),
    path('ingreso-alumnos/', ingreso_miembro,),
    path('inscribir-alumno/', inscribir_alumno),
    path('crear-clase/', crear_clase)
]