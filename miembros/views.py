from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth.models import Group
from accounts.models import Gym, Perfil_usuario, Membership
from .models import Alumnos, Pagos, Clases, Inscripciones, Avisos
from .forms import ingreso_usuario, inscripcion_form, crear_clase_form
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, "miembros/base.html")


def profesores(request):
    gym = request.user.perfil.gym_activo
    membership = Membership.objects.filter(gym=gym,
                                           activo=True)
    
    return render(request, "miembros/profesores.html",{
        "profesores": membership
    })


@login_required
def miembros(request):
    gym = request.user.perfil.gym_activo
    miembro = Alumnos.objects.filter(gym=gym)
    return render(request, "miembros/miembros.html", {
        "miembros": miembro
    })


@login_required
def clases(request):
    gym = request.user.perfil.gym_activo
    clase = Clases.objects.filter(gym=gym)
    profesor = Membership.objects.filter(gym=gym)
    return render(request, "miembros/clases.html", {
        "clases": clase,
        "profesores":profesor
    })


@login_required
def clase(request, slug):
    gym = request.user.perfil.gym_activo
    clase = get_object_or_404(Clases, slug=slug, gym=gym)
    inscripciones_activos = Inscripciones.objects.filter(gym=gym,
        clase=clase,
        activo=True
    )
    inscripciones_inactivos = Inscripciones.objects.filter(gym=gym,
        clase=clase,
        activo=False
    )
    return render(request, "miembros/clase.html", {
        "clas":clase,
        "inscripciones_activos":inscripciones_activos,
        "inscripciones_inactivos":inscripciones_inactivos
    })


@login_required
def ingreso_miembro(request):

    gym = request.user.perfil.gym_activo
    
    msg = str(gym)

    if request.method == "POST":
        form = ingreso_usuario(request.POST)

        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.gym = gym
            alumno.save() 
            return redirect("/miembros/") 

    else:
        form = ingreso_usuario()

    return render(request, "miembros/ingreso_miembros.html", {
        "form": form,
        "msg":msg
    })


@login_required
def inscribir_alumno(request):
    msg = "Inscribir alumno"
    gym = request.user.perfil.gym_activo
    query = request.GET.get("q")

    alumnos = Alumnos.objects.filter(gym=gym)

    if query:
        alumnos = alumnos.filter(nombre__icontains=query)

    form = inscripcion_form(gym=gym)

    form.fields['alumno'].queryset = alumnos

    if request.method == "POST":
        form = inscripcion_form(request.POST, gym=gym)

        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.gym = gym
            inscripcion.save()
            return redirect("/clases/")
        

    return render(request,"miembros/inscribir_alumno.html",{
        "form":form,
        "query":query,
        "msg":msg
    })



@login_required
def crear_clase(request):
    gym = request.user.perfil.gym_activo
    if not gym:
        return redirect("elegir gym")
    msg = "Crear clase"
    if request.method == "POST":
        form = crear_clase_form(request.POST, gym=gym)

        if form.is_valid():

            clase = form.save(commit=False)
            clase.gym = gym
            clase.save()
            
            return redirect("/clases/")

    else:
        form = crear_clase_form(gym=gym)

    return render(request, "miembros/ingreso_miembros.html", {
        "form": form,
        "msg":msg
    })