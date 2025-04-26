from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Employee
from notifications.services import create_notification

@receiver(post_save, sender=Employee)
def create_user_for_employee(sender, instance, created, **kwargs):
    """
    Tạo tài khoản người dùng cho nhân viên mới
    """
    if created and not instance.user:
        # Tạo tên người dùng từ mã nhân viên
        username = instance.code.lower()

        # Tạo email từ email nhân viên
        email = instance.email

        # Tạo mật khẩu mặc định từ mã nhân viên
        password = f"{username}@123"

        # Tạo tài khoản người dùng
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=instance.first_name,
            last_name=instance.last_name
        )

        # Liên kết tài khoản người dùng với nhân viên
        instance.user = user
        instance.save(update_fields=['user'])

        # Gửi thông báo cho admin
        try:
            admin_users = User.objects.filter(is_superuser=True)
            for admin in admin_users:
                create_notification(
                    recipient=admin,
                    title="Nhân viên mới được tạo",
                    message=f"Nhân viên {instance.full_name} ({instance.code}) đã được tạo thành công.",
                    notification_type="system",
                    priority="normal",
                    link=f"/employees/{instance.id}/"
                )
        except:
            pass
