from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'short_name', 'tax_code', 'logo')
        }),
        ('Thông tin liên hệ', {
            'fields': ('address', 'phone', 'email', 'website', 'fax')
        }),
        ('Người đại diện', {
            'fields': ('representative', 'position')
        }),
        ('Phòng nhân sự / Tuyển dụng', {
            'fields': ('hr_department', 'hr_phone', 'career_email')
        }),
        ('Thông tin bổ sung', {
            'fields': ('description', 'foundation_date')
        }),
        ('Thông tin hệ thống', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    list_display = ('name', 'tax_code', 'phone', 'email', 'representative')
    search_fields = ('name', 'tax_code', 'representative', 'phone', 'email')
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        # Chỉ cho phép tạo công ty nếu chưa có công ty nào
        return Company.objects.count() == 0

    def has_delete_permission(self, request, obj=None):
        # Không cho phép xóa công ty nếu chỉ có 1 công ty
        return Company.objects.count() > 1
