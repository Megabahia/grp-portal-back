from ...PERSONAS.personas_personas.models import Personas
from ...CENTRAL.central_catalogo.models import Catalogo
from ...CORP.corp_empresas.models import Empresas
from ..corp_creditoPersonas.models import AutorizacionCredito, CreditoPersonas
from .models import FacturasEncabezados, FacturasDetalles, FacturasFisicas
from .serializers import (
    FacturasSerializer, FacturasDetallesSerializer, FacturasListarSerializer, FacturaSerializer,
    FacturasListarTablaSerializer, FacturasFisicasSerializer
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime
from django.core import serializers
# Enviar Correo
from ...config.util import sendEmail
# TWILIO
from twilio.rest import Client
from django.conf import settings
# Generar codigos aleatorios
import string
import random
# excel
import openpyxl
# JSON
import json
# ObjectId
from bson import ObjectId
# logs
from ...CENTRAL.central_logs.methods import createLog, datosTipoLog, datosFacturas

# declaracion variables log
datosAux = datosFacturas()
datosTipoLogAux = datosTipoLog()
# asignacion datos modulo
logModulo = datosAux['modulo']
logApi = datosAux['api']
# asignacion tipo de datos
logTransaccion = datosTipoLogAux['transaccion']
logExcepcion = datosTipoLogAux['excepcion']


# CRUD PROSPECTO CLIENTES
# LISTAR TODOS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def factura_list(request):
    """
    Este metodo sirve para listar las facturas de la tabla facturas de la base datos corp
    @type request: El campo request recibe razonSocial, identificacion, page, page_size
    @rtype: Devuelve una lista de factura, caso contrario devuelve el error generado
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
                if 'identificacion' != '':
                    filters['identificacion__icontains'] = request.data['identificacion']

            if 'razonSocial' in request.data:
                if 'razonSocial' != '':
                    filters['razonSocial__icontains'] = request.data['razonSocial']

            # Serializar los datos
            query = FacturasEncabezados.objects.filter(**filters).order_by('-created_at')
            serializer = FacturasListarSerializer(query[offset:limit], many=True)
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
def factura_findOne(request, pk):
    """
    Este metodo sirve para obtener un registro de factura de la tabla factura de la base datos corp
    @type pk: El campo pk recibe el id de la factura
    @type request: El campo request no recibe nada
    @rtype: Devuelve la factura encontrada, caso contrario devuelve error generado
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
            query = FacturasEncabezados.objects.get(pk=pk, state=1)
        except FacturasEncabezados.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = FacturasSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ENCONTRAR LA ULTIMA FACTURA
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def factura_list_latest(request):
    """
    Este metodo sirva para obtener la ultima factura del cliente, de la tabla factura de la base datos corp
    @type request: El campo request recibe cliente, negocio
    @rtype: Devuelve la ultima factura encontrada, caso contrario devuelve el error generado
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'listLatest/',
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
            filters = {"state": "1"}
            if 'negocio' in request.data:
                if request.data['negocio'] != '':
                    filters['negocio__isnull'] = False

            if 'cliente' in request.data:
                if request.data['cliente'] != '':
                    filters['cliente__isnull'] = False

            query = FacturasEncabezados.objects.filter(**filters).order_by('-id')[0]
        except FacturasEncabezados.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = FacturasListarSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# CREAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def factura_create(request):
    """
    Este metodo sirve para crear la factura de la tabla factura de la base datos corp
    @type request: El campo request recibe los campos de la factura y el detalla
    @rtype: Devuelve la factura creada, caso contrario devuelve el error generado
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

            request.data['empresaComercial'] = ObjectId(request.data['empresaComercial'])
            request.data['credito'] = request.data['credito']

            serializer = FacturaSerializer(data=request.data)
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


# ACTUALIZAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def factura_update(request, pk):
    """
    Este metodo sirve para actualizar la factura de la tabla factura de la base datos corp
    @type pk: El campo pk recibe el id de la fatura
    @type request: El campo request recibe los campos de la factura y los detalles
    @rtype: DEvuelve la factura actualizada, caso contrario devuelve el error generado
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
            query = FacturasEncabezados.objects.get(pk=pk, state=1)
        except FacturasEncabezados.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')

            if 'empresaComercial' in request.data:
                if request.data['empresaComercial'] != '':
                    request.data['empresaComercial'] = ObjectId(request.data['empresaComercial'])

            if 'credito' in request.data:
                if request.data['credito'] != '':
                    request.data['credito'] = request.data['credito']

            serializer = FacturasSerializer(query, data=request.data, partial=True)
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


# ENCONTRAR UNO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def factura_findOne_credito(request, pk):
    """
    Este metodo sirve para obtener la factura de la tabla factura de base datos corp
    @type pk: El campo pk recibe el id de la factura
    @type request: El campo request no recibe nada
    @rtype: Devuelve el obtener de la factura, caso contrario devuelve el error generado
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'listOne/credito/',
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
            pk = ObjectId(pk)
            query = FacturasEncabezados.objects.get(credito=pk, state=1)
        except FacturasEncabezados.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = FacturasSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


# GENERAR CODIGOS ENVIAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def factura_generar_codigos_envios(request):
    """
    Este metodo genera los codigos de la tabla autorizacion credito de la base datos corp
    @type request: El campo request recibe user_id,empresaComercial_id, credito_id
    @rtype: Devuelve el codigo generado, caso contrario devuelve el error generado
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'generar/habilitantes/credito/',
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
            # Buscar informacion de la persona y empresa corp
            persona = Personas.objects.filter(user_id=request.data['user_id'], state=1).first()
            empresa = Empresas.objects.filter(pk=ObjectId(request.data['empresaComercial_id']), state=1).first()
            montoDisponible = CreditoPersonas.objects.filter(pk=ObjectId(request.data['_id'])).first().montoDisponible
            # Genera el codigo
            longitud_codigo = Catalogo.objects.filter(tipo='CONFIG_TWILIO', nombre='LONGITUD_CODIGO',
                                                      state=1).first().valor
            numeroTwilio = Catalogo.objects.filter(tipo='CONFIG_TWILIO', nombre='NUMERO_TWILIO', state=1).first().valor
            codigoUsuario = (''.join(random.choice(string.digits) for _ in range(int(longitud_codigo))))
            codigoCorp = (''.join(random.choice(string.digits) for _ in range(int(longitud_codigo))))
            # Correo de cliente
            subject, from_email, to = 'Generacion de numero de autorización del cliente', "08d77fe1da-d09822@inbox.mailtrap.io", persona.email
            txt_content = """
                    Se acaba de generar el codigo de autorizacion del crédito
                    Comuniquese con su asesor del credito, el codigo de autorización es """ + codigoUsuario + """
                    Atentamente,
                    Equipo Global Red Pymes Personas.
            """
            html_content = """
            <html>
                <body>
                    <h1>Se acaba de generar el codigo de autorizacion del crédito</h1>
                    Comuniquese con su asesor del credito, el codigo de autorización es """ + codigoUsuario + """<br>
                    Atentamente,<br>
                    Equipo Global Red Pymes Personas.<br>
                </body>
            </html>
            """
            sendEmail(subject, txt_content, from_email, to, html_content)
            # Correo de la corp
            subject, from_email, to = 'Generacion de numero de autorización de la empresa CORP', "08d77fe1da-d09822@inbox.mailtrap.io", empresa.correo
            txt_content = """
                    Se acaba de generar el codigo de autorizacion del crédito
                    Comuniquese con su asesor del credito, el codigo de autorización es """ + codigoCorp + """
                    Atentamente,
                    Equipo Global Red Pymes Personas.
            """
            html_content = """
            <html>
                <body>
                    <h1>Se acaba de generar el codigo de autorizacion del crédito</h1>
                    Comuniquese con su asesor del credito, el codigo de autorización es """ + codigoCorp + """<br>
                    Atentamente,<br>
                    Equipo Global Red Pymes Personas.<br>
                </body>
            </html>
            """
            sendEmail(subject, txt_content, from_email, to, html_content)

            # Enviar correo a whatsapp
            # Enviar codigo
            # account_sid = settings.TWILIO_ACCOUNT_SID
            # auth_token = settings.TWILIO_AUTH_TOKEN
            # client = Client(account_sid, auth_token)
            # message = client.messages.create(
            #     from_='whatsapp:'+numeroTwilio,
            #     body="""Comuniquese con su asesor del credito, el codigo de autorización es """+codigoUsuario,
            #     to='whatsapp:'+persona.whatsapp
            # )
            # message = client.messages.create(
            #     from_='whatsapp:'+numeroTwilio,
            #     body="""Comuniquese con su asesor del credito, el codigo de autorización es """+codigoCorp,
            #     to='whatsapp:+593'+empresa.telefono1
            # )

            # Guardar codigo en base
            AutorizacionCredito.objects.create(codigo=codigoCorp, credito=request.data['_id'],
                                               entidad=request.data['user_id'])
            AutorizacionCredito.objects.create(codigo=codigoUsuario, credito=request.data['_id'],
                                               entidad=request.data['empresaComercial_id'])

            new_serializer_data = {'estado': 'ok', 'codigoUsuario': codigoUsuario, 'codigoCorp': codigoCorp,
                                   'montoDisponible': montoDisponible}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def factura_create_fisica(request):
    """
    Este metodo sirve para crear una factura de la tabla factura fisica de la base datos corp
    @type request: El campo request recibe los campos de la tabla factura fisicca
    @rtype: DEvuelve el registro creado, caso contrario devuelve el error generado
    """
    request.POST._mutable = True
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'create/factura/',
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

            serializer = FacturasFisicasSerializer(data=request.data)
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
def factura_update_fisica(request, pk):
    """
    Este metodo sirve para actulizar una factura de la tabla factura fisica de la base datos corp
    @type pk: El campo pk recibe el id de la factura fisica
    @type request: El campo request recibe los campos de la tabla factura fisicca
    @rtype: DEvuelve el registro actualizado, caso contrario devuelve el error generado
    """
    request.POST._mutable = True
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'update/factura/' + pk,
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
            query = FacturasFisicas.objects.get(pk=ObjectId(pk), state=1)
        except FacturasFisicas.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')

            serializer = FacturasFisicasSerializer(query, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                if 'Negado' == request.data['estado']:
                    cliente = json.loads(serializer.data['cliente'])
                    enviarCorreoNegado(cliente['correo'], serializer.data['precio'], serializer.data['precio'],
                                       request.data['observacion'])
                if 'Procesar' == request.data['estado']:
                    query.estado = 'Aprobado'
                    query.save()
                    getCreditoPersona = CreditoPersonas.objects.filter(_id=ObjectId(query.credito_id)).first()
                    if getCreditoPersona is not None:
                        getCreditoPersona.montoDisponible = getCreditoPersona.montoDisponible - float(query.precio)
                        getCreditoPersona.save()
                if 'Procesado' == request.data['estado']:
                    credito = CreditoPersonas.objects.filter(_id=ObjectId(request.data['credito_id'])).first()
                    credito.montoDisponible = credito.montoDisponible - float(request.data['precio'])
                    credito.save()
                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def factura_listOne_facturaFisica(request, pk):
    """
    Este metodo sirve para obtener un factura de la tabla factura fisica de la base datos corp
    @type pk: El campo pk recibe el id de la factura fisica
    @type request: El campo request no recibe nada
    @rtype: Devuelve el reigstro encontrado, caso contrario devuelve el error generado
    """
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'listOne/factura',
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
            query = FacturasFisicas.objects.filter(credito_id=pk, state=1).order_by('-created_at').first()
        except FacturasFisicas.DoesNotExist:
            err = {"error": "No existe"}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_404_NOT_FOUND)
        # tomar el dato
        if request.method == 'GET':
            serializer = FacturasFisicasSerializer(query)
            createLog(logModel, serializer.data, logTransaccion)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def factura_list_facturaFisica(request):
    """
    Este metodo sirve para listar las facturas de la tabla factura fisicas de la base datos corp
    @type request: El campo request recibe page, page_size, estado
    @rtype: Devuelve la lista de las facturas, caso contrario el error generado
    """
    request.POST._mutable = True
    timezone_now = timezone.localtime(timezone.now())
    logModel = {
        'endPoint': logApi + 'create/factura/',
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
            # paginacion
            page_size = int(request.data['page_size'])
            page = int(request.data['page'])
            offset = page_size * page
            limit = offset + page_size
            # Filtros
            filters = {"state": "1"}

            if 'estado' in request.data and request.data['estado']:
                filters['estado__icontains'] = request.data['estado']

            # Serializar los datos
            query = FacturasFisicas.objects.filter(**filters).order_by('-created_at')
            serializer = FacturasFisicasSerializer(query[offset:limit], many=True)
            new_serializer_data = {'cont': query.count(),
                                   'info': serializer.data}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


def enviarCorreoNegado(email, valorCompra, valorDesembolso, observacion):
    """
    Este metodo sirve para enviar el correo
    @param observacion: El campo observacion recibe la observacion
    @param valorDesembolso: El campo valorDesembolso no recibe nada
    @param valorCompra: El campo valorCompra recibe la cantidad de compra
    @type email: El campo email recibe el email
    @rtype: No devuelve nada
    """
    subject, from_email, to = 'Ha ocurrido un ERROR', "08d77fe1da-d09822@inbox.mailtrap.io", \
                              email
    txt_content = f"""
        PAGO FALLIDO
        
        Lo sentimos!
                                
        Ha ocurrido un error al intentar realizar el pago de su factura por {valorCompra} debido a {observacion} 
                                
        Su motivo es: {observacion}
    
        Si requiere asistencia personalizada, contáctenos a través del siguiente 
        LINK
        Atentamente,
        
        CrediCompra – Big Puntos
    """
    html_content = f"""
                <html>
                    <body>
                        <h1>PAGO FALLIDO</h1>
                        <br>
                        <h3>Lo sentimos!</h3>
                        <br>
                        <p>
                        Ha ocurrido un error al intentar realizar el pago de su factura por {valorCompra} debido a {observacion} 
                        </p>
                        <p>
                        Su motivo es: {observacion}
                        </p>
                        <p>
                        Si requiere asistencia personalizada, contáctenos a través del siguiente 
                        <a href='https://wa.link/5aips'>LINK</a> 
                        </p>
                        <br>
                        Atentamente,
                        <br>
                        CrediCompra – Big Puntos
                    </body>
                </html>
                """
    sendEmail(subject, txt_content, from_email, to, html_content)
