from django.urls import path
from .views import (
    autorizacion_create,
    autorizacion_list,
    autorizacion_listOne,
    autorizacion_update,
    autorizacion_delete
)

# Esta variable se utiliza para colocar el nombre aplicacion de corp_autorizaciones
app_name = 'corp_autorizaciones'

# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    path('create/', autorizacion_create, name="autorizacion_create"),
    path('list/', autorizacion_list, name="autorizacion_list"),
    path('listOne/<str:pk>', autorizacion_listOne, name="autorizacion_listOne"),
    path('update/<str:pk>', autorizacion_update, name="autorizacion_update"),
    path('delete/<str:pk>', autorizacion_delete, name="autorizacion_delete"),
]
