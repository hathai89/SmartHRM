from django.db import models
from django.utils.translation import gettext_lazy as _

class SiteSetting(models.Model):
    """
    Model để lưu trữ các cài đặt của hệ thống
    """
    key = models.CharField(_('Khóa'), max_length=100, unique=True)
    value = models.TextField(_('Giá trị'), blank=True, null=True)
    description = models.TextField(_('Mô tả'), blank=True, null=True)
    is_active = models.BooleanField(_('Kích hoạt'), default=True)
    created_at = models.DateTimeField(_('Ngày tạo'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Ngày cập nhật'), auto_now=True)

    class Meta:
        verbose_name = _('Cài đặt hệ thống')
        verbose_name_plural = _('Cài đặt hệ thống')
        ordering = ['key']

    def __str__(self):
        return self.key
