from django.contrib import admin
from .models import SiteSetting

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value_type', 'is_public', 'updated_at')
    list_filter = ('value_type', 'is_public')
    search_fields = ('key', 'value', 'description')
    fieldsets = (
        (None, {
            'fields': ('key', 'value', 'value_type', 'description', 'is_public')
        }),
    )
