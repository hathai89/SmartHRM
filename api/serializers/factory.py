from rest_framework import serializers
from factories.models import Factory, XiNghiep, BoPhanXiNghiep, NhomXiNghiep

class FactorySerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Factory
        fields = ['id', 'name', 'code', 'factory_type', 'parent', 'parent_name', 'is_active', 'employee_count']
    
    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None
    
    def get_employee_count(self, obj):
        return obj.employees.count()

class FactoryDetailSerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Factory
        fields = '__all__'
    
    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None
    
    def get_children(self, obj):
        children = Factory.objects.filter(parent=obj)
        return FactorySerializer(children, many=True).data

class XiNghiepSerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = XiNghiep
        fields = ['id', 'name', 'code', 'parent', 'parent_name', 'is_active', 'employee_count']
    
    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None
    
    def get_employee_count(self, obj):
        return obj.employees.count()

class BoPhanXiNghiepSerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BoPhanXiNghiep
        fields = ['id', 'name', 'code', 'parent', 'parent_name', 'is_active', 'employee_count']
    
    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None
    
    def get_employee_count(self, obj):
        return obj.employees.count()

class NhomXiNghiepSerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = NhomXiNghiep
        fields = ['id', 'name', 'code', 'parent', 'parent_name', 'is_active', 'employee_count']
    
    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None
    
    def get_employee_count(self, obj):
        return obj.employees.count()
