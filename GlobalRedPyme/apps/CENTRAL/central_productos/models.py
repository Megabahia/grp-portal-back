"""Nube: Bigpuntos
PORTALES: CENTER, PERSONAS
Este archivo sirve para conectar el backend de la nube de bigpuntos con la base datos de bigpuntos central
"""

from djongo import models


def upload_path(instance, filname):
    """
    Este metodo se utiliza para subir los archivos
    @type filname: el campo filname es el nombre del archivo
    @type instance: el campo instance es el registro que se esta guardando
    @rtype: Devuelve la ruta del archivo donde se guardo
    """
    return '/'.join(['CENTRAL/imgProductos', str(instance._id) + "_" + filname])


# ESta clase se relaciona con la tabla productos de la base datos central
class Productos(models.Model):
    _id = models.ObjectIdField()
    nombre = models.TextField(max_length=200, null=False, blank=False)
    marca = models.CharField(max_length=255, null=True, blank=True)
    imagen = models.FileField(blank=True, null=True, upload_to=upload_path)
    precioNormal = models.FloatField(null=False, blank=False)
    precioSupermonedas = models.CharField(max_length=200, null=False, blank=False)
    efectivo = models.FloatField(null=False, blank=False)
    codigoQR = models.CharField(max_length=200, null=True, blank=True)
    cantidad = models.IntegerField(null=True, blank=True)
    empresa_id = models.CharField(max_length=200, null=False, blank=False)
    tipo = models.CharField(default="presentacion", max_length=255, null=False, blank=False)
    vigencia = models.DateField(null=True, blank=True)
    codigoDescuento = models.CharField(max_length=200, null=True, blank=True)
    empresaAplica_id = models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
