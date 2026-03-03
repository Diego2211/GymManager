from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Alumnos, Profesores, Pagos, Clases, Inscripciones, Avisos
from .forms import ingreso_usuario, ingreso_profesor

# Create your views here.

def index(request):
    return render(request, "index.html")

def miembros(request):
    miembro = Alumnos.objects.all()
    return render(request, "miembros.html", {
        "miembros": miembro
    })

def profesores(request):
    profesor = Profesores.objects.all()
    return render(request, "profesores.html", {
        "profesores": profesor
    })

def clases(request):
    clase = Clases.objects.all()
    profesor = Profesores.objects.all()
    return render(request, "clases.html", {
        "clases": clase,
        "profesores":profesor
    })

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
    return render(request, "clase.html", {
        "clas":clase,
        "inscripciones_activos":inscripciones_activos,
        "inscripciones_inactivos":inscripciones_inactivos
    })

"""def clase(request, slug):
    clase = get_object_or_404(Clases, slug=slug)
    return render(request, "clase.html", {
        "clase": clase
    })"""

def ingreso_miembro(request):
    if request.method == "POST":
        form = ingreso_usuario(request.POST)

        if form.is_valid():
            form.save()  
            return redirect("/miembros/") 

    else:
        form = ingreso_usuario()

    return render(request, "ingreso_miembros.html", {
        "form": form
    })

def ingreso_prof(request):
    if request.method == 'POST':
        form = ingreso_profesor(request.POST)

        if form.isvalid():
            form.save()
            return redirect("/miembros/")
    else:
        form = ingreso_profesor()
    return render(request, "ingreso_miembros.html", {
        "form":form
    })