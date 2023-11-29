from .models import Acciones, AccionesPermitidas, AccionesPorRol
from .serializers import AccionesSerializer, AccionesPermitidasSerializer, \
    AccionesPorRolSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone


# CRUD ACCIONES
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def acciones_list(request):
    """
    Este metodo sirve para obtener una lista
    @type request: El campo request no recibe nada
    @rtype: DEvuelve el una lista encontrado, caso contrario devuelve el error generado
    """
    if request.method == 'GET':
        acciones = Acciones.objects.filter(idAccionPadre__isnull=False, state=1)
        serializer = AccionesSerializer(acciones, many=True)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CREAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def acciones_create(request):
    """
    Este metodo sirve para crear un registro
    @type request: El campo request recibe los campos de la tabla
    @rtype: DEvuelve el registro creado, caso contrario devuelve el error generado
    """
    now = timezone.localtime(timezone.now())
    request.data['created_at'] = str(now)
    if 'updated_at' in request.data:
        request.data.pop('updated_at')
    if request.method == 'POST':
        serializer = AccionesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ENCONTRAR UNO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def acciones_findOne(request, pk):
    """
    Este metodo sirve para obtener un registro
    @type pk: El campo pk recibe el id
    @type request: El campo request no recibe nada
    @rtype: DEvuelve el registro encontrado, caso contrario devuelve el error generado
    """
    try:
        acciones = Acciones.objects.get(pk=pk, state=1)
    except Acciones.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # tomar el dato
    if request.method == 'GET':
        serializer = AccionesSerializer(acciones)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ACTUALIZAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def acciones_update(request, pk):
    """
    Este metodo sirve para actualizar
    @type pk: El campo pk recibe el id
    @type request: El campo request recibe el campo de la tabla accionesporrol
    @rtype: DEvuelve el registro actualizado, caso contrario devuelve el errr generado
    """
    try:
        acciones = Acciones.objects.get(pk=pk, state=1)
    except Acciones.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # tomar el dato
    if request.method == 'POST':
        now = timezone.localtime(timezone.now())
        request.data['updated_at'] = str(now)
        if 'created_at' in request.data:
            request.data.pop('created_at')
        serializer = AccionesSerializer(acciones, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ELIMINAR
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def acciones_delete(request, pk):
    """
    Este metodo sirve para obtener un registro
    @type pk: El campo pk recibe el id
    @type request: El campo request no recibe nada
    @rtype: DEvuelve el registro encontrado, caso contrario devuelve el error generado
    """
    try:
        acciones = Acciones.objects.get(pk=pk, state=1)
    except Acciones.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # tomar el dato
    if request.method == 'DELETE':
        now = timezone.localtime(timezone.now())
        serializer = AccionesSerializer(acciones, data={'state': '0', 'updated_at': str(now)}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CRUD ACCIONESPermitidas
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accionesPermitidas_list(request):
    """
    Este metodo sirve para obtener una lista
    @type request: El campo request no recibe nada
    @rtype: DEvuelve el una lista encontrado, caso contrario devuelve el error generado
    """
    if request.method == 'GET':
        accionesPermitidas = AccionesPermitidas.objects.filter(state=1)
        serializer = AccionesPermitidasSerializer(accionesPermitidas, many=True)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CREAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accionesPermitidas_create(request):
    """
    Este metodo sirve para crear un registro
    @type request: El campo request recibe los campos de la tabla
    @rtype: DEvuelve el registro creado, caso contrario devuelve el error generado
    """
    if request.method == 'POST':
        now = timezone.localtime(timezone.now())
        request.data['created_at'] = str(now)
        if 'updated_at' in request.data:
            request.data.pop('updated_at')
        serializer = AccionesPermitidasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ENCONTRAR UNO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accionesPermitidas_findOne(request, pk):
    """
    Este metodo sirve para obtener un registro
    @type pk: El campo pk recibe el id
    @type request: El campo request no recibe nada
    @rtype: DEvuelve el registro encontrado, caso contrario devuelve el error generado
    """
    try:
        acciones = AccionesPermitidas.objects.get(pk=pk, state=1)
    except AccionesPermitidas.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # tomar el dato
    if request.method == 'GET':
        serializer = AccionesPermitidasSerializer(accionesPermitidas)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ACTUALIZAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accionesPermitidas_update(request, pk):
    """
    Este metodo sirve para actualizar
    @type pk: El campo pk recibe el id
    @type request: El campo request recibe el campo de la tabla accionesporrol
    @rtype: DEvuelve el registro actualizado, caso contrario devuelve el errr generado
    """
    try:
        accionesPermitidas = AccionesPermitidas.objects.get(pk=pk, state=1)
    except AccionesPermitidas.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # tomar el dato
    if request.method == 'POST':
        now = timezone.localtime(timezone.now())
        request.data['updated_at'] = str(now)
        if 'created_at' in request.data:
            request.data.pop('created_at')
        serializer = AccionesPermitidasSerializer(accionesPermitidas, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ELIMINAR
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def accionesPermitidas_delete(request, pk):
    """
    Este metodo sirve para obtener un registro
    @type pk: El campo pk recibe el id
    @type request: El campo request no recibe nada
    @rtype: DEvuelve el registro encontrado, caso contrario devuelve el error generado
    """
    try:
        accionesPermitidas = AccionesPermitidas.objects.get(pk=pk, state=1)
    except AccionesPermitidas.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # tomar el dato
    if request.method == 'DELETE':
        now = timezone.localtime(timezone.now())
        serializer = AccionesPermitidasSerializer(accionesPermitidas, data={'state': '0', 'updated_at': str(now)},
                                                  partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CRUD AccionesPorRol
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accionesPorRol_list(request):
    """
    Este metodo sirve para obtener una lista
    @type request: El campo request no recibe nada
    @rtype: DEvuelve el una lista encontrado, caso contrario devuelve el error generado
    """
    if request.method == 'GET':
        accionesPorRol = AccionesPorRol.objects.filter(state=1)
        serializer = AccionesPorRolSerializer(accionesPorRol, many=True)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CREAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accionesPorRol_create(request):
    """
    Este metodo sirve para crear un registro
    @type request: El campo request recibe los campos de la tabla
    @rtype: DEvuelve el registro creado, caso contrario devuelve el error generado
    """
    if request.method == 'POST':
        now = timezone.localtime(timezone.now())
        request.data['created_at'] = str(now)
        if 'updated_at' in request.data:
            request.data.pop('updated_at')
        serializer = AccionesPorRolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ENCONTRAR UNO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accionesPorRol_findOne(request, pk):
    """
    Este metodo sirve para obtener un registro
    @type pk: El campo pk recibe el id
    @type request: El campo request no recibe nada
    @rtype: DEvuelve el registro encontrado, caso contrario devuelve el error generado
    """
    try:
        acciones = AccionesPorRol.objects.get(pk=pk, state=1)
    except AccionesPorRol.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # tomar el dato
    if request.method == 'GET':
        serializer = AccionesPorRolSerializer(accionesPorRol)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ACTUALIZAR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accionesPorRol_update(request, pk):
    """
    Este metodo sirve para actualizar
    @type pk: El campo pk recibe el id
    @type request: El campo request recibe el campo de la tabla accionesporrol
    @rtype: DEvuelve el registro actualizado, caso contrario devuelve el errr generado
    """
    try:
        accionesPorRol = AccionesPorRol.objects.get(pk=pk, state=1)
    except AccionesPorRol.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # tomar el dato
    if request.method == 'POST':
        now = timezone.localtime(timezone.now())
        request.data['updated_at'] = str(now)
        if 'created_at' in request.data:
            request.data.pop('created_at')
        serializer = AccionesPorRolSerializer(accionesPorRol, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ELIMINAR
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def accionesPorRol_delete(request, pk):
    """
    Este metodo sirve para eliminar
    @type pk: El campo pk recibe el id
    @type request: El campo request no recibe nada
    @rtype: DEvuelve el registro eliminado, caso contrario
    """
    try:
        accionesPorRol = AccionesPorRol.objects.get(pk=pk, state=1)
    except AccionesPorRol.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # tomar el dato
    if request.method == 'DELETE':
        now = timezone.localtime(timezone.now())
        serializer = AccionesPorRolSerializer(accionesPorRol, data={'state': '0', 'updated_at': str(now)}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
