from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from smarthrm.utils import get_upload_path
import uuid

def document_file_path(instance, filename):
    """Tạo đường dẫn lưu trữ tài liệu"""
    ext = filename.split('.')[-1]
    filename = f"document-{uuid.uuid4().hex}.{ext}"
    return f'documents/files/{filename}'

class DocumentCategory(models.Model):
    """Danh mục tài liệu"""
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã danh mục")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                              related_name='children', verbose_name="Danh mục cha")
    is_active = models.BooleanField(default=True, verbose_name="Đang sử dụng")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Danh mục tài liệu"
        verbose_name_plural = "Danh mục tài liệu"
        ordering = ['name']

    def __str__(self):
        return self.name

class Document(models.Model):
    """Tài liệu"""
    DOCUMENT_TYPES = (
        ('policy', 'Chính sách'),
        ('procedure', 'Quy trình'),
        ('form', 'Biểu mẫu'),
        ('report', 'Báo cáo'),
        ('contract', 'Hợp đồng'),
        ('other', 'Khác'),
    )
    
    ACCESS_LEVELS = (
        ('public', 'Công khai'),
        ('internal', 'Nội bộ'),
        ('restricted', 'Hạn chế'),
        ('confidential', 'Bảo mật'),
    )
    
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    document_number = models.CharField(max_length=50, unique=True, verbose_name="Số hiệu tài liệu")
    category = models.ForeignKey(DocumentCategory, on_delete=models.PROTECT, 
                                related_name='documents', verbose_name="Danh mục")
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, 
                                    verbose_name="Loại tài liệu")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    content = models.TextField(blank=True, null=True, verbose_name="Nội dung")
    file = models.FileField(upload_to=document_file_path, blank=True, null=True, 
                           verbose_name="Tệp đính kèm")
    version = models.CharField(max_length=20, default="1.0", verbose_name="Phiên bản")
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVELS, 
                                   default='internal', verbose_name="Mức độ truy cập")
    is_active = models.BooleanField(default=True, verbose_name="Đang sử dụng")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                  related_name='created_documents', verbose_name="Người tạo")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='approved_documents', verbose_name="Người phê duyệt")
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name="Ngày phê duyệt")
    effective_date = models.DateField(null=True, blank=True, verbose_name="Ngày hiệu lực")
    expiry_date = models.DateField(null=True, blank=True, verbose_name="Ngày hết hiệu lực")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Tài liệu"
        verbose_name_plural = "Tài liệu"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.document_number} - {self.title}"

    def get_absolute_url(self):
        return reverse('document-detail', kwargs={'pk': self.pk})

class DocumentVersion(models.Model):
    """Phiên bản tài liệu"""
    document = models.ForeignKey(Document, on_delete=models.CASCADE, 
                                related_name='versions', verbose_name="Tài liệu")
    version = models.CharField(max_length=20, verbose_name="Phiên bản")
    content = models.TextField(blank=True, null=True, verbose_name="Nội dung")
    file = models.FileField(upload_to=document_file_path, blank=True, null=True, 
                           verbose_name="Tệp đính kèm")
    change_summary = models.TextField(verbose_name="Tóm tắt thay đổi")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                  related_name='created_versions', verbose_name="Người tạo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")

    class Meta:
        verbose_name = "Phiên bản tài liệu"
        verbose_name_plural = "Phiên bản tài liệu"
        ordering = ['-created_at']
        unique_together = ('document', 'version')

    def __str__(self):
        return f"{self.document.title} - v{self.version}"
