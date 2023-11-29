from bson import ObjectId
from rest_framework import serializers

from .models import (
    MovimientoCobros, Transacciones
)
from ..corp_creditoPersonas.models import RegarcarCreditos
from ..corp_creditoPersonas.serializers import RegarcarCreditosSerializer
from ..corp_pagoEmpleados.models import PagoEmpleados
from ..corp_pagoEmpleados.serializers import PagoEmpleadosSerializer
from ..corp_pagoProveedores.models import PagoProveedores
from ..corp_pagoProveedores.serializers import PagoProveedorSerializer


class MovimientoCobrosSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla MovimientoCobros
    # el campo fields indica los campos que se devolveran
    # el campo read_only_fields
    class Meta:
        model = MovimientoCobros
        fields = '__all__'
        read_only_fields = ['_id']


class TransaccionesSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla MovimientoCobros
    # el campo fields indica los campos que se devolveran
    # el campo read_only_fields
    class Meta:
        model = Transacciones
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        """
        Este metod sirve para modificar los datos que se devulveran a frontend
        @type instance: El campo instance contiene el registro de la base datos
        @rtype: Devuelve la informacion modificada
        """
        data = super(TransaccionesSerializer, self).to_representation(instance)
        pagoProveedores = data.pop('pagoProveedores')
        pagoEmpleados = data.pop('pagoEmpleados')
        regarcarCreditos = data.pop('regarcarCreditos')
        if pagoProveedores:
            data['pagoProveedor'] = PagoProveedorSerializer(PagoProveedores.objects.filter(_id=ObjectId(pagoProveedores)).first()).data
        if pagoEmpleados:
            data['pagoEmpleado'] = PagoEmpleadosSerializer(PagoEmpleados.objects.filter(_id=ObjectId(pagoEmpleados)).first()).data
        if regarcarCreditos:
            data['regarcarCredito'] = RegarcarCreditosSerializer(RegarcarCreditos.objects.filter(_id=ObjectId(regarcarCreditos)).first()).data

        return data
