from rest_framework import serializers
from .models import Department

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
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'dept_type', 'type_display', 'children', 'is_active']
    
    def get_children(self, obj):
        """Lấy danh sách các phòng ban con trực tiếp"""
        children = obj.get_children()
        serializer = DepartmentTreeSerializer(children, many=True)
        return serializer.data
