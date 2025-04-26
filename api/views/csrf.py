from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

@method_decorator(ensure_csrf_cookie, name='dispatch')
class CsrfViewSet(viewsets.ViewSet):
    """
    API endpoint để lấy CSRF token
    """
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['get'])
    def token(self, request):
        """
        Lấy CSRF token
        """
        token = get_token(request)
        return Response({'csrfToken': token})
