import jsonfield
from djongo import models


def upload_path(instance, filname):
    """
    Este metodo se utiliza para subir los archivos
    @type filname: el campo filname es el nombre del archivo
    @type instance: el campo instance es el registro que se esta guardando
    @rtype: Devuelve la ruta del archivo donde se guardo
    """
    return '/'.join(
        ['CORP/documentosCreditosPersonas/' + str(instance.numeroIdentificacion), str(instance._id) + "_" + filname])


# Mundo: coop
# Portales: PERSONAS, coop, center
# Esta clase sirve para conectar con la tabla CreditoPersonas de la base datos corp
class CreditoPersonas(models.Model):
    _id = models.ObjectIdField()
    numero = models.IntegerField(blank=True, null=True)
    canal = models.CharField(max_length=255, blank=True, null=True)
    monto = models.FloatField(blank=True, null=True)
    montoAprobado = models.FloatField(blank=True, null=True)
    gastosAdministrativos = models.FloatField(blank=True, null=True)
    montoLiquidar = models.FloatField(blank=True, null=True)
    cuota = models.FloatField(blank=True, null=True)
    plazo = models.PositiveIntegerField(blank=True, null=True)
    aceptaTerminos = models.SmallIntegerField(default=1)
    estado = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.CharField(max_length=255, blank=True, null=True)  # Relacion usuario
    empresaComercial_id = models.CharField(max_length=255, blank=True, null=True)  # Relacion empresa comercial
    empresaIfis_id = models.CharField(max_length=255, blank=True, null=True)  # Relacion empresa ifis
    reporteBuro = models.FileField(blank=True, null=True, upload_to=upload_path)
    calificacionBuro = models.CharField(max_length=255, blank=True, null=True)
    buroValido = models.CharField(max_length=255, blank=True, null=True)
    identificacion = models.FileField(blank=True, null=True, upload_to=upload_path)
    papeletaVotacion = models.FileField(blank=True, null=True, upload_to=upload_path)
    identificacionConyuge = models.FileField(blank=True, null=True, upload_to=upload_path)
    papeletaVotacionConyuge = models.FileField(blank=True, null=True, upload_to=upload_path)
    planillaLuzNegocio = models.FileField(blank=True, null=True, upload_to=upload_path)
    planillaLuzDomicilio = models.FileField(blank=True, null=True, upload_to=upload_path)
    facturas = models.FileField(blank=True, null=True, upload_to=upload_path)
    matriculaVehiculo = models.FileField(blank=True, null=True, upload_to=upload_path)
    impuestoPredial = models.FileField(blank=True, null=True, upload_to=upload_path)
    buroCredito = models.FileField(blank=True, null=True, upload_to=upload_path)
    evaluacionCrediticia = models.FileField(blank=True, null=True, upload_to=upload_path)
    ruc = models.FileField(blank=True, null=True, upload_to=upload_path)
    rolesPago = models.FileField(blank=True, null=True, upload_to=upload_path)
    panillaIESS = models.FileField(blank=True, null=True, upload_to=upload_path)
    mecanizadoIess = models.FileField(blank=True, null=True, upload_to=upload_path)
    fotoCarnet = models.FileField(blank=True, null=True, upload_to=upload_path)
    solicitudCredito = models.FileField(blank=True, null=True, upload_to=upload_path)
    evaluacionCrediticia = models.FileField(blank=True, null=True, upload_to=upload_path)
    buroCreditoIfis = models.FileField(blank=True, null=True, upload_to=upload_path)
    pagare = models.FileField(blank=True, null=True, upload_to=upload_path)
    contratosCuenta = models.FileField(blank=True, null=True, upload_to=upload_path)
    tablaAmortizacion = models.FileField(blank=True, null=True, upload_to=upload_path)
    facturasVentas2meses = models.FileField(blank=True, null=True, upload_to=upload_path)
    facturasVentas2meses2 = models.FileField(blank=True, null=True, upload_to=upload_path)
    facturasVentas2meses3 = models.FileField(blank=True, null=True, upload_to=upload_path)
    facturasVentasCertificado = models.FileField(blank=True, null=True, upload_to=upload_path)
    codigoClienteCreado = models.CharField(max_length=255, null=True, blank=True)
    codigoCuentaCreada = models.CharField(max_length=255, null=True, blank=True)
    calificacionBuroIfis = models.CharField(max_length=255, null=True, blank=True)
    tomarSolicitud = models.CharField(max_length=255, null=True, blank=True)
    fechaAprobacion = models.DateTimeField(null=True, blank=True)
    tipoCredito = models.CharField(max_length=255, null=True, blank=True)
    concepto = models.CharField(max_length=255, null=True, blank=True)
    documentoAprobacion = models.FileField(blank=True, null=True, upload_to=upload_path)
    empresasAplican = models.TextField(null=True, blank=True)
    vigencia = models.DateField(null=True, blank=True)
    interes = models.FloatField(null=True, blank=True)
    nombres = models.CharField(max_length=255, blank=True, null=True)
    apellidos = models.CharField(max_length=255, blank=True, null=True)
    nombresCompleto = models.CharField(max_length=255, blank=True, null=True)
    fechaAprobado = models.DateField(null=True, blank=True)
    numeroIdentificacion = models.CharField(max_length=255, blank=True, null=True)
    codigoCliente = models.CharField(max_length=255, blank=True, null=True)
    codigoCorp = models.CharField(max_length=255, blank=True, null=True)
    numeroFactura = models.CharField(max_length=255, blank=True, null=True)
    montoVenta = models.CharField(max_length=255, blank=True, null=True)
    checkPagare = models.BooleanField(blank=True, null=True)
    checkTablaAmortizacion = models.BooleanField(blank=True, null=True)
    checkManualPago = models.BooleanField(blank=True, null=True)
    checkCedula = models.BooleanField(blank=True, null=True)
    external_id = models.CharField(max_length=255, blank=True, null=True)
    montoDisponible = models.FloatField(null=True, blank=True)
    codigoPreaprobado = models.CharField(max_length=255, null=True, blank=True)
    tipoPersona = models.CharField(max_length=255, null=True, blank=True)
    estadoCivil = models.CharField(max_length=255, null=True, blank=True)

    user = jsonfield.JSONField()
    observacion = models.TextField(null=True, blank=True)
    ingresosMensuales = models.TextField(null=True, blank=True)
    egresosMensuales = models.TextField(null=True, blank=True)
    patrimonio = models.TextField(null=True, blank=True)
    fechaInicioActividades = models.TextField(null=True, blank=True)
    razonSocial = models.TextField(null=True, blank=True)
    rucEmpresa = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)

    checks = jsonfield.JSONField()
    empresaInfo = jsonfield.JSONField()
    proveedor = models.CharField(max_length=255, null=True, blank=True)
    numeroFacturaproveedor = models.FileField(blank=True, null=True, upload_to=upload_path)
    motivo = models.TextField(null=True, blank=True)

    solicitudCreditoFirmado = models.FileField(blank=True, null=True, upload_to=upload_path)
    pagareFirmado = models.FileField(blank=True, null=True, upload_to=upload_path)
    contratosCuentaFirmado = models.FileField(blank=True, null=True, upload_to=upload_path)
    tablaAmortizacionFirmado = models.FileField(blank=True, null=True, upload_to=upload_path)
    facturasCompras2meses = models.FileField(blank=True, null=True, upload_to=upload_path)
    facturasCompras2meses2 = models.FileField(blank=True, null=True, upload_to=upload_path)
    nombramientoRepresentante = models.FileField(blank=True, null=True, upload_to=upload_path)
    certificadoSuperintendencia = models.FileField(blank=True, null=True, upload_to=upload_path)
    certificadoPatronales = models.FileField(blank=True, null=True, upload_to=upload_path)
    nominaSocios = models.FileField(blank=True, null=True, upload_to=upload_path)
    actaJuntaGeneral = models.FileField(blank=True, null=True, upload_to=upload_path)
    certificadoBancario = models.FileField(blank=True, null=True, upload_to=upload_path)
    referenciasComerciales = models.FileField(blank=True, null=True, upload_to=upload_path)
    balancePerdidasGanancias = models.FileField(blank=True, null=True, upload_to=upload_path)
    balanceResultados = models.FileField(blank=True, null=True, upload_to=upload_path)
    declaracionIva = models.FileField(blank=True, null=True, upload_to=upload_path)
    estadoCuentaTarjeta = models.FileField(blank=True, null=True, upload_to=upload_path)
    facturasPendiente = models.FileField(blank=True, null=True, upload_to=upload_path)
    cargarOrigen = models.TextField(null=True, blank=True)
    alcance = models.TextField(null=True, blank=True)
    enviado = models.SmallIntegerField(default=0)
    autorizacion = models.FileField(blank=True, null=True, upload_to=upload_path)

    cedulaGarante = models.FileField(blank=True, null=True, upload_to=upload_path)
    papeletaVotacionGarante = models.FileField(blank=True, null=True, upload_to=upload_path)
    fotoGarante = models.FileField(blank=True, null=True, upload_to=upload_path)
    impuestoPredialGarante = models.FileField(blank=True, null=True, upload_to=upload_path)
    matriculaVehiculoGarante = models.FileField(blank=True, null=True, upload_to=upload_path)
    planillaDomicilioGarante = models.FileField(blank=True, null=True, upload_to=upload_path)
    empresaEmpleado = jsonfield.JSONField()
    activarMenu = models.SmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)


# Mundo: coop
# Portales: PERSONAS, coop, center
# Esta clase sirve para conectar con la tabla AutorizacionCredito de la base datos corp
class AutorizacionCredito(models.Model):
    _id = models.ObjectIdField()
    codigo = models.CharField(max_length=200, null=False)
    credito = models.CharField(max_length=250, blank=False, null=False)  # Relacion credito persona
    entidad = models.CharField(max_length=250, blank=False,
                               null=False)  # Entidad hace referencina a si es una persona o una empresa se guarda el id

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)


# Mundo: coop
# Portales: PERSONAS, coop, center
# Esta clase sirve para conectar con la tabla LecturaArchivos de la base datos corp
class LecturaArchivos(models.Model):
    _id = models.ObjectIdField()
    numeroCredito = models.CharField(max_length=200, null=False)  # Relacion credito persona
    identificacion = models.CharField(max_length=250, blank=False, null=False)
    ruc = models.CharField(max_length=250, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)


# Mundo: coop
# Portales: PERSONAS, coop, center
# Esta clase sirve para conectar con la tabla CodigoCredito de la base datos corp
class CodigoCredito(models.Model):
    _id = models.ObjectIdField()
    credito_id = models.CharField(max_length=200, blank=False, null=False)
    codigo = models.CharField(max_length=250, blank=False, null=False)
    numeroIdentificacion = models.CharField(max_length=250, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)


# Mundo: coop
# Portales: PERSONAS, coop, center
# Esta clase sirve para conectar con la tabla RegarcarCreditos de la base datos corp
class RegarcarCreditos(models.Model):
    _id = models.ObjectIdField()
    fechaRecarga = models.DateField(null=True, blank=True)
    info = jsonfield.JSONField()
    monto = models.FloatField(blank=True, null=True)
    estado = models.CharField(max_length=250, blank=False, null=False)
    tipoCredito = models.CharField(max_length=250, blank=False, null=False)
    observaciones = models.TextField()
    empresaIfis_id = models.CharField(max_length=255, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
