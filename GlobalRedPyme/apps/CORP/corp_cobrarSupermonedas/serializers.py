from rest_framework import serializers

from .models import (
    CobrarSupermonedas
)


class CobrarSupermonedasSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla CobrarSupermonedas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = CobrarSupermonedas
        fields = '__all__'
        read_only_fields = ['_id']
