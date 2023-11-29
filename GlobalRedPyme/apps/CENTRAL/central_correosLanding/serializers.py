"""Nube: Bigpuntos
PORTALES: CENTER, PERSONAS
"""
from rest_framework import serializers

from .models import (
    Correos
)


# Esta clase se usa para comunicarse con la tabla de Correos landing
class CorreosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Correos
        fields = '__all__'
