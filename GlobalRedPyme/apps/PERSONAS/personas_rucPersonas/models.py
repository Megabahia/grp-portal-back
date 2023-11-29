from djongo import models


# Mundo: coop
# Portales: PErsonas, corp, center
# Esta clase sirve para relacionar con la tabla rucpersonas de la base datos personas
class RucPersonas(models.Model):
    _id = models.ObjectIdField()
    identificacion = models.CharField(max_length=10, null=True, blank=True)
    ruc = models.CharField(max_length=13, null=True, blank=True)
    nombreComercial = models.CharField(max_length=255, null=True, blank=True)
    razonSocial = models.CharField(max_length=255, null=True, blank=True)
    pais = models.CharField(max_length=255, null=True, blank=True)
    provincia = models.CharField(max_length=255, null=True, blank=True)
    ciudad = models.CharField(max_length=255, null=True, blank=True)
    antiguedadRuc = models.SmallIntegerField(null=True, blank=True)
    actividadComercial = models.CharField(max_length=255, null=True, blank=True)
    ventaMensual = models.FloatField(null=True, blank=True)
    gastoMensual = models.FloatField(null=True, blank=True)
    user_id = models.CharField(max_length=250, blank=True, null=True)  # Relacion usuario

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
