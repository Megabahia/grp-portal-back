from djongo import models
from django.utils import timezone


def upload_path(instance, filname):
    """
    Este metodo se utiliza para subir los archivos
    @type filname: el campo filname es el nombre del archivo
    @type instance: el campo instance es el registro que se esta guardando
    @rtype: Devuelve la ruta del archivo donde se guardo
    """
    return '/'.join(['CORP/documentosCreditosArchivos', str(timezone.localtime(timezone.now())) + "_" + filname])


def upload_path2(instance, filname):
    """
    Este metodo se utiliza para subir los archivos
    @type filname: el campo filname es el nombre del archivo
    @type instance: el campo instance es el registro que se esta guardando
    @rtype: Devuelve la ruta del archivo donde se guardo
    """
    return '/'.join(['CORP/archivosFirmados/' + str(instance.numeroIdentificacion),
                     str(timezone.localtime(timezone.now())) + "_" + filname])


# Mundo: coop
# Portales: PERSONAS, coop, center
# Esta clase sirve para conectar con la tabla PreAprobados de la base datos corp
class PreAprobados(models.Model):
    fechaCargaArchivo = models.DateField(null=True)
    campania = models.CharField(max_length=255, null=True, blank=True)
    registrosCargados = models.CharField(max_length=255, null=True, blank=True)
    linkArchivo = models.FileField(blank=True, null=True, upload_to=upload_path)
    tamanioArchivo = models.CharField(max_length=255, null=True, blank=True)
    usuarioCargo = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.CharField(max_length=255, null=True, blank=True)  # Relacion de usuario
    tipoCredito = models.CharField(max_length=255, null=True, blank=True)
    empresa_financiera = models.CharField(max_length=255, null=True, blank=True)
    empresa_comercial = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)


# Mundo: coop
# Portales: PERSONAS, coop, center
# Esta clase sirve para conectar con la tabla ArchivosFirmados de la base datos corp
class ArchivosFirmados(models.Model):
    _id = models.ObjectIdField()
    solicitudCredito = models.FileField(blank=True, null=True, upload_to=upload_path2)
    evaluacionCrediticia = models.FileField(blank=True, null=True, upload_to=upload_path2)
    buro = models.FileField(blank=True, null=True, upload_to=upload_path2)
    identificacion = models.FileField(blank=True, null=True, upload_to=upload_path2)
    papeletaVotacion = models.FileField(blank=True, null=True, upload_to=upload_path2)
    identificacionConyuge = models.FileField(blank=True, null=True, upload_to=upload_path2)
    papeletaVotacionConyuge = models.FileField(blank=True, null=True, upload_to=upload_path2)
    planillaLuzNegocio = models.FileField(blank=True, null=True, upload_to=upload_path2)
    planillaLuzDomicilio = models.FileField(blank=True, null=True, upload_to=upload_path2)
    facturas = models.FileField(blank=True, null=True, upload_to=upload_path2)
    buroCredito = models.FileField(blank=True, null=True, upload_to=upload_path2)
    ruc = models.FileField(blank=True, null=True, upload_to=upload_path2)
    rolesPago = models.FileField(blank=True, null=True, upload_to=upload_path2)
    panillaIESS = models.FileField(blank=True, null=True, upload_to=upload_path2)
    mecanizadoIees = models.FileField(blank=True, null=True, upload_to=upload_path2)
    matriculaVehiculo = models.FileField(blank=True, null=True, upload_to=upload_path2)
    impuestoPredial = models.FileField(blank=True, null=True, upload_to=upload_path2)
    autorizacionInformacion = models.FileField(blank=True, null=True, upload_to=upload_path2)
    fichaCliente = models.FileField(blank=True, null=True, upload_to=upload_path2)
    conveniosCuenta = models.FileField(blank=True, null=True, upload_to=upload_path2)
    pagare = models.FileField(blank=True, null=True, upload_to=upload_path2)
    tablaAmortizacion = models.FileField(blank=True, null=True, upload_to=upload_path2)
    seguroDesgravamen = models.FileField(blank=True, null=True, upload_to=upload_path2)
    gastosAdministracion = models.FileField(blank=True, null=True, upload_to=upload_path2)
    mecanizadoIess = models.FileField(blank=True, null=True, upload_to=upload_path2)
    fotoCarnet = models.FileField(blank=True, null=True, upload_to=upload_path2)
    buroCreditoIfis = models.FileField(blank=True, null=True, upload_to=upload_path2)
    contratosCuenta = models.FileField(blank=True, null=True, upload_to=upload_path2)
    facturasVentas2meses = models.FileField(blank=True, null=True, upload_to=upload_path2)
    facturasVentas2meses2 = models.FileField(blank=True, null=True, upload_to=upload_path2)
    facturasVentas2meses3 = models.FileField(blank=True, null=True, upload_to=upload_path2)
    facturasVentasCertificado = models.FileField(blank=True, null=True, upload_to=upload_path2)
    facturasVenta = models.FileField(blank=True, null=True, upload_to=upload_path2)
    facturasCompra = models.FileField(blank=True, null=True, upload_to=upload_path2)
    numeroIdentificacion = models.CharField(max_length=255, blank=False, null=False)
    credito_id = models.CharField(max_length=255, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
