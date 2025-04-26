from django.contrib.auth.models import User
from rest_framework import serializers
from employees.models import Employee

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'avatar', 'is_staff', 'is_superuser']
        read_only_fields = ['id', 'is_staff', 'is_superuser']

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username

    def get_avatar(self, obj):
        try:
            if hasattr(obj, 'employee') and obj.employee.avatar:
                return obj.employee.avatar.url
        except:
            pass
        return None

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_password = serializers.CharField(required=True, min_length=8)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Mật khẩu cũ không đúng")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Mật khẩu xác nhận không khớp"})
        return data
