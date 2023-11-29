from django.urls import path, include
from .views import (
    acciones_list, acciones_create, acciones_findOne, acciones_update, acciones_delete,
    accionesPermitidas_list, accionesPermitidas_create, accionesPermitidas_findOne, accionesPermitidas_update,
    accionesPermitidas_delete,
    accionesPorRol_list, accionesPorRol_create, accionesPorRol_findOne, accionesPorRol_update, accionesPorRol_delete,

)

# Esta variable se utiliza para colocar el nombre aplicacion de acciones
app_name = 'acciones'

# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    # acciones
    path('list/', acciones_list, name="acciones_list"),
    path('create', acciones_create, name="acciones_create"),
    path('findOne/<int:pk>', acciones_findOne, name="acciones_findOne"),
    path('update/<int:pk>', acciones_update, name="acciones_update"),
    path('delete/<int:pk>', acciones_delete, name="acciones_delete"),
    # accionesPermitidas
    path('accionesPermitidas/list', accionesPermitidas_list, name="accionesPermitidas_list"),
    path('accionesPermitidas/create', accionesPermitidas_create, name="accionesPermitidas_create"),
    path('accionesPermitidas/findOne/<int:pk>', accionesPermitidas_findOne, name="accionesPermitidas_findOne"),
    path('accionesPermitidas/update/<int:pk>', accionesPermitidas_update, name="accionesPermitidas_update"),
    path('accionesPermitidas/delete/<int:pk>', accionesPermitidas_delete, name="accionesPermitidas_delete"),
    # accionesporRol
    path('accionesPorRol/list', accionesPorRol_list, name="accionesPorRol_list"),
    path('accionesPorRol/create', accionesPorRol_create, name="accionesPorRol_create"),
    path('accionesPorRol/findOne/<int:pk>', accionesPorRol_findOne, name="accionesPorRol_findOne"),
    path('accionesPorRol/update/<int:pk>', accionesPorRol_update, name="accionesPorRol_update"),
    path('accionesPorRol/delete/<int:pk>', accionesPorRol_delete, name="accionesPorRol_delete"),

]
