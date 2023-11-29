import boto3
import json

from .s3 import replicate
# Importar configuraciones
from ...config import config
import environ


def publish(data):
    topicArn = config.AWS_TOPIC_ARN
    snsClient = boto3.client(
        'sns',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID_COLAS,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY_COLAS,
        region_name=config.AWS_REGION_NAME,
    )

    elements_to_remove = ['reporteBuro', 'identificacion', 'papeletaVotacion', 'identificacionConyuge',
                          'papeletaVotacionConyuge', 'planillaLuzNegocio', 'planillaLuzDomicilio', 'facturas',
                          'matriculaVehiculo', 'impuestoPredial', 'buroCredito', 'evaluacionCrediticia', 'ruc',
                          'rolesPago', 'panillaIESS', 'mecanizadoIess', 'fotoCarnet', 'solicitudCredito',
                          'buroCreditoIfis', 'documentoAprobacion', 'pagare', 'contratosCuenta', 'tablaAmortizacion',
                          'user_id']

    for element in elements_to_remove:
        if element in data:
            data.pop(element)
    if 'external_id' in data:
        if data['external_id'] is None:
            data['external_id'] = data['_id']
    if 'autorizacion' in data:
        autorizacion = data.pop('autorizacion')
        env = environ.Env()
        environ.Env.read_env()  # LEE ARCHIVO .ENV
        data['autorizacion'] = str(autorizacion).replace(env.str('URL_BUCKET'), '')
        if data['autorizacion'] == 'None':
            data.pop('autorizacion')
        else:
            replicate(data['autorizacion'])

    response = snsClient.publish(
        TopicArn=topicArn,
        Message=json.dumps(data),
        Subject='PURCHASE',
    )
    print(response['ResponseMetadata']['HTTPStatusCode'])
