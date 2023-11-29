from django.urls import path
from .views import (
    envios_create,
    envios_list,
)

# Esta variable se utiliza para colocar el nombre aplicacion de facturas
app_name = 'corp_envios'

# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    path('create/', envios_create, name="envios_create"),
    path('list/', envios_list, name="envios_list"),
]
