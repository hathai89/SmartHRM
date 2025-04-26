from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Department, PhongBan, BoPhan, Nhom

@admin.register(Department)
class DepartmentAdmin(MPTTModelAdmin):
    list_display = ('name', 'code', 'dept_type', 'is_active')
    list_filter = ('dept_type', 'is_active')
    search_fields = ('name', 'code')
    mptt_level_indent = 20

@admin.register(PhongBan)
class PhongBanAdmin(MPTTModelAdmin):
    list_display = ('name', 'code', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')
    mptt_level_indent = 20

@admin.register(BoPhan)
class BoPhanAdmin(MPTTModelAdmin):
    list_display = ('name', 'code', 'is_active', 'parent')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')
    mptt_level_indent = 20

@admin.register(Nhom)
class NhomAdmin(MPTTModelAdmin):
    list_display = ('name', 'code', 'is_active', 'parent')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')
    mptt_level_indent = 20
