from rest_framework import serializers

from .models import FacturasEncabezados, FacturasDetalles, FacturasFisicas
# Archivos firmados
from ..corp_creditoArchivos.models import ArchivosFirmados
from ..corp_creditoArchivos.serializers import ArchivosFirmadosSerializer

from datetime import datetime
from django.utils import timezone
import json


# Actualizar factura
class FacturasDetallesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = FacturasDetalles
        fields = '__all__'


class FacturasSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    detalles = FacturasDetallesSerializer(many=True, allow_empty=False)

    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = FacturasEncabezados
        fields = '__all__'

    def update(self, instance, validated_data):
        """
        ESte metodo sirve para actulizar la factura de la tabla factura detalle
        @type validated_data: El campo validated_data para obtener el registro actualizar
        @type instance: El campo instance obtiene el registro de la tabla factura encabezado
        @rtype: Devuelve el registro actualizado
        """
        detalles_database = {detalle.id: detalle for detalle in instance.detalles.all()}
        detalles_actualizar = {item['id']: item for item in validated_data['detalles']}

        # Actualiza la factura cabecera
        instance.__dict__.update(validated_data)
        instance.save()

        # Eliminar los detalles que no esté incluida en la solicitud de la factura detalles
        for detalle in instance.detalles.all():
            if detalle.id not in detalles_actualizar:
                detalle.delete()

        # Crear o actualizar instancias de detalles que se encuentran en la solicitud de factura detalles
        for detalle_id, data in detalles_actualizar.items():
            detalle = detalles_database.get(detalle_id, None)
            if detalle is None:
                data.pop('id')
                FacturasDetalles.objects.create(**data)
            else:
                now = timezone.localtime(timezone.now())
                data['updated_at'] = str(now)
                FacturasDetalles.objects.filter(id=detalle.id).update(**data)

        return instance


# Listar las facturas cabecera
class FacturasListarSerializer(serializers.ModelSerializer):
    detalles = FacturasDetallesSerializer(many=True, allow_empty=False)

    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = FacturasEncabezados
        fields = '__all__'

    def to_representation(self, instance):
        """
        Este metod sirve para modificar los datos que se devulveran a frontend
        @type instance: El campo instance contiene el registro de la base datos
        @rtype: Devuelve la informacion modificada
        """
        data = super(FacturasListarSerializer, self).to_representation(instance)
        # Quitar los credito de la factura
        credito = str(data.pop('credito'))
        data.update({"credito": credito})
        # Quitar los empresaComercial de la factura
        empresaComercial = str(data.pop('empresaComercial'))
        data.update({"empresaComercial": empresaComercial})
        # Quitar los detalles de la factura
        detalles = data.pop('detalles')
        articulos = ''
        for detalle in detalles:
            articulos += detalle['articulo'] + ','
        data.update({"detalles": articulos})
        return data


# Listar las facturas cabecera tabla
class FacturasListarTablaSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = FacturasEncabezados
        fields = ['id', 'numeroFactura', 'created_at', 'canal', 'numeroProductosComprados', 'total']


# Crear factura
class DetallesSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = FacturasDetalles
        fields = '__all__'


class FacturaSerializer(serializers.ModelSerializer):
    detalles = DetallesSerializer(many=True, allow_empty=False)

    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = FacturasEncabezados
        fields = '__all__'

    def create(self, validated_data):
        """
        ESte metodo sirve para crear la factura de la tabla factura
        @type validated_data: El campo validated_data para obtener el crear registro
        @rtype: Devuelve el registro actualizado
        """
        detalles_data = validated_data.pop('detalles')
        facturaEncabezado = FacturasEncabezados.objects.create(**validated_data)
        if facturaEncabezado.numeroFactura is not None:
            facturaEncabezado.numeroFactura = facturaEncabezado.id + 1
            facturaEncabezado.save()
        else:
            facturaEncabezado.numeroFactura = 1
            facturaEncabezado.save()
        for detalle_data in detalles_data:
            FacturasDetalles.objects.create(facturaEncabezado=facturaEncabezado, **detalle_data)
        return facturaEncabezado

    def to_representation(self, instance):
        """
        Este metod sirve para modificar los datos que se devulveran a frontend
        @type instance: El campo instance contiene el registro de la base datos
        @rtype: Devuelve la informacion modificada
        """
        data = super(FacturaSerializer, self).to_representation(instance)
        # Quitar los credito de la factura
        credito = str(data.pop('credito'))
        data.update({"credito": credito})
        # Quitar los empresaComercial de la factura
        empresaComercial = str(data.pop('empresaComercial'))
        data.update({"empresaComercial": empresaComercial})
        return data


# Actualizar factura
class FacturasDetallesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = FacturasDetalles
        fields = '__all__'


class FacturasSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    detalles = FacturasDetallesSerializer(many=True, allow_empty=False)

    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = FacturasEncabezados
        fields = '__all__'

    def update(self, instance, validated_data):
        """
        ESte metodo sirve para actulizar la factura de la tabla factura detalle
        @type validated_data: El campo validated_data para obtener el registro actualizar
        @type instance: El campo instance obtiene el registro de la tabla factura encabezado
        @rtype: Devuelve el registro actualizado
        """
        # Actualiza la factura cabecera
        instance.__dict__.update(validated_data)
        instance.save()

        if 'detalles' not in validated_data:
            return instance
        detalles_database = {detalle.id: detalle for detalle in instance.detalles.all()}
        detalles_actualizar = {item['id']: item for item in validated_data['detalles']}

        # Eliminar los detalles que no esté incluida en la solicitud de la factura detalles
        for detalle in instance.detalles.all():
            if detalle.id not in detalles_actualizar:
                detalle.delete()

        # Crear o actualizar instancias de detalles que se encuentran en la solicitud de factura detalles
        for detalle_id, data in detalles_actualizar.items():
            detalle = detalles_database.get(detalle_id, None)
            if detalle is None:
                data.pop('id')
                FacturasDetalles.objects.create(**data)
            else:
                now = timezone.localtime(timezone.now())
                data['updated_at'] = str(now)
                FacturasDetalles.objects.filter(id=detalle.id).update(**data)

        return instance

    def to_representation(self, instance):
        """
        Este metod sirve para modificar los datos que se devulveran a frontend
        @type instance: El campo instance contiene el registro de la base datos
        @rtype: Devuelve la informacion modificada
        """
        data = super(FacturasSerializer, self).to_representation(instance)
        # Quitar los credito de la factura
        credito = str(data.pop('credito'))
        data.update({"credito": credito})
        # Quitar los empresaComercial de la factura
        empresaComercial = str(data.pop('empresaComercial'))
        data.update({"empresaComercial": empresaComercial})
        return data


class FacturasFisicasSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = FacturasFisicas
        fields = '__all__'

    def to_representation(self, instance):
        """
        Este metod sirve para modificar los datos que se devulveran a frontend
        @type instance: El campo instance contiene el registro de la base datos
        @rtype: Devuelve la informacion modificada
        """
        data = super(FacturasFisicasSerializer, self).to_representation(instance)
        cliente = json.loads(data['cliente'])
        # Quitar los credito de la factura
        try:
            archivos = ArchivosFirmados.objects.filter(numeroIdentificacion=cliente['identificacion']).first()
            archivosSerializer = ArchivosFirmadosSerializer(archivos).data
            data.update({"archivos": archivosSerializer})
        except ArchivosFirmados.DoesNotExist:
            data.update({"archivos": {}})
        return data
