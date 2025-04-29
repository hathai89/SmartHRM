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

def id_card_image_path(instance, filename):
    """Tạo đường dẫn lưu trữ ảnh CCCD/CMND"""
    ext = filename.split('.')[-1]
    filename = f"id-card-{uuid.uuid4().hex}.{ext}"
    return f'recruitment/id_cards/{filename}'

def avatar_image_path(instance, filename):
    """Tạo đường dẫn lưu trữ ảnh đại diện"""
    ext = filename.split('.')[-1]
    filename = f"avatar-{uuid.uuid4().hex}.{ext}"
    return f'recruitment/avatars/{filename}'


class MaritalStatus(models.Model):
    """Tình trạng hôn nhân"""
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã")
    name = models.CharField(max_length=50, verbose_name="Tên")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự")

    class Meta:
        verbose_name = "Tình trạng hôn nhân"
        verbose_name_plural = "Tình trạng hôn nhân"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class FamilyPolicyType(models.Model):
    """Loại chính sách gia đình"""
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã")
    name = models.CharField(max_length=100, verbose_name="Tên")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự")

    class Meta:
        verbose_name = "Loại chính sách gia đình"
        verbose_name_plural = "Loại chính sách gia đình"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Gender(models.Model):
    """Giới tính"""
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã")
    name = models.CharField(max_length=50, verbose_name="Tên")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự")

    class Meta:
        verbose_name = "Giới tính"
        verbose_name_plural = "Giới tính"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class EducationLevel(models.Model):
    """Trình độ học vấn"""
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã")
    name = models.CharField(max_length=100, verbose_name="Tên")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự")

    class Meta:
        verbose_name = "Trình độ học vấn"
        verbose_name_plural = "Trình độ học vấn"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

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

    EMPLOYMENT_TYPE_CHOICES = (
        ('full_time', 'Toàn thời gian'),
        ('part_time', 'Bán thời gian'),
        ('contract', 'Hợp đồng'),
        ('temporary', 'Tạm thời'),
        ('internship', 'Thực tập'),
    )

    EXPERIENCE_LEVEL_CHOICES = (
        ('entry', 'Mới tốt nghiệp'),
        ('junior', 'Sơ cấp (1-2 năm)'),
        ('mid', 'Trung cấp (3-5 năm)'),
        ('senior', 'Cao cấp (5+ năm)'),
        ('lead', 'Nhóm trưởng/Quản lý'),
        ('executive', 'Điều hành cấp cao'),
    )

    @staticmethod
    def generate_job_code():
        """Tạo mã tin tuyển dụng tự động với định dạng JOB-YYYYMM-XXXX"""
        import random
        import string
        from django.utils import timezone

        # Lấy năm và tháng hiện tại
        now = timezone.now()
        year_month = now.strftime("%Y%m")

        # Tạo mã ngẫu nhiên
        while True:
            # Tạo 4 ký tự ngẫu nhiên (chữ hoa và số)
            random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            job_code = f"JOB-{year_month}-{random_chars}"

            # Kiểm tra xem mã đã tồn tại chưa
            if not JobPosting.objects.filter(job_code=job_code).exists():
                return job_code

    EDUCATION_REQUIRED_CHOICES = (
        ('none', 'Không yêu cầu bằng cấp'),
        ('high_school', 'Tốt nghiệp THPT'),
        ('vocational', 'Trung cấp nghề'),
        ('college', 'Cao đẳng'),
        ('bachelor', 'Đại học'),
        ('master', 'Thạc sĩ'),
        ('phd', 'Tiến sĩ'),
    )

    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    job_code = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="Mã tin tuyển dụng")
    description = models.TextField(verbose_name="Mô tả công việc")
    requirements = models.TextField(verbose_name="Yêu cầu")
    benefits = models.TextField(verbose_name="Quyền lợi")
    positions = models.PositiveIntegerField(default=1, verbose_name="Số lượng cần tuyển")
    min_salary = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True,
                                    verbose_name="Lương tối thiểu")
    max_salary = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True,
                                    verbose_name="Lương tối đa")
    is_salary_visible = models.BooleanField(default=False, verbose_name="Hiển thị lương")
    is_salary_negotiable = models.BooleanField(default=False, verbose_name="Lương thỏa thuận")
    is_open_until_filled = models.BooleanField(default=False, verbose_name="Tuyển dụng đến khi đủ")

    # Liên kết với phòng ban hoặc xí nghiệp
    workplace_type = models.CharField(max_length=20, choices=WORKPLACE_TYPE_CHOICES,
                                     default='department', verbose_name="Loại nơi làm việc")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True,
                                  related_name='job_postings', verbose_name="Phòng ban")
    factory = models.ForeignKey(Factory, on_delete=models.SET_NULL, blank=True, null=True,
                               related_name='job_postings', verbose_name="Xí nghiệp")
    division = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='division_job_postings', verbose_name="Bộ phận",
                                limit_choices_to={'dept_type': 'division'})
    team = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True,
                            related_name='team_job_postings', verbose_name="Nhóm",
                            limit_choices_to={'dept_type': 'team'})

    # Thông tin công việc
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES,
                                     default='full_time', verbose_name="Hình thức làm việc")
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES,
                                      default='entry', verbose_name="Kinh nghiệm")
    education_required = models.CharField(max_length=20, choices=EDUCATION_REQUIRED_CHOICES,
                                        default='bachelor', verbose_name="Học vấn")

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

    # Giới tính được quản lý bởi model Gender

    # Tình trạng hôn nhân được quản lý bởi model MaritalStatus

    CURRENCY_CHOICES = (
        ('VND', 'VND'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    )

    # Thông tin cơ bản
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE,
                                   related_name='applications', verbose_name="Tin tuyển dụng")
    first_name = models.CharField(max_length=50, verbose_name="Tên", blank=True, null=True)
    last_name = models.CharField(max_length=50, verbose_name="Họ và tên đệm", blank=True, null=True)
    full_name = models.CharField(max_length=100, verbose_name="Họ và tên")
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Giới tính")
    date_of_birth = models.DateField(verbose_name="Ngày sinh", blank=True, null=True)
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    marital_status = models.ForeignKey(MaritalStatus, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Tình trạng hôn nhân")
    nationality = models.CharField(max_length=50, default="Việt Nam", blank=True, null=True, verbose_name="Quốc tịch")
    birth_place = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nơi sinh")
    ethnicity = models.CharField(max_length=50, blank=True, null=True, verbose_name="Dân tộc")
    religion = models.CharField(max_length=50, blank=True, null=True, verbose_name="Tôn giáo")
    is_party_member = models.BooleanField(default=False, verbose_name="Là Đảng viên", blank=True)

    # Thông tin CCCD/CMND
    id_card_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Số CCCD/CMND")
    id_card_issue_date = models.DateField(blank=True, null=True, verbose_name="Ngày cấp CCCD/CMND")
    id_card_issue_place = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nơi cấp CCCD/CMND")
    id_card_front_image = models.ImageField(upload_to=id_card_image_path, blank=True, null=True, verbose_name="Ảnh mặt trước CCCD/CMND")
    id_card_back_image = models.ImageField(upload_to=id_card_image_path, blank=True, null=True, verbose_name="Ảnh mặt sau CCCD/CMND")

    # Thông tin địa chỉ
    permanent_address = models.TextField(blank=True, null=True, verbose_name="Địa chỉ thường trú")
    address = models.TextField(verbose_name="Địa chỉ liên hệ", blank=True, null=True)

    # Thông tin liên hệ khẩn cấp
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tên người liên hệ khẩn cấp")
    emergency_contact_relationship = models.CharField(max_length=50, blank=True, null=True, verbose_name="Mối quan hệ")
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Số điện thoại liên hệ khẩn cấp")

    # Thông tin gia đình
    father_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tên cha")
    father_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Số điện thoại cha")
    mother_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tên mẹ")
    mother_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Số điện thoại mẹ")
    is_family_policy = models.BooleanField(default=False, verbose_name="Thuộc diện chính sách", blank=True)
    family_policy_type = models.ForeignKey(FamilyPolicyType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Loại chính sách")
    family_policy_detail = models.TextField(blank=True, null=True, verbose_name="Chi tiết chính sách")

    # Thông tin nghĩa vụ quân sự
    military_service = models.BooleanField(default=False, verbose_name="Đã hoàn thành nghĩa vụ quân sự", blank=True)
    military_service_date = models.DateField(blank=True, null=True, verbose_name="Ngày bắt đầu nghĩa vụ quân sự")
    military_service_end_date = models.DateField(blank=True, null=True, verbose_name="Ngày kết thúc nghĩa vụ quân sự")
    military_service_role = models.CharField(max_length=100, blank=True, null=True, verbose_name="Chức vụ trong quân đội")

    # Thông tin chuyên môn
    education_level = models.ForeignKey(EducationLevel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Trình độ học vấn")
    education_detail = models.TextField(blank=True, null=True, verbose_name="Chi tiết học vấn")
    experience = models.TextField(blank=True, null=True, verbose_name="Kinh nghiệm làm việc")
    skills = models.TextField(blank=True, null=True, verbose_name="Kỹ năng")
    resume = models.FileField(upload_to=resume_file_path, blank=True, null=True, verbose_name="CV")
    avatar = models.ImageField(upload_to=avatar_image_path, blank=True, null=True, verbose_name="Ảnh đại diện")
    cover_letter = models.TextField(blank=True, null=True, verbose_name="Thư giới thiệu")

    # Thông tin bổ sung
    portfolio_url = models.URLField(blank=True, null=True, verbose_name="Liên kết portfolio")
    linkedin_profile = models.URLField(blank=True, null=True, verbose_name="LinkedIn")
    expected_salary = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True, verbose_name="Mức lương mong muốn")
    salary_currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default='VND', verbose_name="Đơn vị tiền tệ")

    # Trạng thái đơn
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new', verbose_name="Trạng thái")
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
