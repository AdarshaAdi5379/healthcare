from django.db import models
from django.conf import settings


class Mapping(models.Model):
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='mappings',
        db_index=True
    )
    doctor = models.ForeignKey(
        'doctors.Doctor',
        on_delete=models.CASCADE,
        related_name='mappings',
        db_index=True
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_mappings',
        db_index=True
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('patient', 'doctor')
        verbose_name_plural = 'mappings'
        ordering = ['-assigned_at']

    def __str__(self):
        return f'{self.patient.name} -> Dr. {self.doctor.name}'
