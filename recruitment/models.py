from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from smarthrm.utils import get_upload_path
from departments.models import Department
from factories.models import Factory
import uuid

def resume_file_path(instance, filename):
    """Tạo đường dẫn lưu trữ CV"""
    ext = filename.split('.')[-1]
    filename = f"resume-{uuid.uuid4().hex}.{ext}"
    return f'recruitment/resumes/{filename}'

class JobPosting(models.Model):
    """Tin tuyển dụng"""
    STATUS_CHOICES = (
        ('draft', 'Nháp'),
        ('pending', 'Chờ duyệt'),
        ('published', 'Đã đăng'),
        ('closed', 'Đã đóng'),
        ('cancelled', 'Đã hủy'),
    )
    
    WORKPLACE_TYPE_CHOICES = (
        ('department', 'Phòng ban'),
        ('factory', 'Xí nghiệp'),
    )
    
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    job_code = models.CharField(max_length=50, unique=True, verbose_name="Mã tin tuyển dụng")
    description = models.TextField(verbose_name="Mô tả công việc")
    requirements = models.TextField(verbose_name="Yêu cầu")
    benefits = models.TextField(verbose_name="Quyền lợi")
    positions = models.PositiveIntegerField(default=1, verbose_name="Số lượng cần tuyển")
    min_salary = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, 
                                    verbose_name="Lương tối thiểu")
    max_salary = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, 
                                    verbose_name="Lương tối đa")
    is_salary_visible = models.BooleanField(default=False, verbose_name="Hiển thị lương")
    
    # Liên kết với phòng ban hoặc xí nghiệp
    workplace_type = models.CharField(max_length=20, choices=WORKPLACE_TYPE_CHOICES, 
                                     default='department', verbose_name="Loại nơi làm việc")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True, 
                                  related_name='job_postings', verbose_name="Phòng ban")
    factory = models.ForeignKey(Factory, on_delete=models.SET_NULL, blank=True, null=True, 
                               related_name='job_postings', verbose_name="Xí nghiệp")
    
    location = models.CharField(max_length=100, verbose_name="Địa điểm làm việc")
    publish_date = models.DateField(verbose_name="Ngày đăng")
    closing_date = models.DateField(verbose_name="Ngày hết hạn")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', 
                             verbose_name="Trạng thái")
    
    # Thông tin người tạo và phê duyệt
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                  related_name='created_job_postings', verbose_name="Người tạo")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='approved_job_postings', verbose_name="Người phê duyệt")
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name="Ngày phê duyệt")
    
    # Trường hệ thống
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Tin tuyển dụng"
        verbose_name_plural = "Tin tuyển dụng"
        ordering = ['-publish_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('job-posting-detail', kwargs={'pk': self.pk})

class JobApplication(models.Model):
    """Đơn ứng tuyển"""
    STATUS_CHOICES = (
        ('new', 'Mới'),
        ('screening', 'Đang sàng lọc'),
        ('interview_department', 'Phỏng vấn phòng ban'),
        ('interview_factory', 'Phỏng vấn xí nghiệp'),
        ('offered', 'Đã đề xuất'),
        ('accepted', 'Đã chấp nhận'),
        ('rejected', 'Từ chối'),
        ('cancelled', 'Đã hủy'),
    )
    
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, 
                                   related_name='applications', verbose_name="Tin tuyển dụng")
    full_name = models.CharField(max_length=100, verbose_name="Họ và tên")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    date_of_birth = models.DateField(verbose_name="Ngày sinh")
    address = models.TextField(verbose_name="Địa chỉ")
    education = models.TextField(verbose_name="Học vấn")
    experience = models.TextField(verbose_name="Kinh nghiệm làm việc")
    skills = models.TextField(verbose_name="Kỹ năng")
    resume = models.FileField(upload_to=resume_file_path, verbose_name="CV")
    cover_letter = models.TextField(blank=True, null=True, verbose_name="Thư xin việc")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new', 
                             verbose_name="Trạng thái")
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú")
    
    # Trường hệ thống
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Đơn ứng tuyển"
        verbose_name_plural = "Đơn ứng tuyển"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.job_posting.title}"

    def get_absolute_url(self):
        return reverse('job-application-detail', kwargs={'pk': self.pk})

class Interview(models.Model):
    """Phỏng vấn"""
    INTERVIEW_TYPES = (
        ('department', 'Phòng ban'),
        ('factory', 'Xí nghiệp'),
        ('hr', 'Nhân sự'),
    )
    
    STATUS_CHOICES = (
        ('scheduled', 'Đã lên lịch'),
        ('completed', 'Đã hoàn thành'),
        ('cancelled', 'Đã hủy'),
    )
    
    RESULT_CHOICES = (
        ('pending', 'Chưa có kết quả'),
        ('passed', 'Đạt'),
        ('failed', 'Không đạt'),
    )
    
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, 
                                   related_name='interviews', verbose_name="Đơn ứng tuyển")
    interview_type = models.CharField(max_length=20, choices=INTERVIEW_TYPES, 
                                     verbose_name="Loại phỏng vấn")
    interviewers = models.ManyToManyField(User, related_name='conducted_interviews', 
                                         verbose_name="Người phỏng vấn")
    scheduled_date = models.DateTimeField(verbose_name="Thời gian phỏng vấn")
    location = models.CharField(max_length=100, verbose_name="Địa điểm phỏng vấn")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', 
                             verbose_name="Trạng thái")
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, default='pending', 
                             verbose_name="Kết quả")
    evaluation = models.TextField(blank=True, null=True, verbose_name="Đánh giá")
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú")
    
    # Trường hệ thống
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                  related_name='scheduled_interviews', verbose_name="Người tạo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Phỏng vấn"
        verbose_name_plural = "Phỏng vấn"
        ordering = ['-scheduled_date']

    def __str__(self):
        return f"{self.application.full_name} - {self.get_interview_type_display()} - {self.scheduled_date.strftime('%d/%m/%Y %H:%M')}"
