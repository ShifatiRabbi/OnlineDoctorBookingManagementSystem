from django.db import models
from branches.models import Branch
from accounts.models import User

class Specialty(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    degrees = models.CharField(max_length=200)
    specialties = models.ManyToManyField(Specialty)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    default_branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"

class DoctorSchedule(models.Model):
    WEEKDAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_duration = models.IntegerField(help_text="Duration in minutes")  # e.g., 15, 30
    capacity = models.IntegerField(default=1, help_text="Number of patients per slot")
    
    class Meta:
        unique_together = ('doctor', 'branch', 'weekday')
    
    def __str__(self):
        return f"{self.doctor} at {self.branch} on {self.get_weekday_display()}"

class TimeSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.IntegerField(default=1)
    booked_count = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('doctor', 'branch', 'date', 'start_time')
    
    def __str__(self):
        return f"{self.doctor} - {self.date} {self.start_time}"

class DoctorSignature(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)
    image_url = models.URLField()
    
    def __str__(self):
        return f"Signature of {self.doctor}"