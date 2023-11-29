from .models import CobrarSupermonedas
from ..corp_autorizaciones.models import Autorizaciones
from ...PERSONAS.personas_personas.models import Personas
from ...PERSONAS.personas_personas.serializers import PersonasSearchSerializer
from .serializers import (
    CobrarSupermonedasSerializer
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
# Swagger
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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


# CRUD CORP
# LISTAR TODOS
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'],
                     request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         required=['page_size', 'page'],
                         properties={
                             'page_size': openapi.Schema(type=openapi.TYPE_NUMBER),
                             'page': openapi.Schema(type=openapi.TYPE_NUMBER),
                             'identificacion': openapi.Schema(type=openapi.TYPE_STRING),
                             'codigoCobro': openapi.Schema(type=openapi.TYPE_STRING),
                             'monto': openapi.Schema(type=openapi.TYPE_STRING),
                             'correo': openapi.Schema(type=openapi.TYPE_STRING),
                         },
                     ),
                     operation_description='Uninstall a version of Site',
                     responses={200: CobrarSupermonedasSerializer(many=True)})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cobrarSupermonedas_list(request):
    """
    Este metodo sirve para listar
    @type request: recibe page, page_size, identificacion, codigoCobro, monto, correo
    @rtype: Devuelve una lista, caso contrario devuelve el error generado
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

            if 'identificacion' in request.data:
                if request.data['identificacion'] != '':
                    filters['identificacion__icontains'] = str(request.data['identificacion'])
            if 'codigoCobro' in request.data:
                if request.data['codigoCobro'] != '':
                    filters['codigoCobro__icontains'] = str(request.data['codigoCobro'])
            if 'monto' in request.data:
                if request.data['monto'] != '':
                    filters['monto__icontains'] = str(request.data['monto'])
            if 'correo' in request.data:
                if request.data['correo'] != '':
                    filters['correo__icontains'] = str(request.data['correo'])

            # Serializar los datos
            query = CobrarSupermonedas.objects.filter(**filters).order_by('estado')
            serializer = CobrarSupermonedasSerializer(query[offset:limit], many=True)
            new_serializer_data = {'cont': query.count(),
                                   'info': serializer.data}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


# CREAR
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'], request_body=CobrarSupermonedasSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cobrarSupermonedas_create(request):
    """
    El metodo sirve para crear
    @type request: recibe los campos de la tabla cobrarsupermonedas
    @rtype: DEvuelve el registro, caso contrario devuelve el error generado
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

            serializer = CobrarSupermonedasSerializer(data=request.data)
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
def cobrarSupermonedas_listOne(request, pk):
    """
    El metodo sirve para obtener un registro
    @type pk: recibe el id de la tabla cobrar supermonedas
    @type request: no recibe nada
    @rtype: DEvuelve el registro, caso contrario devuelve el error generado
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
            # Creo un ObjectoId porque la primaryKey de mongo es ObjectId
            pk = ObjectId(pk)
            query = CobrarSupermonedas.objects.get(pk=pk, state=1)
        except CobrarSupermonedas.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = CobrarSupermonedasSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ACTUALIZAR
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'], request_body=CobrarSupermonedasSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cobrarSupermonedas_update(request, pk):
    """
    Este metodo sirve para actualizar
    @param pk: El campo recibe el id de la tabla cobrarsupermonedas
    @type request: Recibe los campos de la tabla de cobrar supermonedas
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
            # Creo un ObjectoId porque la primaryKey de mongo es ObjectId
            pk = ObjectId(pk)
            query = CobrarSupermonedas.objects.get(pk=pk, state=1)
        except CobrarSupermonedas.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')

            serializer = CobrarSupermonedasSerializer(query, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                if request.data['estado'] == 'Pre-autorizado':
                    autorizacion = Autorizaciones.objects.filter(cobrar=query).first()
                    if autorizacion is None:
                        Autorizaciones.objects.create(codigoAutorizacion='', estado=request.data['estado'],
                                                      user_id=request.data['user_id'], cobrar=query)
                    else:
                        autorizacion.estado = request.data['estado']
                        autorizacion.save()
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
def cobrarSupermonedas_delete(request, pk):
    """
    Este metodo sirve para eliminar
    @param pk: el campo recibe el id de la tabla cobrar supermonedas
    @type request: no recibe nada
    @rtype: Devuelve el registro elimado, caso contrario devuelve el error generado
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
            # Creo un ObjectoId porque la primaryKey de mongo es ObjectId
            pk = ObjectId(pk)
            persona = CobrarSupermonedas.objects.get(pk=pk, state=1)
        except CobrarSupermonedas.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'DELETE':
            serializer = CobrarSupermonedasSerializer(persona, data={'state': '0', 'updated_at': str(nowDate)},
                                                      partial=True)
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
def cobrarSupermonedas_search(request):
    """
    Este metodo sirve para buscar
    @type request: Recibe el campo codigoCobro
    @rtype: DEvuelve una lista, caso contrario devuelve el error generado
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

            if 'codigoCobro' in request.data:
                if request.data['codigoCobro'] != '':
                    filters['codigoCobro__icontains'] = str(request.data['codigoCobro'])

            # Serializar los datos
            query = CobrarSupermonedas.objects.filter(**filters).first()
            persona = Personas.objects.filter(user_id=query.user_id).first()
            serializer = PersonasSearchSerializer(persona)
            # envio de datos
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
