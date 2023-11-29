from django.urls import path
from .views import (
    pagoEmpleados_list,
    uploadEXCEL_pagosEmpleados,
    pagoEmpleados_update,
    firmar
)

# Esta variable se utiliza para colocar el nombre aplicacion de corp_pagoEmpleados
app_name = 'corp_pagoEmpleados'

# La variable urlpatterns se utiliza para exportar las diferentes rutas a las que pueden acceder el front
urlpatterns = [
    path('list/', pagoEmpleados_list, name="pagoEmpleados_list"),
    path('upload/', uploadEXCEL_pagosEmpleados, name="uploadEXCEL_pagosEmpleados"),
    path('update/<str:pk>', pagoEmpleados_update, name="pagoEmpleados_update"),
    path('firmar/', firmar, name="firmar"),
]
