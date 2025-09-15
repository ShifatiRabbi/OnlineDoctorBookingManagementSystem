from django.urls import path
from .views import *

urlpatterns = [
    path('send/', send_sms, name='send_sms'),
    path('history/', get_sms_history, name='get_sms_history'),
]