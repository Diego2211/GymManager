from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import inicio_sesion_form, registro_form


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
    
"""
def ingreso_prof(request):
    msg = "Crear profesor"
    if request.method == "POST":
        form = ingreso_profesor(request.POST)

        if form.is_valid():

            #crear usuario
            user = settings.AUTH_USER_MODEL.objects.create_user(
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

    return render(request, "miembros/ingreso_miembros.html", {
        "form": form,
        "msg":msg
        })
"""