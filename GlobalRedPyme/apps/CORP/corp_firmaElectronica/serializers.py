from rest_framework import serializers

from .models import (
    FirmaElectronica
)


class FirmaElectronicaSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = FirmaElectronica
        fields = '__all__'
        read_only_fields = ['_id']
