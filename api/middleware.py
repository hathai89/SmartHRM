from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import get_token

class CsrfTokenMiddleware(MiddlewareMixin):
    """
    Middleware để thêm CSRF token vào response header
    """
    def process_response(self, request, response):
        # Thêm CSRF token vào header cho tất cả các response
        response['X-CSRFToken'] = get_token(request)
        return response
