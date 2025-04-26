# factories/models.py
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from company.models import Company


class Factory(MPTTModel):
    """
    Model quản lý xí nghiệp, bộ phận, nhóm theo cấu trúc cây phân cấp
    Cấu trúc: Xí nghiệp > Bộ phận > Nhóm
    """
    FACTORY_TYPES = (
        ('factory', 'Xí nghiệp'),
        ('division', 'Bộ phận'),
        ('team', 'Nhóm'),
    )
    
    name = models.CharField(max_length=100, verbose_name="Tên")
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    factory_type = models.CharField(max_length=20, choices=FACTORY_TYPES, verbose_name="Loại")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='factories', verbose_name="Công ty")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    
    # Quan hệ phân cấp (MPTT)
    parent = TreeForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children',
        verbose_name="Đơn vị cha"
    )
    
    # Thông tin người quản lý
    manager_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tên người quản lý")
    manager_title = models.CharField(max_length=100, blank=True, null=True, verbose_name="Chức danh người quản lý")
    manager_email = models.EmailField(blank=True, null=True, verbose_name="Email người quản lý")
    manager_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="SĐT người quản lý")
    
    # Thông tin bổ sung
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name="Vị trí")
    capacity = models.CharField(max_length=100, blank=True, null=True, verbose_name="Công suất")
    established_date = models.DateField(blank=True, null=True, verbose_name="Ngày thành lập")
    
    # Trường hệ thống
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class MPTTMeta:
        order_insertion_by = ['name']
    
    class Meta:
        verbose_name = "Xí nghiệp"
        verbose_name_plural = "Xí nghiệp"
        unique_together = ('company', 'code')
    
    def __str__(self):
        return f"{self.get_factory_type_display()}: {self.name} ({self.code})"
    
    def get_absolute_url(self):
        return reverse('factory-detail', kwargs={'pk': self.pk})
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Kiểm tra ràng buộc: Xí nghiệp không có parent
        if self.factory_type == 'factory' and self.parent:
            raise ValidationError({'parent': 'Xí nghiệp không thể có đơn vị cha.'})
        
        # Kiểm tra ràng buộc: Bộ phận chỉ có thể là con của xí nghiệp
        if self.factory_type == 'division' and self.parent and self.parent.factory_type != 'factory':
            raise ValidationError({'parent': 'Bộ phận chỉ có thể trực thuộc xí nghiệp.'})
        
        # Kiểm tra ràng buộc: Nhóm chỉ có thể là con của bộ phận
        if self.factory_type == 'team' and self.parent and self.parent.factory_type != 'division':
            raise ValidationError({'parent': 'Nhóm chỉ có thể trực thuộc bộ phận.'})
        
        # Kiểm tra ràng buộc: Bộ phận phải có parent
        if self.factory_type == 'division' and not self.parent:
            raise ValidationError({'parent': 'Bộ phận phải trực thuộc một xí nghiệp.'})
        
        # Kiểm tra ràng buộc: Nhóm phải có parent
        if self.factory_type == 'team' and not self.parent:
            raise ValidationError({'parent': 'Nhóm phải trực thuộc một bộ phận.'})


# Managers cho các proxy models
class FactoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(factory_type='factory')

class FactoryDivisionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(factory_type='division')

class FactoryTeamManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(factory_type='team')


# Proxy Models
class XiNghiep(Factory):
    """Proxy model cho xí nghiệp"""
    objects = FactoryManager()
    
    class Meta:
        proxy = True
        verbose_name = "Xí nghiệp"
        verbose_name_plural = "Xí nghiệp"
    
    def save(self, *args, **kwargs):
        self.factory_type = 'factory'
        super().save(*args, **kwargs)


class BoPhanXiNghiep(Factory):
    """Proxy model cho bộ phận thuộc xí nghiệp"""
    objects = FactoryDivisionManager()
    
    class Meta:
        proxy = True
        verbose_name = "Bộ phận xí nghiệp"
        verbose_name_plural = "Bộ phận xí nghiệp"
    
    def save(self, *args, **kwargs):
        self.factory_type = 'division'
        super().save(*args, **kwargs)


class NhomXiNghiep(Factory):
    """Proxy model cho nhóm thuộc xí nghiệp"""
    objects = FactoryTeamManager()
    
    class Meta:
        proxy = True
        verbose_name = "Nhóm xí nghiệp"
        verbose_name_plural = "Nhóm xí nghiệp"
    
    def save(self, *args, **kwargs):
        self.factory_type = 'team'
        super().save(*args, **kwargs)

# Tạo alias cho class BoPhanXiNghiep và NhomXiNghiep để có thể import dễ dàng
Section = BoPhanXiNghiep
Team = NhomXiNghiep
