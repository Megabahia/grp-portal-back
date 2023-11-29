from rest_framework import serializers

from .models import (
    Autorizaciones
)


class AutorizacionSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Autorizaciones
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        """
        Este metod sirve para modificar los datos que se devulveran a frontend
        @type instance: El campo instance contiene el registro de la base datos
        @rtype: Devuelve la informacion modificada
        """
        data = super(AutorizacionSerializer, self).to_representation(instance)
        # tomo el campo persona y convierto de OBJECTID a string
        cobrar = str(data.pop('cobrar'))
        data.update({"cobrar": cobrar})
        return data
