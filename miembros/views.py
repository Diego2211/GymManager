from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from .models import Alumnos, Profesores, Pagos, Clases, Inscripciones, Avisos
from .forms import ingreso_usuario, ingreso_profesor, login_usuario, inscripcion_form, crear_clase_form
from django.contrib.auth.decorators import login_required

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
    if request.method == "POST":
        form = ingreso_profesor(request.POST)

        if form.is_valid():

            #crear usuario
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
                email=form.cleaned_data["email"]
            )

            #añadir usuario al grupo
            grupo = Group.objects.get(name="profesor")
            user.groups.add(grupo)

            #vincular usuario con profesor
            profesor = form.save(commit=False)
            profesor.usuario = user
            profesor.save()
            print("Usuario creado:", user.username)

            return redirect("/profesores/")
        
    else:
        form = ingreso_profesor()

    return render(request, "ingreso_miembros.html", {
        "form": form})


def iniciar_sesion(request):
    if request.method == 'POST':
        form = login_usuario(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                
                login(request, user)

                return redirect("/clases/")
    else:
        form = login_usuario()
        
        return render(request, "inicio_sesion.html", {
            "form":form})


@login_required
def inscribir_alumno(request):

    query = request.GET.get("q")

    alumnos = Alumnos.objects.all()

    if query:
        alumnos = alumnos.filter(nombre__icontains=query)

    form = inscripcion_form()

    form.fields['alumno'].queryset = alumnos

    if request.method == "POST":
        form = inscripcion_form(request.POST)

        if form.is_valid():
            form.save()  
            return redirect("/clases/") 

    return render(request,"inscribir_alumno.html",{
        "form":form,
        "query":query
    })


def crear_clase(request):

    if request.method == "POST":
        form = crear_clase_form(request.POST)

        if form.is_valid():
            form.save()  
            return redirect("/clases/") 

    else:
        form = crear_clase_form()

    return render(request, "ingreso_miembros.html", {
        "form": form
    })