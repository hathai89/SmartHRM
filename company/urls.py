from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from .api import CompanyViewSet

# Tạo router cho API
router = DefaultRouter()
router.register(r'api', CompanyViewSet)

urlpatterns = [
    # Chuyển hướng đến trang admin khi truy cập vào /company/
    path('', RedirectView.as_view(pattern_name='admin:company_company_changelist'), name='company-list'),

    # API endpoints
    path('', include(router.urls)),
]
