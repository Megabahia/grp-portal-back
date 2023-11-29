from djongo import models


# Mundo: Bigpuntos
# Portales: CENter, corp, personas, ifis, credit
# Esta clase sirve para relacionar con la tabla TipoUsuario
class TipoUsuario(models.Model):
    _id = models.ObjectIdField()
    nombre = models.CharField(max_length=200, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
