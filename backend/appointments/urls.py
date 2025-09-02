from django.urls import path
from .views import *

urlpatterns = [
    path('new_appointments/', create_appointment, name='create_appointment'),
    path('appointments/<int:appointment_id>/', get_appointment, name='get_appointment'),
]