import jsonfield
from djongo import models
from ..corp_empresas.models import Empresas


def upload_path(instance, filname):
    """
    Este metodo se utiliza para subir los archivos
    @type filname: el campo filname es el nombre del archivo
    @type instance: el campo instance es el registro que se esta guardando
    @rtype: Devuelve la ruta del archivo donde se guardo
    """
    return '/'.join(['CORP/facturas', str(instance._id) + "_" + filname])


# Nube: coop
# PORTALES: CENTER, CORP
# Esta clase sirve para relacionar la tabla facturas encabezado de la base datos corp
class FacturasEncabezados(models.Model):
    numeroFactura = models.CharField(max_length=150, null=True, blank=True)
    fecha = models.DateField(null=True)
    tipoIdentificacion = models.CharField(max_length=150, null=True, blank=True)
    identificacion = models.CharField(max_length=150, null=True, blank=True)
    razonSocial = models.CharField(max_length=150, null=True, blank=True)
    direccion = models.CharField(max_length=150, null=True, blank=True)
    telefono = models.CharField(max_length=150, null=True, blank=True)
    correo = models.EmailField(max_length=150, null=True, blank=True)
    nombreVendedor = models.CharField(max_length=150, null=True, blank=True)
    subTotal = models.FloatField(null=True, blank=True)
    descuento = models.FloatField(null=True, blank=True)
    iva = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    canal = models.CharField(max_length=150, null=True, blank=True)
    numeroProductosComprados = models.IntegerField(null=True, blank=True)
    user_id = models.CharField(max_length=255, null=True, blank=True)  # Relacion de usuario
    empresaComercial = models.ForeignKey(Empresas, null=True, on_delete=models.DO_NOTHING)  # Relacion Con la categoria
    credito = models.CharField(max_length=255, null=True, blank=True)  # Relacion Con el credito persona
    estado = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)


# Nube: coop
# PORTALES: CENTER, CORP
# Esta clase sirve para relacionar la tabla facturas detalle de la base datos corp
class FacturasDetalles(models.Model):
    # NOMBRAMOS A LA RELACION DETALLATES
    facturaEncabezado = models.ForeignKey(FacturasEncabezados, related_name='detalles', null=True, blank=True,
                                          on_delete=models.DO_NOTHING)  # Relacion Factura
    articulo = models.CharField(max_length=150, null=True, blank=True)
    valorUnitario = models.FloatField(null=True, blank=True)
    cantidad = models.PositiveIntegerField(null=True, blank=True)
    precio = models.FloatField(null=True, blank=True)
    codigo = models.CharField(max_length=250, null=True, blank=True)
    informacionAdicional = models.CharField(max_length=250, null=True, blank=True)
    descuento = models.FloatField(null=True, blank=True)
    impuesto = models.FloatField(null=True, blank=True)
    valorDescuento = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)


# Nube: coop
# PORTALES: CENTER, CORP
# Esta clase sirve para relacionar la tabla facturas fisicas de la base datos corp
class FacturasFisicas(models.Model):
    _id = models.ObjectIdField()
    credito_id = models.CharField(max_length=255, null=True, blank=True)
    cliente = jsonfield.JSONField()
    descripcion = models.CharField(max_length=150, null=True, blank=True)
    cantidad = models.PositiveIntegerField(null=True, blank=True)
    precio = models.FloatField(null=True, blank=True)
    facturaFisica = models.FileField(blank=True, null=True, upload_to=upload_path)
    cooperativa = models.CharField(max_length=150, null=True, blank=True)
    estado = models.CharField(max_length=255, null=True, blank=True)
    casaComercial = jsonfield.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
