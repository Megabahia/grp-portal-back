from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from apps.CENTRAL.central_usuarios.models import Usuarios, UsuariosEmpresas
# Importar base de datos personas
from apps.PERSONAS.personas_personas.models import Personas
# Importar serializers empresa y base de datos empresa
from apps.CORP.corp_creditoPersonas.models import CreditoPersonas
# Importar serializers empresa y base de datos empresa
from apps.CORP.corp_empresas.models import Empresas
from apps.CORP.corp_empresas.serializers import EmpresasSerializer
# Importar serializer de personas
from apps.PERSONAS.personas_personas.serializers import PersonasSerializer
from apps.CENTRAL.central_usuarios.serializers import UsuarioSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout, authenticate
# ObjectId
from bson import ObjectId
# token login
from rest_framework.authtoken.views import ObtainAuthToken
from apps.CENTRAL.central_autenticacion.models import Token
from apps.CENTRAL.central_autenticacion.auth import token_expire_handler, expires_in, deleteExpiredTokens
from django.utils import timezone
# logs
from apps.CENTRAL.central_logs.methods import createLog, datosAuth, datosTipoLog
# permisos
from apps.CENTRAL.central_roles.models import RolesUsuarios
from apps.CENTRAL.central_roles.serializers import ListRolesSerializer
from apps.CENTRAL.central_acciones.models import Acciones, AccionesPermitidas, AccionesPorRol

# declaracion variables log
datosAux = datosAuth()
datosTipoLogAux = datosTipoLog()
# asignacion datos modulo
logModulo = datosAux['modulo']
logApi = datosAux['api']
# asignacion tipo de datos
logTransaccion = datosTipoLogAux['transaccion']
logExcepcion = datosTipoLogAux['excepcion']


class login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        # log
        timezone_now = timezone.localtime(timezone.now())
        logModel = {
            'endPoint': logApi + 'login/',
            'modulo': logModulo,
            'tipo': logExcepcion,
            'accion': 'LEER',
            'fechaInicio': str(timezone_now),
            'dataEnviada': '{}',
            'fechaFin': str(timezone_now),
            'dataRecibida': '{}'
        }
        try:
            logModel['dataEnviada'] = str(request.data)
            serializer = self.serializer_class(data=request.data, context={'request': request})
            if serializer.is_valid():
                user = serializer.validated_data['user']
                if user.state == 1:
                    if user.estado == "1":
                        data = {
                            'code': 400,
                            'msg': 'Confirme la dirección de su correo electrónico, el link de acceso fue enviado a la dirección de correo registrada.'
                        }
                        return Response(data, status=status.HTTP_200_OK)
                    if user.tipoUsuario.nombre != request.data['tipoUsuario']:
                        data = {'error': 'Usted no tiene una cuenta.'}
                        return Response(data, status=status.HTTP_404_NOT_FOUND)
                    token = Token.objects.create(user=user)
                    # ELIMINAR USUARIOS EXPIRADOS
                    deleteExpiredTokens()
                    # Consultar roles de usuario
                    rolesUsuario = RolesUsuarios.objects.filter(usuario=user, state=1)
                    roles = ListRolesSerializer(rolesUsuario, many=True).data
                    # Consultar datos de la persona en GRP_PERSONAS_PERSONAS
                    try:
                        persona = Personas.objects.get(user_id=user._id)
                        personaSerializer = PersonasSerializer(persona).data
                    except Exception as e:
                        personaSerializer = {}

                    try:
                        empresa = UsuariosEmpresas.objects.filter(usuario=user).first()
                        empresaSerializer = EmpresasSerializer(
                            Empresas.objects.filter(_id=ObjectId(empresa.empresa_id)).first()).data
                    except Exception as e:
                        empresaSerializer = {}

                    try:
                        credito = CreditoPersonas.objects.filter(user_id=str(user.pk), state=1).order_by('-created_at').first()
                        if credito is not None:
                            if credito.estado == 'Por Completar' or credito.estado == 'Negado':
                                creditoAprobado = 8
                            else:
                                creditoAprobado = 0
                        else:
                            creditoAprobado = 0
                    except Exception as e:
                        print(e)
                        creditoAprobado = 0

                    data = {
                        'token': token.key,
                        'id': str(user.pk),
                        'persona': personaSerializer,
                        'empresa': empresaSerializer,
                        'email': user.email,
                        'tokenExpiracion': expires_in(token),
                        'roles': roles,
                        'estado': user.estado,
                        'creditoAprobado': creditoAprobado,
                    }
                    createLog(logModel, data, logTransaccion)
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    err = {'error': 'el usuario no existe!'}
                    createLog(logModel, err, logExcepcion)
                    return Response(err, status=status.HTTP_404_NOT_FOUND)
            else:
                createLog(logModel, serializer.errors, logExcepcion)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
