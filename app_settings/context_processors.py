from .models import SiteSetting

def export_settings(request):
    """
    Context processor để xuất các cài đặt hệ thống vào template
    """
    settings = {}
    try:
        site_settings = SiteSetting.objects.filter(is_active=True)
        for setting in site_settings:
            settings[setting.key] = setting.value
    except:
        # Nếu bảng chưa được tạo hoặc có lỗi, trả về dict rỗng
        pass
    
    return {'site_settings': settings}
