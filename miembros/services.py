from datetime import date
from dateutil.relativedelta import relativedelta
from .models import Pagos

MARGEN_GRACIA_DIAS = 7

def calcular_periodo_pago(inscripcion):

    hoy = date.today()

    ultimo_pago = Pagos.objects.filter(
        inscripcion=inscripcion
    ).order_by('-fecha_fin').first()

    if ultimo_pago:
        diferencia = (hoy - ultimo_pago.fecha_fin).days

        if diferencia <= MARGEN_GRACIA_DIAS:
            fecha_inicio = ultimo_pago.fecha_fin
        else:
            fecha_inicio = hoy
    else:
        fecha_inicio = hoy

    fecha_fin = fecha_inicio + relativedelta(months=1)

    return fecha_inicio, fecha_fin