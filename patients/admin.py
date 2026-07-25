from django.contrib import admin
from .models import Patient


class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'contact_number', 'created_by', 'created_at')
    list_filter = ('gender', 'created_at')
    search_fields = ('name', 'contact_number')
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


admin.site.register(Patient, PatientAdmin)
