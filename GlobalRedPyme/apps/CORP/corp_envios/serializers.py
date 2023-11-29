from rest_framework import serializers

from .models import (
    Envios
)


class EnviosSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Envios
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Envios
        fields = '__all__'
        read_only_fields = ['_id']
