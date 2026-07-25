from django.contrib import admin
from .models import Doctor


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'email', 'contact_number', 'experience')
    list_filter = ('specialization', 'created_at')
    search_fields = ('name', 'specialization', 'email')
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


admin.site.register(Doctor, DoctorAdmin)
