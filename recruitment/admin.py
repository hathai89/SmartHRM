from django.contrib import admin
from .models import (
    JobPosting, JobApplication, Interview,
    MaritalStatus, FamilyPolicyType, Gender, EducationLevel
)

@admin.register(MaritalStatus)
class MaritalStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')
    ordering = ('order', 'name')

@admin.register(FamilyPolicyType)
class FamilyPolicyTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'code', 'description')
    ordering = ('order', 'name')

@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')
    ordering = ('order', 'name')

@admin.register(EducationLevel)
class EducationLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'code', 'description')
    ordering = ('order', 'name')

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'job_code', 'workplace_type', 'status', 'publish_date', 'closing_date')
    list_filter = ('status', 'workplace_type', 'employment_type', 'experience_level')
    search_fields = ('title', 'job_code', 'description')
    date_hierarchy = 'publish_date'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('title', 'job_code', 'description', 'requirements', 'benefits', 'positions')
        }),
        ('Thông tin lương', {
            'fields': ('min_salary', 'max_salary', 'is_salary_visible', 'is_salary_negotiable')
        }),
        ('Nơi làm việc', {
            'fields': ('workplace_type', 'department', 'factory', 'division', 'team', 'location')
        }),
        ('Yêu cầu công việc', {
            'fields': ('employment_type', 'experience_level', 'education_required')
        }),
        ('Thời gian', {
            'fields': ('publish_date', 'closing_date', 'is_open_until_filled')
        }),
        ('Trạng thái', {
            'fields': ('status', 'created_by', 'approved_by', 'approved_at')
        }),
        ('Thông tin hệ thống', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'job_posting', 'email', 'phone', 'status', 'created_at')
    list_filter = ('status', 'job_posting')
    search_fields = ('full_name', 'email', 'phone')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('job_posting', 'status', 'notes')
        }),
        ('Thông tin cá nhân', {
            'fields': ('first_name', 'last_name', 'full_name', 'gender', 'date_of_birth',
                      'email', 'phone', 'marital_status', 'nationality', 'birth_place',
                      'ethnicity', 'religion', 'is_party_member')
        }),
        ('Thông tin CCCD/CMND', {
            'fields': ('id_card_number', 'id_card_issue_date', 'id_card_issue_place',
                      'id_card_front_image', 'id_card_back_image')
        }),
        ('Thông tin địa chỉ', {
            'fields': ('permanent_address', 'address')
        }),
        ('Thông tin liên hệ khẩn cấp', {
            'fields': ('emergency_contact_name', 'emergency_contact_relationship', 'emergency_contact_phone')
        }),
        ('Thông tin gia đình', {
            'fields': ('father_name', 'father_phone', 'mother_name', 'mother_phone',
                      'is_family_policy', 'family_policy_type', 'family_policy_detail')
        }),
        ('Thông tin nghĩa vụ quân sự', {
            'fields': ('military_service', 'military_service_date', 'military_service_end_date', 'military_service_role')
        }),
        ('Thông tin chuyên môn', {
            'fields': ('education_level', 'education_detail', 'experience', 'skills', 'resume', 'avatar', 'cover_letter')
        }),
        ('Thông tin bổ sung', {
            'fields': ('portfolio_url', 'linkedin_profile', 'expected_salary', 'salary_currency')
        }),
        ('Thông tin hệ thống', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('application', 'interview_type', 'scheduled_date', 'status', 'result')
    list_filter = ('status', 'result', 'interview_type')
    search_fields = ('application__full_name', 'evaluation', 'notes')
    date_hierarchy = 'scheduled_date'
    filter_horizontal = ('interviewers',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('application', 'interview_type', 'interviewers', 'scheduled_date', 'location')
        }),
        ('Kết quả', {
            'fields': ('status', 'result', 'evaluation', 'notes')
        }),
        ('Thông tin hệ thống', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
