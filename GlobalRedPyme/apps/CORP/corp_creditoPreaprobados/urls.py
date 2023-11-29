from django.urls import path
from .views import (
    creditoPreaprobados_create,
    creditoPreaprobados_list,
    creditoPreaprobados_listOne,
    creditoPreaprobados_update,
    creditoPreaprobados_delete,
    creditoPreaprobados_list_corp,
    creditoPreaprobados_list_ifis,
    uploadEXCEL_creditosPreaprobados,
)

# Esta variable se utiliza para colocar el nombre aplicacion de corp_creditoPreaprobados
app_name = 'corp_creditoPreaprobados'

# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    path('create/', creditoPreaprobados_create, name="creditoPreaprobados_create"),
    path('list/', creditoPreaprobados_list, name="creditoPreaprobados_list"),
    path('list/corp/', creditoPreaprobados_list_corp, name="creditoPreaprobados_list_corp"),
    path('list/ifis/', creditoPreaprobados_list_ifis, name="creditoPreaprobados_list_ifis"),
    path('listOne/<str:pk>', creditoPreaprobados_listOne, name="creditoPreaprobados_listOne"),
    path('update/<str:pk>', creditoPreaprobados_update, name="creditoPreaprobados_update"),
    path('delete/<str:pk>', creditoPreaprobados_delete, name="creditoPreaprobados_delete"),
    path('upload/creditos/preaprobados/', uploadEXCEL_creditosPreaprobados, name="uploadEXCEL_creditosPreaprobados"),
]
