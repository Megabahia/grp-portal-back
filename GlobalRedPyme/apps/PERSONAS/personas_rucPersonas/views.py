from .models import RucPersonas
from ..personas_personas.models import Personas
from ..personas_personas.serializers import PersonasSearchSerializer
from .serializers import (
    RucPersonasSerializer
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.conf import settings
# Swagger
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# Generar codigos aleatorios
import string
import random
# Sumar minutos
from dateutil.relativedelta import relativedelta
# ObjectId
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


# CRUD
# CREAR
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'], request_body=RucPersonasSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rucPersonas_create(request):
    """
    ESte metodo sirve para crear un rucpersona de la tabla rucpersona de la base datos personas
    @type request: El campo request recibe los campos de la tabla rucpersonas
    @rtype: DEvuelve el registro creado, caso contrario devuelve el error generado
    """
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
            logModel['dataEnviada'] = str(request.data)
            request.data['created_at'] = str(timezone_now)
            if 'updated_at' in request.data:
                request.data.pop('updated_at')

            rucPersona = RucPersonas.objects.filter(ruc=request.data['ruc'], state=1).first()
            if rucPersona is not None:
                if rucPersona.identificacion != request.data['identificacion']:
                    data = {'error': 'El ruc ya esta registrado'}
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    query = RucPersonas.objects.filter(identificacion=request.data['identificacion'],
                                                       ruc=request.data['ruc'], state=1).first()
                    serializer = RucPersonasSerializer(query, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        createLog(logModel, serializer.data, logTransaccion)
                        return Response(serializer.data)

            serializer = RucPersonasSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ENCONTRAR UNO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rucPersonas_listOne(request, pk):
    """
    ESte metodo sirve para obtener un rucpersona de la tabla rucpersona de la base datos personas
    @type pk: El campo pk recibe el id de la tabla rucpersona
    @type request: El campo request no recibe nada
    @rtype: DEvuelve el rucpersona obtenido, caso contrario devuelve el error generado
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'listOne/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'LEER',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    try:
        try:
            query = RucPersonas.objects.filter(user_id=pk, state=1).first()
        except RucPersonas.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = RucPersonasSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ACTUALIZAR
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'], request_body=RucPersonasSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rucPersonas_update(request, pk):
    """
    ESte metodo sirve para actualizar un rucpersona de la tabla rucpersona de la base datos personas
    @type request: El campo request recibe los campos de la tabla rucpersonas
    @rtype: DEvuelve el registro actualizado, caso contrario devuelve el error generado
    """
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
            query = RucPersonas.objects.filter(user_id=pk, state=1).first()
        except RucPersonas.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
            serializer = RucPersonasSerializer(query, data=request.data, partial=True)
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

    # ELIMINAR


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def rucPersonas_delete(request, pk):
    """
    ESte metodo sirve para borrar un rucpersona de la tabla rucpersona de la base datos personas
    @type pk: El campo pk recibe el id de la tabla rucpersona
    @type request: El campo request no recibe nada
    @rtype: DEvuelve el registro borrado, caso contrario devuelve el error generado
    """
    nowDate = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'delete/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'BORRAR',
        'fechaInicio': str(nowDate),
        'dataEnviada': '{}',
        'fechaFin': str(nowDate),
        'dataRecibida': '{}'
    }
    try:
        try:
            query = RucPersonas.objects.filter(user_id=pk, state=1).first()
        except RucPersonas.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'DELETE':
            serializer = RucPersonasSerializer(query, data={'state': '0', 'updated_at': str(nowDate)}, partial=True)
            if serializer.is_valid():
                serializer.save()
                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data, status=status.HTTP_200_OK)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rucPersonas_list(request):
    """
    ESte metodo sirve para listar rucpersona de la tabla rucpersona de la base datos personas
    @type request: El campo request recibe los campos codigoCobro, empresa_id
    @rtype: DEvuelve una lista de rucpersonas, caso contrario devuelve el error generado
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
            # Filtros
            filters = {"state": "1"}

            if "codigoCobro" in request.data:
                if request.data["codigoCobro"] != '':
                    filters['codigoCobro'] = str(request.data["codigoCobro"])

            if "empresa_id" in request.data:
                if request.data["empresa_id"] != '':
                    filters['empresa_id'] = str(request.data["empresa_id"])

            # Serializar los datos
            query = RucPersonas.objects.filter(**filters).order_by('-created_at').first()
            if query.duracion >= timezone_now:
                persona = Personas.objects.filter(user_id=query.user_id).first()
                serializer = PersonasSearchSerializer(persona)
                new_serializer_data = serializer.data
            else:
                new_serializer_data = {'error': {'tiempo': 'Se le termino el tiempo', 'estado': 'Inactivo'}}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
