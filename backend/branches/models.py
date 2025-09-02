from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    address = models.TextField()
    phones = models.CharField(max_length=100)  # Comma-separated phone numbers
    theme_config = models.JSONField(default=dict)  # For UI customization
    prescription_format = models.JSONField(default=dict)  # For prescription template
    
    def __str__(self):
        return self.name