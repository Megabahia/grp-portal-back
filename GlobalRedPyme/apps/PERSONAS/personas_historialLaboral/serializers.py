from rest_framework import serializers
# ObjectId
from bson import ObjectId

from .models import (
    HistorialLaboral
)

from ...CORP.corp_empresas.models import Empresas
from ...CORP.corp_empresas.serializers import EmpresasInfoBasicaSerializer


class HistorialLaboralSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = HistorialLaboral
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        """
        Este metodo se usa para modificar la respuesta de los campos
        @type instance: El campo instance contiene el registro con los campos
        @rtype: DEvuelve los valores modificados
        """
        data = super(HistorialLaboralSerializer, self).to_representation(instance)
        # tomo el campo persona y convierto de OBJECTID a string
        empresa = str(data.pop('empresa'))
        empresa = Empresas.objects.filter(pk=ObjectId(empresa), state=1).first()
        if (empresa):
            serializer = EmpresasInfoBasicaSerializer(empresa)
            data['nombreEmpresa'] = serializer.data['nombreEmpresa']
            data['nombreComercial'] = serializer.data['nombreComercial']
            data['imagen'] = serializer.data['imagen']
        return data
