"""Nube: Bigpuntos
PORTALES: CENTER, PERSONAS
Este archivo sirve para conectar el backend de la nube de bigpuntos con la base datos de bigpuntos central
"""

from djongo import models
from ..central_usuarios.models import Usuarios


# ESTA CLASE se relaciona con la tabla infousuario de la base datos central
class InfoUsuarios(models.Model):
    _id = models.ObjectIdField()
    nombres = models.CharField(max_length=200, null=True, blank=True)
    apellidos = models.CharField(max_length=200, null=True, blank=True)
    telefono = models.CharField(max_length=200, null=True, blank=True)
    whatsapp = models.CharField(max_length=200, null=True, blank=True)
    cargo = models.CharField(max_length=200, null=True, blank=True)
    fechaNacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(default="Activo", max_length=200, null=True, blank=True)
    usuario = models.ForeignKey(Usuarios, null=False, on_delete=models.CASCADE)  # Relacion Rol    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
