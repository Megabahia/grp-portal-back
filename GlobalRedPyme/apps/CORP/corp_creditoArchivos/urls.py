from django.urls import path
from .views import (
    creditoArchivos_create,
    creditoArchivos_list,
    creditoArchivos_delete,
    uploadEXCEL_creditosPreaprobados,
    uploadEXCEL_microCreditosPreaprobados,
    uploadEXCEL_creditosPreaprobados_empleados,
    creditoArchivos_subir_documentosFirmados_create,
    creditoArchivos_ver_documentosFirmados_list,
    creditoArchivos_ver_documentosFirmados_list_todos,
    uploadEXCEL_creditosPreaprobados_negocios,
    viewEXCEL_creditosPreaprobados_negocios,
    uploadEXCEL_creditosPreaprobados_automotriz_empleados,
    uploadEXCEL_creditosPreaprobadosDigitales_empleados,
    uploadEXCEL_creditosPreaprobadosLineasCreditosDigitales_empleados,
    uploadEXCEL_creditosPreaprobadosAutomotrizDigitales_empleados,
)

# Esta variable se utiliza para colocar el nombre aplicacion de corp_creditoArchivos
app_name = 'corp_creditoArchivos'

# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    path('create/', creditoArchivos_create, name="creditoArchivos_create"),
    path('list/', creditoArchivos_list, name="creditoArchivos_list"),
    path('delete/<int:pk>', creditoArchivos_delete, name="creditoArchivos_delete"),
    path('upload/creditos/preaprobados/<int:pk>', uploadEXCEL_creditosPreaprobados,
         name="uploadEXCEL_creditosPreaprobados"),
    path('upload/microcreditos/preaprobados/<int:pk>', uploadEXCEL_microCreditosPreaprobados,
         name="uploadEXCEL_creditosPreaprobados"),
    path('upload/creditos/preaprobados/empleados/<int:pk>', uploadEXCEL_creditosPreaprobados_empleados,
         name="uploadEXCEL_creditosPreaprobados_empleados"),
    path('subir/documentosFirmados/', creditoArchivos_subir_documentosFirmados_create,
         name="creditoArchivos_subir_documentosFirmados_create"),
    path('documentosFirmados/listar/', creditoArchivos_ver_documentosFirmados_list,
         name="creditoArchivos_ver_documentosFirmados_list"),
    path('documentosFirmados/listar/todos', creditoArchivos_ver_documentosFirmados_list_todos,
         name="creditoArchivos_ver_documentosFirmados_list_todos"),
    path('upload/creditos/preaprobados/negocios/<int:pk>', uploadEXCEL_creditosPreaprobados_negocios,
         name="uploadEXCEL_creditosPreaprobados_negocios"),
    path('view/creditos/preaprobados/negocios/<int:pk>', viewEXCEL_creditosPreaprobados_negocios,
         name="viewEXCEL_creditosPreaprobados_negocios"),
    path('upload/creditos/preaprobados/automotriz/empleados/<int:pk>',
         uploadEXCEL_creditosPreaprobados_automotriz_empleados,
         name="uploadEXCEL_creditosPreaprobados_automotriz_empleados"),
    path('upload/creditos/preaprobadosDigitales/empleados/<int:pk>',
         uploadEXCEL_creditosPreaprobadosDigitales_empleados,
         name="uploadEXCEL_creditosPreaprobadosDigitales_empleados"),
    path('upload/creditos/preaprobadosLineasCreditosDigitales/empleados/<int:pk>',
         uploadEXCEL_creditosPreaprobadosLineasCreditosDigitales_empleados,
         name="uploadEXCEL_creditosPreaprobadosDigitales_empleados"),
    path('upload/creditos/preaprobadosAutomotrizDigitales/empleados/<int:pk>',
         uploadEXCEL_creditosPreaprobadosAutomotrizDigitales_empleados,
         name="uploadEXCEL_creditosPreaprobadosDigitales_empleados"),
]