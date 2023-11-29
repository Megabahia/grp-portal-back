from django.urls import path, include
from .views import (
    rucPersonas_create,
    rucPersonas_listOne,
    rucPersonas_update,
    rucPersonas_delete,
    rucPersonas_list,
)

# Esta variable se utiliza para colocar el nombre aplicacion de facturas
app_name = 'personas_rucPersonas'
# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    path('create/', rucPersonas_create, name="rucPersonas_create"),
    path('list/', rucPersonas_list, name="rucPersonas_list"),
    path('listOne/<str:pk>', rucPersonas_listOne, name="rucPersonas_listOne"),
    path('update/<str:pk>', rucPersonas_update, name="rucPersonas_update"),
    path('delete/<str:pk>', rucPersonas_delete, name="rucPersonas_delete"),
]
