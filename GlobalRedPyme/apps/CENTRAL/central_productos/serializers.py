from rest_framework import serializers
# ObjectId
from bson import ObjectId

from ...CORP.corp_empresas.models import Empresas
from ...CORP.corp_empresas.serializers import EmpresasSerializer

from .models import (
    Productos
)


# NUBE DE BIGPUNTOS
# PORTALES: CENTER, PERSONAS
# Esta clase sirve para conectar el modelo de la tabla de Productos de la nube de bigpuntos
# para convertir en un objeto de python con el objetivo de manipular los datos y se utiliza
# para retornar todos los campos de la tabla
class ProductosSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Productos
        fields = '__all__'

    def to_representation(self, instance):
        """
        Este metodo se usa para modificar los datos que se devolveran a de la productos
        @type instance: el campo instance son los valores que se desean modificar
        @rtype: revuelve los campos que se modificaron
        """
        data = super(ProductosSerializer, self).to_representation(instance)
        empresa_id = data.pop('empresa_id')
        empresa = Empresas.objects.get(pk=ObjectId(empresa_id))
        if empresa:
            data['empresa'] = empresa.nombreComercial
            data['local'] = empresa.direccion
            data['pais'] = empresa.pais
            data['provincia'] = empresa.provincia
            data['ciudad'] = empresa.ciudad
            data['imagen_empresa'] = EmpresasSerializer(empresa).data['imagen']
        return data


class ProductosImagenSerializer(serializers.HyperlinkedModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Productos
        fields = ['imagen', 'updated_at']
