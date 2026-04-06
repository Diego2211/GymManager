from django.db.models import Max
from .models import Inscripciones

def obtener_inscripciones_con_estado(gym, clase):

    return Inscripciones.objects.filter(
        gym=gym,
        clase=clase
    ).select_related("alumno").annotate(
        ultimo_fin=Max("pagos__fecha_fin")
    )