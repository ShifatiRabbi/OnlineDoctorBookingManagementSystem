from django.urls import path
from .views import *

urlpatterns = [
    path('daily/', daily_report, name='daily_report'),
    path('monthly/', monthly_report, name='monthly_report'),
]