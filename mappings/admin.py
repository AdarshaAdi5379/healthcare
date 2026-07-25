from django.contrib import admin
from .models import Mapping


class MappingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'assigned_by', 'assigned_at')
    list_filter = ('assigned_at',)
    search_fields = ('patient__name', 'doctor__name')


admin.site.register(Mapping, MappingAdmin)
