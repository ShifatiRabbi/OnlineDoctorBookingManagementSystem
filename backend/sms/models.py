from django.db import models

class SMSMessage(models.Model):
    TYPE_CHOICES = (
        ('APPOINTMENT', 'Appointment'),
        ('OFFER', 'Offer'),
        ('NOTICE', 'Notice'),
        ('OTHER', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('FAILED', 'Failed'),
    )
    
    to = models.CharField(max_length=15)
    content = models.TextField()
    type = models.CharField(max_length=11, choices=TYPE_CHOICES)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='PENDING')
    provider_id = models.CharField(max_length=100, blank=True)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"SMS to {self.to} ({self.status})"