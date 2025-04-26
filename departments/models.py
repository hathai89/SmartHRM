# departments/models.py
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from company.models import Company


class Department(MPTTModel):
    """
    Model quản lý phòng ban, bộ phận, nhóm theo cấu trúc cây phân cấp
    Cấu trúc: Phòng ban > Bộ phận > Nhóm
    """
    DEPARTMENT_TYPES = (
        ('department', 'Phòng ban'),
        ('division', 'Bộ phận'),
        ('team', 'Nhóm'),
    )
    
    name = models.CharField(max_length=100, verbose_name="Tên")
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    dept_type = models.CharField(max_length=20, choices=DEPARTMENT_TYPES, verbose_name="Loại")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='departments', verbose_name="Công ty")
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
    
    # Trường hệ thống
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class MPTTMeta:
        order_insertion_by = ['name']
    
    class Meta:
        verbose_name = "Phòng ban"
        verbose_name_plural = "Phòng ban"
        unique_together = ('company', 'code')
    
    def __str__(self):
        return f"{self.get_dept_type_display()}: {self.name} ({self.code})"
    
    def get_absolute_url(self):
        return reverse('department-detail', kwargs={'pk': self.pk})
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Kiểm tra ràng buộc: Phòng ban không có parent
        if self.dept_type == 'department' and self.parent:
            raise ValidationError({'parent': 'Phòng ban không thể có đơn vị cha.'})
        
        # Kiểm tra ràng buộc: Bộ phận chỉ có thể là con của phòng ban
        if self.dept_type == 'division' and self.parent and self.parent.dept_type != 'department':
            raise ValidationError({'parent': 'Bộ phận chỉ có thể trực thuộc phòng ban.'})
        
        # Kiểm tra ràng buộc: Nhóm chỉ có thể là con của bộ phận
        if self.dept_type == 'team' and self.parent and self.parent.dept_type != 'division':
            raise ValidationError({'parent': 'Nhóm chỉ có thể trực thuộc bộ phận.'})
        
        # Kiểm tra ràng buộc: Bộ phận phải có parent
        if self.dept_type == 'division' and not self.parent:
            raise ValidationError({'parent': 'Bộ phận phải trực thuộc một phòng ban.'})
        
        # Kiểm tra ràng buộc: Nhóm phải có parent
        if self.dept_type == 'team' and not self.parent:
            raise ValidationError({'parent': 'Nhóm phải trực thuộc một bộ phận.'})


# Managers cho các proxy models
class DepartmentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(dept_type='department')

class DivisionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(dept_type='division')

class TeamManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(dept_type='team')


# Proxy Models
class PhongBan(Department):
    """Proxy model cho phòng ban"""
    objects = DepartmentManager()
    
    class Meta:
        proxy = True
        verbose_name = "Phòng ban"
        verbose_name_plural = "Phòng ban"
    
    def save(self, *args, **kwargs):
        self.dept_type = 'department'
        super().save(*args, **kwargs)


class BoPhan(Department):
    """Proxy model cho bộ phận"""
    objects = DivisionManager()
    
    class Meta:
        proxy = True
        verbose_name = "Bộ phận"
        verbose_name_plural = "Bộ phận"
    
    def save(self, *args, **kwargs):
        self.dept_type = 'division'
        super().save(*args, **kwargs)


class Nhom(Department):
    """Proxy model cho nhóm"""
    objects = TeamManager()
    
    class Meta:
        proxy = True
        verbose_name = "Nhóm"
        verbose_name_plural = "Nhóm"
    
    def save(self, *args, **kwargs):
        self.dept_type = 'team'
        super().save(*args, **kwargs)
