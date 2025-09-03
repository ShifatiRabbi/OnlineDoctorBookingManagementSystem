from django.urls import path
from .views import *

urlpatterns = [
    path('prescriptions/', create_prescription, name='create_prescription'),
    path('prescriptions/<int:prescription_id>/', get_prescription, name='get_prescription'),
    path('patients/<int:patient_id>/prescriptions/', get_patient_prescriptions, name='get_patient_prescriptions'),
    path('medicines/', list_medicines, name='list_medicines'),
    path('tests/', list_tests, name='list_tests'),
]