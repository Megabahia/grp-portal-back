from django.urls import path
from .views import (
    monedasEmpresa_create,
    monedasEmpresa_list,
)

# Esta variable se utiliza para colocar el nombre aplicacion de facturas
app_name = 'corp_monedasEmpresa'

# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    path('create/', monedasEmpresa_create, name="monedasEmpresa_create"),
    path('list/', monedasEmpresa_list, name="monedasEmpresa_list"),
]
