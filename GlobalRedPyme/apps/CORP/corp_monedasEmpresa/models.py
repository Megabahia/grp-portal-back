from djongo import models


# Nube: coop
#Portales: Central, Corp
#Esta clase hace referencia la tabla de datos MonedasEmpresa de la base datos corp
class MonedasEmpresa(models.Model):
    _id = models.ObjectIdField()
    fechaCobro = models.DateField(auto_now_add=True, null=True, blank=True)
    numeroFactura = models.TextField(max_length=255, null=True, blank=True)
    montoSupermonedas = models.FloatField(null=True, blank=True)
    montoTotalFactura = models.FloatField(null=True, blank=True)
    nombreCompleto = models.CharField(max_length=255, null=True, blank=True)
    nombres = models.CharField(max_length=255, null=True, blank=True)
    apellidos = models.CharField(max_length=255, null=True, blank=True)
    identificacion = models.CharField(max_length=10, null=True, blank=True)
    whatsapp = models.CharField(max_length=20, null=True, blank=True)
    empresa_id = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
