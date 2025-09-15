from django.urls import path
from .views import *

urlpatterns = [
    path('logs/', get_audit_logs, name='get_audit_logs'),
]