from django.shortcuts import redirect
from .models import Membership
from django.urls import reverse

class OnboardingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        user = request.user

        # ⚠️ Solo si está logueado
        if user.is_authenticated:

            # Rutas que NO deben bloquearse
            rutas_permitidas = [
                reverse("editar perfil"),
                reverse("crear gimnasio"),
                reverse("crear gimnasio"),
                reverse("aceptar invitacion"),
                reverse("elegir gym"),
                reverse("cerrar sesion"),
            ]

            if any(request.path.startswith(ruta) for ruta in rutas_permitidas):
                return self.get_response(request)

            perfil = getattr(user, "perfil", None)

            # 🔴 1. Perfil obligatorio
            if not perfil or not perfil.nombre:
                return redirect("editar perfil")

            # 🔴 2. Membership obligatorio
            if not Membership.objects.filter(usuario=user, activo=True).exists():
                return redirect("crear gimnasio")

            # 🔴 3. Gym activo obligatorio
            if not perfil.gym_activo:
                return redirect("elegir gym")

        return self.get_response(request)