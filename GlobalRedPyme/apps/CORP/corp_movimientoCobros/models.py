from djongo import models

from ..corp_creditoPersonas.models import RegarcarCreditos
from ..corp_pagoEmpleados.models import PagoEmpleados
from ..corp_pagoProveedores.models import PagoProveedores


# Nube: coop
# PORTALES: CENTER, PERSONAS, CORP, IFIS
# Este archivo sirve para conectar el backend de la nube de bigpuntos con la base datos de corp
class MovimientoCobros(models.Model):
    _id = models.ObjectIdField()
    autorizacion = models.IntegerField(null=True, blank=True)
    codigoCobro = models.CharField(max_length=200, null=True, blank=True)
    fechaCobro = models.DateField(null=True, blank=True)
    montoTotalFactura = models.FloatField(null=True, blank=True)
    montoSupermonedas = models.FloatField(null=True, blank=True)
    user_id = models.CharField(max_length=250, blank=True, null=True)  # Relacion usuario
    empresa_id = models.CharField(max_length=250, blank=True, null=True)  # Relacion empresa

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)


# Nube: coop
# PORTALES: CENTER, PERSONAS, CORP, IFIS
# Este archivo sirve para conectar el backend de la nube de coop con la base datos de corp
class Transacciones(models.Model):
    _id = models.ObjectIdField()
    fechaTransaccion = models.DateField(null=True, blank=True)
    tipo = models.CharField(max_length=200, null=True, blank=True)
    estado = models.CharField(max_length=200, null=True, blank=True)
    informacion = models.CharField(max_length=200, null=True, blank=True)
    egreso = models.FloatField(null=True, blank=True)
    ingreso = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    user_id = models.CharField(max_length=250, blank=True, null=True)  # Relacion usuario
    empresa_id = models.CharField(max_length=250, blank=True, null=True)  # Relacion empresa
    creditoPersona_id = models.CharField(max_length=250, blank=True, null=True)  # Relacion empresa
    pagoEmpleados = models.ForeignKey(PagoEmpleados, null=True, on_delete=models.CASCADE)  # Relacion pagoEmpleados
    pagoProveedores = models.ForeignKey(PagoProveedores, null=True,
                                        on_delete=models.CASCADE)  # Relacion pagoProveedores
    regarcarCreditos = models.ForeignKey(RegarcarCreditos, null=True,
                                         on_delete=models.CASCADE)  # Relacion regarcarCreditos

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
