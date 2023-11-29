from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from .views import (
    rol_list,
    rol_listExport,
    rol_create,
    rol_findOne,
    rol_update,
    rol_delete,
    rol_listFiltro,
    rol_listAccionPadre,
    rol_createUsuario,
    rol_listUsuario
)

# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    path('list/', rol_list, name="rol_list"),
    path('list/export/', rol_listExport, name="rol_listExport"),
    path('create/', rol_create, name="rol_create"),
    path('listOne/<str:pk>', rol_findOne, name="rol_findOne"),
    path('update/<str:pk>', rol_update, name="rol_update"),
    path('delete/<str:pk>', rol_delete, name="rol_delete"),
    path('list/filtro/', rol_listFiltro, name="listFiltro"),
    path('list/padres/', rol_listAccionPadre, name="listFiltro"),
    path('usuario/create/', rol_createUsuario, name="rol_createUsuario"),
    path('usuario/list/<str:pk>', rol_listUsuario, name="rol_listUsuario"),
]
