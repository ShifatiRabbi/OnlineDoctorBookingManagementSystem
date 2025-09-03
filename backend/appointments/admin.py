from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'branch', 'date', 'time', 'status')
    list_filter = ('status', 'branch', 'doctor', 'date')
    search_fields = ('patient__name', 'doctor__user__first_name', 'doctor__user__last_name')