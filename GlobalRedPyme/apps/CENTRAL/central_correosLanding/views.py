from .models import Correos
from .serializers import (
    CorreosSerializer
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
# Enviar Correo
from apps.config.util import sendEmail
# Generar codigos aleatorios
import string
import random
# logs
from ..central_logs.methods import createLog, datosTipoLog, datosProductosMDP

# declaracion variables log
datosAux = datosProductosMDP()
datosTipoLogAux = datosTipoLog()
# asignacion datos modulo
logModulo = datosAux['modulo']
logApi = datosAux['api']
# asignacion tipo de datos
logTransaccion = datosTipoLogAux['transaccion']
logExcepcion = datosTipoLogAux['excepcion']


# CRUD PERSONAS
# LISTAR TODOS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def correos_list(request):
    """
    Este metodo se usa para listar todos los correos de la tabla de carreos de la base de datos central
    @type request: El campo request recibe dos campos page, page_size y tipo
    @rtype: Devuelve un lista de los correos que cumplan con el filtro, caso contrario devuelve un error
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'list/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'LEER',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    if request.method == 'POST':
        try:
            logModel['dataEnviada'] = str(request.data)
            # paginacion
            page_size = int(request.data['page_size'])
            page = int(request.data['page'])
            offset = page_size * page
            limit = offset + page_size
            # Filtros
            filters = {"state": "1"}

            if "tipo" in request.data:
                filters['tipo'] = request.data["tipo"]

            # Serializar los datos
            query = Correos.objects.filter(**filters).order_by('-created_at')
            serializer = CorreosSerializer(query[offset:limit], many=True)
            new_serializer_data = {'cont': query.count(),
                                   'info': serializer.data}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


# CREAR
@api_view(['POST'])
def correos_create(request):
    """
    Este metodo se usa para crear un registro de los correos en la tabla de correos de la base datos central
    @type request: El campo request recibe los campos de la tabla de correos
    @rtype: Devuelve el registro que se acaba de ingresar, caso contrario devuelve un error
    """
    request.POST._mutable = True
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'create/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'CREAR',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    if request.method == 'POST':
        try:
            # Generar codigo
            length_of_string = 5
            codigo = ''.join(
                random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
            request.data['codigo'] = codigo

            logModel['dataEnviada'] = str(request.data)
            request.data['created_at'] = str(timezone_now)
            if 'updated_at' in request.data:
                request.data.pop('updated_at')

            try:
                # Comprobar si exite correo
                query = Correos.objects.get(correo=request.data['correo'], state=1)
                serializer = CorreosSerializer(query, data=request.data, partial=True)
            except Correos.DoesNotExist:
                # No existe correo crearlo
                serializer = CorreosSerializer(data=request.data)

            subject, from_email, to = 'OBTENER MIS DESCUENTOS', "08d77fe1da-d09822@inbox.mailtrap.io", request.data[
                'correo']
            txt_content = """
                    Código generado
                    El código generado para que descubras tu premio es """ + codigo + """
                    Atentamente,
                    Equipo Global Red Pymes Personas.
            """
            html_content = """
            <html>
                <body>
                    <h1>Código generado</h1>
                    El código generado para que descubras tu premio es """ + codigo + """<br>
                    Atentamente,<br>
                    Equipo Global Red Pymes Personas.<br>
                </body>
            </html>
            """

            if serializer.is_valid():
                serializer.save()
                createLog(logModel, serializer.data, logTransaccion)
                sendEmail(subject, txt_content, from_email, to, html_content)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ACTUALIZAR
@api_view(['POST'])
def correos_update(request, pk):
    """
    Este metodo se utiliza para actualizar los correos de la tabla de correos de la base datos central
    @type pk: El campo pk es el id que se buscara para actualizar
    @type request: Recibe los campos de la tabla de correos
    @rtype: Devuelve el registro que se acaba de actualizar
    """
    request.POST._mutable = True
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'update/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'ESCRIBIR',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    try:
        try:
            logModel['dataEnviada'] = str(request.data)
            query = Correos.objects.get(pk=pk, state=1)
        except Correos.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')

            if 'imagen' in request.data:
                if request.data['imagen'] == None:
                    request.data.pop('imagen')

            serializer = CorreosSerializer(query, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)
