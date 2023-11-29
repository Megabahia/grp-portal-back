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


# Mundo: coop
# Portales: PERSONAS, corp, center
# Esta clase sirve para conectar con la tabla PagoEmpleados de la base datos corp
class PagoEmpleados(models.Model):
    _id = models.ObjectIdField()
    nombresCompletos = models.CharField(max_length=255, null=True, blank=True)
    cedula = models.CharField(max_length=255, null=True, blank=True)
    celular = models.CharField(max_length=255, null=True, blank=True)
    correo = models.EmailField(max_length=255, null=True, blank=True)
    montoPagar = models.CharField(max_length=255, null=True, blank=True)
    codigoEmpleado = models.CharField(max_length=255, null=True, blank=True)
    numeroCuentaEmpleado = models.CharField(max_length=255, null=True, blank=True)
    bancoDestino = models.CharField(max_length=255, null=True, blank=True)
    mesPago = models.CharField(max_length=255, null=True, blank=True)
    anio = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=255, null=True, blank=True)
    archivoFirmado = models.FileField(blank=True, null=True, upload_to=upload_path)
    fechaFirma = models.DateTimeField(null=True, blank=True)
    user_id = models.CharField(max_length=255, null=True, blank=True)
    observacion = models.TextField()
    numeroComprobante = models.CharField(max_length=255, null=True, blank=True)
    fechaProceso = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
