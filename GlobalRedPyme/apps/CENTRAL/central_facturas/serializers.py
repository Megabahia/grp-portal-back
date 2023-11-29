import xmltodict
from datetime import datetime

from rest_framework import serializers


from .models import (
    Facturas
)

# NUBE DE BIGPUNTOS
# PORTALES: CENTER, PERSONAS
# Esta clase sirve para conectar el modelo de la tabla de Facturas de la nube de bigpuntos
# para convertir en un objeto de python con el objetivo de manipular los datos y se utiliza
# para retornar todos los campos de la tabla
class FacturasSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Facturas
        fields = '__all__'

# NUBE DE BIGPUNTOS
# PORTALES: CENTER, PERSONAS
# Esta clase sirve para conectar el modelo de la tabla de Facturas de la nube de bigpuntos
# para convertir en un objeto de python con el objetivo de manipular los datos y se utiliza
# para retornar todos los campos de la tabla
class SubirFacturasSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Facturas
        fields = ['urlArchivo','user_id']

    # def create(self, validated_data):
    #     extension = str(validated_data['urlArchivo'])
    #     if '.xml' in extension:
    #         archivoXML = dict(xmltodict.parse(validated_data['urlArchivo']))
    #         if 'RespuestaAutorizacionComprobante' in archivoXML.keys():
    #             archivoXML = archivoXML['RespuestaAutorizacionComprobante']['autorizaciones']
            
    #         if 'autorizacion' in archivoXML.keys():
    #             contentido = archivoXML['autorizacion']
    #         else:
    #             contentido = archivoXML['Autorizacion']

            
    #         comprobante = xmltodict.parse(contentido['comprobante'])
            
    #         validated_data['razonSocial'] = comprobante['factura']['infoTributaria']['razonSocial']
    #         validated_data['fechaEmision'] = datetime.strptime(comprobante['factura']['infoFactura']['fechaEmision'],'%d/%m/%Y')
    #         validated_data['importeTotal'] = comprobante['factura']['infoFactura']['importeTotal']
    #         validated_data['numeroFactura'] = contentido['numeroAutorizacion'][24:39]

    #     factura = Facturas.objects.create(**validated_data)
    #     return factura


# NUBE DE BIGPUNTOS
# PORTALES: CENTER, PERSONAS
# Esta clase sirve para conectar el modelo de la tabla de Facturas de la nube de bigpuntos
# para convertir en un objeto de python con el objetivo de manipular los datos y se utiliza
# para retornar todos los campos de la tabla
# Listar factura
class ListFacturasSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveranƒ
    class Meta:
        model = Facturas
        fields = ['_id', 'created_at', 'numeroFactura',
                  'urlFoto', 'urlArchivo', 'estado', 'razonSocial','pais','provincia','ciudad','importeTotal']
