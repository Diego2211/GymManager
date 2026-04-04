from miembros.views import index, miembros, clases, clase, ingreso_miembro, inscribir_alumno, crear_clase, profesores, eventos, ver_calendario, avisos, editar_inscripcion, baja_inscripcion, reactivar_inscripcion
from django.urls import path

urlpatterns = [
    path('', index, name="index"),
    path('miembros/', miembros, name="miembros"),
    path('clases/', clases, name="clases"),
    path('clases/<slug:slug>/', clase, name="clase"),
    path('ingreso-alumnos/', ingreso_miembro, name="ingreso alumnos"),
    path('inscribir-alumno/', inscribir_alumno, name="inscripcion"),
    path('crear-clase/', crear_clase, name="crear clase"),
    path('profesores/', profesores, name="profesores"),
    path('api/eventos/', eventos, name="eventos"),
    path('calendario/', ver_calendario, name="calendario"),
    path('avisos/', avisos, name="avisos"),
    path('editar-inscripcion/<int:insc_id>/', editar_inscripcion, name="editar_inscripcion"),
    path("baja-inscripcion/<int:insc_id>/", baja_inscripcion, name="baja_inscripcion"),
    path("reactivar-inscripcion/<int:insc_id>/", reactivar_inscripcion, name="reactivar_inscripcion")
]