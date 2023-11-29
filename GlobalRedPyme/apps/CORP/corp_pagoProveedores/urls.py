from django.urls import path, include
from .views import (
    pagoProveedores_create,
    pagoProveedores_update,
    pagoProveedores_list,
    firmar
)

# Esta variable se utiliza para colocar el nombre aplicacion de facturas
app_name = 'corp_pagoProveedores'

# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    path('create/', pagoProveedores_create, name="pagoProveedores_create"),
    path('update/<str:pk>', pagoProveedores_update, name="pagoProveedores_update"),
    path('list/', pagoProveedores_list, name="pagoProveedores_list"),
    path('firmar/', firmar, name="firmar"),
]
