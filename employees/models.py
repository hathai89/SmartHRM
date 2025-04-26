from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse
from django.contrib.auth.models import User
from departments.models import Department
from factories.models import Factory
from smarthrm.utils import employee_avatar_path, employee_id_card_path
import random
import string
from datetime import date, timedelta

class JobTitle(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên chức danh")
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã chức danh")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    department_type = models.CharField(
        max_length=20,
        choices=[
            ('all', 'Tất cả'),
            ('department', 'Phòng ban'),
            ('factory', 'Xí nghiệp')
        ],
        default='all',
        verbose_name="Áp dụng cho"
    )
    position_type = models.CharField(
        max_length=20,
        choices=[
            ('employee', 'Nhân viên'),
            ('deputy', 'Phó phòng'),
            ('manager', 'Trưởng phòng'),
            ('director', 'Giám đốc'),
            ('other', 'Khác')
        ],
        default='employee',
        verbose_name="Loại chức vụ"
    )
    is_active = models.BooleanField(default=True, verbose_name="Đang sử dụng")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Chức danh"
        verbose_name_plural = "Danh sách chức danh"
        ordering = ['name']

    def __str__(self):
        return self.name

class Employee(models.Model):
    """
    Model quản lý thông tin nhân viên
    """
    GENDER_CHOICES = (
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác'),
    )

    MARITAL_STATUS_CHOICES = (
        ('single', 'Độc thân'),
        ('married', 'Đã kết hôn'),
        ('divorced', 'Đã ly hôn'),
        ('widowed', 'Góa phụ/phu'),
    )

    CONTRACT_TYPE_CHOICES = (
        ('pending', 'Chờ tạo'),
        ('probation', 'Thử việc'),
        ('full_time', 'Chính thức'),
    )

    STATUS_CHOICES = (
        ('pending', 'Chờ xử lý'),
        ('active', 'Đang làm việc'),
        ('probation', 'Thử việc'),
        ('failed_probation', 'Không đạt thử việc'),
        ('leave', 'Nghỉ phép'),
        ('suspended', 'Tạm đình chỉ'),
        ('terminated', 'Đã nghỉ việc'),
    )

    # Thông tin cơ bản
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã nhân viên", blank=True)
    attendance_code = models.CharField(max_length=10, unique=True, verbose_name="Mã chấm công", blank=True)
    first_name = models.CharField(max_length=50, verbose_name="Tên")
    last_name = models.CharField(max_length=50, verbose_name="Họ và tên đệm")
    full_name = models.CharField(max_length=100, blank=True, verbose_name="Họ và tên đầy đủ")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Giới tính")
    date_of_birth = models.DateField(verbose_name="Ngày sinh")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                message="Số điện thoại phải có định dạng: '+999999999'. Tối đa 15 chữ số.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, verbose_name="Số điện thoại")

    # Ảnh đại diện
    avatar = models.ImageField(
        upload_to=employee_avatar_path,
        blank=True,
        null=True,
        verbose_name="Ảnh đại diện"
    )

    # Thông tin công việc
    job_title = models.ForeignKey(
        JobTitle,
        on_delete=models.PROTECT,
        verbose_name="Chức danh",
        related_name='employees'
    )
    join_date = models.DateField(verbose_name="Ngày vào làm")
    contract_type = models.CharField(max_length=20, choices=CONTRACT_TYPE_CHOICES, verbose_name="Loại hợp đồng", default='probation')

    # Liên kết với phòng ban hoặc xí nghiệp
    workplace_type = models.CharField(
        max_length=20,
        choices=[
            ('department', 'Phòng ban'),
            ('factory', 'Xí nghiệp')
        ],
        default='department',
        verbose_name="Loại nơi làm việc"
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='employees',
        verbose_name="Phòng ban"
    )
    factory = models.ForeignKey(
        Factory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='employees',
        verbose_name="Xí nghiệp"
    )

    # Liên kết với tài khoản người dùng (nếu có)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True,
                               related_name='employee', verbose_name="Tài khoản")

    # Thông tin liên hệ và địa chỉ
    permanent_address = models.TextField(verbose_name="Địa chỉ thường trú")
    current_address = models.TextField(verbose_name="Địa chỉ hiện tại")

    # Thông tin CCCD/CMND
    id_card_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Số CCCD/CMND")
    id_card_issue_date = models.DateField(verbose_name="Ngày cấp", blank=True, null=True)
    id_card_issue_place = models.CharField(max_length=100, verbose_name="Nơi cấp", blank=True, null=True)
    id_card_front_image = models.ImageField(
        upload_to=employee_id_card_path,
        verbose_name="Ảnh mặt trước CCCD",
        blank=True,
        null=True
    )
    id_card_back_image = models.ImageField(
        upload_to=employee_id_card_path,
        verbose_name="Ảnh mặt sau CCCD",
        blank=True,
        null=True
    )

    # Trường hệ thống
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    is_active = models.BooleanField(default=True, verbose_name="Đang làm việc")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    password_changed = models.BooleanField(default=False, verbose_name="Đã đổi mật khẩu")

    class Meta:
        verbose_name = "Nhân viên"
        verbose_name_plural = "Nhân viên"
        ordering = ['code', 'last_name', 'first_name']

    def __str__(self):
        return f"{self.code} - {self.full_name}"

    @staticmethod
    def generate_employee_code(first_name):
        """Tạo mã nhân viên từ chữ cái đầu của tên và 4 số ngẫu nhiên"""
        # Lấy chữ cái đầu của tên đệm và tên (nếu có)
        name_parts = first_name.strip().split()
        if name_parts:
            prefix = name_parts[0][0].upper()  # Chữ cái đầu của tên đệm hoặc tên
        else:
            prefix = 'E'

        while True:
            random_numbers = ''.join(random.choices(string.digits, k=4))
            code = f"{prefix}{random_numbers}"
            if not Employee.objects.filter(code=code).exists():
                return code

    @staticmethod
    def generate_attendance_code():
        """Tạo mã chấm công gồm 4 số ngẫu nhiên"""
        while True:
            code = ''.join(random.choices(string.digits, k=4))
            if not Employee.objects.filter(attendance_code=code).exists():
                return code

    def save(self, *args, **kwargs):
        # Tự động cập nhật tên đầy đủ khi lưu - Họ và tên đệm trước, tên sau theo tiêu chuẩn Việt Nam
        self.full_name = f"{self.last_name} {self.first_name}"

        # Tạo mã nhân viên và mã chấm công nếu chưa có
        if not self.code:
            self.code = self.generate_employee_code(self.first_name)

        if not self.attendance_code:
            self.attendance_code = self.generate_attendance_code()

        # Nếu là nhân viên mới (chưa có ID), đặt trạng thái mặc định
        if not self.pk:
            self.contract_type = 'pending'  # Loại hợp đồng là 'Chờ tạo'
            self.status = 'pending'  # Trạng thái là 'Chờ xử lý'

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('employee-detail', kwargs={'pk': self.pk})
