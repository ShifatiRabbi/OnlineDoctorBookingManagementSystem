from django.contrib import admin
from .models import Doctor, Specialty, DoctorSchedule, TimeSlot, DoctorSignature

@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'degrees', 'fee', 'default_branch', 'active')
    list_filter = ('specialties', 'default_branch', 'active')
    filter_horizontal = ('specialties',)

@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'branch', 'weekday', 'start_time', 'end_time')
    list_filter = ('doctor', 'branch', 'weekday')

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'branch', 'date', 'start_time', 'capacity', 'booked_count')
    list_filter = ('doctor', 'branch', 'date')

@admin.register(DoctorSignature)
class DoctorSignatureAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'image_url')