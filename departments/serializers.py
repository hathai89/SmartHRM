from rest_framework import serializers
from .models import Department
from employees.models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer cho model Employee trong context của Department"""
    job_title_name = serializers.CharField(source='job_title.name', read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'code', 'full_name', 'avatar', 'job_title_name', 'status', 'join_date']

class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer cho model Department"""

    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'description', 'dept_type', 'company', 'parent',
                 'is_active', 'manager_name', 'manager_title', 'manager_email',
                 'manager_phone', 'location', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class DepartmentTreeSerializer(serializers.ModelSerializer):
    """Serializer cho cấu trúc cây Department"""
    children = serializers.SerializerMethodField()
    type_display = serializers.CharField(source='get_dept_type_display', read_only=True)
    employees = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'dept_type', 'type_display', 'children', 'is_active', 'employees']

    def get_children(self, obj):
        """Lấy danh sách các phòng ban con trực tiếp"""
        children = obj.get_children()
        serializer = DepartmentTreeSerializer(children, many=True)
        return serializer.data

    def get_employees(self, obj):
        """Lấy danh sách nhân viên thuộc phòng ban"""
        employees = obj.employees.all()
        serializer = EmployeeSerializer(employees, many=True)
        return serializer.data
