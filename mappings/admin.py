from django.contrib import admin
from .models import Mapping


class MappingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'assigned_by', 'assigned_at')
    list_filter = ('assigned_at',)
    search_fields = ('patient__name', 'doctor__name')
    date_hierarchy = 'assigned_at'
    ordering = ['-assigned_at']


admin.site.register(Mapping, MappingAdmin)
