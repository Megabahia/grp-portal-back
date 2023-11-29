from .models import Roles, RolesUsuarios
from ..central_tipoUsuarios.models import TipoUsuario
from ..central_acciones.models import Acciones, AccionesPermitidas, AccionesPorRol
from ..central_acciones.serializers import AccionesSerializer, AccionesPadreSerializer, \
    AccionesPermitidasSerializer, AccionesPorRolSerializer
from ..central_roles.serializers import RolSerializer, RolCreateSerializer, RolFiltroSerializer, \
    RolesUsuarioSerializer, ListRolesSerializer
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
from ..central_logs.methods import createLog, datosRoles, datosTipoLog

# declaracion variables log
datosAux = datosRoles()
datosTipoLogAux = datosTipoLog()
# asignacion datos modulo
logModulo = datosAux['modulo']
logApi = datosAux['api']
# asignacion tipo de datos
logTransaccion = datosTipoLogAux['transaccion']
logExcepcion = datosTipoLogAux['excepcion']


# Listar
# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'],
                     request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         required=['page_size', 'page'],
                         properties={
                             'page_size': openapi.Schema(type=openapi.TYPE_NUMBER),
                             'page': openapi.Schema(type=openapi.TYPE_NUMBER),
                         },
                     ),
                     operation_description='Uninstall a version of Site',
                     responses={200: RolSerializer(many=True)})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rol_list(request):
    """
    Este metodo lista los roles de la tabla de roles de la base datos central
    @type request: El campo request recibe page, page_size, tipoUsuario
    @rtype: Devuelve una lista de los roles, caso contrario devuelve el error generado
    """
    nowDate = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'list/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'LEER',
        'fechaInicio': str(nowDate),
        'dataEnviada': '{}',
        'fechaFin': str(nowDate),
        'dataRecibida': '{}'
    }
    try:
        if request.method == 'POST':
            logModel['dataEnviada'] = str(request.data)
            # paginacion
            page_size = int(request.data['page_size'])
            page = int(request.data['page'])
            offset = page_size * page
            limit = offset + page_size
            filters = {"state": "1"}

            if 'tipoUsuario' in request.data:
                if request.data['tipoUsuario'] != '':
                    rol = TipoUsuario.objects.filter(nombre=request.data['tipoUsuario'], state=1).first()
                    filters['tipoUsuario'] = rol._id
            # Serializar los datos
            rol = Roles.objects.filter(**filters).order_by('-created_at')
            serializer = RolSerializer(rol[offset:limit], many=True)
            new_serializer_data = {'cont': rol.count(),
                                   'info': serializer.data}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)
    # EXPORTAR


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rol_listExport(request):
    """
    Este metodo se usa consultar la lista a exportar de la tabla roles de la base de datos central
    @type request: El campo request no recibe nada
    @rtype: Devuelve una lista de los roles, caso contrario devuelve el error generado
    """
    try:
        if request.method == 'POST':
            # Serializar los datos
            rol = Roles.objects.filter(state=1).order_by('-created_at')
            serializer = RolSerializer(rol, many=True)
            new_serializer_data = {'cont': rol.count(),
                                   'info': serializer.data}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        return Response(err, status=status.HTTP_400_BAD_REQUEST)

    # CREAR ROL


# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'], request_body=RolCreateSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rol_create(request):
    """
    Este metodo se usa para crear el rol en la tabla de roles de la base datos central
    @type request: El campo request recibe los campos de la tabla roles
    @rtype: Devuelve el registro del rol creado, caso contrario devuelve los error generados
    """
    nowDate = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'create/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'CREAR',
        'fechaInicio': str(nowDate),
        'dataEnviada': '{}',
        'fechaFin': str(nowDate),
        'dataRecibida': '{}'
    }
    try:
        nowDate = timezone.localtime(timezone.now())
        rolId = 0
        if request.method == 'POST':
            logModel['dataEnviada'] = str(request.data)
            # asigno datos del rol
            rolCrear = request.data['rol']
            # agrego la fecha en la que va ser guardada
            rolCrear['created_at'] = str(nowDate)
            if 'updated_at' in request.data:
                rolCrear.pop('updated_at')
            # Guardo los roles
            tipoUsuario = TipoUsuario.objects.filter(nombre=rolCrear['tipoUsuario'], state=1).first()
            rolCrear['tipoUsuario'] = tipoUsuario._id
            serializer = RolCreateSerializer(data=rolCrear, partial=True)
            if serializer.is_valid():
                serializer.save()
                # Asigno id del rol creado para usarlo en las acciones
                rolId = serializer.data['_id']
                dataExitosa = {"mensaje": "rol y acciones creadas exitosamente", "rol": serializer.data}
                createLog(logModel, dataExitosa, logTransaccion)
                return Response(dataExitosa, status=status.HTTP_201_CREATED)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)

    # 'methods' can be used to apply the same modification to multiple methods


@swagger_auto_schema(methods=['post'], request_body=RolCreateSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rol_update(request, pk):
    """
    El metodo se usa para actualizar el rol de la tabla roles de la base datos central
    @type pk: El campo request recibe el id del rol
    @type request: El campo request recibe los campos de la tabla rol
    @rtype: Devuelve el rol actualizado, caso contrario devuelve el error generado
    """
    nowDate = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'update/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'ESCRIBIR',
        'fechaInicio': str(nowDate),
        'dataEnviada': '{}',
        'fechaFin': str(nowDate),
        'dataRecibida': '{}'
    }
    try:
        rolId = ""
        if request.method == 'POST':
            logModel['dataEnviada'] = str(request.data)
            # asigno los datos del rol
            rolUpdate = request.data['rol']
            try:
                # Creo un ObjectoId porque la primaryKey de mongo es ObjectId
                pk = ObjectId(pk)
                rol = Roles.objects.get(pk=pk, state=1)
            except Roles.DoesNotExist:
                err = {"err": "El rol no existe"}
                createLog(logModel, err, logExcepcion)
                return Response(err, status=status.HTTP_404_NOT_FOUND)
            rolId = rol._id
            # agrego la fecha actualizar
            rolUpdate['updated_at'] = str(nowDate)
            if 'created_at' in request.data:
                rolUpdate.pop('created_at')

            serializer = RolSerializer(rol, data=rolUpdate, partial=True)
            if serializer.is_valid():
                serializer.save()
                dataExitosa = {"mensaje": "rol y acciones creadas exitosamente", "rol": serializer.data}
                createLog(logModel, dataExitosa, logTransaccion)
                return Response(dataExitosa, status=status.HTTP_201_CREATED)
            else:
                createLog(logModel, serializer.errors, logExcepcion)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rol_findOne(request, pk):
    """
    Este metodo se usa para lista un rol de la tabla roles de la base datos central
    @type pk: El campo pk recibe el id del rol
    @type request: El campo request no recibe nada
    @rtype: Devuelve el rol buscado, caso contrario devuelve el error generado
    """
    nowDate = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'listOne/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'LEER',
        'fechaInicio': str(nowDate),
        'dataEnviada': '{}',
        'fechaFin': str(nowDate),
        'dataRecibida': '{}'
    }
    try:
        rolId = ""
        accionesList = {}
        if request.method == 'GET':
            logModel['dataEnviada'] = str(request.data)
            # Verifico si existe el rol
            try:
                # Creo un ObjectoId porque la primaryKey de mongo es ObjectId
                pk = ObjectId(pk)
                rol = Roles.objects.get(pk=pk, state=1)
            except Roles.DoesNotExist:
                err = {"err": "El rol no existe"}
                createLog(logModel, err, logExcepcion)
                return Response(err, status=status.HTTP_404_NOT_FOUND)
            # tomo los datos del rol
            serializer = RolCreateSerializer(rol)
            rolId = serializer.data['_id']
            # recorro los padres(modulos)
            for accionPadre in Acciones.objects.filter(idAccionPadre__isnull=True):
                accionesCrud = {}  # guardo las acciones leer,escribir,editar,borrar
                # recorro las acciones de cada padre y las almaceno
                for accionHijo in AccionesPorRol.objects.filter(idRol_id=rolId, idAccion__idAccionPadre__nombre=str(
                        accionPadre.nombre)).order_by('id'):
                    accionesCrud[str(accionHijo.idAccion.nombre)] = int(accionHijo.state)
                # asigno el crud a la lista
                accionesList[str(accionPadre.nombre)] = accionesCrud
            # envio la data
            dataExitosa = {"rol": serializer.data, "acciones": accionesList}
            return Response(dataExitosa, status=status.HTTP_201_CREATED)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def rol_delete(request, pk):
    """
    Este metodo se usa para eliminar el rol de la tabla roles de la base datos central
    @type pk: El campo pk recibe el id del rol
    @type request: El campo request no recibe nada
    @rtype: Devuelve el rol eliminado, caso contrario devuelve el error generado
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
            rol = Roles.objects.get(pk=pk, state=1)
        except Roles.DoesNotExist:
            err = {"err": "El rol no existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'DELETE':
            serializer = RolSerializer(rol, data={'state': '0', 'updated_at': str(nowDate)}, partial=True)
            if serializer.is_valid():
                serializer.save()
                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)

    # LISTA MODULOS


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rol_listAccionPadre(request):
    """
    Este metodo lista las acciones del padre del catalogo
    @type request: El campo request no recibe
    @rtype: Devuelve una lista de las acciones
    """
    try:
        if request.method == 'GET':
            # Serializar los datos
            query = Acciones.objects.filter(idAccionPadre__isnull=True, state=1)
            serializer = AccionesPadreSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        return Response(err, status=status.HTTP_400_BAD_REQUEST)

    # ROLES ID


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rol_listFiltro(request):
    """
    Este metodo lista las acciones del padre del catalogo
    @type request: El campo request no recibe
    @rtype: Devuelve una lista de las acciones
    """
    try:
        if request.method == 'GET':
            rol = Roles.objects.filter(state=1)
            serializer = RolFiltroSerializer(rol, many=True)
            return Response(serializer.data)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        return Response(err, status=status.HTTP_400_BAD_REQUEST)

    # CREAR


# 'methods' can be used to apply the same modification to multiple methods
@swagger_auto_schema(methods=['post'], request_body=RolesUsuarioSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rol_createUsuario(request):
    """
    Este metodo lista las acciones del padre del catalogo
    @type request: El campo request no recibe
    @rtype: Devuelve una lista de las acciones
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'usuarios/create/',
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

            # Creo un ObjectoId porque la primaryKey de mongo es ObjectId
            request.data['rol'] = ObjectId(request.data['rol'])
            # Creo un ObjectoId porque la primaryKey de mongo es ObjectId
            request.data['usuario'] = ObjectId(request.data['usuario'])
            tipoUsuario = TipoUsuario.objects.filter(nombre=rolCrear['tipoUsuario'], state=1).first()
            rolCrear['tipoUsuario'] = tipoUsuario._id

            serializer = RolesUsuarioSerializer(data=request.data)
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

        # LISTAR ROLES USUARIO


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rol_listUsuario(request, pk):
    """
    Este metodo lista las acciones del padre del catalogo
    @type request: El campo request no recibe
    @rtype: Devuelve una lista de las acciones
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
            query = RolesUsuarios.objects.filter(usuario=pk, state=1)
        except RolesUsuarios.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = ListRolesSerializer(query, many=True)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)
