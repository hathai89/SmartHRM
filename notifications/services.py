from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from .models import Notification
from django.utils import timezone

def create_notification(recipient, title, message, notification_type='system', 
                       priority='normal', sender=None, link=None, related_object=None,
                       display_type='toast', requires_action=False, action_url=None, 
                       action_text=None, expires_at=None):
    """
    Tạo thông báo mới và gửi qua WebSocket
    
    Args:
        recipient: User object - người nhận thông báo
        title: Tiêu đề thông báo
        message: Nội dung thông báo
        notification_type: Loại thông báo (system, document, task, message, approval, other)
        priority: Mức độ ưu tiên (low, normal, high, urgent)
        sender: User object - người gửi thông báo (có thể None)
        link: Đường dẫn khi click vào thông báo
        related_object: Đối tượng liên quan đến thông báo
        display_type: Kiểu hiển thị (popup, toast, badge, email, sms)
        requires_action: Có yêu cầu hành động không
        action_url: URL khi click vào nút hành động
        action_text: Nội dung nút hành động
        expires_at: Thời gian hết hạn thông báo
        
    Returns:
        Notification object
    """
    # Tạo thông báo mới
    notification = Notification(
        recipient=recipient,
        sender=sender,
        title=title,
        message=message,
        notification_type=notification_type,
        priority=priority,
        link=link,
        display_type=display_type,
        requires_action=requires_action,
        action_url=action_url or link,
        action_text=action_text,
        expires_at=expires_at
    )
    
    # Nếu có đối tượng liên quan
    if related_object:
        content_type = ContentType.objects.get_for_model(related_object)
        notification.content_type = content_type
        notification.object_id = related_object.id
    
    # Lưu thông báo
    notification.save()
    
    # Gửi thông báo qua WebSocket
    channel_layer = get_channel_layer()
    notification_group_name = f'notifications_{recipient.id}'
    
    # Chuẩn bị dữ liệu để gửi
    notification_data = {
        'id': notification.id,
        'title': notification.title,
        'message': notification.message,
        'type': notification.notification_type,
        'priority': notification.priority,
        'link': notification.link,
        'created_at': notification.created_at.isoformat(),
        'display_type': notification.display_type,
        'requires_action': notification.requires_action,
        'action_url': notification.action_url,
        'action_text': notification.action_text,
    }
    
    # Gửi thông báo
    try:
        async_to_sync(channel_layer.group_send)(
            notification_group_name,
            {
                'type': 'notification_message',
                'message': notification_data
            }
        )
        
        # Cập nhật số lượng thông báo chưa đọc
        unread_count = Notification.objects.filter(
            recipient=recipient,
            is_read=False,
            is_deleted=False
        ).count()
        
        async_to_sync(channel_layer.group_send)(
            notification_group_name,
            {
                'type': 'notification_message',
                'unread_count': unread_count
            }
        )
    except Exception as e:
        # Ghi log lỗi nếu cần
        print(f"Error sending notification: {str(e)}")
    
    return notification
