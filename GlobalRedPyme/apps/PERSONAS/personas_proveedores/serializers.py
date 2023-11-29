from rest_framework import serializers

from .models import (
    Proveedores
)


class ProveedoresSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Proveedores
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Proveedores
        fields = '__all__'
        read_only_fields = ['_id']
