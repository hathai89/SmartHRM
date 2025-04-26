from django.db import models
from smarthrm.utils import company_logo_path, normalize_filename
from django.db.models.signals import pre_save
from django.dispatch import receiver
import os

class Company(models.Model):
    """
    Model quản lý thông tin công ty
    """
    name = models.CharField(max_length=200, verbose_name="Tên công ty")
    short_name = models.CharField(max_length=50, verbose_name="Tên viết tắt", blank=True, null=True)
    tax_code = models.CharField(max_length=20, verbose_name="Mã số thuế", unique=True)
    address = models.TextField(verbose_name="Địa chỉ")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    email = models.EmailField(verbose_name="Email")
    website = models.URLField(verbose_name="Website", blank=True, null=True)
    representative = models.CharField(max_length=100, verbose_name="Người đại diện")
    position = models.CharField(max_length=100, verbose_name="Chức vụ người đại diện")

    # Thông tin phòng nhân sự/tuyển dụng
    hr_department = models.CharField(max_length=100, verbose_name="Tên phòng nhân sự", default="Phòng Nhân sự")
    hr_phone = models.CharField(max_length=20, verbose_name="Số điện thoại phòng nhân sự", blank=True, null=True)
    career_email = models.EmailField(verbose_name="Email tuyển dụng", blank=True, null=True)

    logo = models.ImageField(
        upload_to=company_logo_path,
        blank=True,
        null=True,
        verbose_name="Logo"
    )
    fax = models.CharField(max_length=20, blank=True, null=True, verbose_name="Số Fax")

    # Thông tin thêm
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    foundation_date = models.DateField(blank=True, null=True, verbose_name="Ngày thành lập")

    # Trường hệ thống
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Công ty"
        verbose_name_plural = "Công ty"

    def __str__(self):
        return self.name

    @classmethod
    def get_company_info(cls):
        """
        Lấy thông tin công ty đầu tiên trong hệ thống
        Sử dụng phương thức này để lấy thông tin công ty từ các ứng dụng khác
        """
        return cls.objects.first()

@receiver(pre_save, sender=Company)
def normalize_company_files(sender, instance, **kwargs):
    """
    Đảm bảo logo công ty được chuẩn hóa trước khi lưu
    """
    # Chuẩn hóa file logo
    if instance.logo and hasattr(instance.logo, 'name') and instance.logo.name:
        file_dir = os.path.dirname(instance.logo.name)
        file_basename = os.path.basename(instance.logo.name)
        if any(c in file_basename for c in ' àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệ'):
            normalized_name = normalize_filename(file_basename)
            instance.logo.name = os.path.join(file_dir, normalized_name)
