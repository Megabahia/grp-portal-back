from rest_framework import serializers

from .models import Acciones, AccionesPermitidas, AccionesPorRol


class AccionesPadreSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Acciones
        fields = ['id', 'codigo', 'nombre']


class AccionesSerializer(serializers.ModelSerializer):
    idAccionPadre = AccionesPadreSerializer(many=False, read_only=True)

    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Acciones
        fields = '__all__'

    def to_representation(self, instance):
        """
        Este metodo se usa para modificar la respuesta de los campos
        @type instance: El campo instance contiene el registro con los campos
        @rtype: DEvuelve los valores modificados
        """
        data = super(AccionesSerializer, self).to_representation(instance)
        accionPadre = data.pop('idAccionPadre')
        if accionPadre['codigo']:
            data = {'codigoPadre': accionPadre['codigo'],
                    'info': data
                    }
        return data


class AccionesPermitidasSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = AccionesPermitidas
        fields = '__all__'


class AccionesPorRolSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = AccionesPorRol
        fields = '__all__'
