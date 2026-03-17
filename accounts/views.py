from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import inicio_sesion_form, registro_form, gym_form, perfil_form
from .models import Perfil_usuario, Gym


def index(request):
    return render(request, "accounts/index.html")


def registro(request):

    if request.method == 'POST':
        form = registro_form(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = registro_form

    return render(request, "accounts/registro.html",{
        "form":form
    })


def iniciar_sesion(request):
    if request.method == 'POST':
        form = inicio_sesion_form(request, data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)
            if user is not None:
                
                login(request, user)

                return redirect("/clases/")
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
            form.save()
            return redirect("crear gimnasio")
    else:
        form = gym_form()

    return render(request, "accounts/crear_gym.html",{
        "form": form
    })


@login_required
def editar_perfil(request):

    perfil = request.user.perfil_usuario

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

    perfil = request.user.perfil_usuario

    return render(request, "accounts/ver_perfil.html",{
        "perfil":perfil
    })


def cerrar_sesion(request):
    logout(request)
    return redirect("login")