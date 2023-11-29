from rest_framework import serializers

from .models import (
    Publicaciones, CompartirPublicaciones
)


class PublicacionesSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Publicaciones
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Publicaciones
        fields = '__all__'


class PublicacionesImagenSerializer(serializers.HyperlinkedModelSerializer):
    # La clase meta se relaciona con la tabla Publicaciones
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Publicaciones
        fields = ['imagen', 'updated_at']


class CompartirPublicacionesSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Publicaciones
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = CompartirPublicaciones
        fields = '__all__'

    def to_representation(self, instance):
        """
        Este metodo se usa para modificar la respuesta de los campos
        @type instance: El campo instance contiene el registro con los campos
        @rtype: DEvuelve los valores modificados
        """
        data = super(CompartirPublicacionesSerializer, self).to_representation(instance)
        # publicacion
        publicacion = str(data.pop('publicacion'))
        data.update({"publicacion": publicacion})
        # user
        user = str(data.pop('user'))
        data.update({"user": user})
        return data


class ListCompartirPublicacionesSerializer(serializers.ModelSerializer):
    publicacion = PublicacionesSerializer(many=False, read_only=True)

    # La clase meta se relaciona con la tabla Publicaciones
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = CompartirPublicaciones
        fields = '__all__'

    def to_representation(self, instance):
        """
        Este metodo se usa para modificar la respuesta de los campos
        @type instance: El campo instance contiene el registro con los campos
        @rtype: DEvuelve los valores modificados
        """
        data = super(ListCompartirPublicacionesSerializer, self).to_representation(instance)
        # user
        data.pop('user')
        return data


class PublicacionesSinCompartirSerializer(serializers.ModelSerializer):
    publicacion = PublicacionesSerializer(many=False, read_only=True)

    # La clase meta se relaciona con la tabla Publicaciones
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = CompartirPublicaciones
        fields = ['publicacion']

    def to_representation(self, instance):
        """
        Este metodo se usa para modificar la respuesta de los campos
        @type instance: El campo instance contiene el registro con los campos
        @rtype: DEvuelve los valores modificados
        """
        data = super(PublicacionesSinCompartirSerializer, self).to_representation(instance)
        # publicacion
        publicacion = data.pop('publicacion')
        data['_id'] = publicacion['_id']
        data['titulo'] = publicacion['titulo']
        data['subtitulo'] = publicacion['subtitulo']
        data['descripcion'] = publicacion['descripcion']
        data['imagen'] = publicacion['imagen']
        data['created_at'] = publicacion['created_at']
        data['updated_at'] = publicacion['updated_at']
        data['state'] = publicacion['state']
        return data
