from rest_framework import serializers
# ObjectId
from bson import ObjectId

from .models import (
    PreAprobados,
    ArchivosFirmados,
)

from ...CORP.corp_empresas.models import Empresas


class CreditoArchivosSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla ArchivosFirmados
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = PreAprobados
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        """
        Este metod sirve para modificar los datos que se devulveran a frontend
        @type instance: El campo instance contiene el registro de la base datos
        @rtype: Devuelve la informacion modificada
        """
        data = super(CreditoArchivosSerializer, self).to_representation(instance)
        # tomo el campo persona y convierto de OBJECTID a string
        empresa_financiera = data.pop('empresa_financiera')
        empresa_comercial = data.pop('empresa_comercial')
        entidadFinanciera = Empresas.objects.filter(_id=ObjectId(empresa_financiera), state=1).first()
        entidadComercial = Empresas.objects.filter(_id=ObjectId(empresa_comercial), state=1).first()
        if entidadFinanciera:
            data['empresa_financiera'] = entidadFinanciera.nombreComercial
        if entidadComercial:
            data['empresa_comercial'] = entidadComercial.nombreComercial
        return data


class ArchivosFirmadosSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla ArchivosFirmados
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = ArchivosFirmados
        fields = '__all__'
