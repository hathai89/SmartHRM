from django.db import models
from django.urls import reverse
from smarthrm.utils import get_upload_path
import uuid
from django.utils import timezone

def asset_image_path(instance, filename):
    """Tạo đường dẫn lưu trữ ảnh tài sản"""
    ext = filename.split('.')[-1]
    filename = f"asset-{uuid.uuid4().hex}.{ext}"
    return f'assets/images/{filename}'

class AssetCategory(models.Model):
    """Danh mục loại tài sản"""
    name = models.CharField(max_length=100, verbose_name="Tên loại tài sản")
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã loại")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    is_active = models.BooleanField(default=True, verbose_name="Đang sử dụng")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Loại tài sản"
        verbose_name_plural = "Loại tài sản"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('asset-category-detail', kwargs={'pk': self.pk})

class Asset(models.Model):
    """Thông tin tài sản"""
    STATUS_CHOICES = (
        ('available', 'Sẵn sàng cấp phát'),
        ('assigned', 'Đã cấp phát'),
        ('maintenance', 'Đang bảo trì'),
        ('retired', 'Đã thanh lý'),
        ('lost', 'Mất/Thất lạc'),
    )
    
    ASSET_TYPE_CHOICES = (
        ('assigned', 'Tài sản được cấp'),
        ('managed', 'Tài sản được quản lý'),
    )
    
    name = models.CharField(max_length=100, verbose_name="Tên tài sản")
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã tài sản")
    serial_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Số serial")
    category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT, related_name='assets', verbose_name="Loại tài sản")
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE_CHOICES, default='assigned', verbose_name="Loại quản lý")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả chi tiết")
    purchase_date = models.DateField(blank=True, null=True, verbose_name="Ngày mua")
    purchase_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Giá mua")
    warranty_end_date = models.DateField(blank=True, null=True, verbose_name="Ngày hết hạn bảo hành")
    supplier = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nhà cung cấp")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name="Trạng thái")
    image = models.ImageField(upload_to=asset_image_path, blank=True, null=True, verbose_name="Hình ảnh")
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Tài sản"
        verbose_name_plural = "Tài sản"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_absolute_url(self):
        return reverse('asset-detail', kwargs={'pk': self.pk})

class AssetAssignment(models.Model):
    """Quản lý việc cấp phát tài sản cho nhân viên"""
    STATUS_CHOICES = (
        ('pending', 'Chờ bàn giao'),
        ('assigned', 'Đã bàn giao'),
        ('returned', 'Đã trả lại'),
        ('damaged', 'Hư hỏng'),
        ('lost', 'Mất/Thất lạc'),
    )
    
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='assignments', verbose_name="Tài sản")
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='asset_assignments', verbose_name="Nhân viên")
    assigned_date = models.DateField(default=timezone.now, verbose_name="Ngày cấp phát")
    expected_return_date = models.DateField(blank=True, null=True, verbose_name="Ngày dự kiến trả")
    returned_date = models.DateField(blank=True, null=True, verbose_name="Ngày đã trả")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    condition_on_assignment = models.TextField(blank=True, null=True, verbose_name="Tình trạng khi cấp phát")
    condition_on_return = models.TextField(blank=True, null=True, verbose_name="Tình trạng khi trả lại")
    assigned_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_assets', verbose_name="Người cấp phát")
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Cấp phát tài sản"
        verbose_name_plural = "Cấp phát tài sản"
        ordering = ['-assigned_date']

    def __str__(self):
        return f"{self.asset.name} - {self.employee.full_name}"

    def get_absolute_url(self):
        return reverse('asset-assignment-detail', kwargs={'pk': self.pk})

class AssetMaintenance(models.Model):
    """Quản lý bảo trì, sửa chữa tài sản"""
    STATUS_CHOICES = (
        ('scheduled', 'Đã lên lịch'),
        ('in_progress', 'Đang thực hiện'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Đã hủy'),
    )
    
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='maintenance_records', verbose_name="Tài sản")
    maintenance_type = models.CharField(max_length=100, verbose_name="Loại bảo trì")
    start_date = models.DateField(verbose_name="Ngày bắt đầu")
    end_date = models.DateField(blank=True, null=True, verbose_name="Ngày kết thúc")
    cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Chi phí")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', verbose_name="Trạng thái")
    performed_by = models.CharField(max_length=100, blank=True, null=True, verbose_name="Đơn vị thực hiện")
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Bảo trì tài sản"
        verbose_name_plural = "Bảo trì tài sản"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.asset.name} - {self.maintenance_type}"

class AssetInventory(models.Model):
    """Quản lý kiểm kê tài sản"""
    STATUS_CHOICES = (
        ('planned', 'Kế hoạch'),
        ('in_progress', 'Đang thực hiện'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Đã hủy'),
    )
    
    title = models.CharField(max_length=200, verbose_name="Tiêu đề kiểm kê")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    start_date = models.DateField(verbose_name="Ngày bắt đầu")
    end_date = models.DateField(verbose_name="Ngày kết thúc")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned', verbose_name="Trạng thái")
    conducted_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='conducted_inventories', verbose_name="Người thực hiện")
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Kiểm kê tài sản"
        verbose_name_plural = "Kiểm kê tài sản"
        ordering = ['-start_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('asset-inventory-detail', kwargs={'pk': self.pk})

class AssetInventoryItem(models.Model):
    """Chi tiết từng tài sản trong đợt kiểm kê"""
    STATUS_CHOICES = (
        ('pending', 'Chưa kiểm kê'),
        ('verified', 'Đã xác minh'),
        ('missing', 'Không tìm thấy'),
        ('damaged', 'Hư hỏng'),
    )
    
    inventory = models.ForeignKey(AssetInventory, on_delete=models.CASCADE, related_name='items', verbose_name="Đợt kiểm kê")
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='inventory_records', verbose_name="Tài sản")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú")
    checked_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='checked_assets', verbose_name="Người kiểm tra")
    checked_at = models.DateTimeField(blank=True, null=True, verbose_name="Thời gian kiểm tra")
    
    class Meta:
        verbose_name = "Chi tiết kiểm kê"
        verbose_name_plural = "Chi tiết kiểm kê"
        unique_together = ('inventory', 'asset')
        
    def __str__(self):
        return f"{self.inventory.title} - {self.asset.name}"
