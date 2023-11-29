from rest_framework import serializers

from .models import Catalogo


# NUBE DE BIGPUNTOS
# PORTALES: CENTER, CORP, PERSONAS, IFIS, CREDIT
# Esta clase sirve para conectar el modelo de la tabla de catalogo de la nube de bigpuntos
# para convertir en un objeto de python con el objetivo de manipular los datos y se utiliza
# para retornar todos los campos de la tabla
class CatalogoSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Catalogo
    # el campo fields indica los campos que se devolveran
    # el campo read_only_fields solo permite la lectura no escritura
    class Meta:
        model = Catalogo
        fields = '__all__'
        read_only_fields = ['_id']

    # La funcion to_representation transforma los datos que se van a devolver al controlador
    # recibe el campo self que hace referencia a si mismo e instance que es el valor actual
    # retorna data con los campos modificados
    def to_representation(self, instance):
        data = super(CatalogoSerializer, self).to_representation(instance)
        idPadre = str(data['idPadre'])
        data.update({"idPadre": idPadre})
        return data


# NUBE DE BIGPUNTOS
# PORTALES: CENTER, CORP, PERSONAS, IFIS, CREDIT
# Esta clase sirve para conectar el modelo de la tabla de catalogo de la nube de bigpuntos
# para convertir en un objeto de python con el objetivo de manipular los datos
# y se utiliza para para retornar todos los campos de la tabla de catalogo para los hijos de una parametrizacion
class CatalogoHijoSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Catalogo
    # el campo fields indica los campos que se devolveran
    # el campo read_only_fields solo permite la lectura no escritura
    class Meta:
        model = Catalogo
        fields = ['_id', 'nombre', 'valor', 'config']
        read_only_fields = ['_id']


# NUBE DE BIGPUNTOS
# PORTALES: CENTER
# Esta clase sirve para conectar el modelo de la tabla de catalogo de la nube de bigpuntos
# para convertir en un objeto de python con el objetivo de manipular los datos
# y se utiliza para para retornar unos determinados campos de la tabla de catalogo de una parametrizacion
class CatalogoListaSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Catalogo
    # el campo fields indica los campos que se devolveran
    # el campo read_only_fields solo permite la lectura no escritura
    class Meta:
        model = Catalogo
        fields = ['_id', 'nombre', 'tipo', 'tipoVariable', 'valor', 'descripcion', 'config']
        read_only_fields = ['_id']


# NUBE DE BIGPUNTOS
# PORTALES: CENTER
# Esta clase sirve para conectar el modelo de la tabla de catalogo de la nube de bigpuntos
# y se utiliza para retornar unos determinados campos de la tabla de catalogo de una parametrizacion al momento de filtar
class CatalogoFiltroSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Catalogo
    # el campo fields indica los campos que se devolveran
    # el campo read_only_fields solo permite la lectura no escritura
    class Meta:
        model = Catalogo
        fields = ['_id', 'nombre', 'valor']
        read_only_fields = ['_id']


# NUBE DE BIGPUNTOS
# PORTALES: CENTER
# Esta clase sirve para conectar el modelo de la tabla de catalogo de la nube de bigpuntos
# y se utiliza para el filtrado por Tipo de parametrizacion por el campo tipo
class CatalogoTipoSerializer(serializers.ModelSerializer):
    # asignamos como nombre al dato tipo en la bd
    valor = serializers.CharField(source='tipo')

    # La clase meta se relaciona con la tabla Catalogo
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Catalogo
        fields = ['valor']

    # La funcion to_representation transforma los datos que se van a devolver al controlador ordenados por la fecha de creacion
    # recibe el campo self que hace referencia a si mismo e instance que es el valor actual
    # retorna data con los campos modificados
    def to_representation(self, instance):
        data = super(CatalogoTipoSerializer, self).to_representation(instance)
        # tomo el campo factura y convierto de OBJECTID a string
        catalogo = Catalogo.objects.filter(tipo=data['valor']).order_by('created_at').first()
        _id = str(catalogo._id)
        data.update({"_id": _id})
        return data
