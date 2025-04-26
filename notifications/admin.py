from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient', 'notification_type', 'priority', 'is_read', 'created_at')
    list_filter = ('notification_type', 'priority', 'is_read', 'is_deleted')
    search_fields = ('title', 'message', 'recipient__username')
    date_hierarchy = 'created_at'
