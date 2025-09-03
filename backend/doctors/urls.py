from django.urls import path
from .views import *

urlpatterns = [
    path('doctors/', create_doctor, name='create_doctor'),
    path('doctors/list/', list_doctors, name='list_doctors'),
    path('doctors/<int:doctor_id>/', update_doctor, name='update_doctor'),
    path('doctors/<int:doctor_id>/schedule/', create_doctor_schedule, name='create_doctor_schedule'),
    path('doctors/<int:doctor_id>/branches/<int:branch_id>/generate-slots/', generate_time_slots_view, name='generate_time_slots'),
]