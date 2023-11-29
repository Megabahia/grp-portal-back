from rest_framework import serializers
from ..central_roles.models import Roles, RolesUsuarios


# NUBE DE BIGPUNTOS
# Portales: Central, personas, corp, ifis, credit
# Esta clase sirve para conectar el modelo de la tabla de RolSerializer de la nube de bigpuntos
# para convertir en un objeto de python con el objetivo de manipular los datos
class RolSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Roles
    # el campo fields indica los campos que se devolveran
    # el campo read_only_fields solo permite la lectura de los campos
    class Meta:
        model = Roles
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        """
        Este metodo se usa para modificar la respuesta de los campos
        @type instance: El campo instance contiene el registro con los campos
        @rtype: DEvuelve los valores modificados
        """
        data = super(RolSerializer, self).to_representation(instance)
        # convierto a str tipoUsuario
        tipoUsuario = str(data.pop('tipoUsuario'))
        data.update({"tipoUsuario": tipoUsuario})
        return data


class RolCreateSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Roles
    # el campo fields indica los campos que se devolveran
    # el campo read_only_fields solo permite la lectura de los campos
    class Meta:
        model = Roles
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        """
        Este metodo se usa para modificar la respuesta de los campos
        @type instance: El campo instance contiene el registro con los campos
        @rtype: DEvuelve los valores modificados
        """
        data = super(RolCreateSerializer, self).to_representation(instance)
        # convierto a str tipoUsuario
        tipoUsuario = str(data.pop('tipoUsuario'))
        data.update({"tipoUsuario": tipoUsuario})
        return data


class RolFiltroSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Roles
    # el campo fields indica los campos que se devolveran
    # el campo read_only_fields solo permite la lectura de los campos
    class Meta:
        model = Roles
        fields = ['_id', 'codigo', 'nombre', 'config']


class ListRolSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Roles
    # el campo fields indica los campos que se devolveran
    # el campo read_only_fields solo permite la lectura de los campos
    class Meta:
        model = Roles
        fields = ['_id', 'codigo', 'nombre', 'config']


# LISTAR ROLES USUARIO LOGIN
class ListRolesSerializer(serializers.ModelSerializer):
    rol = ListRolSerializer(many=False, read_only=True)

    # La clase meta se relaciona con la tabla RolesUsuarios
    # el campo fields indica los campos que se devolveran
    # el campo read_only_fields solo permite la lectura de los campos
    class Meta:
        model = RolesUsuarios
        fields = ['_id', 'rol']

    def to_representation(self, instance):
        """
        Este metodo se usa para modificar la respuesta de los campos
        @type instance: El campo instance contiene el registro con los campos
        @rtype: DEvuelve los valores modificados
        """
        data = super(ListRolesSerializer, self).to_representation(instance)
        rol = data.pop('rol')
        if rol['codigo']:
            data['codigo'] = rol['codigo']
        if rol['nombre']:
            data['nombre'] = rol['nombre']
        if rol['config']:
            data['config'] = rol['config']
        return data


class RolesUsuarioSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Roles
    # el campo fields indica los campos que se devolveran
    # el campo read_only_fields solo permite la lectura de los campos
    class Meta:
        model = RolesUsuarios
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        """
        Este metodo se usa para modificar la respuesta de los campos
        @type instance: El campo instance contiene el registro con los campos
        @rtype: DEvuelve los valores modificados
        """
        data = super(RolesUsuarioSerializer, self).to_representation(instance)
        # tomo el campo rol y convierto de OBJECTID a string
        rol = str(data.pop('rol'))
        data.update({"rol": rol})
        # tomo el campo usuario y convierto de OBJECTID a string
        usuario = str(data.pop('usuario'))
        data.update({"usuario": usuario})
        # convierto a str tipoUsuario
        tipoUsuario = str(data.pop('tipoUsuario'))
        data.update({"tipoUsuario": tipoUsuario})
        return data
