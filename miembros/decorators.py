from django.contrib.auth.decorators import user_passes_test
from .models import Membership
from django.shortcuts import redirect
from functools import wraps


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

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            user = request.user

            # 🔴 Seguridad básica (por si middleware falla)
            if not user.is_authenticated:
                return redirect("login")

            perfil = getattr(user, "perfil", None)

            if not perfil or not perfil.gym_activo:
                return redirect("onboarding")

            # 🔥 CACHE en request (clave)
            if not hasattr(request, "_membership"):

                request._membership = Membership.objects.select_related("gym").filter(
                    usuario=user,
                    gym=perfil.gym_activo,
                    activo=True
                ).first()

            membership = request._membership
            
            

            # 🔴 No tiene membership
            if not membership:
                return redirect("crear gimnasio")
            
            request.membership = membership
            request.gym = membership.gym

            # 🔴 No tiene rol permitido
            if membership.rol not in roles_permitidos:
                return HttpResponseForbidden("No tenés permisos")

            # opcional: dejarlo accesible
            request.membership = membership

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