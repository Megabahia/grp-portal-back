from apps.CENTRAL.central_logs.serializers import LogsSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import json
from apps.CENTRAL.central_catalogo.models import Catalogo
#crea el log en la base de datos
def saveLog(logModel):
    try:
        logModel['fechaFin']=str(timezone.localtime(timezone.now()))
        serializer = LogsSerializer(data=logModel,partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        return Response(err,status=status.HTTP_400_BAD_REQUEST)
#ingresa los datos del log
def createLog(logModel,logRecibida,logTransaccion):
    try:
        if logRecibida:
            logModel['dataRecibida']=str(logRecibida)
        if logTransaccion:
            logModel['tipo']=str(logTransaccion)
        #VERIFICA EL PERMISO TOMA DEL CATALOGO
        try:
            permiso=Catalogo.objects.filter(tipo='LOG'+str(logModel['tipo']),nombre=str(logModel['accion']),state=1).only('valor').first()
        except Catalogo.DoesNotExist:
            err={'error':'No existe la configuracion de permisos'}
            return Response(err,status=status.HTTP_404_NOT_FOUND)
        if permiso.valor=='1':
            saveLog(logModel)
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        return Response(err,status=status.HTTP_400_BAD_REQUEST)
#TIPOS DE LOG
def datosTipoLog():
    data={
        'excepcion':'EXCEPCIONES',
        'transaccion':'TRANSACCIONES'
    }
    return data
#MODULO ADM-AUTH
def datosAuth():
    data={
        'modulo':'ADM',
        'api':'auth/'
    }
    return data
#MODULO ADM-USUARIOS
def datosUsuarios():
    data={
        'modulo':'ADM',
        'api':'usuarios/'
    }
    return data
#MODULO ADM-ROLES
def datosRoles():
    data={
        'modulo':'ADM',
        'api':'roles/'
    }
    return data
#MODULO ADM-ACCIONES
def datosAcciones():
    data={
        'modulo':'ADM',
        'api':'acciones/'
    }
#MODULO ADM-CATALOGO
def datosCatalogo():
    data={
        'modulo':'ADM',
        'api':'param/'
    }
    return data  
#MODULO MDM-PARAMETRIZACIONES
def datosParametrizaciones():
    data={
        'modulo':'MDM',
        'api':'param/'
    }
    return data  
#MODULO MDM-CLIENTES
def datosClientes():
    data={
        'modulo':'MDM',
        'api':'clientes/'
    }
    return data  
#MODULO MDM-PROSPECTOS-CLIENTES
def datosProspectosClientes():
    data={
        'modulo':'MDM',
        'api':'prospectosClientes/'
    }
    return data  
#MODULO MDM-NEGOCIOS
def datosNegocios():
    data={
        'modulo':'MDM',
        'api':'negocios/'
    }
    return data  
#MODULO MDM-FACTURAS
def datosFacturas():
    data={
        'modulo':'MDM',
        'api':'facturas/'
    }
    return data  
#MODULO MDP-PARAMETRIZACIONES
def datosParametrizacionesMDP():
    data={
        'modulo':'MDP',
        'api':'param/'
    }
    return data  

#MODULO MDP-CATEGORIAS
def datosCategoriasMDP():
    data={
        'modulo':'MDP',
        'api':'categorias/'
    }
    return data  

#MODULO MDP-SUBCATEGORIAS
def datosSubCategoriasMDP():
    data={
        'modulo':'MDP',
        'api':'subCategorias/'
    }
    return data  

#MODULO MDP-PRODUCTOS
def datosProductosMDP():
    data={
        'modulo':'MDP',
        'api':'productos/'
    }
    return data  

#MODULO MDP-FICHA TECNICA PRODUCTOS
def datosFichaTecnicaProductosMDP():
    data={
        'modulo':'MDP',
        'api':'fichaTecnicaProductos/'
    }
    return data  

#MODULO MDO-PARAMETRIZACIONES
def datosParametrizacionesMDO():
    data={
        'modulo':'MDO',
        'api':'parametrizaciones/'
    }
    return data  

#MODULO MDO-PARAMETRIZACIONES
def datosPrediccionCrosselingMDO():
    data={
        'modulo':'MDO',
        'api':'prediccionCrosseling/'
    }
    return data  

#MODULO MDO-PARAMETRIZACIONES
def datosPrediccionProductosNuevosMDO():
    data={
        'modulo':'MDO',
        'api':'prediccionProductosNuevos/'
    }
    return data  

#MODULO MDO-PARAMETRIZACIONES
def datosParametrizacionesGDO():
    data={
        'modulo':'GDO',
        'api':'parametrizaciones/'
    }
    return data  

#MODULO MDO-PARAMETRIZACIONES
def datosGestionOfertaGDO():
    data={
        'modulo':'GDO',
        'api':'gestionOferta/'
    }
    return data  

#MODULO MDO-PARAMETRIZACIONES
def datosParametrizacionesGDE():
    data={
        'modulo':'GDE',
        'api':'parametrizaciones/'
    }
    return data  

#MODULO MDO-PARAMETRIZACIONES
def datosGestionEntregaGDE():
    data={
        'modulo':'GDE',
        'api':'gestionEntrega/'
    }
    return data  
