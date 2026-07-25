from django.contrib import admin
from .models import Patient


class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'contact_number', 'created_by', 'created_at')
    list_filter = ('gender',)
    search_fields = ('name', 'contact_number')


admin.site.register(Patient, PatientAdmin)
