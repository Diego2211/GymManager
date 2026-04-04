from datetime import date, timedelta
from .models import Inscripciones, Avisos

def generar_avisos():
    hoy = date.today()

    inscripciones = Inscripciones.objects.filter(activo=True)

    for insc in inscripciones:
        vencimiento = insc.fecha_vencimiento

        #  Próximo a vencer (3 días antes)
        if 0 <= (vencimiento - hoy).days <= 3:

            Avisos.objects.get_or_create(
                gym=insc.gym,
                inscripcion=insc,
                tipo='vencimiento',
                defaults={
                    "mensaje": f"{insc.alumno} vence el {vencimiento}"
                }
            )

        #  Vencido
        elif hoy > vencimiento:

            Avisos.objects.get_or_create(
                gym=insc.gym,
                inscripcion=insc,
                tipo='Vencida',
                defaults={
                    "mensaje": f"{insc.alumno} tiene cuota vencida ({vencimiento})"
                }
            )