from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Min, Max
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.conf import settings
from dateutil.relativedelta import relativedelta
from miembros.permissions import es_admin, es_profesor
from .decorators import requiere_roles
from accounts.models import Gym, Perfil_usuario, Membership
from .models import Alumnos, Pagos, Clases, Inscripciones, Avisos, Horario
from .forms import ingreso_usuario, inscripcion_form, crear_clase_form, Horario_FormSet
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone
from .task import generar_avisos

# Create your views here.
@requiere_roles("owner", "admin", "profesor")
@login_required
def index(request):
    nombre = str(request.user.perfil.nombre)
    return render(request, "miembros/base.html",{
        "nombre": nombre
    })


@requiere_roles("owner", "admin")
@login_required
def profesores(request):
    gym = request.user.perfil.gym_activo
    membership = Membership.objects.filter(gym=gym,
                                           activo=True)
    
    return render(request, "miembros/profesores.html",{
        "profesores": membership
    })


@requiere_roles("owner", "admin")
@login_required
def miembros(request):
    gym = request.user.perfil.gym_activo
    miembro = Alumnos.objects.filter(gym=gym)
    return render(request, "miembros/miembros.html", {
        "miembros": miembro
    })


@requiere_roles("owner", "admin", "profesor")
@login_required
def clases(request):
    gym = request.user.perfil.gym_activo
    membership = Membership.objects.get(gym=gym,
                                           usuario=request.user)
    
    if es_admin(membership):
        clase = Clases.objects.filter(gym=gym)
    elif es_profesor(membership):
        clase = Clases.objects.filter(gym=gym,
                                      profesor=membership)
    else:
        return HttpResponseForbidden("no tenes permisos")

    return render(request, "miembros/clases.html", {
        "clases": clase,
    })


@requiere_roles("owner", "admin", "profesor")
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
@requiere_roles("owner", "admin", "profesor")
def baja_inscripcion(request, insc_id):
    insc = get_object_or_404(Inscripciones, id=insc_id)

    if insc.gym != request.user.perfil.gym_activo:
        return HttpResponseForbidden()

    insc.activo = False
    insc.save()

    return redirect("clase", slug=insc.clase.slug)


@login_required
@requiere_roles("owner", "admin", "profesor")
def editar_inscripcion(request, insc_id):
    insc = get_object_or_404(Inscripciones, id=insc_id)

    form = inscripcion_form(instance=insc)

    if request.method == "POST":
        form = inscripcion_form(request.POST, instance=insc)
        if form.is_valid():
            form.save()
            return redirect("clase", slug=insc.clase.slug)

    return render(request, "miembros/inscribir_alumno.html", {
        "form": form})


@requiere_roles("owner", "admin", "profesor")
@login_required
def reactivar_inscripcion(request, insc_id):
    insc = get_object_or_404(Inscripciones, id=insc_id)

    insc.activo = True
    insc.save()

    return redirect("clase", slug=insc.clase.slug)


@requiere_roles("owner", "admin", "profesor")
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


@requiere_roles("owner", "admin", "profesor")
@login_required
def inscribir_alumno(request):
    msg = "Inscribir alumno"
    gym = request.user.perfil.gym_activo
    query = request.GET.get("q")
    membership = Membership.objects.get(gym=gym,
                                        usuario=request.user)
    
    if es_admin(membership):
        clases = Clases.objects.filter(gym=gym)
    elif es_profesor(membership):
        clases = Clases.objects.filter(gym=gym,
                                       profesor=membership)

    alumnos = Alumnos.objects.filter(gym=gym)

    if query:
        alumnos = alumnos.filter(nombre__icontains=query)

    form = inscripcion_form(gym=gym)

    form.fields['alumno'].queryset = alumnos
    form.fields['clase'].queryset = clases

    if request.method == "POST":
        form = inscripcion_form(request.POST, gym=gym)
        form.fields['alumno'].queryset = alumnos
        form.fields['clase'].queryset = clases

        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.gym = gym
            inscripcion.fecha_vencimiento = (timezone.now().date() + relativedelta(months=1))
            inscripcion.creado_por = membership.usuario
            inscripcion.save()
            return redirect("clases")
        

    return render(request,"miembros/inscribir_alumno.html",{
        "form":form,
        "query":query,
        "msg":msg
    })


@requiere_roles("owner", "admin")
@login_required
def crear_clase(request):
    gym = request.user.perfil.gym_activo
    if not gym:
        return redirect("elegir gym")
    msg = "Crear clase"
    if request.method == "POST":
        form = crear_clase_form(request.POST, gym=gym)
        formset = Horario_FormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            clase = form.save(commit=False)
            clase.gym = gym
            clase.save()
            horarios = formset.save(commit=False)
            for h in horarios:
                h.clase = clase
                h.save()

            return redirect('clases')

    else:
        form = crear_clase_form(gym=gym)
        formset = Horario_FormSet()

    return render(request, "miembros/crear_clase.html", {
        "form": form,
        "formset":formset,
        "msg":msg
    })




def eventos(request):
    MAP_DIAS = {
    "domingo": 0,
    "lunes": 1,
    "martes": 2,
    "miercoles": 3,
    "jueves": 4,
    "viernes": 5,
    "sabado": 6,
    }
    eventos = []

    horarios = Horario.objects.select_related('clase')
    for h in horarios:
        eventos.append({
            "title": h.clase.clase,
            "daysOfWeek": [MAP_DIAS.get(h.dia)],
            "startTime": h.hora_inicio.strftime("%H:%M:%S"),
            "endTime": h.hora_fin.strftime("%H:%M:%S"),
            "extendedProps": {
        "profesor": str(h.clase.profesor.usuario.perfil.nombre),
        "hora": f"{h.hora_inicio.strftime('%H:%M')} - {h.hora_fin.strftime('%H:%M')}"
    },
    
        })
    min_hora = horarios.aggregate(Min('hora_inicio'))['hora_inicio__min']
    max_hora = horarios.aggregate(Max('hora_fin'))['hora_fin__max']

    return JsonResponse({
        "eventos": eventos,
        "min": min_hora.strftime("%H:%M:%S") if min_hora else "00:00:00",
        "max": max_hora.strftime("%H:%M:%S") if max_hora else "24:00:00",
        })

@requiere_roles("owner", "admin", "profesor")
@login_required
def ver_calendario(request):
    return render(request, "miembros/calendario.html")


@requiere_roles("owner", "admin", "profesor")
@login_required
def avisos(request):

    gym = request.user.perfil.gym_activo
    membership = Membership.objects.get(gym=gym,
                                        usuario=request.user)
    if es_admin(membership):
        avisos = Avisos.objects.filter(gym=gym,
                                       visto_por_profesor=False)
        
    elif es_profesor(membership):
        avisos = Avisos.objects.filter(gym=gym,
                                       visto_por_profesor=False,
                                       inscripcion__clase__profesor=membership)

    if request.method == "POST":
        generar_avisos()


    return render(request, "miembros/avisos.html", {
        "avisos": avisos})
