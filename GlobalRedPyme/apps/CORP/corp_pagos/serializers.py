from rest_framework import serializers

from .models import (
    Pagos
)


class PagosSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Pagos
        fields = '__all__'
        read_only_fields = ['_id']
