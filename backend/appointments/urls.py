from django.urls import path
from .views import *

urlpatterns = [
    path('appointments/', create_appointment, name='create_appointment'),
    path('appointments/<int:appointment_id>/', get_appointment, name='get_appointment'),
]