from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import inicio_sesion_form, registro_form, gym_form, perfil_form, invitacion_form
from .models import Perfil_usuario, Gym, Invitacion, Membership, User
from django.http import HttpResponseForbidden
from django.utils import timezone
from datetime import timedelta
from miembros.permissions import es_admin, es_profesor
from miembros.decorators import requiere_roles


def registro(request):

    if request.method == 'POST':
        form = registro_form(request.POST)

        if form.is_valid():
            form.save()

            return redirect("login")
        else:
            print(form.errors)
    else:
        form = registro_form()

    return render(request, "accounts/registro.html",{
        "form":form
    })


def iniciar_sesion(request):
    if request.method == 'POST':
        form = inicio_sesion_form(request, data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)
            perfil = request.user.perfil
            if not perfil or not perfil.nombre:
                return redirect("editar perfil")

            # 🔴 Membership
            if not Membership.objects.filter(usuario=user, activo=True).exists():
                return redirect("crear gimnasio")

            # 🔴 Gym activo
            if not perfil.gym_activo:
                return redirect("elegir gym")

            return redirect("index")
    else:
        form = inicio_sesion_form()
        
    return render(request, "accounts/inicio_sesion.html", {
            "form":form
            })


@login_required
def crear_gimnasio(request):
    
    if request.method == 'POST':

        form = gym_form(request.POST)

        if form.is_valid():
            gym = form.save()
            
            Membership.objects.create(
                usuario=request.user,
                gym=gym,
                rol="owner",
            )
            return redirect("index")
    else:
        form = gym_form()

    return render(request, "accounts/crear_gym.html",{
        "form": form
    })
@login_required
def elegir(request):
    """
    Pantalla intermedia: el usuario elige entre
    unirse con código o crear su propio gimnasio.
    """
    return render(request, 'accounts/unirse_crear.html')


@login_required
def editar_perfil(request):

    perfil = request.user.perfil

    if request.method == 'POST':
        form = perfil_form(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect("perfil")
        
    else:
        form = perfil_form(instance=perfil)

    return render(request, "accounts/editar_perfil.html",{
        "form":form
    })

@login_required
def ver_perfil(request):

    perfil = request.user.perfil

    return render(request, "accounts/ver_perfil.html",{
        "perfil":perfil
    })


@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect("login")



@login_required
@requiere_roles("owner", "admin")
def crear_invitacion(request):
    gym = request.gym
    membership = request.membership

    if not es_admin(membership):
        return HttpResponseForbidden("No tenés permisos para crear invitaciones")

    if request.method == 'POST':
        form = invitacion_form(request.POST)
        if form.is_valid():
            invitacion = form.save(commit=False)
            expira = form.cleaned_data["expiracion"]

            if expira == "1h":
                invitacion.expira_en = timezone.now() + timedelta(hours=1)
            elif expira == "24h":
                invitacion.expira_en = timezone.now() + timedelta(hours=24)
            elif expira == "7d":
                invitacion.expira_en = timezone.now() + timedelta(days=7)

            invitacion.gym = gym
            invitacion.creado_por = request.user
            invitacion.save()

            # Guardás el código en la sesión y redirigís
            request.session['codigo_generado'] = str(invitacion.codigo)
            return redirect('crear invitacion')
    else:
        form = invitacion_form()

    # Leés y limpiás el código de la sesión
    codigo_generado = request.session.pop('codigo_generado', None)

    return render(request, "accounts/crear_invitacion.html", {
        "form": form,
        "codigo_generado": codigo_generado,
    })

@login_required
def seleccionar_gym(request):

    memberships = Membership.objects.filter(usuario=request.user, activo=True)

    if request.method == "POST":
        gym_id = request.POST.get("gym_id")

        membership = memberships.filter(gym_id=gym_id,).first()
        if membership:
            perfil = request.user.perfil
            perfil.gym_activo = membership.gym
            perfil.save()

            return redirect("index")

    return render(request, "accounts/seleccionar_gym.html", {
        "memberships": memberships
    })


@login_required
def ver_invitaciones(request):

    gym = request.user.perfil.gym_activo

    member = Membership.objects.filter(gym=gym)
    
    invitacion = Invitacion.objects.filter(gym=gym)

    return render(request, "accounts/ver_invitaciones.html",{
        "invitaciones":invitacion,
        "membership":member
    })


@login_required
def aceptar_invitacion(request):

    if request.method == "POST":
        codigo = request.POST.get("codigo")

        try:
            invitacion = Invitacion.objects.get(codigo=codigo)
        except Invitacion.DoesNotExist:
            messages.error(request, "Código inválido")
            return redirect("aceptar invitacion")

        # Validaciones
        if not invitacion.puede_usarse():
            messages.error(request, "La invitación no es válida o expiró")
            return redirect("aceptar invitacion")

        # Crear membership
        membership = Membership.objects.create(
            usuario=request.user,
            gym=invitacion.gym,
            rol=invitacion.rol,
            invitacion=invitacion
        )
        membership.save()

        # Registrar uso
        invitacion.registrar_uso()

        return redirect("index")

    return render(request, "accounts/aceptar_invitacion.html")