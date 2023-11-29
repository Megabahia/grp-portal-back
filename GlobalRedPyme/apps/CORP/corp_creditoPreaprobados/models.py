from djongo import models
from ..corp_empresas.models import Empresas


# Mundo: coop
# Portales: PERSONAS, corp
# Esta clase sirve para conectar con la tabla CreditoPreaprobados de la base datos corp
class CreditoPreaprobados(models.Model):
    _id = models.ObjectIdField()
    fechaAprobado = models.DateField(null=True, blank=True)
    vigencia = models.DateField(null=True, blank=True)
    concepto = models.CharField(max_length=255, null=True, blank=True)
    monto = models.FloatField(null=True, blank=True)
    plazo = models.SmallIntegerField(null=True, blank=True)
    interes = models.FloatField(null=True, blank=True)
    estado = models.CharField(default="Pre aprobado", max_length=255, null=True, blank=True)
    tipoPersona = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.CharField(max_length=255, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    empresa_financiera = models.ForeignKey(Empresas, null=False, on_delete=models.DO_NOTHING)  # Empresa
    empresa_comercial = models.CharField(max_length=255, null=True, blank=True)  # Empresa
    tomarSolicitud = models.CharField(max_length=255, null=True, blank=True)
    tipoCredito = models.CharField(max_length=255, null=True, blank=True)
    empresasAplican = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
