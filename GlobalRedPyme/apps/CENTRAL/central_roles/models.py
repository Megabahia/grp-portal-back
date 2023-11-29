from django.db.models.signals import post_save
from django.dispatch import receiver
from djongo import models

from ..central_usuarios.models import Usuarios
from ..central_tipoUsuarios.models import TipoUsuario


# Nube: Bigpuntos
# Portales: Central, personas, corp, ifis, credit
# La clase Roles hace referencia a la tabla roles de la base datos central
class Roles(models.Model):
    _id = models.ObjectIdField()
    codigo = models.CharField(unique=True, max_length=150, null=True)
    nombre = models.CharField(max_length=150, null=False)
    descripcion = models.CharField(max_length=250, null=True, blank=True)
    config = models.TextField(default='{}', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)

    tipoUsuario = models.ForeignKey(TipoUsuario, null=True, on_delete=models.CASCADE)  # Relacion Tipo usuario

    def __str__(self):
        return self.nombre


# Nube: Bigpuntos
# Portales: Central, personas, corp, ifis, credit
# La clase RolesUsuarios hace referencia a la tabla roles de la base datos central
class RolesUsuarios(models.Model):
    _id = models.ObjectIdField()
    rol = models.ForeignKey(Roles, null=False, on_delete=models.CASCADE)  # Relacion Rol
    usuario = models.ForeignKey(Usuarios, null=False, on_delete=models.CASCADE)  # Relacion Rol    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
