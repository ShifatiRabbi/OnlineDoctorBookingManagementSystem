from django.db import models

class Patient(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, db_index=True)
    address = models.TextField(blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    
    def __str__(self):
        return self.name