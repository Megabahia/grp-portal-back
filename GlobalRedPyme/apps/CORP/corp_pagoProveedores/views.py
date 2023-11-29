import io
import os

from ..corp_creditoPersonas.models import CreditoPersonas
from ..corp_movimientoCobros.models import Transacciones

# Establecer el directorio base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import datetime
import qrcode
import fitz
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12
from endesive.pdf import cms
## Libreria para agregar imagenes a pdf
from PIL import Image, ImageDraw, ImageFont
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import PagoProveedores
from .serializers import (
    PagoProveedorSerializer
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
import json
# Importar boto3
import boto3
import tempfile
import environ
import os
# Import PDF
from fpdf import FPDF
# Enviar Correo
from apps.config.util import sendEmail
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
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pagoProveedores_create(request):
    """
    ESte metodo sirve para crear un proveedor en la tabla proveedor de la base datos corp
    @type request: El campo request recibe los campo de la tabla proveedores
    @rtype: DEvuelve el registro creado, caso contrario devuelve el error generado
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

            serializer = PagoProveedorSerializer(data=request.data)
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
def pagoProveedores_update(request, pk):
    """
    ESte metodo sirve para actualizar un proveedor en la tabla proveedor de la base datos corp
    @param pk: El campo pk recibe el id del proveedor
    @type request: El campo request recibe los campo de la tabla proveedores
    @rtype: DEvuelve el registro actualizar, caso contrario devuelve el error generado
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
            query = PagoProveedores.objects.filter(pk=ObjectId(pk), state=1).first()
        except PagoProveedores.DoesNotExist:
            errorNoExiste = {'error': 'No existe'}
            createLog(logModel, errorNoExiste, logExcepcion)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            now = timezone.localtime(timezone.now())
            request.data['updated_at'] = str(now)
            if 'created_at' in request.data:
                request.data.pop('created_at')

            if 'claveFirma' in request.data:
                if request.data != '':
                    # certificado = open('/Users/papamacone/Downloads/6194645_identity.p12', 'rb')
                    # pdf2 = open('/Users/papamacone/Downloads/CASH API-v8.pdf', 'rb')
                    datau, datas = firmar(request, query)
                    archivo_pdf_para_enviar_al_cliente = io.BytesIO()
                    archivo_pdf_para_enviar_al_cliente.write(datau)
                    archivo_pdf_para_enviar_al_cliente.write(datas)
                    archivo_pdf_para_enviar_al_cliente.seek(0)

                    request.data['archivoFirmado'] = InMemoryUploadedFile(archivo_pdf_para_enviar_al_cliente,
                                                                          'media',
                                                                          'documentoFirmado.pdf',
                                                                          'application/pdf',
                                                                          archivo_pdf_para_enviar_al_cliente.getbuffer().nbytes,
                                                                          None
                                                                          )

            serializer = PagoProveedorSerializer(query, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                usuario = json.loads(query.usuario)
                if 'Negado' in query.estado:
                    enviarNegadoPago(usuario['email'], query.valorPagar, query)

                if 'Procesar' in query.estado:
                    enviarProcesandoPago(usuario['email'], query.valorPagar, query)
                    credito = CreditoPersonas.objects.filter(user_id=serializer.data['user_id'], estado='Aprobado',
                                                             state=1).order_by('-created_at').first()
                    Transacciones.objects.create(**{
                        'fechaTransaccion': timezone_now,
                        'tipo': 'Pago proveedor',
                        'estado': 'Aprobado',
                        'informacion': json.dumps(serializer.data),
                        'egreso': float(serializer.data['valorPagar']),
                        'total': (credito.montoDisponible - float(serializer.data['valorPagar'])),
                        'user_id': serializer.data['user_id'],
                        'creditoPersona_id': credito._id,
                        'pagoProveedores': query,
                    })

                createLog(logModel, serializer.data, logTransaccion)
                return Response(serializer.data)
            createLog(logModel, serializer.errors, logExcepcion)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        err = {"error": 'Un error ha ocurrido: {}'.format(e)}
        createLog(logModel, err, logExcepcion)
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pagoProveedores_list(request):
    """
    ESte metodo sirve para listar un proveedor en la tabla proveedor de la base datos corp
    @type request: El campo request recibe empresa_id, page, page_size
    @rtype: DEvuelve una lista proveedores, caso contrario devuelve el error generado
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

            if "empresa_id" in request.data:
                if request.data["empresa_id"] != '':
                    filters['empresa_id'] = str(request.data["empresa_id"])

            # Serializar los datos
            query = PagoProveedores.objects.filter(**filters).order_by('-created_at')
            serializer = PagoProveedorSerializer(query[offset:limit], many=True)
            new_serializer_data = {'cont': query.count(),
                                   'info': serializer.data}
            # envio de datos
            return Response(new_serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            err = {"error": 'Un error ha ocurrido: {}'.format(e)}
            createLog(logModel, err, logExcepcion)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12
from endesive.pdf import cms


def firmar(request, query):
    """
    Este metodo sirve para firmar documentos
    @type query: El campo query recibe la consulta de la tabla pago proveedores
    @type request: El campo request recibe el archivo
    @rtype: DEvuelve el archivo firmado
    """
    usuario = json.loads(query.usuario)
    certificado = request.data['certificado']
    pdf = request.FILES['pdf']
    contrasenia = request.data['claveFirma']
    date = timezone_now = timezone.localtime(timezone.now())
    date = date.strftime("D:%Y%m%d%H%M%S+00'00'")
    dct = {
        "aligned": 0,
        "sigflags": 3,
        "sigflagsft": 132,
        "sigpage": 0,
        "sigbutton": True,
        "sigfield": "Signature1",
        "auto_sigfield": True,
        "sigandcertify": True,
        "signaturebox": (470, 840, 570, 640),
        "signature": usuario['nombresCompleto'],
        "signature_manual": [],
        # "signature_img": "signature_test.png",
        "contact": usuario['email'],
        "location": "Ubicación",
        "signingdate": date,
        "reason": "Pago a proveedor " + query.nombrePyme,
        "password": contrasenia,
    }
    # with open("cert.p12", "rb") as fp:
    p12 = pkcs12.load_key_and_certificates(
        certificado.read(), contrasenia.encode("ascii"), backends.default_backend()
    )

    # datau = open(fname, "rb").read()
    # Ruta de destino para guardar el archivo
    # ruta = '/Users/papamacone/Documents/Edgar/grp-back-coop/GlobalRedPyme/' + pdf.name
    ruta = os.path.join(BASE_DIR, '../' + pdf.name)

    # Leer los datos del archivo
    with open(ruta, 'wb') as archivo_destino:
        for chunk in pdf.chunks():
            archivo_destino.write(chunk)

    date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    datosFirmante = f"""FIRMADO POR:\n {dct['signature']} \n FECHA:\n {date}"""
    generarQR(datosFirmante)
    output_file = "example-with-barcode.pdf"
    agregarQRDatosFirmante(datosFirmante, output_file, ruta)
    datau = open(output_file, "rb").read()
    dct.pop('signature')
    datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")
    return datau, datas
    # return Response('new_serializer_data', status=status.HTTP_200_OK)


def agregarQRDatosFirmante(datosFirmante, output_file, ruta):
    """
    ESte metodo sirve para agregar la firma qr en al archivo pdf
    @type ruta: el campo ruta recibe la ruta de donde esta el archivo
    @type output_file: El campo output_file recibe el archivo donde se guardara el archivo firmado
    @type datosFirmante: El campo datosfirmante recibe los datos del usuario
    @rtype: DEvuelve
    """
    # Define the position and size of the image rectangle
    image_rectangle = fitz.Rect(0, 0, 250, 220)  # Adjust the coordinates and size as needed

    # Retrieve the first page of the PDF
    file_handle = fitz.open(ruta)
    first_page = file_handle[0]

    # Open and flip the image vertically
    image_path = 'output.png'
    image = Image.open(image_path).transpose(Image.FLIP_TOP_BOTTOM)
    image.save('flipped_image.png')

    # Insert the flipped image into the PDF
    img = open('output.png', "rb").read()  # an image file
    img_xref = 0
    first_page.insert_image(image_rectangle, stream=img, xref=img_xref)
    ##############

    # Crear una nueva imagen con fondo blanco
    width = 400
    height = 400
    image = Image.new('RGB', (width, height), 'white')

    # Crear un objeto ImageDraw para dibujar en la imagen
    draw = ImageDraw.Draw(image)

    # Especificar la fuente a utilizar
    font = ImageFont.truetype('Arial Unicode.ttf', size=40)

    # Especificar el texto y su posición en la imagen
    text_position = (10, 50)

    # Dibujar el texto en la imagen
    draw.text(text_position, datosFirmante, font=font, fill='black')

    # Guardar la imagen resultante
    image.save('imagen_con_texto.png')
    ##############
    # Open and flip the text image vertically
    text_image_path = 'imagen_con_texto.png'
    text_image = Image.open(text_image_path).transpose(Image.FLIP_TOP_BOTTOM)
    text_image.save('flipped_text_image.png')

    img1 = open('imagen_con_texto.png', "rb").read()  # an image file
    first_page.insert_image(fitz.Rect(250, 0, 450, 220), stream=img1, xref=img_xref)

    # Save the modified PDF
    file_handle.save(output_file)


def generarQR(datos):
    """
    ESte metodo sirve para generar el codigo QR
    @type datos: El campo datos recibe los datos del usuario
    @rtype: No devuelve nada
    """
    img = qrcode.make(datos)
    f = open("output.png", "wb")
    img.save(f)
    f.close()


def enviarNegadoPago(email, monto, registro):
    """
    Este metodo sirve para enviar el correo de pago negado
    @type registro: El campo registro recibe la insercion de la fila
    @type monto: El campo monto recibe el monto
    @type email: El campo email recibe el email
    @rtype: Devuelve verdadero o falso del envio de correo
    """
    subject, from_email, to = 'RAZÓN POR LA QUE SE NIEGA EL PAGO A PROVEEDORES', "08d77fe1da-d09822@inbox.mailtrap.io", \
                              email
    txt_content = f"""
        Pago a proveedores – Crédito Pagos
        
        Lo sentimos
        
        Su pago a proveedores por ${monto} ha sido NEGADO debido a {registro.observacion}
        
        Si necesita ayuda personalizada, contáctese con un asesor a través del siguiente enlace: https://wa.link/7v6pcn
        
        Atentamente,
        
        Cooperativa San José de Vittoria – Crédito Pagos
    """
    html_content = f"""
                <html>
                    <body>
                        <h1>Pago a proveedores – Crédito Pagos</h1>
                        <br>
                        <h3><b>Lo sentimos</b></h3>
                        <br>
                        <p>Su pago a proveedores por ${monto} ha sido NEGADO debido a {registro.observacion}</p>
                        <br>
                        <br>
                        <p>
                        Si necesita ayuda personalizada, contáctese con un asesor a través del siguiente enlace: https://wa.link/7v6pcn
                        </p>
                        <br>
                        Atentamente,
                        <br>
                        Global RedPyme – Crédito Pagos
                        <br>
                    </body>
                </html>
                """
    sendEmail(subject, txt_content, from_email, to, html_content)


def enviarProcesandoPago(email, monto, registro):
    """
    Este metodo sirve para enviar el correo de pago negado
    @type registro: El campo registro recibe la insercion de la fila
    @type monto: El campo monto recibe el monto
    @type email: El campo email recibe el email
    @rtype: Devuelve verdadero o falso del envio de correo
    """
    subject, from_email, to = 'Transferencia exitosa', "08d77fe1da-d09822@inbox.mailtrap.io", \
                              email
    txt_content = f"""
        Pago a proveedores – Crédito Pagos
        
        FELICIDADES!!
        
        Usted acaba de realizar un pago a su proveedor por ${monto}. A continuación le mostramos un resumen de su pago:

        Número de comprobante de transferencia: {registro.numeroComprobante}
        Fecha de transferencia: {registro.fechaProceso}
        Nombre del proveedor: {registro.nombreProveedor}
        Numero de RUC del proveedor: {registro.rucProveedor}
        Monto pagado: ${monto}
        Número de cuenta del proveedor: {registro.numeroCuenta}
        Banco destino: {registro.banco}
        Estado: APROBADO
                            
        Atentamente,
        
        Cooperativa San José de Vittoria – Crédito Pagos 
    """
    html_content = f"""
                <html>
                    <body>
                        <h1>Pago a proveedores – Crédito Pagos</h1>
                        <br>
                        <h3><b>FELICIDADES!!</b></h3>
                        <br>
                        <p>Usted acaba de realizar un pago a su proveedor por ${monto}. A continuación le mostramos un resumen de su pago:</p>
                        <br>
                        Número de comprobante de transferencia: {registro.numeroComprobante}
                        Fecha de transferencia: {registro.fechaProceso}
                        Nombre del proveedor: {registro.nombreProveedor}
                        Numero de RUC del proveedor: {registro.rucProveedor}
                        Monto pagado: ${monto}
                        Número de cuenta del proveedor: {registro.numeroCuenta}
                        Banco destino: {registro.banco}
                        Estado: APROBADO
                        <br>
                        Atentamente,
                        <br>
                        Cooperativa San José de Vittoria – Crédito Pagos
                        <br>
                    </body>
                </html>
                """
    sendEmail(subject, txt_content, from_email, to, html_content)


def generarPDF(datos):
    """
    Este metodo sirve para generar un pdf
    @type datos: El campo datos no recibe nada
    @rtype: DEvuelve el documento pdf
    """
    # save FPDF() class into a
    # variable pdf
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size=15)

    # create a cell
    pdf.cell(200, 10, txt="GeeksforGeeks",
             ln=1, align='C')

    # add another cell
    pdf.cell(200, 10, txt="A Computer Science portal for geeks.",
             ln=2, align='C')

    return pdf
