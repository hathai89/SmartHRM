from django.db import models
from django.core.cache import cache
from django.conf import settings

class SiteSetting(models.Model):
    """
    Model quản lý cài đặt hệ thống
    """
    SETTING_TYPES = (
        ('text', 'Văn bản'),
        ('number', 'Số'),
        ('boolean', 'Boolean'),
        ('json', 'JSON'),
        ('email', 'Email'),
        ('url', 'URL'),
        ('color', 'Màu sắc'),
        ('date', 'Ngày'),
        ('datetime', 'Ngày giờ'),
    )
    
    key = models.CharField(max_length=100, unique=True, verbose_name="Khóa")
    value = models.TextField(blank=True, null=True, verbose_name="Giá trị")
    value_type = models.CharField(max_length=20, choices=SETTING_TYPES, default='text', verbose_name="Kiểu dữ liệu")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    is_public = models.BooleanField(default=False, verbose_name="Công khai")
    
    # Trường hệ thống
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Cài đặt hệ thống"
        verbose_name_plural = "Cài đặt hệ thống"
        ordering = ['key']
    
    def __str__(self):
        return self.key
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Xóa cache khi cài đặt được cập nhật
        cache_key = f"site_setting_{self.key}"
        cache.delete(cache_key)
    
    @classmethod
    def get_setting(cls, key, default=None):
        """
        Lấy giá trị cài đặt theo khóa
        """
        cache_key = f"site_setting_{key}"
        cached_value = cache.get(cache_key)
        
        if cached_value is not None:
            return cached_value
        
        try:
            setting = cls.objects.get(key=key)
            value = setting.value
            
            # Chuyển đổi giá trị theo kiểu dữ liệu
            if setting.value_type == 'number':
                try:
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                except (ValueError, TypeError):
                    value = 0
            elif setting.value_type == 'boolean':
                value = value.lower() in ('true', '1', 'yes', 'y', 'on')
            elif setting.value_type == 'json':
                import json
                try:
                    value = json.loads(value)
                except (ValueError, TypeError):
                    value = {}
            
            # Lưu vào cache
            cache.set(cache_key, value, timeout=settings.CACHE_TTL)
            return value
        except cls.DoesNotExist:
            return default
