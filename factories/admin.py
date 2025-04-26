from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Factory, XiNghiep, BoPhanXiNghiep, NhomXiNghiep

@admin.register(Factory)
class FactoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'code', 'factory_type', 'is_active')
    list_filter = ('factory_type', 'is_active')
    search_fields = ('name', 'code')
    mptt_level_indent = 20

@admin.register(XiNghiep)
class XiNghiepAdmin(MPTTModelAdmin):
    list_display = ('name', 'code', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')
    mptt_level_indent = 20

@admin.register(BoPhanXiNghiep)
class BoPhanXiNghiepAdmin(MPTTModelAdmin):
    list_display = ('name', 'code', 'is_active', 'parent')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')
    mptt_level_indent = 20

@admin.register(NhomXiNghiep)
class NhomXiNghiepAdmin(MPTTModelAdmin):
    list_display = ('name', 'code', 'is_active', 'parent')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')
    mptt_level_indent = 20
