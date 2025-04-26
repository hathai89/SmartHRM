from django.contrib import admin
from .models import Asset, AssetCategory, AssetAssignment, AssetMaintenance, AssetInventory, AssetInventoryItem

@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'status', 'asset_type')
    list_filter = ('status', 'asset_type', 'category')
    search_fields = ('name', 'code', 'serial_number')

@admin.register(AssetAssignment)
class AssetAssignmentAdmin(admin.ModelAdmin):
    list_display = ('asset', 'employee', 'assigned_date', 'status')
    list_filter = ('status',)
    search_fields = ('asset__name', 'asset__code', 'employee__full_name')

@admin.register(AssetMaintenance)
class AssetMaintenanceAdmin(admin.ModelAdmin):
    list_display = ('asset', 'maintenance_type', 'start_date', 'end_date', 'status')
    list_filter = ('status',)
    search_fields = ('asset__name', 'asset__code', 'maintenance_type')

@admin.register(AssetInventory)
class AssetInventoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'status')
    list_filter = ('status',)
    search_fields = ('title',)

@admin.register(AssetInventoryItem)
class AssetInventoryItemAdmin(admin.ModelAdmin):
    list_display = ('inventory', 'asset', 'status')
    list_filter = ('status',)
    search_fields = ('inventory__title', 'asset__name', 'asset__code')
