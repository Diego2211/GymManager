from django.urls import path
from .views import index, iniciar_sesion, registro

urlpatterns = [
    path("index/", index),
    path("iniciar-sesion/", iniciar_sesion, name="login"),
    path("registrarse/", registro, name="registro")
]