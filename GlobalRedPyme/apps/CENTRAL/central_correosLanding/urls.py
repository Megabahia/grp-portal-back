from django.urls import path, include
from .views import (
    correos_create,
    correos_list,
    correos_update,
)

# el campo app_name se utiliza para hacer referencia a las rutas que sera configuradas en el archivo settings
app_name = 'central_correosLanding'

# la variabla urlpatterns contiene todas las rutas del modulo de correos landing
urlpatterns = [
    path('create/', correos_create, name="correos_create"),
    path('list/', correos_list, name="correos_list"),
    path('update/<str:pk>', correos_update, name="correos_update"),
]
