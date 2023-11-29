"""NUBE DE BIGPUNTOS
PORTALES: CENTER, PERSONAS
Este archivo sirve para conectar el backend de la nube de bigpuntos con la base datos de bigpuntos central
"""

from djongo import models

# La clase Correos se utiliza para guardar los correos que ingresan por el portal personas y lista en el portal center
class Correos(models.Model):
    fechaRegistro = models.DateField(auto_now_add=True)
    correo = models.EmailField(max_length=255,null=False, blank=False)
    correoValido = models.BooleanField(default=False)
    codigoValido = models.BooleanField(default=False)
    accedio = models.BooleanField(default=False)
    codigo = models.CharField(max_length=255,null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)