from django.db import models

class ReportCache(models.Model):
    aggregation_key = models.CharField(max_length=100, unique=True)
    json_data = models.JSONField()
    period = models.CharField(max_length=20)  # daily, weekly, monthly, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.aggregation_key