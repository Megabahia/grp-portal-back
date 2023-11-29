import boto3
import json
# Importar configuraciones
from ...config import config
from .serializers import CreditoPersonasSerializer
from .models import CreditoPersonas
from bson import ObjectId
# logs
from ...CENTRAL.central_logs.methods import createLog, datosTipoLog, datosProductosMDP

# declaracion variables log
datosAux = datosProductosMDP()
datosTipoLogAux = datosTipoLog()
# asignacion datos modulo
logModulo = datosAux['modulo']
logApi = datosAux['api']
# asignacion tipo de datos
logTransaccion = datosTipoLogAux['transaccion']
logExcepcion = datosTipoLogAux['excepcion']


def get_queue_url():
    """
    Este metodo sirve para consumir la cola de aws
    @rtype: No devuelve nada
    """
    print('cron')
    logModel = {
        'endPoint': logApi + 'listOne/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'CRON_SQS_BIGBUNTOS',
        # 'fechaInicio' : str(timezone_now),
        'dataEnviada': '{}',
        # 'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    try:
        region_name = config.AWS_REGION_NAME
        queue_name = config.AWS_QUEUE_NAME
        max_queue_messages = 10
        aws_access_key_id = config.AWS_ACCESS_KEY_ID_COLAS
        aws_secret_access_key = config.AWS_SECRET_ACCESS_KEY_COLAS
        sqs = boto3.resource('sqs', region_name=region_name,
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key)
        queue = sqs.get_queue_by_name(QueueName=queue_name)
        # Consultar la cola maximo 10 mensajes
        for message in queue.receive_messages(MaxNumberOfMessages=max_queue_messages):
            # process message body
            body = json.loads(message.body)
            jsonRequest = json.loads(body['Message'])
            _idCredidPerson = jsonRequest.pop('_id')
            # Por el momento crea los nuevos registros que llegan sqs
            query = CreditoPersonas.objects.filter(external_id=_idCredidPerson, state=1).first()
            credito = ''
            if query is None:
                # Quitar los campos que no estan en el modelo de credito persona
                query = CreditoPersonas.objects.filter(_id=ObjectId(jsonRequest['external_id']), state=1).first()
                if query is not None:
                    print('antes de actualizar desde bigpuntos')
                    if 'entidadFinanciera' in jsonRequest:
                        jsonRequest.pop('entidadFinanciera')
                    if jsonRequest['estado'] == 'Enviado':
                        jsonRequest['estado'] = 'Nuevo'
                    if jsonRequest['estado'] == 'Completado':
                        jsonRequest['estado'] = 'Completado'
                    CreditoPersonas.objects.filter(_id=ObjectId(jsonRequest['external_id'])).update(**jsonRequest)
                    credito = query
                    print('se guardo')
                else:
                    if 'whatsappPersona' in jsonRequest:
                        jsonRequest.pop('whatsappPersona')
                    if 'emailPersona' in jsonRequest:
                        jsonRequest.pop('emailPersona')
                    jsonRequest['external_id'] = _idCredidPerson
                    if jsonRequest['estado'] == 'Enviado':
                        jsonRequest['estado'] = 'Nuevo'
                    if jsonRequest['estado'] == 'Completado':
                        jsonRequest['estado'] = 'Completado'
                    print('antes de guardar')
                    credito = CreditoPersonas.objects.create(**jsonRequest)
                    print('se guardo')
            else:
                # Quitar los campos que no estan en el modelo de credito persona

                jsonRequest['external_id'] = _idCredidPerson
                if jsonRequest['estado'] == 'Enviado':
                    jsonRequest['estado'] = 'Nuevo'
                if jsonRequest['estado'] == 'Completado':
                    jsonRequest['estado'] = 'Completado'

                print('antes de actualizar')
                if 'whatsappPersona' in jsonRequest:
                    jsonRequest.pop('whatsappPersona')
                if 'emailPersona' in jsonRequest:
                    jsonRequest.pop('emailPersona')
                CreditoPersonas.objects.filter(external_id=query.external_id).update(**jsonRequest)
                credito = query
                print('se guardo')

            # Crear objeto en firebase para las notificaciones
            config.FIREBASE_DB.collection('creditosPersonas').document(str(credito._id)).set(jsonRequest)
            # Borramos SQS
            message.delete()
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        print(err)
        return err
