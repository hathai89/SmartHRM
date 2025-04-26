from django.conf import settings

def export_settings(request):
    """
    Xuất các cài đặt cần thiết cho templates
    """
    return {
        'SITE_NAME': 'SmartHRM',
        'SITE_VERSION': '1.0.0',
        'SITE_DESCRIPTION': 'Hệ thống quản lý nhân sự thông minh',
        'SITE_URL': settings.SITE_URL,
        'COMPANY_NAME': 'SmartHRM',
        'COMPANY_ADDRESS': 'Hà Nội, Việt Nam',
        'COMPANY_PHONE': '0123456789',
        'COMPANY_EMAIL': 'info@smarthrm.vn',
        'COMPANY_WEBSITE': 'https://smarthrm.vn',
        'SUPPORT_EMAIL': 'support@smarthrm.vn',
        'SUPPORT_PHONE': '0123456789',
        'COPYRIGHT_YEAR': '2024',
        'COPYRIGHT_TEXT': '© 2024 SmartHRM. Bản quyền thuộc về SmartHRM.',
    }
