from django.urls import path
from .views import *

urlpatterns = [
    path('patients/', create_patient, name='create_patient'),
    path('patients/search/', search_patients, name='search_patients'),
    path('patients/<int:patient_id>/', update_patient, name='update_patient'),
    path('patients/<int:patient_id>/details/', get_patient, name='get_patient'),
]