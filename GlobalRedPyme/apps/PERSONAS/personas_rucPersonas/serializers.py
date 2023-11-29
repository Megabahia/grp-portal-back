from rest_framework import serializers

from .models import (
    RucPersonas
)


class RucPersonasSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla RucPersonas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = RucPersonas
        fields = '__all__'
        read_only_fields = ['_id']
