from djongo import models


def upload_path(instance, filname):
    """
    Este metodo se utiliza para subir los archivos
    @type filname: el campo filname es el nombre del archivo
    @type instance: el campo instance es el registro que se esta guardando
    @rtype: Devuelve la ruta del archivo donde se guardo
    """
    return '/'.join(['CENTRAL/imgPublicaciones', str(instance._id) + "_" + filname])


from ..central_usuarios.models import Usuarios


# Nube: Bigpuntos
# Portales: CEntral, Personas
# Se usa para almacenar las publicaciones en la tabla de publicaciones de base datos central
class Publicaciones(models.Model):
    _id = models.ObjectIdField()
    titulo = models.CharField(max_length=200, null=False)
    subtitulo = models.CharField(max_length=200, null=False)
    descripcion = models.TextField(null=False)
    imagen = models.FileField(blank=True, null=True, upload_to=upload_path)
    url = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)


# Nube: Bigpuntos
# Portales: CEntral, Personas
# Se usa para llevar un registro de las veces que un usuario comparte una publicacion
class CompartirPublicaciones(models.Model):
    _id = models.ObjectIdField()
    publicacion = models.ForeignKey(Publicaciones, null=False, on_delete=models.CASCADE)  # Relacion Rol
    user = models.ForeignKey(Usuarios, null=False, on_delete=models.CASCADE)  # Relacion Rol   

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
