from django.db import models
from appointments.models import Appointment
from doctors.models import Doctor
from patients.models import Patient
from branches.models import Branch

class Medicine(models.Model):
    FORM_CHOICES = (
        ('TAB', 'Tablet'),
        ('CAP', 'Capsule'),
        ('SYR', 'Syrup'),
        ('INI', 'Injection'),
        ('OIN', 'Ointment'),
        ('DRP', 'Drops'),
    )
    
    name = models.CharField(max_length=100)
    generic = models.CharField(max_length=100, blank=True)
    strength = models.CharField(max_length=50, blank=True)
    form = models.CharField(max_length=3, choices=FORM_CHOICES, blank=True)
    
    def __str__(self):
        return self.name

class Test(models.Model):
    CATEGORY_CHOICES = (
        ('BLOOD', 'Blood Test'),
        ('URINE', 'Urine Test'),
        ('IMAGING', 'Imaging'),
        ('ECG', 'ECG'),
        ('OTHER', 'Other'),
    )
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='OTHER')
    
    def __str__(self):
        return self.name

class PrescriptionTemplate(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    header_blocks = models.JSONField(default=list)
    footer_blocks = models.JSONField(default=list)
    sign_placeholders = models.JSONField(default=dict)
    
    def __str__(self):
        if self.doctor:
            return f"Template for {self.doctor} at {self.branch}"
        return f"Default template for {self.branch}"

class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    items = models.JSONField()  # List of medicine objects with dosage, duration, etc.
    tests = models.JSONField()  # List of test objects
    advice = models.TextField(blank=True)
    printable_key = models.CharField(max_length=32, unique=True)  # For secure PDF access
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Prescription for {self.patient} by {self.doctor}"