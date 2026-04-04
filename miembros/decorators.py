from django.contrib.auth.decorators import user_passes_test
from .models import Membership
from django.shortcuts import redirect


def admin_required(view_decorator):
    decorated_view = user_passes_test(
        lambda u: u.is_authenticated and u.groups.filter(name='admin_gym').exists()
    )(view_decorator)

    return decorated_view

def profesor_required(view_decorator):
    decorated_view = user_passes_test(
        lambda u: u.is_authenticated and u.groups.filter(name='profesor').exists()
    )(view_decorator)

    return decorated_view

def staff_required(view_decorator):
    decorated_view = user_passes_test(
        lambda u: u.is_authenticated and (
            u.groups.filter(name='Admin_Gym').exists() or
            u.groups.filter(name='profesor').exists()
        )
    )(view_decorator)

    return decorated_view

from django.http import HttpResponseForbidden

def requiere_roles(*roles_permitidos):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            gym = request.user.perfil.gym_activo

            try:
                membership = Membership.objects.get(
                    gym=gym,
                    usuario=request.user
                )
            except Membership.DoesNotExist:
                return HttpResponseForbidden()

            if membership.rol not in roles_permitidos:
                return HttpResponseForbidden()

            request.membership = membership  # 👈 útil
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator



def requiere_onboarding(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect("login")

        if not hasattr(user, 'profile') or not user.profile.completo:
            return redirect("completar_perfil")

        if not Membership.objects.filter(usuario=user).exists():
            return redirect("onboarding")

        return view_func(request, *args, **kwargs)
    return wrapper