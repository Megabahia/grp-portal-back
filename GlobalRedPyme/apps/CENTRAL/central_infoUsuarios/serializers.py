from rest_framework import serializers

from .models import InfoUsuarios


# NUBE DE BIGPUNTOS
# PORTALES: CENTER, PERSONAS
# Esta clase sirve para conectar el modelo de la tabla de Facturas de la nube de bigpuntos
# para convertir en un objeto de python con el objetivo de manipular los datos y se utiliza
# para retornar todos los campos de la tabla
class InfoUsuarioSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla InfoUsuarios
    # el campo fields indica los campos que se devolveran
    # el campo read_only_fields indica que campos permite solo leer
    class Meta:
        model = InfoUsuarios
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        """
        Este metodo se usa para modificar los datos que se devolveran a de la info usuarios
        @type instance: el campo instance son los valores que se desean modificar
        @rtype: revuelve los campos que se modificaron
        """
        data = super(InfoUsuarioSerializer, self).to_representation(instance)
        # convierto a str tipoUsuario
        usuario = str(data.pop('usuario'))
        data.update({"usuario": usuario})
        return data
