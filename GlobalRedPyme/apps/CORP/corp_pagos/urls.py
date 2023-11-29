from django.urls import path, include
from .views import (
    pagos_create,
    pagos_listOne,
    pagos_update,
    pagos_delete,
    pagos_list,
    consumirCola,
)

# Esta variable se utiliza para colocar el nombre aplicacion de facturas
app_name = 'corp_pagos'

# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    path('create/', pagos_create, name="pagos_create"),
    path('list/', pagos_list, name="pagos_list"),
    path('listOne/<str:pk>', pagos_listOne, name="pagos_listOne"),
    path('update/<str:pk>', pagos_update, name="pagos_update"),
    path('delete/<str:pk>', pagos_delete, name="pagos_delete"),
    path('consumirCola', consumirCola, name="consumirCola"),
]
