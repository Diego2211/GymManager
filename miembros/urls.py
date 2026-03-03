from miembros.views import index, miembros, profesores, clases, clase, ingreso_miembro, ingreso_prof
from django.urls import path

urlpatterns = [
    path('', index),
    path('miembros/', miembros),
    path('profesores/', profesores),
    path('clases/', clases),
    path('clases/<slug:slug>/', clase, name="clase"),
    path('ingreso-alumnos/', ingreso_miembro,),
    path('ingreso-profesor/', ingreso_prof)
]