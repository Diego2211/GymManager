from django.urls import path
from .views import index, iniciar_sesion, registro, crear_gimnasio, editar_perfil, ver_perfil, cerrar_sesion

urlpatterns = [
    path("index/", index),
    path("iniciar-sesion/", iniciar_sesion, name="login"),
    path("registrarse/", registro, name="registro"),
    path('crear-gimnasio/', crear_gimnasio, name="crear gimnasio"),
    path("editar-perfil/", editar_perfil, name="editar perfil"),
    path("ver-perfil/", ver_perfil, name="perfil"),
    path("cerrar-sesion/", cerrar_sesion, name="cerrar sesion")
]