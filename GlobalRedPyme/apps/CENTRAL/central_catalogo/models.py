"""NUBE DE BIGPUNTOS
PORTALES: CENTER, CORP, PERSONAS, IFIS, CREDIT
Este archivo sirve para conectar el backend de la nube de bigpuntos con la base datos de bigpuntos central
"""

import jsonfield
from djongo import models


# Create your models here.
class Catalogo(models.Model):
    _id = models.ObjectIdField()
    idPadre = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)  # Relacion Padre
    nombre = models.CharField(max_length=255, null=True)
    tipo = models.CharField(max_length=255, null=False)
    tipoVariable = models.CharField(max_length=255, null=False)
    valor = models.TextField()
    descripcion = models.CharField(max_length=255, null=True)
    config = jsonfield.JSONField()
    minimo = models.IntegerField(null=True, blank=True)
    maximo = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    # El metodo save convierte en mayuscula el campo tipo
    def save(self, *args, **kwargs):
        self.tipo = self.tipo.upper()
        return super(Catalogo, self).save(*args, **kwargs)

    # El metodo solo imprime el nombre al momento de realizar una consulta con el mapeador de Django
    def __str__(self):
        return '{}'.format(self.nombre)
