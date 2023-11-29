from .models import Pagos
from ...CORE.core_monedas.models import Monedas
from django.utils import timezone


def hi():
    """
    Este metodo sirve para ejecutar la tarea programada
    @rtype: No devuelve nada
    """
    # f = open('/home/sysadmin/prueba.txt','a')
    timezone_now = timezone.localtime(timezone.now())
    pagos = Pagos.objects.filter(duracion__lte=str(timezone_now), state=1)

    for pago in pagos:
        monedasUsuario = Monedas.objects.filter(user_id=pago.user_id, state=1).order_by('-created_at').first()
        data = {
            'user_id': pago.user_id,
            'empresa_id': pago.empresa_id,
            'tipo': 'Credito',
            'estado': 'aprobado',
            'credito': pago.monto,
            'saldo': monedasUsuario.saldo + pago.monto,
            'descripcion': 'Devolución de monedas al no usar el comprobante de pago.'
        }
        Monedas.objects.create(**data)
        pago.state = 0
        pago.save()
        # f.write(pago)
        # f.write("se ejecuto \n")

    # f.close()
