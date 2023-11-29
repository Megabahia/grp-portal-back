from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from ..central_usuarios.models import Usuarios, UsuariosEmpresas
from ..central_tipoUsuarios.models import TipoUsuario
from ..central_infoUsuarios.models import InfoUsuarios
from ..central_infoUsuarios.serializers import InfoUsuarioSerializer
from ...PERSONAS.personas_personas.models import Personas
from ...CORP.corp_empresas.models import Empresas
from ...PERSONAS.personas_personas.serializers import PersonasSerializer
from ..central_roles.models import Roles, RolesUsuarios
from ..central_roles.serializers import ListRolesSerializer
from ..central_usuarios.serializers import UsuarioSerializer, UsuarioImagenSerializer, UsuarioRolSerializer, \
    UsuarioCrearSerializer, UsuarioFiltroSerializer, UsuarioEmpresaSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import logout
from ..central_autenticacion.models import Token
from ..central_autenticacion.auth import token_expire_handler, expires_in, deleteExpiredTokens
# ObjectId
from bson import ObjectId
# Swagger
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# contraeña
from django.utils.crypto import get_random_string
# logs
from ..central_logs.methods import createLog, datosUsuarios, datosTipoLog
from django_rest_passwordreset.views import ResetPasswordRequestToken
# enviar email usuario creado
from ..central_autenticacion.password_reset import resetPasswordNewUser, enviarEmailCreacionPersona

from ...CORP.corp_creditoPersonas.models import CreditoPersonas

# declaracion variables log
datosAux = datosUsuarios()
datosTipoLogAux = datosTipoLog()
# asignacion datos modulo
logModulo = datosAux['modulo']
logApi = datosAux['api']
# asignacion tipo de datos
logTransaccion = datosTipoLogAux['transaccion']
logExcepcion = datosTipoLogAux['excepcion']


# USUARIO LISTAR
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
                     responses={200: UsuarioRolSerializer(many=True)})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def usuario_list(request):
    """
    ESte metodo sirve para listar usuario de la tabla usuario de la base datos central
    @type request: El campo request recibe page, page_size, estado, tipoUsuario
    @rtype: DEvuelve una lista de usuarios, caso contrario devuelve el error generado
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
    try:
        if request.method == 'POST':
            logModel['dataEnviada'] = str(request.data)
            if 'page_size' not in request.data or 'page' not in request.data:
                # error no existen los datos
                errorPaginacion = {'error': 'No existe el/los parámetros de páginacion'}
                createLog(logModel, errorPaginacion, logExcepcion)
                return Response(errorPaginacion, status=status.HTTP_400_BAD_REQUEST)
            # paginacion
            page_size = int(request.data['page_size'])
            page = int(request.data['page'])
            offset = page_size * page
            limit = offset + page_size
            # Filtros
            filters = {"state": "1"}
            # if 'roles' in request.data:
            #     if request.data['roles']!=0:
            #         filters['roles'] = int(request.data['roles'])
            if 'estado' in request.data:
                if request.data['estado'] != '':
                    filters['estado'] = str(request.data['estado'])
            if 'tipoUsuario' in request.data:
                if request.data['tipoUsuario'] != '':
                    filters['tipoUsuario'] = TipoUsuario.objects.filter(nombre=request.data['tipoUsuario'],
                                                                        state=1).first()._id
            # toma de datos
            usuario = Usuarios.objects.filter(**filters).order_by('-created_at')
            serializer = UsuarioRolSerializer(usuario[offset:limit], many=True)
            new_serializer_data = {'cont': usuario.count(),
                                   'info': serializer.data}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        # envio de errores
        createLog(logModel, serializer.errors, logExcepcion)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)

    # USUARIO LISTAR


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
                     responses={200: UsuarioEmpresaSerializer(many=True)})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def usuario_list_corp(request):
    """
    ESte metodo sirve para listar usuario de la tabla usuario de la base datos central
    @type request: El campo request recibe page, page_size, tipoUsuario
    @rtype: DEvuelve una lista de usuarios, caso contrario devuelve el error generado
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
    try:
        if request.method == 'POST':
            logModel['dataEnviada'] = str(request.data)
            if 'page_size' not in request.data or 'page' not in request.data:
                # error no existen los datos
                errorPaginacion = {'error': 'No existe el/los parámetros de páginacion'}
                createLog(logModel, errorPaginacion, logExcepcion)
                return Response(errorPaginacion, status=status.HTTP_400_BAD_REQUEST)
            # paginacion
            page_size = int(request.data['page_size'])
            page = int(request.data['page'])
            offset = page_size * page
            limit = offset + page_size
            # Filtros
            filters = {"state": "1"}
            # if 'tipoUsuario' in request.data:
            #     if request.data['tipoUsuario']!='':
            filters['tipoUsuario'] = TipoUsuario.objects.filter(nombre='corp', state=1).first()._id
            # toma de datos
            usuario = Usuarios.objects.filter(**filters).order_by('-created_at')
            serializer = UsuarioEmpresaSerializer(usuario[offset:limit], many=True)
            new_serializer_data = {'cont': usuario.count(),
                                   'info': serializer.data}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        # envio de errores
        createLog(logModel, serializer.errors, logExcepcion)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)

    # USUARIO LISTAR EXPORTAR


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def usuario_listExport(request):
    """
    ESte metodo sirve para listar usuario de la tabla usuario de la base datos central
    @type request: El campo request recibe page, page_size, estado, roles
    @rtype: DEvuelve una lista de usuarios, caso contrario devuelve el error generado
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
    try:
        if request.method == 'POST':
            logModel['dataEnviada'] = str(request.data)
            # Filtros
            filters = {"state": "1"}
            if 'roles' in request.data:
                if request.data['roles'] != 0:
                    filters['roles'] = int(request.data['roles'])
            if 'estado' in request.data:
                if request.data['estado'] != '':
                    filters['estado'] = str(request.data['estado'])

            # toma de datos
            usuario = Usuarios.objects.filter(**filters).order_by('-created_at')
            serializer = UsuarioRolSerializer(usuario, many=True)
            new_serializer_data = {'cont': usuario.count(),
                                   'info': serializer.data}
            return Response(new_serializer_data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usuario_findOne(request, pk):
    """
    ESte metodo sirve un usuario de la tabla usuario de la base datos central
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
            logModel['dataEnviada'] = str(request.data)
            usuario = Usuarios.objects.get(pk=ObjectId(pk), state=1)
        except Usuarios.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            logModel['dataRecibida'] = str(errorNoExiste)
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(errorNoExiste, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = UsuarioEmpresaSerializer(usuario)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def usuario_update(request, pk):
    """
    ESte metodo sirve para actualizar usuario de la tabla usuario de la base datos central
    @type request: El campo request recibe los campos de la tabla usuarios
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
            usuario = Usuarios.objects.get(pk=pk, state=1)
        except Usuarios.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')

            if 'tipoUsuario' in request.data:
                if request.data['tipoUsuario'] != '':
                    request.data['tipoUsuario'] = TipoUsuario.objects.filter(nombre=request.data['tipoUsuario'],
                                                                             state=1).first()._id

            infoUsuario = {}
            if 'empresa' in request.data:
                if request.data['empresa'] != '':
                    empresa_id = Empresas.objects.filter(_id=ObjectId(request.data['empresa']), state=1).first()
                    UsuariosEmpresas.objects.filter(usuario=usuario).update(empresa_id=empresa_id._id, usuario=usuario,
                                                                            state=1)
                else:
                    UsuariosEmpresas.objects.filter(usuario=usuario).update(state=0)

                infoUsuario = InfoUsuarios.objects.filter(usuario=usuario, state=1).first()
                infoUsuario = InfoUsuarioSerializer(infoUsuario, data=request.data, partial=True)
                if infoUsuario.is_valid():
                    infoUsuario.save()

            if 'roles' in request.data:
                if request.data['roles'] != '':
                    role = Roles.objects.filter(nombre=request.data['roles'], state=1).first()
                    RolesUsuarios.objects.filter(usuario=ObjectId(request.data['_id'])).update(rol=role,
                                                                                               usuario=ObjectId(
                                                                                                   request.data['_id']),
                                                                                               state=1)
                else:
                    RolesUsuarios.objects.filter(usuario=usuario).update(state=0)

            serializer = UsuarioEmpresaSerializer(usuario, data=request.data, partial=True)
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
def usuario_delete(request, pk):
    """
    ESte metodo sirve para borrar usuario de la tabla usuario de la base datos central
    @type pk: El campo pk recibe el id del usuario
    @type request: El campo request no recibe
    @rtype: DEvuelve el registro eliminado, caso contrario devuelve el error generado
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'delete/',
        'modulo': logModulo,
        'tipo': logExcepcion,
        'accion': 'BORRAR',
        'fechaInicio': str(timezone_now),
        'dataEnviada': '{}',
        'fechaFin': str(timezone_now),
        'dataRecibida': '{}'
    }
    try:
        try:
            logModel['dataEnviada'] = str(request.data)
            pk = ObjectId(pk)
            usuario = Usuarios.objects.get(pk=pk, state=1)
        except Usuarios.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'DELETE':
            now = timezone.localtime(timezone.now())
            serializer = UsuarioSerializer(usuario, data={'state': '0', 'updated_at': str(now)}, partial=True)
            if serializer.is_valid():
                serializer.save()
                usuario.delete()
                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)

    # CREAR USUARIO CORP


@api_view(['POST'])
def usuario_core_create(request):
    """
    ESte metodo sirve para crear usuario de la tabla usuario de la base datos central
    @type request: El campo request recibe los campos de la tabla usuarios
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

    try:
        if request.method == 'POST':
            request.data['created_at'] = str(timezone_now)
            if 'updated_at' in request.data:
                request.data.pop('updated_at')
            logModel['dataEnviada'] = str(request.data)
            tipoUsuario = TipoUsuario.objects.filter(nombre='corp', state=1).first()
            request.data['tipoUsuario'] = tipoUsuario._id
            serializer = UsuarioCrearSerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                account = serializer.save()
                rol = Roles.objects.filter(nombre=str(request.data['roles']), state=1).first()
                rolUsuario = RolesUsuarios.objects.filter(usuario=account, rol=rol, state=1).first()

                if rolUsuario is None:
                    RolesUsuarios.objects.create(
                        rol=rol,
                        usuario=account
                    )
                # Consultar roles de usuario
                rolesUsuario = RolesUsuarios.objects.filter(usuario=account, state=1)
                roles = ListRolesSerializer(rolesUsuario, many=True).data
                # Consultar datos de la persona en GRP_PERSONAS_PERSONAS
                dataPeronsa = {}
                dataPeronsa['user_id'] = str(account.pk)
                dataPeronsa['email'] = str(account.email)
                if 'nombres' in request and 'apellidos' in request:
                    dataPeronsa['nombresCompleto'] = request.data['nombres'] + ' ' + request.data['apellidos']
                persona = Personas.objects.create(**dataPeronsa)
                personaSerializer = PersonasSerializer(persona).data

                # data['response'] = 'Usuario creado correctamente'
                # data['email'] = account.email
                token = Token.objects.get(user=account)
                # data['token'] = token
                data = {
                    'token': token.key,
                    'id': str(account.pk),
                    'persona': personaSerializer,
                    'email': account.email,
                    'tokenExpiracion': expires_in(token),
                    'roles': roles,
                    'estado': account.estado
                }
                createLog(logModel, data, logTransaccion)
                # data['tokenEmail']=str(resetPasswordNewUser(data['email']))
            else:
                data = serializer.errors
                createLog(logModel, data, logExcepcion)
            return Response(data)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)

    # CREAR USUARIO


@api_view(['POST'])
def usuario_create(request):
    """
    ESte metodo sirve para crear usuario de la tabla usuario de la base datos central
    @type request: El campo request recibe los campos de la tabla usuarios
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

    try:
        if request.method == 'POST':
            request.data['created_at'] = str(timezone_now)
            if 'updated_at' in request.data:
                request.data.pop('updated_at')
            logModel['dataEnviada'] = str(request.data)
            tipoUsuario = TipoUsuario.objects.filter(nombre=request.data['tipoUsuario'], state=1).first()
            request.data['tipoUsuario'] = tipoUsuario._id
            # AGREGA CONTRASEÑA
            if 'password' not in request.data:
                request.data['password'] = get_random_string(length=32)
            serializer = UsuarioCrearSerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                account = serializer.save()

                # creditos = CreditoPersonas.objects.filter(email=request.data['email'], state=1)
                # for credito in creditos:
                #     credito.user_id = str(account.pk)
                #     credito.save()

                if 'roles' in request.data:
                    if request.data['roles'] != '':
                        rol = Roles.objects.filter(nombre=request.data['roles'], state=1).first()
                        RolesUsuarios.objects.create(
                            rol=rol,
                            usuario=account
                        )
                infoUsuario = {}
                if 'empresa' in request.data:
                    if request.data['empresa'] != '':
                        empresa_id = Empresas.objects.filter(_id=ObjectId(request.data['empresa']), state=1).first()
                        UsuariosEmpresas.objects.create(empresa_id=empresa_id._id, usuario=account)

                request.data['usuario'] = account._id
                infoUsuario = InfoUsuarioSerializer(data=request.data)
                if infoUsuario.is_valid():
                    infoUsuario.save()

                # Consultar roles de usuario
                rolesUsuario = RolesUsuarios.objects.filter(usuario=account, state=1)
                roles = ListRolesSerializer(rolesUsuario, many=True).data
                # Consultar datos de la persona en GRP_PERSONAS_PERSONAS
                dataPeronsa = {}
                dataPeronsa['user_id'] = str(account.pk)
                dataPeronsa['email'] = str(account.email)
                if 'nombres' in request.data and 'apellidos' in request.data:
                    dataPeronsa['nombresCompleto'] = request.data['nombres'] + ' ' + request.data['apellidos']
                persona = Personas.objects.create(**dataPeronsa)

                # data['response'] = 'Usuario creado correctamente'
                # data['email'] = account.email
                token = Token.objects.get(user=account)
                # data['token'] = token
                createLog(logModel, data, logTransaccion)
                data = {
                    'token': token.key,
                    'id': str(account.pk),
                    'email': account.email,
                    'tokenExpiracion': expires_in(token),
                    'roles': roles,
                    'estado': account.estado
                }
                if 'roles' in request.data:
                    if 'SuperMonedas' == request.data['roles']:
                        # enviarEmailCreacionPersona(data['email'])
                        data['tokenEmail'] = str(resetPasswordNewUser(data['email']))
                    else:
                        data['tokenEmail'] = str(resetPasswordNewUser(data['email']))

                if 'empresa' not in request.data:
                    personaSerializer = PersonasSerializer(persona).data

                data['infoUsuario'] = infoUsuario.data

            else:
                data = serializer.errors
                createLog(logModel, data, logExcepcion)
            return Response(data)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def usuarioImagen_update(request, pk):
    """
    ESte metodo sirve para actualizar la imagen usuario de la tabla usuario de la base datos central
    @type request: El campo request recibe el archivo
    @rtype: DEvuelve el registro actualizado, caso contrario devuelve el error generado
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'update/imagen/',
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
            usuario = Usuarios.objects.get(pk=pk, state=1)
        except Usuarios.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')
            serializer = UsuarioImagenSerializer(usuario, data=request.data, partial=True)
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

    # toma los vendedores


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vendedor_list(request):
    """
    ESte metodo sirve para listar usuario de la tabla usuario de la base datos central
    @type request: El campo request recibe el nombre del rol
    @rtype: DEvuelve una lista de usuario, caso contrario devuelve el error generado
    """
    if request.method == 'GET':
        try:
            query = Usuarios.objects.filter(state=1, idRol__nombre="Vendedor")
            serializer = UsuarioFiltroSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

        # toma los usuarios


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def usuarios_list_rol(request):
    """
    ESte metodo sirve para listar usuario de la tabla usuario de la base datos central
    @type request: El campo request recibe el nombre del rol
    @rtype: DEvuelve una lista de usuario, caso contrario devuelve el error generado
    """
    if request.method == 'POST':
        try:
            query = Usuarios.objects.filter(state=1, idRol__nombre=request.data['rol'])
            serializer = UsuarioFiltroSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def usuario_update_by_email(request):
    """
    ESte metodo sirve para crear usuario de la tabla usuario de la base datos central
    @type request: El campo request recibe los campos de la tabla usuarios
    @rtype: DEvuelve el registro creado, caso contrario devuelve el error generado
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
            usuario = Usuarios.objects.get(email=request.data['email'], state=1)
        except Usuarios.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)

            if usuario.estado == "1":
                request.data['estado'] = "2"

            serializer = UsuarioEmpresaSerializer(usuario, data=request.data, partial=True)
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
