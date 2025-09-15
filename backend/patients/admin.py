from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'gender')
    list_filter = ('gender',)
    search_fields = ('name', 'phone')