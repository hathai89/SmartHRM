from rest_framework import serializers
from departments.models import Department, PhongBan, BoPhan, Nhom

class DepartmentSerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'dept_type', 'parent', 'parent_name', 'is_active', 'employee_count']
    
    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None
    
    def get_employee_count(self, obj):
        return obj.employees.count()

class DepartmentDetailSerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = '__all__'
    
    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None
    
    def get_children(self, obj):
        children = Department.objects.filter(parent=obj)
        return DepartmentSerializer(children, many=True).data

class PhongBanSerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = PhongBan
        fields = ['id', 'name', 'code', 'parent', 'parent_name', 'is_active', 'employee_count']
    
    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None
    
    def get_employee_count(self, obj):
        return obj.employees.count()

class BoPhanSerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BoPhan
        fields = ['id', 'name', 'code', 'parent', 'parent_name', 'is_active', 'employee_count']
    
    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None
    
    def get_employee_count(self, obj):
        return obj.employees.count()

class NhomSerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Nhom
        fields = ['id', 'name', 'code', 'parent', 'parent_name', 'is_active', 'employee_count']
    
    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None
    
    def get_employee_count(self, obj):
        return obj.employees.count()
