from django.urls import path, include
from .views import (
    facturas_create,
    facturas_list,
    facturas_listOne,
    facturas_update,
    facturas_delete,
    facturas_subirArchivo,
)

# Esta variable se utiliza para colocar el nombre aplicacion de facturas
app_name = 'central_facturas'

# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    path('subir/factura/', facturas_subirArchivo, name="facturas_subirArchivo"),
    path('create/', facturas_create, name="facturas_create"),
    path('list/', facturas_list, name="facturas_list"),
    path('listOne/<str:pk>', facturas_listOne, name="facturas_listOne"),
    path('update/<str:pk>', facturas_update, name="facturas_update"),
    path('delete/<str:pk>', facturas_delete, name="facturas_delete"),
]
