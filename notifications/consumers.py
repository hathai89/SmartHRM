import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        
        # Kiểm tra xem người dùng đã đăng nhập chưa
        if self.user.is_anonymous:
            await self.close()
            return
        
        # Tạo tên nhóm dựa trên ID người dùng
        self.notification_group_name = f'notifications_{self.user.id}'
        
        # Tham gia nhóm
        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Gửi thông báo chưa đọc khi kết nối
        unread_count = await self.get_unread_count()
        await self.send(text_data=json.dumps({
            'type': 'unread_count',
            'count': unread_count
        }))
    
    async def disconnect(self, close_code):
        # Rời khỏi nhóm
        await self.channel_layer.group_discard(
            self.notification_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'mark_as_read':
            notification_id = data.get('notification_id')
            if notification_id:
                await self.mark_notification_as_read(notification_id)
                
                # Cập nhật số lượng thông báo chưa đọc
                unread_count = await self.get_unread_count()
                await self.send(text_data=json.dumps({
                    'type': 'unread_count',
                    'count': unread_count
                }))
        
        elif message_type == 'mark_all_as_read':
            await self.mark_all_as_read()
            
            # Cập nhật số lượng thông báo chưa đọc
            await self.send(text_data=json.dumps({
                'type': 'unread_count',
                'count': 0
            }))
    
    # Xử lý sự kiện từ channel layer
    async def notification_message(self, event):
        # Gửi thông báo đến WebSocket
        await self.send(text_data=json.dumps(event))
    
    # Các phương thức truy vấn cơ sở dữ liệu
    @database_sync_to_async
    def get_unread_count(self):
        return Notification.objects.filter(
            recipient=self.user,
            is_read=False,
            is_deleted=False
        ).count()
    
    @database_sync_to_async
    def mark_notification_as_read(self, notification_id):
        try:
            notification = Notification.objects.get(
                id=notification_id,
                recipient=self.user
            )
            notification.mark_as_read()
            return True
        except Notification.DoesNotExist:
            return False
    
    @database_sync_to_async
    def mark_all_as_read(self):
        Notification.objects.filter(
            recipient=self.user,
            is_read=False,
            is_deleted=False
        ).update(is_read=True, read_at=timezone.now())
