from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class Notification(models.Model):
    """
    Model quản lý thông báo
    """
    NOTIFICATION_TYPES = (
        ('system', 'Hệ thống'),
        ('document', 'Tài liệu'),
        ('task', 'Công việc'),
        ('message', 'Tin nhắn'),
        ('approval', 'Phê duyệt'),
        ('other', 'Khác'),
    )
    
    PRIORITY_LEVELS = (
        ('low', 'Thấp'),
        ('normal', 'Bình thường'),
        ('high', 'Cao'),
        ('urgent', 'Khẩn cấp'),
    )
    
    DISPLAY_TYPES = (
        ('popup', 'Popup'),
        ('toast', 'Toast'),
        ('badge', 'Badge'),
        ('email', 'Email'),
        ('sms', 'SMS'),
    )
    
    # Người nhận và người gửi
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name="Người nhận")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications', verbose_name="Người gửi")
    
    # Nội dung thông báo
    title = models.CharField(max_length=255, verbose_name="Tiêu đề")
    message = models.TextField(verbose_name="Nội dung")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='system', verbose_name="Loại thông báo")
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='normal', verbose_name="Mức độ ưu tiên")
    
    # Liên kết đến đối tượng liên quan (Generic Foreign Key)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Loại đối tượng")
    object_id = models.PositiveIntegerField(null=True, blank=True, verbose_name="ID đối tượng")
    related_object = GenericForeignKey('content_type', 'object_id')
    
    # Liên kết
    link = models.CharField(max_length=255, blank=True, null=True, verbose_name="Đường dẫn")
    
    # Trạng thái
    is_read = models.BooleanField(default=False, verbose_name="Đã đọc")
    read_at = models.DateTimeField(null=True, blank=True, verbose_name="Thời gian đọc")
    is_deleted = models.BooleanField(default=False, verbose_name="Đã xóa")
    
    # Hiển thị
    display_type = models.CharField(max_length=20, choices=DISPLAY_TYPES, default='toast', verbose_name="Kiểu hiển thị")
    requires_action = models.BooleanField(default=False, verbose_name="Yêu cầu hành động")
    action_url = models.CharField(max_length=255, blank=True, null=True, verbose_name="URL hành động")
    action_text = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nội dung nút hành động")
    
    # Thời gian
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Cập nhật lần cuối")
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Thời gian hết hạn")
    
    class Meta:
        verbose_name = "Thông báo"
        verbose_name_plural = "Thông báo"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} - {self.recipient.username}"
    
    def mark_as_read(self):
        """Đánh dấu thông báo đã đọc"""
        self.is_read = True
        self.read_at = timezone.now()
        self.save(update_fields=['is_read', 'read_at', 'updated_at'])
        
    def mark_as_unread(self):
        """Đánh dấu thông báo chưa đọc"""
        self.is_read = False
        self.read_at = None
        self.save(update_fields=['is_read', 'read_at', 'updated_at'])
        
    def soft_delete(self):
        """Xóa mềm thông báo"""
        self.is_deleted = True
        self.save(update_fields=['is_deleted', 'updated_at'])
        
    def restore(self):
        """Khôi phục thông báo đã xóa mềm"""
        self.is_deleted = False
        self.save(update_fields=['is_deleted', 'updated_at'])
        
    @property
    def is_expired(self):
        """Kiểm tra xem thông báo đã hết hạn chưa"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
