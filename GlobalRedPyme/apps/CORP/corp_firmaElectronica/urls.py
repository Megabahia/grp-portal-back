from django.urls import path
from .views import (
    firmaElectronica_create,
    firmaElectronica_list,
)

# Esta variable se utiliza para colocar el nombre aplicacion de facturas
app_name = 'corp_monedasEmpresa'

# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    path('create/', firmaElectronica_create, name="firmaElectronica_create"),
    path('list/', firmaElectronica_list, name="firmaElectronica_list"),
]
