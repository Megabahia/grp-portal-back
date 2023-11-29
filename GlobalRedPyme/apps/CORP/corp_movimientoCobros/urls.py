from django.urls import path
from .views import (
    movimientoCobros_create,
    movimientoCobros_list,
    movimientoCobros_listOne,
    movimientoCobros_update,
    movimientoCobros_delete,
    list_transacciones,
)

# Esta variable se utiliza para colocar el nombre aplicacion de facturas
app_name = 'corp_movimientoCobros'

# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    path('create/', movimientoCobros_create, name="movimientoCobros_create"),
    path('list/', movimientoCobros_list, name="movimientoCobros_list"),
    path('listOne/<str:pk>', movimientoCobros_listOne, name="movimientoCobros_listOne"),
    path('update/<str:pk>', movimientoCobros_update, name="movimientoCobros_update"),
    path('delete/<str:pk>', movimientoCobros_delete, name="movimientoCobros_delete"),
    path('list/transacciones', list_transacciones, name="list_transacciones"),
]
