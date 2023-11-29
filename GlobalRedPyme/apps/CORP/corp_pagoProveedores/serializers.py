import json

from rest_framework import serializers

from .models import (
    PagoProveedores
)
from ..corp_creditoArchivos.models import ArchivosFirmados
from ..corp_creditoArchivos.serializers import ArchivosFirmadosSerializer


class PagoProveedorSerializer(serializers.ModelSerializer):
    # La clase meta se relaciona con la tabla Facturas
    # el campo fields indica los campos que se devolveran
    class Meta:
        model = PagoProveedores
        fields = '__all__'
        read_only_fields = ['_id']

    def to_representation(self, instance):
        """
        Este metodo se usa para modificar la respuesta de los campos
        @type instance: El campo instance contiene el registro con los campos
        @rtype: DEvuelve los valores modificados
        """
        data = super(PagoProveedorSerializer, self).to_representation(instance)
        # tomo el campo persona y convierto de OBJECTID a string
        if data['archivoFirmado']:
            env = environ.Env()
            environ.Env.read_env()  # LEE ARCHIVO .ENV
            data['documentoVerificado'] = prueba_verificar(data['archivoFirmado'].replace(env.str('URL_BUCKET'), ''))
        else:
            data['documentoVerificado'] = False

        if data['usuario']:
            usuario_json = json.loads(data['usuario'])
            if usuario_json:
                archivosFirmados = ArchivosFirmados.objects.filter(
                    numeroIdentificacion=json.loads(data['usuario'])['identificacion'], state=1).first()
                data['archivosFirmados'] = ArchivosFirmadosSerializer(archivosFirmados).data

        return data


# Importar boto3
import boto3
import tempfile
import environ
from endesive import pdf


def prueba_verificar(url):
    """
    ESte metodo sirve para verificar la verificacion de lafirma del documento
    @type url: REcibe la url del archivo que esta en S3
    @rtype: Devuelve true o false
    """
    env = environ.Env()
    environ.Env.read_env()  # LEE ARCHIVO .ENV
    client_s3 = boto3.client(
        's3',
        aws_access_key_id=env.str('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=env.str('AWS_SECRET_ACCESS_KEY')
    )
    with tempfile.TemporaryDirectory() as d:
        ruta = d + 'creditosPreAprobados.xlsx'
        s3 = boto3.resource('s3')
        s3.meta.client.download_file(env.str('AWS_STORAGE_BUCKET_NAME'), str(url), ruta)

    try:
        data = open(ruta, "rb").read()
    except:
        print('golaa error')
    no = 0
    for (hashok, signatureok, certok) in pdf.verify(
            data
    ):
        # print("*" * 10, "signature no:", no)
        # print("signature ok?", signatureok)
        print("hash ok?", hashok)
        # print("cert ok?", certok)

    return hashok
