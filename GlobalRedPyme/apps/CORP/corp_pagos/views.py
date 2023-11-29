from ...CENTRAL.central_catalogo.models import Catalogo
from .models import Pagos
from ...PERSONAS.personas_personas.models import Personas
from ...PERSONAS.personas_personas.serializers import PersonasSearchSerializer
from .serializers import (
    PagosSerializer
)
from .consumer_pagos import get_queue_url
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
@swagger_auto_schema(methods=['post'], request_body=PagosSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pagos_create(request):
    """
    ESTE metodo sirve para crear pagos en la tabla pagos de la base datos corp
    @type request: El campo request recibe los campos de la tabla pagos
    @rtype: DEvuelve el pago creado, caso contrario devuelve el error generado
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

            tiempo = Catalogo.objects.filter(tipo='CONFIG_DURACION', nombre='DURACION_CODIGO', state=1).first().valor
            # Genera el codigo
            request.data['duracion'] = timezone_now + relativedelta(minutes=int(tiempo))

            serializer = PagosSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                # monedasUsuario = Monedas.objects.filter(user_id=request.data['user_id']).order_by('-created_at').first()
                # request.data['tipo'] = 'Pagos'
                # request.data['estado'] = 'aprobado'
                # request.data['debito'] = request.data['monto']
                # request.data['saldo'] = monedasUsuario.saldo - float(request.data['monto'])
                # request.data['descripcion'] = 'Generar comprobante de pago con supermonedas.'
                # monedasSerializer = MonedasGuardarSerializer(data=request.data)
                # if monedasSerializer.is_valid():
                #     monedasSerializer.save()

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
def pagos_listOne(request, pk):
    """
    Este metodo obtiene el pago por id de la tabla pagos de la base datos corp
    @type pk: El campos pk recibe el id del pago
    @type request: El campo request no recibe nada
    @rtype: DEvuelve el pago, caso contrario devuelve el error generado
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
            query = Pagos.objects.filter(user_id=pk, state=1).first()
        except Pagos.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = PagosSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ACTUALIZAR
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'], request_body=PagosSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pagos_update(request, pk):
    """
    Este metodo actualiza el pago de la tabla de pagos de la base datos corp
    @type pk: El campo pk recibe el id de la tabla pagos
    @type request: El campo request recibe los campos de la tabla pagos
    @rtype: Devuelve el registro actualizado, caso contrario devuelve el error generado
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
            query = Pagos.objects.filter(user_id=pk, state=1).first()
        except Pagos.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
            serializer = PagosSerializer(query, data=request.data, partial=True)
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
def pagos_delete(request, pk):
    """
    Este metodo sirve para eliminar pagos de la tabla pagos de la base datos
    @type pk: El campo pk recibe el id del pago
    @type request: El campo request no recibe nada
    @rtype: DEvuelve el registro eliminado, caso contrario no devuelve nada
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
            query = Pagos.objects.filter(user_id=pk, state=1).first()
        except Pagos.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'DELETE':
            serializer = PagosSerializer(query, data={'state': '0', 'updated_at': str(nowDate)}, partial=True)
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
def pagos_list(request):
    """
    Este metodo sirve para listar los pagos de la tabla pagos de la base datos corp
    @type request: El campo request recibe codigoCobro, codigoReferido, empresa_id
    @rtype: object
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
            query = Pagos.objects.filter(**filters).order_by('-created_at').first()
            if query is None:
                new_serializer_data = {'error': {'message': 'No existe el codigo'}}
                return Response(new_serializer_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                if query.duracion >= timezone_now:
                    persona = Personas.objects.filter(user_id=query.user_id).first()
                    serializer = PersonasSearchSerializer(persona)
                    new_serializer_data = serializer.data
                    new_serializer_data['monto'] = query.monto
                else:
                    new_serializer_data = {'error': {'tiempo': 'Se le termino el tiempo', 'estado': 'Inactivo'}}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def consumirCola(request):
    """
    ESte metodo sirve para consumir la cola de aws
    @type request: El campo request no recibe nada
    @rtype: No devuelve nada
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
        get_queue_url()
        msg = {"msg": "Se actualizo la cola"}
        return Response(msg, status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)
