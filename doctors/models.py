from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    contact_number = models.CharField(max_length=15)
    experience = models.IntegerField(default=0)
    available_from = models.TimeField(null=True, blank=True)
    available_to = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Dr. {self.name} ({self.specialization})'
