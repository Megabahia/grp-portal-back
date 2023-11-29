import jsonfield
from django.utils import timezone
from djongo import models


def upload_path(instance, filname):
    """
    Este metodo se utiliza para subir los archivos
    @type filname: el campo filname es el nombre del archivo
    @type instance: el campo instance es el registro que se esta guardando
    @rtype: Devuelve la ruta del archivo donde se guardo
    """
    return '/'.join(['CORP/documentosCreditosArchivos', str(timezone.localtime(timezone.now())) + "_" + filname])


# Mundo: bigpuntos
# Portales: PERSONAS
# Esta clase sirve para conectar con la tabla PagoProveedores de la base datos personas
class PagoProveedores(models.Model):
    _id = models.ObjectIdField()
    valorPagar = models.CharField(max_length=255, null=True, blank=True)
    factura = models.FileField(blank=True, null=True, upload_to=upload_path)
    nombreProveedor = models.CharField(max_length=255, null=True, blank=True)
    rucProveedor = models.CharField(max_length=255, null=True, blank=True)
    banco = models.CharField(max_length=255, null=True, blank=True)
    numeroCuenta = models.CharField(max_length=255, null=True, blank=True)
    archivoFirmado = models.FileField(blank=True, null=True, upload_to=upload_path)
    nombrePyme = models.CharField(max_length=255, null=True, blank=True)
    usuario = jsonfield.JSONField()
    estado = models.CharField(max_length=255, null=True, blank=True)
    observacion = models.CharField(max_length=255, null=True, blank=True)
    fechaFirma = models.DateTimeField(null=True, blank=True)
    user_id = models.CharField(max_length=255, null=True, blank=True)
    numeroComprobante = models.CharField(max_length=255, null=True, blank=True)
    fechaProceso = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
