from rest_framework import serializers
from employees.models import Employee, JobTitle
from departments.models import Department
from factories.models import Factory
from django.contrib.auth.models import User

class JobTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitle
        fields = ['id', 'name', 'code', 'department_type', 'position_type', 'is_active']

class EmployeeListSerializer(serializers.ModelSerializer):
    job_title_name = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()
    factory_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = [
            'id', 'code', 'full_name', 'job_title', 'job_title_name', 
            'department', 'department_name', 'factory', 'factory_name',
            'status', 'is_active', 'avatar'
        ]
    
    def get_job_title_name(self, obj):
        return obj.job_title.name if obj.job_title else None
    
    def get_department_name(self, obj):
        return obj.department.name if obj.department else None
    
    def get_factory_name(self, obj):
        return obj.factory.name if obj.factory else None

class EmployeeDetailSerializer(serializers.ModelSerializer):
    job_title_name = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()
    factory_name = serializers.SerializerMethodField()
    user_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['id', 'code', 'user', 'password_changed']
    
    def get_job_title_name(self, obj):
        return obj.job_title.name if obj.job_title else None
    
    def get_department_name(self, obj):
        return obj.department.name if obj.department else None
    
    def get_factory_name(self, obj):
        return obj.factory.name if obj.factory else None
    
    def get_user_info(self, obj):
        if obj.user:
            return {
                'id': obj.user.id,
                'username': obj.user.username,
                'email': obj.user.email,
                'is_active': obj.user.is_active,
                'is_staff': obj.user.is_staff,
                'is_superuser': obj.user.is_superuser,
            }
        return None

class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ['user', 'password_changed']
        
    def validate(self, data):
        # Kiểm tra ràng buộc: Nếu workplace_type là department thì phải chọn department
        if data.get('workplace_type') == 'department' and not data.get('department'):
            raise serializers.ValidationError({"department": "Vui lòng chọn phòng ban."})
        
        # Kiểm tra ràng buộc: Nếu workplace_type là factory thì phải chọn factory
        if data.get('workplace_type') == 'factory' and not data.get('factory'):
            raise serializers.ValidationError({"factory": "Vui lòng chọn xí nghiệp."})
        
        return data

class EmployeeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ['user', 'code', 'password_changed']
        
    def validate(self, data):
        # Kiểm tra ràng buộc: Nếu workplace_type là department thì phải chọn department
        if data.get('workplace_type') == 'department' and not data.get('department'):
            raise serializers.ValidationError({"department": "Vui lòng chọn phòng ban."})
        
        # Kiểm tra ràng buộc: Nếu workplace_type là factory thì phải chọn factory
        if data.get('workplace_type') == 'factory' and not data.get('factory'):
            raise serializers.ValidationError({"factory": "Vui lòng chọn xí nghiệp."})
        
        return data
