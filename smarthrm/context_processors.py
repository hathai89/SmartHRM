from django.conf import settings

def vue_settings(request):
    """
    Thêm các cài đặt Vue.js vào context của template.
    """
    return {
        'debug': settings.DEBUG,
        'api_url': '/api/',
        'static_url': settings.STATIC_URL,
        'media_url': settings.MEDIA_URL,
    }
