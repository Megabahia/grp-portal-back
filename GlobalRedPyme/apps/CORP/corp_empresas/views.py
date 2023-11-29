from .models import Empresas, EmpresasConvenio, Empleados
from .serializers import (
    EmpresasSerializer, EmpresasFiltroSerializer, EmpresasFiltroIfisSerializer, EmpresasConvenioSerializer,
    EmpresasConvenioCreateSerializer,
    EmpresasLogosSerializer,
    EmpleadosSerializer,
)
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
# Enviar Correo
from apps.config.util import sendEmail
# Importar config
from ...config import config
# excel
import openpyxl
# Utils
from ...utils import utils
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


# CRUD PERSONAS
# LISTAR TODOS
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'],
                     request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         required=['page_size', 'page'],
                         properties={
                             'page_size': openapi.Schema(type=openapi.TYPE_NUMBER),
                             'page': openapi.Schema(type=openapi.TYPE_NUMBER)
                         },
                     ),
                     operation_description='Uninstall a version of Site',
                     responses={200: EmpresasSerializer(many=True)})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def empresas_list(request):
    """
    ESte metodo sirve para listar las empresas de la tabla empresas de la base datos corp
    @type request: El campo request recibe nombreComercial, tipoEmpresa, estado, page, page_size
    @rtype: Devuelve una lista de empresas con los filtros que coincidan, caso contrario devuele el error generado
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

            if "nombreComercial" in request.data:
                if request.data["nombreComercial"] != '':
                    filters['nombreComercial__icontains'] = str(request.data["nombreComercial"])

            # Serializar los datos
            query = Empresas.objects.filter(**filters).order_by('-created_at')
            serializer = EmpresasSerializer(query[offset:limit], many=True)
            new_serializer_data = {'cont': query.count(),
                                   'info': serializer.data}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'],
                     request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         required=[],
                         properties={
                             'ruc': openapi.Schema(type=openapi.TYPE_STRING),
                         },
                     ),
                     operation_description='Uninstall a version of Site',
                     responses={200: EmpresasFiltroSerializer(many=True)})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def empresas_list_filtro(request):
    """
    Este metodo sirve para filtrar empresas en la tabla de empresas de la tabla corp
    @type request: El campo request recibe el campo ruc
    @rtype: Devuelve una lista de empresas que coincidad, caso contrario devuelve el error generado
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
            page_size = int(20)
            page = int(0)
            offset = page_size * page
            limit = offset + page_size
            # Filtros
            filters = {"state": "1"}

            if "ruc" in request.data:
                if request.data["ruc"] != '':
                    filters['ruc__icontains'] = str(request.data["ruc"])

            # Serializar los datos
            query = Empresas.objects.filter(Q(ruc__icontains=str(request.data["ruc"]), state=1) | Q(nombreEmpresa__icontains=str(request.data["ruc"]), state=1)).order_by('-created_at')
            serializer = EmpresasFiltroSerializer(query[offset:limit], many=True)
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
@swagger_auto_schema(methods=['post'], request_body=EmpresasSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def empresas_create(request):
    """
    Este metodo sirve para crear la empresa en la tabla empresas de la base datos corp
    @type request: El campo request recibe los campos de la tabla empresas
    @rtype: Devuelve el registro de la empresa creada, caso contrario devuelve el error generado
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
            logModel['dataEnviada'] = str(request.data)
            request.data['created_at'] = str(timezone_now)
            if 'updated_at' in request.data:
                request.data.pop('updated_at')
            empresa = Empresas.objects.filter(ruc=request.data['ruc'], state=1).first()
            if empresa is not None:
                data = {'error': 'El ruc ya esta registrado.'}
                createLog(logModel, data, logExcepcion)
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            serializer = EmpresasSerializer(data=request.data)
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
def empresas_listOne(request, pk):
    """
    Este metodo sirve para obtener la empresa por el id de la tabla empresas de la base datos corp
    @type pk: El campo pk recibe el id de la empresa
    @type request: El campo request no recibe nada
    @rtype: devuelve el registro de la empresa obtenido, caso contrario devuelve el error generado
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
            query = Empresas.objects.get(pk=pk, state=1)
        except Empresas.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = EmpresasSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ACTUALIZAR
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'], request_body=EmpresasSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def empresas_update(request, pk):
    """
    Este metodo sirve para actualizar la empresa de la tabla empresas de la base datos corp
    @type pk: El campo pk recibe el id de la empresa
    @type request: El campo request recibe los campos de la tabla empresa
    @rtype: Devuelve el registro actualizado de la empresa, caso contrario devuelve el error generado
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
            # Creo un ObjectoId porque la primaryKey de mongo es ObjectId
            pk = ObjectId(pk)
            query = Empresas.objects.get(pk=pk, state=1)
        except Empresas.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')

            if query.ruc != request.data['ruc']:
                data = {'error': 'El ruc ya esta registrado.'}
                createLog(logModel, data, logExcepcion)
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            serializer = EmpresasSerializer(query, data=request.data, partial=True)
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
def empresas_delete(request, pk):
    """
    Este metodo sirve para eliminar una empresa de la tabla empresa de la base datos corp
    @type pk: El campo pk recibe el id de la empresa
    @type request: El campo request no recibe nada
    @rtype: devuelve el registro eliminado
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
            persona = Empresas.objects.get(pk=pk, state=1)
        except Empresas.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'DELETE':
            serializer = EmpresasSerializer(persona, data={'state': '0', 'updated_at': str(nowDate)}, partial=True)
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
def empresas_list_comercial(request):
    """
    Este metodo sirve para listar la empresas comerciales de la tabla empresas de la base datos corp
    @type request: El campo request recibe los campos ciudad, tipoCategoria
    @rtype: Devuelve una lista de la empresas comerciales, caso contrario devuelve el error generado
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'list/ifis',
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
            page_size = 20
            page = 0
            offset = page_size * page
            limit = offset + page_size
            # Filtros
            filters = {"state": "1"}

            filters['tipoEmpresa'] = 'corp'

            if "ciudad" in request.data:
                if request.data["ciudad"] != '':
                    filters['ciudad__icontains'] = str(request.data["ciudad"])

            if "tipoCategoria" in request.data:
                if request.data["tipoCategoria"] != '':
                    filters['tipoCategoria__icontains'] = str(request.data["tipoCategoria"])

            # Serializar los datos
            query = Empresas.objects.filter(**filters).order_by('-created_at')
            serializer = EmpresasFiltroIfisSerializer(query[offset:limit], many=True)
            new_serializer_data = {'cont': query.count(),
                                   'info': serializer.data}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def empresas_list_ifis(request):
    """
    Este metodo sirve para listar todas las empresas ifis de la tabla empresas de la base datos corp
    @type request: El campo request recibe el campo ciudad, tipoCategoria
    @rtype: Devuelve una lista de empresas que coicidan, caso contrario devuelve el error generado
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'list/ifis',
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
            page_size = 20
            page = 0
            offset = page_size * page
            limit = offset + page_size
            # Filtros
            filters = {"state": "1"}

            filters['tipoEmpresa'] = 'ifis'

            if "ciudad" in request.data:
                if request.data["ciudad"] != '':
                    filters['ciudad__icontains'] = str(request.data["ciudad"])

            if "tipoCategoria" in request.data:
                if request.data["tipoCategoria"] != '':
                    filters['tipoCategoria__icontains'] = str(request.data["tipoCategoria"])

            # Serializar los datos
            query = Empresas.objects.filter(**filters).order_by('-created_at')
            serializer = EmpresasFiltroIfisSerializer(query[offset:limit], many=True)
            new_serializer_data = {'cont': query.count(),
                                   'info': serializer.data}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def empresas_list_convenio(request):
    """
    Este metodo sirve para listar todas las empresas que tienen convenio de la tabla empresasConvenio de la base datos corp
    @type request: El campo request no recibe nada
    @rtype: Devuelve una lista de empresas que coicidan, caso contrario devuelve el error generado
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'list/convenio/',
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
            page_size = 20
            page = 0
            offset = page_size * page
            limit = offset + page_size
            # Filtros
            filters = {"state": "1"}

            # Serializar los datos
            query = EmpresasConvenio.objects.filter(**filters).order_by('-created_at')
            serializer = EmpresasConvenioSerializer(query[offset:limit], many=True)
            new_serializer_data = {'cont': query.count(),
                                   'info': serializer.data}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def empresas_create_convenio(request):
    """
    Este metodo sirve para crear empresas convenio de la tabla empresasconvenio de la base datos corp
    @type request: El campo request recibe los campos de la tabla empresa convenio
    @rtype: Devuelve la empresa que se guardo, caso contrario devuelve el error generado
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'create/convenio',
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

            request.data['convenio'] = ObjectId(request.data['convenio'])

            serializer = EmpresasConvenioCreateSerializer(data=request.data)
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def empresas_listOne_filtros(request):
    """
    Este metodo sirve para listar una empresa de la tabla empresas de la base datos corp
    @type request: El campo request recibe el campo nombreComercial, nombreEmpresa, ruc
    @rtype: Devuelve una empresa que coicidan, caso contrario devuelve el error generado
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

            if "nombreComercial" in request.data:
                if request.data["nombreComercial"] != '':
                    filters['nombreComercial__icontains'] = str(request.data["nombreComercial"])

            if "nombreEmpresa" in request.data:
                if request.data["nombreEmpresa"] != '':
                    filters['nombreEmpresa__icontains'] = str(request.data["nombreEmpresa"])

            if "ruc" in request.data:
                if request.data["ruc"] != '':
                    filters['ruc__icontains'] = str(request.data["ruc"])

            # Serializar los datos
            query = Empresas.objects.filter(**filters).order_by('-created_at').first()
            serializer = EmpresasSerializer(query)
            # envio de datos
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def empresas_list_logos(request):
    """
    Este metodo lista los logos de la empresa de la tabla empresas de la base datos corp
    @type request: El campo request no recibe nada
    @rtype: Devuelve una lista de los logos de las empresas, caso contrario devuelve error generado
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'list/convenio/',
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

            # Serializar los datos
            query = Empresas.objects.filter(**filters).order_by('-created_at')
            serializer = EmpresasLogosSerializer(query, many=True)
            new_serializer_data = {'cont': query.count(),
                                   'info': serializer.data}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def empresas_list_array(request):
    """
    Este metodo sirve para listar las empresas de la tabla empresas de la base datos corp
    @type request: El campo request recibe una lista de empresas
    @rtype: Devuelve una lista de empresas, caso contrario devuelve los errores generados
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'list/empresas/array/',
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
            filters["ruc__in"] = request.data['empresas'].split(",")

            # Serializar los datos
            query = Empresas.objects.filter(**filters).order_by('-created_at')
            serializer = EmpresasSerializer(query, many=True)
            new_serializer_data = {'cont': query.count(),
                                   'info': serializer.data}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


# METODO SUBIR ARCHIVOS EXCEL
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def empresas_uploadEmpleados(request):
    """
    Este metodo sirve para cargar los empleados de la empresa en la tabla empleados de la base datos corp
    @type request: El campo request recibe el archivo de los empleados
    @rtype: Devuelve una lista de los registros correctos, incorrectos, caso contrario devuelve los errores generados
    """
    contValidos = 0
    contInvalidos = 0
    contTotal = 0
    errores = []
    try:
        if request.method == 'POST':
            first = True  # si tiene encabezado
            uploaded_file = request.FILES['documento']
            # you may put validations here to check extension or file size
            wb = openpyxl.load_workbook(uploaded_file)
            # getting a particular sheet by name out of many sheets
            worksheet = wb["Clientes"]
            lines = list()
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            lines.append(row_data)

        for dato in lines:
            contTotal += 1
            if first:
                first = False
                continue
            else:
                if len(dato) == 9:
                    resultadoInsertar = insertarDato_empleado(dato, request.data['empresa'])
                    if resultadoInsertar != 'Dato insertado correctamente':
                        contInvalidos += 1
                        errores.append({"error": "Error en la línea " + str(contTotal) + ": " + str(resultadoInsertar)})
                    else:
                        contValidos += 1
                else:
                    contInvalidos += 1
                    errores.append({"error": "Error en la línea " + str(
                        contTotal) + ": la fila tiene un tamaño incorrecto (" + str(len(dato)) + ")"})

        result = {"mensaje": "La Importación se Realizo Correctamente",
                  "correctos": contValidos,
                  "incorrectos": contInvalidos,
                  "errores": errores
                  }
        return Response(result, status=status.HTTP_201_CREATED)

    except Exception as e:
        err = {"error": 'Error verifique el archivo, un error ha ocurrido: {}'.format(e)}
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# INSERTAR DATOS EN LA BASE INDIVIDUAL
def insertarDato_empleado(dato, empresaRuc):
    """
    Este metodo sirve para insertar el empleado en la tabla empleados de la base de datos corp
    @type empresaRuc: El campo empresaRuc recibe el id de la empresa a la cual pertence
    @type dato: El campo dato recibe la fila del excel
    @rtype: Devuelve el esta de dato ingresado, caso contrario los errores del registro
    """
    try:
        if ('None' in dato):
            return 'Tiene campos vacios'
        if (not utils.__validar_ced_ruc(dato[3], 0)):
            return 'Cedula incorrecta'
        if (not utils.isValidEmail(dato[6])):
            return 'Email incorrecto'
        if (not utils.isValidTelefono(dato[7])):
            return 'Celular incorrecto'
        if (not utils.isValidTelefono(dato[8])):
            return 'Whatsapp incorrecto'
        data = {}
        data['tipoIdentificacion'] = dato[2]
        data['identificacion'] = dato[3]
        data['nombres'] = dato[4]
        data['apellidos'] = dato[5]
        data['correo'] = dato[6]
        data['celular'] = dato[7]
        data['whatsapp'] = dato[8]
        empresa = Empresas.objects.filter(_id=ObjectId(empresaRuc), state=1).first()
        data['empresa'] = empresa
        data['state'] = 1
        # inserto el dato con los campos requeridos
        Empleados.objects.update_or_create(**data)
        subject, from_email, to = 'OBTENER MIS DESCUENTOS', "credicompra.bigpuntos@corporacionomniglobal.com", dato[6]
        txt_content = f"""
            REGISTRO DE CUENTA

            Su cuenta para acceder al portal Corp ha sido registrada.

            Para completar su registro haga click en el siguiente {config.API_FRONT_END_CORP_BP}/grp/registro?email={dato[6]}&nombre={dato[4] + ' ' + dato[5]}

            Si el enlace no funciona, copie el siguiente link en una ventana del navegador:
            {config.API_FRONT_END_CORP_BP}/grp/registro?email={dato[6]}&nombre={dato[4] + ' ' + dato[5]}

            Atentamente,
            Equipo Global Redpyme
        """
        html_content = f"""
        <html>
            <body>
                <h1>REGISTRO DE CUENTA</h1>
                <br>
                <p>Su cuenta para acceder al portal Corp ha sido registrada.</p>
                <br>
                <p>
                Para completar su registro haga click en el siguiente 
                <a href='{config.API_FRONT_END_CORP_BP}/grp/registro?email={dato[6]}&nombre={dato[4] + ' ' + dato[5]}'>ENLACE</a>
                </p>
                <br>
                <p>
                Si el enlace no funciona, copie el siguiente link en una ventana del navegador:
                {config.API_FRONT_END_CORP_BP}/grp/registro?email={dato[6]}&nombre={dato[4] + ' ' + dato[5]}
                </p>
                <br>
                Atentamente,
                <br>
                Equipo Global Redpyme
            </body>
        </html>
        """
        sendEmail(subject, txt_content, from_email, to, html_content)
        return 'Dato insertado correctamente'
    except Exception as e:
        return str(e)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def empresas_listEmpleados(request):
    """
    Este metodo sirve para listar los empleados de la empresa
    @type request: El campo request recibe page, page_size, empresa
    @rtype: Devuelve una lista de las empleados de la empresa, caso contrario devuelve los errores generados
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

            if "empresa" in request.data:
                if request.data["empresa"] != '':
                    filters['empresa'] = ObjectId(request.data["empresa"])

            # Serializar los datos
            query = Empleados.objects.filter(**filters).order_by('-created_at')
            serializer = EmpleadosSerializer(query[offset:limit], many=True)
            new_serializer_data = {'cont': query.count(),
                                   'info': serializer.data}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ENCONTRAR UNO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def empresas_listOne_empleado(request, pk):
    """
    Este metodo sirve para lista un empleado de la tabla empleados de la base datos corp
    @type pk: el campo pk recibe el id del empleado
    @type request: El campo request no recibe nada
    @rtype: Devuelve el empleado, caso contrario devuelve los errores generados
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'listOne/empleado',
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
            query = Empleados.objects.get(pk=pk, state=1)
        except Empleados.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = EmpleadosSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ACtualizar
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def empresas_update_empleado(request, pk):
    """
    Este metodo sirve para actualizar un empleado de la tabla empleados de la base datos corp
    @type pk: El campo pk recibe el id del empleado
    @type request: El campo request recibe los campos de la tabla empleados
    @rtype: Devuelve el registro del empleado actualizado, caso contrario devuelve los errores generados
    """
    request.POST._mutable = True
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'update/empleado',
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
            query = Empleados.objects.get(pk=pk, state=1)
        except Empleados.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')

            if query.identificacion != request.data['identificacion']:
                data = {'error': 'La identificacion ya esta registrado.'}
                createLog(logModel, data, logExcepcion)
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            serializer = EmpleadosSerializer(query, data=request.data, partial=True)
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


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def empresas_delete_empleado(request, pk):
    """
    Este metodo sirve para borrar el empleado de la tabla empleados de la base datos corp
    @type pk: El campo pk recibe el id del empleado
    @type request: El campo request no recibe nada
    @rtype: Devuelve el registro eliminado, caso contrario devuelve el error generado
    """
    nowDate = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'empleado/delete/',
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
            persona = Empleados.objects.get(pk=pk, state=1)
        except Empleados.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'DELETE':
            serializer = EmpleadosSerializer(persona, data={'state': '0', 'updated_at': str(nowDate)}, partial=True)
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
