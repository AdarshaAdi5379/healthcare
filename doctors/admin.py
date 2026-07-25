from django.contrib import admin
from .models import Doctor


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'email', 'contact_number', 'experience')
    list_filter = ('specialization',)
    search_fields = ('name', 'specialization', 'email')


admin.site.register(Doctor, DoctorAdmin)
