from miembros.views import index, miembros, clases, clase, ingreso_miembro, inscribir_alumno, crear_clase, profesores
from django.urls import path

urlpatterns = [
    path('', index, name="index"),
    path('miembros/', miembros, name="miembros"),
    path('clases/', clases, name="clases"),
    path('clases/<slug:slug>/', clase, name="clase"),
    path('ingreso-alumnos/', ingreso_miembro, name="ingreso alumnos"),
    path('inscribir-alumno/', inscribir_alumno, name="inscripcion"),
    path('crear-clase/', crear_clase, name="crear clase"),
    path("profesores/", profesores, name="profesores")
]