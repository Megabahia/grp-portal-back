import jsonfield
from djongo import models


# Mundo: coop
# Portales: PERSONAS
# Esta clase sirve para conectar con la tabla personas de la base datos personas
class Proveedores(models.Model):
    _id = models.ObjectIdField()
    tipoPersona = models.CharField(max_length=10, null=True, blank=True)
    identificacion = models.CharField(max_length=13, null=True, blank=True)
    nombreRepresentante = models.CharField(max_length=255, null=True, blank=True)
    nombreComercial = models.CharField(max_length=255, null=True, blank=True)
    cuentas = jsonfield.JSONField()
    user_id = models.CharField(max_length=250, blank=True, null=True)  # Relacion usuario

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
