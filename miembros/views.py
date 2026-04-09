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
from datetime import timedelta, date
from django.utils import timezone
from .task import generar_avisos
from .services import calcular_periodo_pago
from .selectors import obtener_inscripciones_con_estado
from decimal import Decimal
# Create your views here.
@login_required
@requiere_roles("owner", "admin", "profesor")
def index(request):
    return render(request, "miembros/index.html")


@login_required
@requiere_roles("owner", "admin", "profesor")
def profesores(request):
    gym = request.user.perfil.gym_activo
    membership = Membership.objects.filter(gym=gym,
                                           activo=True)
    
    return render(request, "miembros/profesores.html",{
        "profesores": membership
    })



@login_required
@requiere_roles("owner", "admin")
def expulsar_profesor(request, membership_id):
    if request.method == "POST":
        gym = request.user.perfil.gym_activo
        membership = Membership.objects.filter(
            id=membership_id,
            gym=gym
        ).first()

        if not membership:
            return HttpResponseForbidden("No tenés permisos")

        membership.delete()
        return redirect("profesores")

    return redirect("profesores")


@login_required
@requiere_roles("owner", "admin", "profesor")
def miembros(request):
    gym = request.user.perfil.gym_activo
    miembro = Alumnos.objects.filter(gym=gym)
    return render(request, "miembros/miembros.html", {
        "miembros": miembro
    })
@login_required
@requiere_roles("owner", "admin")
def editar_alumno(request, alumno_id):
    gym = request.user.perfil.gym_activo
    alumno = get_object_or_404(Alumnos, id=alumno_id, gym=gym)

    if request.method == "POST":
        form = ingreso_usuario(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            return redirect("miembros")
    else:
        form = ingreso_usuario(instance=alumno)

    return render(request, "miembros/form_simple.html", {
        "form": form,
        "msg": f"Editar alumno — {alumno}"
    })


@login_required
@requiere_roles("owner", "admin")
def eliminar_alumno(request, alumno_id):
    gym = request.user.perfil.gym_activo
    alumno = get_object_or_404(Alumnos, id=alumno_id, gym=gym)

    if request.method == "POST":
        alumno.delete()
        return redirect("miembros")

    return redirect("miembros")

@login_required
@requiere_roles("owner", "admin", "profesor")
def clases(request):
    gym = request.gym
    membership = request.membership
    
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


@login_required
@requiere_roles("owner", "admin", "profesor")
def clase(request, slug):

    gym = request.gym  # 🔥 ya lo tenés del decorator

    clase = get_object_or_404(Clases, slug=slug, gym=gym)

    inscripciones = obtener_inscripciones_con_estado(gym, clase)

    inscripciones_activos = inscripciones.filter(activo=True)
    inscripciones_inactivos = inscripciones.filter(activo=False)

    return render(request, "miembros/clase.html", {
        "clas": clase,
        "inscripciones_activos": inscripciones_activos,
        "inscripciones_inactivos": inscripciones_inactivos,
        "today": date.today()
    })


@login_required
@requiere_roles("owner", "admin")
def editar_clase(request, slug):
    gym = request.user.perfil.gym_activo
    clase = get_object_or_404(Clases, slug=slug, gym=gym)

    if request.method == "POST":
        form = crear_clase_form(request.POST, instance=clase, gym=gym)
        formset = Horario_FormSet(request.POST, instance=clase)

        if form.is_valid() and formset.is_valid():
            form.save()
            horarios = formset.save(commit=False)
            for h in horarios:
                h.clase = clase
                h.save()
            for h in formset.deleted_objects:
                h.delete()
            return redirect("clases")
    else:
        form = crear_clase_form(instance=clase, gym=gym)
        formset = Horario_FormSet(instance=clase)

    return render(request, "miembros/crear_clase.html", {
        "form": form,
        "formset": formset,
        "msg": f"Editar clase — {clase.clase}"
    })

@login_required
@requiere_roles("owner", "admin")
def eliminar_clase(request, slug):
    gym = request.user.perfil.gym_activo
    clase = get_object_or_404(Clases, slug=slug, gym=gym)

    if request.method == "POST":
        clase.delete()
        return redirect("clases")

    return redirect("clases")

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

    return render(request, "miembros/form_simple.html", {
        "form": form})


@login_required
@requiere_roles("owner", "admin", "profesor")
def reactivar_inscripcion(request, insc_id):
    insc = get_object_or_404(Inscripciones, id=insc_id)

    insc.activo = True
    insc.save()

    return redirect("clase", slug=insc.clase.slug)



@login_required
@requiere_roles("owner", "admin", "profesor")
def registrar_pago(request, insc_id):

    insc = get_object_or_404(Inscripciones, id=insc_id)

    if insc.gym != request.gym:
        return HttpResponseForbidden()

    if request.method == "POST":

        pago_completo = request.POST.get("pago_completo")

        if pago_completo:
            monto = insc.clase.cuota_mensual
        else:
            monto_raw = request.POST.get("monto", "").strip()
            if not monto_raw:
                return redirect("clase", slug=insc.clase.slug)
            monto = Decimal(monto_raw)

        fecha_inicio, fecha_fin = calcular_periodo_pago(insc)

        Pagos.objects.create(
            gym=request.gym,
            inscripcion=insc,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            monto=monto,
            registrado_por=request.user
        )

        cuota = insc.clase.cuota_mensual

        if monto < cuota:
            diferencia = cuota - monto
            # update_or_create por el unique_together ["inscripcion", "tipo"]
            Avisos.objects.update_or_create(
                inscripcion=insc,
                tipo="pago_parcial",
                defaults={
                    "gym": request.gym,
                    "mensaje": (
                        f"{insc.alumno.nombre} {insc.alumno.apellido} "
                        f"pagó ${monto} de ${cuota}. Adeuda ${diferencia}."
                    ),
                    "visto_por_profesor": False,
                    "fecha_visto": None,
                }
            )
        else:
            # Si pagó completo, eliminar aviso de deuda si existía
            Avisos.objects.filter(inscripcion=insc, tipo="pago_parcial").delete()

        return redirect("clase", slug=insc.clase.slug)

    return redirect("clase", slug=insc.clase.slug)


@login_required
@requiere_roles("owner", "admin", "profesor")
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

    return render(request, "miembros/form_simple.html", {
        "form": form,
        "msg":msg
    })


@login_required
@requiere_roles("owner", "admin", "profesor")
def inscribir_alumno(request):
    msg = "Inscribir alumno"
    gym = request.user.perfil.gym_activo
    query = request.GET.get("q")
    alumno_nuevo_id = request.GET.get("alumno_nuevo")  # viene después de crear alumno
    membership = Membership.objects.get(gym=gym, usuario=request.user)

    if es_admin(membership):
        clases = Clases.objects.filter(gym=gym)
    elif es_profesor(membership):
        clases = Clases.objects.filter(gym=gym, profesor=membership)

    alumnos = Alumnos.objects.filter(gym=gym)
    if query:
        alumnos = alumnos.filter(nombre__icontains=query)

    # Form inscripción
    form_insc = inscripcion_form(gym=gym)
    form_insc.fields['alumno'].queryset = alumnos
    form_insc.fields['clase'].queryset = clases

    # Preseleccionar alumno recién creado
    alumno_preseleccionado = None
    if alumno_nuevo_id:
        try:
            alumno_preseleccionado = Alumnos.objects.get(id=alumno_nuevo_id, gym=gym)
            form_insc.fields['alumno'].initial = alumno_preseleccionado
        except Alumnos.DoesNotExist:
            pass

    # Form alumno nuevo
    form_alumno = ingreso_usuario()

    if request.method == "POST":

        # Guardar alumno nuevo
        if "guardar_alumno" in request.POST:
            form_alumno = ingreso_usuario(request.POST)
            if form_alumno.is_valid():
                alumno = form_alumno.save(commit=False)
                alumno.gym = gym
                alumno.save()
                return redirect(f"{request.path}?alumno_nuevo={alumno.id}")

        # Inscribir alumno
        elif "inscribir" in request.POST:
            form_insc = inscripcion_form(request.POST, gym=gym)
            form_insc.fields['alumno'].queryset = alumnos
            form_insc.fields['clase'].queryset = clases

            if form_insc.is_valid():
                inscripcion = form_insc.save(commit=False)
                inscripcion.gym = gym
                inscripcion.fecha_vencimiento = timezone.now().date() + relativedelta(months=1)
                inscripcion.creado_por = membership.usuario
                inscripcion.save()
                return redirect("clases")

    return render(request, "miembros/inscribir_alumno.html", {
        "form": form_insc,
        "form_alumno": form_alumno,
        "query": query,
        "msg": msg,
        "alumno_preseleccionado": alumno_preseleccionado,
    })

@login_required
@requiere_roles("owner", "admin")
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

    horarios = Horario.objects.select_related('clase__profesor__usuario__perfil').prefetch_related(
        'clase__inscripciones_set'
    )

    for h in horarios:
        alumnos_activos = Inscripciones.objects.filter(
            clase=h.clase,
            activo=True
        ).count()

        eventos.append({
            "title": h.clase.clase,
            "daysOfWeek": [MAP_DIAS.get(h.dia)],
            "startTime": h.hora_inicio.strftime("%H:%M:%S"),
            "endTime": h.hora_fin.strftime("%H:%M:%S"),
            "extendedProps": {
                "profesor": str(h.clase.profesor.usuario.perfil.nombre),
                "hora": f"{h.hora_inicio.strftime('%H:%M')} - {h.hora_fin.strftime('%H:%M')}",
                "alumnos": alumnos_activos,
                "slug": h.clase.slug,
            },
        })

    min_hora = horarios.aggregate(Min('hora_inicio'))['hora_inicio__min']
    max_hora = horarios.aggregate(Max('hora_fin'))['hora_fin__max']

    dias_con_horario = set(
    MAP_DIAS[h.dia] for h in horarios if h.dia in MAP_DIAS)
    todos_los_dias = set(range(7))
    dias_ocultos = list(todos_los_dias - dias_con_horario)

    return JsonResponse({
        "eventos": eventos,
        "min": min_hora.strftime("%H:%M:%S") if min_hora else "00:00:00",
        "max": max_hora.strftime("%H:%M:%S") if max_hora else "24:00:00",
        "dias_ocultos": dias_ocultos})

@login_required
@requiere_roles("owner", "admin", "profesor")
def ver_calendario(request):
    return render(request, "miembros/calendario.html")


@login_required
@requiere_roles("owner", "admin", "profesor")
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
