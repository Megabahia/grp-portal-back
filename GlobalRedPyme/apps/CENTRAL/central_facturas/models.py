from djongo import models


def upload_path(instance, filname):
    """
    Este metodo se utiliza para subir los archivos
    @type filname: el campo filname es el nombre del archivo
    @type instance: el campo instance es el registro que se esta guardando
    @rtype: Devuelve la ruta del archivo donde se guardo
    """
    return '/'.join(['CENTRAL/imgFacturas', filname])


def upload_path2(instance, filname):
    """
    Este metodo se utiliza para subir los archivos
    @type filname: el campo filname es el nombre del archivo
    @type instance: el campo instance es el registro que se esta guardando
    @rtype: Devuelve la ruta del archivo donde se guardo
    """
    return '/'.join(['CENTRAL/archivosFacturas', filname])


# Esta clase se relaciona con la tabla facturas de la base datos central
class Facturas(models.Model):
    _id = models.ObjectIdField()
    numeroFactura = models.CharField(max_length=200, null=True, blank=True)
    razonSocial = models.TextField(max_length=200, null=False, blank=False)
    pais = models.CharField(max_length=255, null=True, blank=True)
    provincia = models.CharField(max_length=255, null=True, blank=True)
    ciudad = models.CharField(max_length=255, null=True, blank=True)
    fechaEmision = models.DateField(null=True, blank=True)
    importeTotal = models.FloatField(null=False, blank=False)
    categoria = models.CharField(max_length=200, null=True, blank=True)
    urlFoto = models.FileField(blank=True, null=True, upload_to=upload_path)
    urlArchivo = models.FileField(blank=True, null=True, upload_to=upload_path2)
    estado = models.CharField(max_length=200, null=True, blank=True, default='Sin calificar')
    user_id = models.CharField(max_length=255, null=True, blank=True)
    atencion = models.CharField(max_length=255, null=True, blank=True)
    calificacion = models.SmallIntegerField(null=True, blank=True)
    observaciones = models.TextField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
