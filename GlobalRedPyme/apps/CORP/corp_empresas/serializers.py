from rest_framework import serializers

from .models import (
    Empresas, EmpresasConvenio, Empleados
)


class EmpresasSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Empresas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Empresas
        fields = '__all__'
        read_only_fields = ['_id']


class EmpresasInfoBasicaSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Empresas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Empresas
        fields = ['_id', 'nombreEmpresa', 'imagen', 'nombreComercial']


class EmpresasFiltroSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Empresas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Empresas
        fields = ['_id', 'nombreEmpresa', 'ruc', 'tipoEmpresa', 'tipoCategoria']


class EmpresasFiltroIfisSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Empresas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Empresas
        fields = ['_id', 'nombreEmpresa', 'nombreComercial', 'tipoCategoria', 'ruc']


class EmpresasConvenioCreateSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla EmpresasConvenio
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = EmpresasConvenio
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        """
        Este metodo se usa para modificar la respuesta de los campos
        @type instance: El campo instance contiene el registro con los campos
        @rtype: DEvuelve los valores modificados
        """
        data = super(EmpresasConvenioCreateSerializer, self).to_representation(instance)
        # tomo el campo persona y convierto de OBJECTID a string
        convenio = str(data.pop('convenio'))
        data.update({"convenio": convenio})
        return data


class EmpresasConvenioSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla EmpresasConvenio
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = EmpresasConvenio
        fields = ['convenio']

    def to_representation(self, instance):
        """
        Este metodo se usa para modificar la respuesta de los campos
        @type instance: El campo instance contiene el registro con los campos
        @rtype: DEvuelve los valores modificados
        """
        data = super(EmpresasConvenioSerializer, self).to_representation(instance)
        # tomo el campo persona y convierto de OBJECTID a string
        convenio = data.pop('convenio')
        empresa = Empresas.objects.filter(_id=convenio, state=1).first()
        data.update(EmpresasSerializer(empresa).data)
        return data


class EmpresasLogosSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Empresas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Empresas
        fields = ['imagen']


class EmpleadosSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Empleados
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = Empleados
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        """
        Este metodo se usa para modificar la respuesta de los campos
        @type instance: El campo instance contiene el registro con los campos
        @rtype: DEvuelve los valores modificados
        """
        data = super(EmpleadosSerializer, self).to_representation(instance)
        # tomo el campo persona y convierto de OBJECTID a string
        empresa = data.pop('empresa')
        empresa = Empresas.objects.filter(_id=empresa, state=1).first()
        if empresa is not None:
            data['ruc'] = (EmpresasSerializer(empresa).data['ruc'])
            data['nombreComercial'] = (EmpresasSerializer(empresa).data['nombreComercial'])
        return data
