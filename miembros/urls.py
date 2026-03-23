from miembros.views import index, miembros, clases, clase, ingreso_miembro, inscribir_alumno, crear_clase
from django.urls import path

urlpatterns = [
    path('', index, name="index"),
    path('miembros/', miembros),
    path('clases/', clases),
    path('clases/<slug:slug>/', clase, name="clase"),
    path('ingreso-alumnos/', ingreso_miembro,),
    path('inscribir-alumno/', inscribir_alumno),
    path('crear-clase/', crear_clase),
]