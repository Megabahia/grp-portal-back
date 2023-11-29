import json
from rest_framework import serializers
# ObjectId
from bson import ObjectId

from .models import (
    CreditoPersonas,
    CodigoCredito,
    RegarcarCreditos,
)

from ..corp_empresas.models import Empresas
from ...PERSONAS.personas_personas.models import Personas
from ..corp_empresas.serializers import EmpresasInfoBasicaSerializer


class CreditoPersonasSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla CreditoPersonas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = CreditoPersonas
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        """
        Este metod sirve para modificar los datos que se devulveran a frontend
        @type instance: El campo instance contiene el registro de la base datos
        @rtype: Devuelve la informacion modificada
        """
        data = super(CreditoPersonasSerializer, self).to_representation(instance)
        # tomo el campo persona y convierto de OBJECTID a string
        # empresaIfis_id = data.pop('empresaIfis_id')
        # entidadFinanciera = Empresas.objects.filter(_id=ObjectId(empresaIfis_id), state=1).first()
        # data.update({"entidadFinanciera": entidadFinanciera.nombreComercial})
        # data['empresaIfis_id'] = str(empresaIfis_id)
        # empresaSerializer = EmpresasInfoBasicaSerializer(entidadFinanciera).data
        # data['imagen'] = empresaSerializer['imagen']
        # # Info empresa comercial
        # empresaComercial_id = data.pop('empresaComercial_id')
        # data['empresaComercial_id'] = str(empresaComercial_id)
        # if empresaComercial_id:
        #     entidadComercial = Empresas.objects.filter(_id=ObjectId(empresaComercial_id), state=1).first()
        #     data['rucComercial'] = entidadComercial.ruc
        #     data['nombreComercial'] = entidadComercial.nombreComercial
        #     data['correoCorp'] = entidadComercial.correo
        #     data['telefono1'] = entidadComercial.telefono1
        #     data['imagenComercial'] = EmpresasInfoBasicaSerializer(entidadComercial).data['imagen']
        # Informacion persona
        # persona = Personas.objects.filter(user_id=str(instance.user_id),state=1).first()
        # if persona is not None:
        #     data.update({"nombres": persona.nombres})
        #     data.update({"apellidos": persona.apellidos})
        #     data.update({"whatsappPersona": persona.whatsapp})
        #     data.update({"emailPersona": persona.email})
        return data


class CreditoPersonasPersonaSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla ArchivosFirmados
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = CreditoPersonas
        fields = ['_id', 'monto', 'plazo', 'user_id', 'empresaIfis_id']
        read_only_fields = ['_id']

    def to_representation(self, instance):
        """
        Este metod sirve para modificar los datos que se devulveran a frontend
        @type instance: El campo instance contiene el registro de la base datos
        @rtype: Devuelve la informacion modificada
        """
        data = super(CreditoPersonasPersonaSerializer, self).to_representation(instance)
        # tomo el campo persona y convierto de OBJECTID a string
        empresaIfis_id = data.pop('empresaIfis_id')
        entidadFinanciera = Empresas.objects.filter(_id=ObjectId(empresaIfis_id), state=1).first()
        data.update({"entidadFinanciera": entidadFinanciera.nombreComercial})
        data['empresaIfis_id'] = str(empresaIfis_id)
        empresaSerializer = EmpresasInfoBasicaSerializer(entidadFinanciera).data
        data['imagen'] = empresaSerializer['imagen']
        # Informacion persona
        persona = Personas.objects.filter(user_id=str(instance.user_id), state=1).first()
        if persona is not None:
            data.update({"identificacion": persona.identificacion})
            data.update({"nombres": persona.nombres})
            data.update({"apellidos": persona.apellidos})
            data.update({"pais": persona.pais})
            data.update({"provincia": persona.provincia})
            data.update({"ciudad": persona.ciudad})
            data.update({"telefono": persona.telefono})
            data.update({"whatsapp": persona.whatsapp})
            data.update({"email": persona.email})
        return data


class CodigoCreditoSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla ArchivosFirmados
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = CodigoCredito
        fields = '__all__'
        read_only_fields = ['_id']


class RegarcarCreditosSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla ArchivosFirmados
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = RegarcarCreditos
        fields = '__all__'
        read_only_fields = ['_id']
