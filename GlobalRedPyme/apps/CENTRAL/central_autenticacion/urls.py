from django.urls import path,include
from apps.CENTRAL.central_autenticacion.views import(
	login
	
)

app_name = 'autenticacion'

urlpatterns = [
	path('login/', login.as_view(), name="login"), # -> see accounts/api/views.py for response and url info
]

