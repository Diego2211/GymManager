from miembros.views import index, miembros, clases, clase, ingreso_miembro, inscribir_alumno, crear_clase, profesores, eventos, ver_calendario, avisos, editar_inscripcion, baja_inscripcion, reactivar_inscripcion, registrar_pago, editar_clase, eliminar_clase, editar_alumno, eliminar_alumno
from django.urls import path

urlpatterns = [
    path('', index, name="index"),
    path('miembros/', miembros, name="miembros"),
    path("alumnos/<int:alumno_id>/editar/", editar_alumno, name="editar_alumno"),
    path("alumnos/<int:alumno_id>/eliminar/", eliminar_alumno, name="eliminar_alumno"),
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
    path("reactivar-inscripcion/<int:insc_id>/", reactivar_inscripcion, name="reactivar_inscripcion"),
    path("registrar-pago/<int:insc_id>/", registrar_pago, name="registrar_pago"),
    path("clases/<slug:slug>/editar/", editar_clase, name="editar_clase"),
    path("clases/<slug:slug>/eliminar/", eliminar_clase, name="eliminar_clase"),
]