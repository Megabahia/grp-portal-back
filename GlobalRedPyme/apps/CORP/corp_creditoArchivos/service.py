import base64
import requests
import json
from ...CENTRAL.central_catalogo.models import Catalogo
from ...config import config
# logs
from ...CENTRAL.central_logs.methods import createLog, datosTipoLog, datosProductosMDP
from django.utils import timezone

timezone_now = timezone.localtime(timezone.now())
# declaracion variables log
datosAux = datosProductosMDP()
datosTipoLogAux = datosTipoLog()
# asignacion datos modulo
logModulo = datosAux['modulo']
logApi = datosAux['api']
# asignacion tipo de datos
logTransaccion = datosTipoLogAux['transaccion']
logExcepcion = datosTipoLogAux['excepcion']

url = config.API_FIRMA_ELECTRONICO_URL
# Usuario y contraseña para la autenticación básica
usuario = config.API_FIRMA_ELECTRONICO_USERNAME
contrasenia = config.API_FIRMA_ELECTRONICO_PASSWORD

# Codifica las credenciales en base64
credenciales = base64.b64encode(f'{usuario}:{contrasenia}'.encode()).decode()

# Define el encabezado de autorización
encabezado_auth = {'Authorization': f'Basic {credenciales}'}

# LEE ARCHIVO .ENV
import environ

env = environ.Env()
environ.Env.read_env()


def enviarDocumentos(archivos, cliente):
    """
    Este metodo sirve para enviar a firmar los documentos con el proveedor nexty
    @type cliente: recibe los datos del cliente
    @type archivos: recibe los archivos
    @rtype: DEveuele codigo del envio al servicio
    """
    campos = ['_id', 'numeroIdentificacion', 'credito_id', 'created_at', 'updated_at', 'state']
    files = []
    for key, value in archivos.items():
        if key not in campos and value is not None:
            catalogo = Catalogo.objects.filter(tipo='NEXTI', nombre=key).first()
            files.append({
                "filename": value.split('/')[-1],
                "input_path": f"{env.str('AWS_STORAGE_BUCKET_NAME')}/CORP/archivosFirmados/{cliente['identificacion']}/",
                "ouput_path": f"{env.str('AWS_STORAGE_BUCKET_NAME')}/CORP/nexti/archivosFirmados/{cliente['identificacion']}/",
                "template_id": '652c613be2a2fce03f75ab87' if catalogo is None else catalogo.valor
            })
    del files[1:]
    data = {
        "data": {
            "product_number": "303030",
            "signatory": {
                "client_id": cliente['identificacion'],
                "type": "natural",
                "email": cliente['email'],
                "identification": cliente['identificacion'],
                "phone": "+593" + cliente['celular'],
                "first_name": cliente['nombres'].split(' ')[0],
                "second_name": cliente['nombres'].split(' ')[1],
                "first_last_name": cliente['apellidos'].split(' ')[0],
                "second_last_name": cliente['apellidos'].split(' ')[1],
                "address": cliente['direccionDomicilio'],
                "postal_code": "170150",
                "state": cliente['ciudad'],
                "city": cliente['ciudad']
            },
            "file_type": "D",
            "files": files
        }
    }
    print(data)

    # Realiza una solicitud GET al endpoint con la autenticación básica
    response = requests.post(url, json=data, headers=encabezado_auth)
    # Verifica si la solicitud fue exitosa (código de estado 200)
    logModel = {
        'endPoint': 'Nexti',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'CREAR',
        'fechaInicio': str(timezone_now),
        'dataEnviada': json.dumps(data),
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    if response.status_code == 200:
        print('Respuesta del servidor:', response.text)
    else:
        print('Error al realizar la solicitud. Código de estado:', response.status_code)
        print('Error al realizar la solicitud. Código de body:', response.text)
    createLog(logModel, response.text, datosTipoLogAux['transaccion'])
    return response.status_code
