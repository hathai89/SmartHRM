from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import JobApplication, JobPosting
from notifications.services import create_notification

@receiver(post_save, sender=JobApplication)
def notify_new_application(sender, instance, created, **kwargs):
    """
    Gửi thông báo khi có đơn ứng tuyển mới
    """
    if created:
        # Tìm người tạo tin tuyển dụng
        job_creator = instance.job_posting.created_by

        if job_creator:
            # Gửi thông báo cho người tạo tin tuyển dụng
            create_notification(
                recipient=job_creator,
                title="Đơn ứng tuyển mới",
                message=f"{instance.full_name} đã ứng tuyển vào vị trí {instance.job_posting.title}",
                notification_type="recruitment",
                priority="normal",
                link=f"/recruitment/applications/{instance.id}/",
                related_object=instance
            )

        # Gửi thông báo cho admin
        try:
            admin_users = User.objects.filter(is_superuser=True)
            for admin in admin_users:
                if admin != job_creator:  # Không gửi lại cho người tạo tin
                    create_notification(
                        recipient=admin,
                        title="Đơn ứng tuyển mới",
                        message=f"{instance.full_name} đã ứng tuyển vào vị trí {instance.job_posting.title}",
                        notification_type="recruitment",
                        priority="normal",
                        link=f"/recruitment/applications/{instance.id}/",
                        related_object=instance
                    )
        except:
            pass

@receiver(post_save, sender=JobPosting)
def notify_job_posting_status_change(sender, instance, created, **kwargs):
    """
    Gửi thông báo khi trạng thái tin tuyển dụng thay đổi
    """
    if not created and instance.status in ['published', 'closed', 'cancelled']:
        # Tìm người tạo tin tuyển dụng
        job_creator = instance.created_by

        if job_creator:
            status_text = {
                'published': 'đã được đăng',
                'closed': 'đã đóng',
                'cancelled': 'đã bị hủy'
            }

            # Gửi thông báo cho người tạo tin tuyển dụng
            create_notification(
                recipient=job_creator,
                title="Cập nhật tin tuyển dụng",
                message=f"Tin tuyển dụng '{instance.title}' {status_text.get(instance.status)}",
                notification_type="recruitment",
                priority="normal",
                link=f"/recruitment/jobs/{instance.id}/",
                related_object=instance
            )
