from django.contrib import admin
from .models import Employee, JobTitle

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('code', 'full_name', 'job_title', 'status', 'is_active')
    list_filter = ('status', 'is_active', 'gender', 'contract_type')
    search_fields = ('code', 'first_name', 'last_name', 'full_name', 'email', 'phone_number')
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('code', 'attendance_code', 'first_name', 'last_name', 'gender', 'date_of_birth', 'avatar')
        }),
        ('Thông tin liên hệ', {
            'fields': ('email', 'phone_number', 'permanent_address', 'current_address')
        }),
        ('Thông tin công việc', {
            'fields': ('job_title', 'join_date', 'contract_type', 'workplace_type', 'department', 'factory')
        }),
        ('Thông tin CCCD/CMND', {
            'fields': ('id_card_number', 'id_card_issue_date', 'id_card_issue_place', 'id_card_front_image', 'id_card_back_image')
        }),
        ('Trạng thái', {
            'fields': ('status', 'is_active')
        }),
        ('Tài khoản', {
            'fields': ('user', 'password_changed')
        }),
    )

@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department_type', 'position_type', 'is_active')
    list_filter = ('department_type', 'position_type', 'is_active')
    search_fields = ('name', 'code')
