from .models import CreditoPreaprobados
from ...PERSONAS.personas_personas.models import Personas
from ...CORP.corp_empresas.models import Empresas
from django.db.models import Q
from .serializers import (
    CreditoPreaprobadosSerializer, CreditoPreaprobadosIfisSerializer
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
# excel
import openpyxl
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
                     responses={200: CreditoPreaprobadosSerializer(many=True)})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def creditoPreaprobados_list(request):
    """
    ESte metodo sirve para listar los creditos
    @type request: recibe user_id, tipoPersona, page, page_size
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
            # paginacion
            page_size = int(request.data['page_size'])
            page = int(request.data['page'])
            offset = page_size * page
            limit = offset + page_size
            # Filtros
            filters = {"state": "1"}

            if "user_id" in request.data:
                if request.data["user_id"] != '':
                    filters['user_id'] = str(request.data["user_id"])
            if "tipoPersona" in request.data:
                if request.data["tipoPersona"] != '':
                    filters['tipoPersona__icontains'] = str(request.data["tipoPersona"])

            # Serializar los datos
            query = CreditoPreaprobados.objects.filter(**filters).order_by('-created_at')
            serializer = CreditoPreaprobadosSerializer(query[offset:limit], many=True)
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
@swagger_auto_schema(methods=['post'], request_body=CreditoPreaprobadosSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def creditoPreaprobados_create(request):
    """
    Este metodo sirve para crear un credito
    @type request: recibe los campos de la tabla credipreaprobados
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

            request.data['empresa'] = ObjectId(request.data['empresa'])

            serializer = CreditoPreaprobadosSerializer(data=request.data)
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
def creditoPreaprobados_listOne(request, pk):
    """
    Este metodo sirve para obtener un registro
    @type pk: El campo recibe el id de la tabla credito preprobados
    @type request: El campo request no recibe nada
    @rtype: DEvuelve el registro obtenido, caso contrario devuelve el error generado
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
            query = CreditoPreaprobados.objects.get(pk=pk, state=1)
        except CreditoPreaprobados.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = CreditoPreaprobadosSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ACTUALIZAR
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'], request_body=CreditoPreaprobadosSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def creditoPreaprobados_update(request, pk):
    """
    Este metodo sirve para actualizar el credito preaprobado
    @param pk: Recibe el id de la tabla credito preaprobado
    @type request: recibe los campos de la tabla creditos preaprobados
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
            query = CreditoPreaprobados.objects.get(pk=pk, state=1)
        except CreditoPreaprobados.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')

            if 'empresa_financiera' in request.data:
                if 'empresa_financiera' != '':
                    request.data['empresa_financiera'] = ObjectId(request.data['empresa_financiera'])

            if query.estado == 'Aprobado':
                serializer = CreditoPreaprobadosSerializer(query)
                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data)

            serializer = CreditoPreaprobadosSerializer(query, data=request.data, partial=True)
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
def creditoPreaprobados_delete(request, pk):
    """
    ESte metodo sirve para eliminar el credito preaprobado
    @param pk: recibe el id del credito preaprobado
    @type request: El campo request no recibe nada
    @rtype: DEvuelve el registro elimnado, caso contrario devuelve el error generado
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
            persona = CreditoPreaprobados.objects.get(pk=pk, state=1)
        except CreditoPreaprobados.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'DELETE':
            serializer = CreditoPreaprobadosSerializer(persona, data={'state': '0', 'updated_at': str(nowDate)},
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
def creditoPreaprobados_list_corp(request):
    """
    Este metodo sirve para listar
    @type request: recibe page, page_size, empresa_comercial, tipoPersona, cedula, nombresCompleto
    @rtype: DEvuelve una lista, caso contrario devuelve el error generado
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'list/corp/',
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

            if "empresa_comercial" in request.data:
                if request.data["empresa_comercial"] != '':
                    filters['empresa_comercial'] = request.data["empresa_comercial"]
            if "tipoPersona" in request.data:
                if request.data["tipoPersona"] != '':
                    filters['tipoPersona'] = str(request.data["tipoPersona"])

            if "cedula" in request.data:
                if request.data["cedula"] != '':
                    cedulas = Personas.objects.filter(identificacion__icontains=str(request.data["cedula"]),
                                                      state=1).values_list('user_id', flat=True)
                    arr = []
                    for id in cedulas:
                        arr.append(str(id))
                    filters['user_id__in'] = arr

            if "nombresCompleto" in request.data:
                if request.data["nombresCompleto"] != '':
                    cedulas = Personas.objects.filter(
                        Q(nombresCompleto__icontains=str(request.data["nombresCompleto"])), state=1).values_list(
                        'user_id', flat=True).distinct()
                    arr = []
                    for id in cedulas:
                        arr.append(str(id))
                    filters['user_id__in'] = arr

            # Serializar los datos
            query = CreditoPreaprobados.objects.filter(**filters).order_by('-created_at')
            serializer = CreditoPreaprobadosSerializer(query[offset:limit], many=True)
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
def creditoPreaprobados_list_ifis(request):
    """
    Este metodo sirve para listar
    @type request: recibe page, page_size, empresa_financiera, tipoPersona, estado, tipoCredito
    @rtype: DEvuelve una lista, caso contrario devuelve el error generado
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'list/corp/',
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

            if "empresa_financiera" in request.data:
                if request.data["empresa_financiera"] != '':
                    filters['empresa_financiera'] = ObjectId(request.data["empresa_financiera"])

            if "tipoPersona" in request.data:
                if request.data["tipoPersona"] != '':
                    filters['tipoPersona'] = str(request.data["tipoPersona"])

            if "estado" in request.data:
                if request.data["estado"] != '':
                    filters['estado'] = str(request.data["estado"])

            if "tipoCredito" in request.data:
                if request.data["tipoCredito"] != '':
                    filters['tipoCredito'] = str(request.data["tipoCredito"])

            # Serializar los datos
            query = CreditoPreaprobados.objects.filter(**filters).order_by('-created_at')
            serializer = CreditoPreaprobadosIfisSerializer(query[offset:limit], many=True)
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
def uploadEXCEL_creditosPreaprobados(request):
    """
    ESte metodo sirve para cargar el excel con los credito preaprobados
    @type request: REcibe el archivo excel
    @rtype: Devuelve los registro correctos, incorrectos, caso contrario devuele el error generado
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
                if len(dato) == 7:
                    resultadoInsertar = insertarDato_creditoPreaprobado(dato, request.data['empresa_financiera'])
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
def insertarDato_creditoPreaprobado(dato, empresa_financiera):
    """
    Este metodo sirve para insertar la fila del excel en la tabla credito preaprobado
    @param empresa_financiera: REcibe el id de la empresa finaniera
    @type dato: recibe la fila del excel
    @rtype: DEvuelve el registro guardado, caso contrario devuele el error generado
    """
    try:
        timezone_now = timezone.localtime(timezone.now())
        data = {}
        data['vigencia'] = dato[0].replace('"', "")[0:10] if dato[0] != "NULL" else None
        data['concepto'] = dato[1].replace('"', "") if dato[1] != "NULL" else None
        data['monto'] = dato[2].replace('"', "") if dato[2] != "NULL" else None
        data['plazo'] = dato[3].replace('"', "") if dato[3] != "NULL" else None
        data['interes'] = dato[4].replace('"', "") if dato[4] != "NULL" else None
        data['estado'] = 'Pre aprobado'
        data['tipoPersona'] = 'SuperMonedas'
        data['tipoCredito'] = 'Preaprobado'
        persona = Personas.objects.filter(identificacion=dato[5], state=1).first()
        data['user_id'] = persona.user_id
        # data['observaciones'] = dato[8].replace('"', "") if dato[8] != "NULL" else None
        # data['descripcion'] = dato[9].replace('"', "") if dato[9] != "NULL" else None
        data['empresa_financiera'] = Empresas.objects.get(_id=ObjectId(empresa_financiera))
        # empresa = Empresas.objects.filter(ruc=dato[6],state=1).first()
        # data['empresa_comercial'] = empresa._id
        data['empresasAplican'] = dato[6]
        data['created_at'] = str(timezone_now)
        # inserto el dato con los campos requeridos
        CreditoPreaprobados.objects.create(**data)
        return 'Dato insertado correctamente'
    except Exception as e:
        return str(e)
