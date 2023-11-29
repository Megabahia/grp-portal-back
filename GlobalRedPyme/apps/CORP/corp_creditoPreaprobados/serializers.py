from rest_framework import serializers
# ObjectId
from bson import ObjectId

from .models import (
    CreditoPreaprobados
)

from ...CORP.corp_empresas.models import Empresas
from ...PERSONAS.personas_personas.models import Personas
from ...PERSONAS.personas_rucPersonas.models import RucPersonas
from ...CORP.corp_notasPedidos.models import FacturasEncabezados
from ...CENTRAL.central_usuarios.models import UsuariosEmpresas
from ...CORP.corp_empresas.serializers import EmpresasInfoBasicaSerializer


class CreditoPreaprobadosSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = CreditoPreaprobados
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        """
        Este metod sirve para modificar los datos que se devulveran a frontend
        @type instance: El campo instance contiene el registro de la base datos
        @rtype: Devuelve la informacion modificada
        """
        data = super(CreditoPreaprobadosSerializer, self).to_representation(instance)
        # tomo el campo persona y convierto de OBJECTID a string
        empresa_financiera = data.pop('empresa_financiera')
        entidadFinanciera = Empresas.objects.filter(_id=empresa_financiera, state=1).first()
        data.update({"entidadFinanciera": entidadFinanciera.nombreComercial})
        data['empresa_financiera'] = str(empresa_financiera)
        empresaSerializer = EmpresasInfoBasicaSerializer(entidadFinanciera).data
        data['imagen'] = empresaSerializer['imagen']
        # Informacion persona
        persona = Personas.objects.filter(user_id=str(instance.user_id), state=1).first()
        if persona is not None:
            data.update({"nombres": persona.nombres})
            data.update({"apellidos": persona.apellidos})
        return data


class CreditoPreaprobadosIfisSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = CreditoPreaprobados
        fields = ['_id', 'fechaAprobado', 'estado', 'empresa_comercial', 'monto', 'plazo', 'interes', 'vigencia',
                  'concepto']
        read_only_fields = ['_id']

    def to_representation(self, instance):
        """
        Este metod sirve para modificar los datos que se devulveran a frontend
        @type instance: El campo instance contiene el registro de la base datos
        @rtype: Devuelve la informacion modificada
        """
        data = super(CreditoPreaprobadosIfisSerializer, self).to_representation(instance)
        # tomo el campo persona y convierto de OBJECTID a string
        empresa_comercial = data.pop('empresa_comercial')
        empresa_comercial = Empresas.objects.filter(_id=ObjectId(empresa_comercial), state=1).first()
        empresaSerializer = EmpresasInfoBasicaSerializer(empresa_comercial).data
        data.update({"empresa_comercial": empresaSerializer['nombreComercial']})
        data['empresa_comercial_id'] = empresaSerializer['_id']
        data['imagen'] = empresaSerializer['imagen']
        # Informacion persona
        persona = Personas.objects.filter(user_id=str(instance.user_id), state=1).first()
        if persona is not None:
            data.update({"nombres": persona.nombres})
            data.update({"apellidos": persona.apellidos})
            data.update({"identificacion": persona.identificacion})
            data.update({"telefono": persona.telefono})
        # Ruc de la persona
        rucPersona = RucPersonas.objects.filter(user_id=str(instance.user_id), state=1).first()
        if rucPersona is not None:
            data.update({"ruc_persona": rucPersona.ruc})
        # Info de nota pedido
        factura = FacturasEncabezados.objects.filter(credito=instance._id, state=1).first()
        if factura is not None:
            data.update({"numeroFactura": int(factura.numeroFactura)})
        # Info de la empresa que trabaja
        usuarioEmpresa = UsuariosEmpresas.objects.filter(usuario=ObjectId(instance.user_id), state=1).first()
        if usuarioEmpresa is not None:
            empresaTrabaja = Empresas.objects.filter(_id=ObjectId(usuarioEmpresa.empresa_id), state=1).first()
            data.update({"ruc": empresaTrabaja.ruc})
            data.update({"empresa_id": str(empresaTrabaja._id)})
            data.update({"empresa_trabaja": str(empresaTrabaja.nombreComercial)})
        return data
