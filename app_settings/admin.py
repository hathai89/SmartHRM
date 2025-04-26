from django.contrib import admin
from .models import SiteSetting

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('key', 'value', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('key', 'value', 'description', 'is_active')
        }),
        ('Thông tin thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
