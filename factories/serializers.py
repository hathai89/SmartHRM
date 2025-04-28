from rest_framework import serializers
from .models import Factory

class FactorySerializer(serializers.ModelSerializer):
    """Serializer cho model Factory"""
    
    class Meta:
        model = Factory
        fields = ['id', 'name', 'code', 'description', 'factory_type', 'company', 'parent', 
                 'is_active', 'manager_name', 'manager_title', 'manager_email', 
                 'manager_phone', 'location', 'capacity', 'established_date', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class FactoryTreeSerializer(serializers.ModelSerializer):
    """Serializer cho cấu trúc cây Factory"""
    children = serializers.SerializerMethodField()
    type_display = serializers.CharField(source='get_factory_type_display', read_only=True)
    
    class Meta:
        model = Factory
        fields = ['id', 'name', 'code', 'factory_type', 'type_display', 'children', 'is_active']
    
    def get_children(self, obj):
        """Lấy danh sách các xí nghiệp con trực tiếp"""
        children = obj.get_children()
        serializer = FactoryTreeSerializer(children, many=True)
        return serializer.data
