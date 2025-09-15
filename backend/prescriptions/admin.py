from django.contrib import admin
from .models import Prescription, PrescriptionTemplate, Medicine, Test

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'generic', 'strength', 'form')
    search_fields = ('name', 'generic')

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(PrescriptionTemplate)
class PrescriptionTemplateAdmin(admin.ModelAdmin):
    list_display = ('branch', 'doctor')
    list_filter = ('branch',)

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'created_at')
    list_filter = ('created_at', 'doctor')
    search_fields = ('patient__name', 'doctor__user__first_name', 'doctor__user__last_name')