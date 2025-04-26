from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer cho model Company
    """
    logo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'short_name', 'tax_code', 'address', 'phone', 
            'email', 'website', 'representative', 'position', 'hr_department',
            'hr_phone', 'career_email', 'logo', 'logo_url', 'fax', 'description',
            'foundation_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_logo_url(self, obj):
        """
        Lấy URL đầy đủ của logo
        """
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None
