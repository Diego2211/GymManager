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


@login_required
def miembros(request):
    miembro = Alumnos.objects.all()
    return render(request, "miembros/miembros.html", {
        "miembros": miembro
    })


@login_required
def profesores(request):
    profesor = Perfil_usuario.objects.all()
    return render(request, "miembros/profesores.html", {
        "profesores": profesor
    })


@login_required
def clases(request):
    clase = Clases.objects.all()
    profesor = Membership.objects.all()
    return render(request, "miembros/clases.html", {
        "clases": clase,
        "profesores":profesor
    })


@login_required
def clase(request, slug):
    clase = get_object_or_404(Clases, slug=slug)
    inscripciones_activos = Inscripciones.objects.filter(
        clase=clase,
        activo=True
    )
    inscripciones_inactivos = Inscripciones.objects.filter(
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
    if request.method == "POST":
        form = ingreso_usuario(request.POST)

        if form.is_valid():
            form.save()  
            return redirect("/miembros/") 

    else:
        form = ingreso_usuario()

    return render(request, "miembros/ingreso_miembros.html", {
        "form": form
    })








@login_required
def inscribir_alumno(request):
    msg = "Inscribir alumno"

    query = request.GET.get("q")

    alumnos = Alumnos.objects.filter(Gym)

    if query:
        alumnos = alumnos.filter(nombre__icontains=query)

    form = inscripcion_form()

    form.fields['alumno'].queryset = alumnos

    if request.method == "POST":
        form = inscripcion_form(request.POST)

        if form.is_valid():
            form.save()  
            return redirect("/clases/") 

    return render(request,"miembros/inscribir_alumno.html",{
        "form":form,
        "query":query,
        "msg":msg
    })



@login_required
def crear_clase(request):
    msg = "Crear clase"
    if request.method == "POST":
        form = crear_clase_form(request.POST)

        if form.is_valid():

            form.save()
            
            return redirect("/clases/")

    else:
        form = crear_clase_form()

    return render(request, "miembros/ingreso_miembros.html", {
        "form": form,
        "msg":msg
    })