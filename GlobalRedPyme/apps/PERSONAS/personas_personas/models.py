import jsonfield
from djongo import models


def upload_path(instance, filname):
    """
    Este metodo se utiliza para subir los archivos
    @type filname: el campo filname es el nombre del archivo
    @type instance: el campo instance es el registro que se esta guardando
    @rtype: Devuelve la ruta del archivo donde se guardo
    """
    return '/'.join(['PERSONAS/imgPersonas', str(instance._id) + "_" + filname])


# Mundo: bigpuntos
# Portales: PERSONAS
# Esta clase sirve para conectar con la tabla personas de la base datos personas
class Personas(models.Model):
    _id = models.ObjectIdField()
    identificacion = models.TextField()
    nombres = models.TextField()
    apellidos = models.TextField()
    nombresCompleto = models.TextField()
    genero = models.TextField()
    fechaNacimiento = models.TextField()
    edad = models.TextField()
    ciudad = models.TextField()
    provincia = models.TextField()
    pais = models.TextField()
    direccion = models.TextField()
    email = models.TextField()
    emailAdicional = models.TextField()
    telefono = models.TextField()
    whatsapp = models.TextField()
    facebook = models.TextField()
    instagram = models.TextField()
    twitter = models.TextField()
    tiktok = models.TextField()
    youtube = models.TextField()
    imagen = models.FileField(blank=True, null=True, upload_to=upload_path)
    user_id = models.CharField(max_length=250, blank=False, null=False)  # Relacion usuario
    empresaInfo = models.TextField()
    nivelInstruccion = models.TextField()
    tipoVivienda = models.TextField()
    nombreDueno = models.TextField()
    direccionDomicilio = models.TextField()
    referenciaDomicilio = models.TextField()
    ocupacionSolicitante = models.TextField()
    referenciasSolicitante = models.TextField()
    ingresosSolicitante = models.TextField()
    gastosSolicitante = models.TextField()
    datosPyme = models.TextField()
    estadoCivil = models.TextField()
    cedulaRepresentante = models.TextField()
    direccionRepresentante = models.TextField()
    celularRepresentante = models.TextField()
    whatsappRepresentante = models.TextField()
    correoRepresentante = models.TextField()
    tipoIdentificacion = models.TextField()
    tipoPersona = models.TextField()
    celular = models.TextField()
    codigoUsuario = models.TextField()
    autorizacion = models.TextField()
    garante = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)


# Mundo: bigpuntos
# Portales: PERSONAS
# Esta clase sirve para conectar con la tabla personas de la base datos personas
class ValidarCuenta(models.Model):
    _id = models.ObjectIdField()
    codigo = models.CharField(max_length=200, null=False)
    user_id = models.CharField(max_length=250, blank=False, null=False)  # Relacion usuario

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
