from rest_framework import serializers
from notifications.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    recipient_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'message', 'recipient', 'recipient_name', 
            'notification_type', 'priority', 'is_read', 'requires_action',
            'action_url', 'action_text', 'created_at'
        ]
    
    def get_recipient_name(self, obj):
        return obj.recipient.get_full_name() if obj.recipient else None
