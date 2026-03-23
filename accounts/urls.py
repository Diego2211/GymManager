from django.urls import path
from .views import iniciar_sesion, registro, crear_gimnasio, editar_perfil, ver_perfil, cerrar_sesion, crear_invitacion, ver_invitaciones, seleccionar_gym, aceptar_invitacion

urlpatterns = [
    path("iniciar-sesion/", iniciar_sesion, name="login"),
    path("registrarse/", registro, name="registro"),
    path('crear-gimnasio/', crear_gimnasio, name="crear gimnasio"),
    path("editar-perfil/", editar_perfil, name="editar perfil"),
    path("ver-perfil/", ver_perfil, name="perfil"),
    path("cerrar-sesion/", cerrar_sesion, name="cerrar sesion"),
    path("crear-invitacion/", crear_invitacion, name="crear invitacion"),
    path("ver-invitaciones/", ver_invitaciones, name="ver invitaciones"),
    path("elegir-gym/", seleccionar_gym, name="elegir gym"),
    path("aceptar-invitacion/", aceptar_invitacion, name="aceptar invitacion")

]