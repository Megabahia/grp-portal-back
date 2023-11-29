from rest_framework import serializers

from .models import (
    MonedasEmpresa
)


class MonedasEmpresaSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    # el campo read_only_fields solo permite la lectura de los campos
    class Meta:
        model = MonedasEmpresa
        fields = '__all__'
        read_only_fields = ['_id']
