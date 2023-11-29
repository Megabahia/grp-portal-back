import boto3
import json
# Importar configuraciones
from ...config import config


def publish(data):
    """
    Este metodo sirve para publicar en la cola de aws
    @type data: El campo recibe la data que se desea publicar
    @rtype: no devuelve nada
    """
    if 'solicitudCredito' in data:
        data.pop('solicitudCredito')
    if 'cedulaGarante' in data:
        data.pop('cedulaGarante')
    if 'papeletaVotacionGarante' in data:
        data.pop('papeletaVotacionGarante')
    if 'fotoGarante' in data:
        data.pop('fotoGarante')
    if 'impuestoPredialGarante' in data:
        data.pop('impuestoPredialGarante')
    if 'matriculaVehiculoGarante' in data:
        data.pop('matriculaVehiculoGarante')
    if 'planillaDomicilioGarante' in data:
        data.pop('planillaDomicilioGarante')

    topicArn = config.AWS_TOPIC_ARN
    snsClient = boto3.client(
        'sns',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID_COLAS,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY_COLAS,
        region_name=config.AWS_REGION_NAME,
    )

    response = snsClient.publish(
        TopicArn=topicArn,
        Message=json.dumps(data),
        Subject='IFIS',
    )
