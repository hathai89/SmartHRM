from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.auth import AuthViewSet
from api.views.employee import EmployeeViewSet, JobTitleViewSet
from api.views.department import DepartmentViewSet, PhongBanViewSet, BoPhanViewSet, NhomViewSet
from api.views.factory import FactoryViewSet, XiNghiepViewSet, BoPhanXiNghiepViewSet, NhomXiNghiepViewSet
from api.views.document import DocumentViewSet, DocumentCategoryViewSet
from api.views.notification import NotificationViewSet
from api.views.dashboard import DashboardViewSet
from api.views.csrf import CsrfViewSet
from api.views.health import HealthCheckView
from company.api import CompanyViewSet

# Tạo router
router = DefaultRouter()

# Đăng ký các viewset
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'employees', EmployeeViewSet)
router.register(r'job-titles', JobTitleViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'phong-ban', PhongBanViewSet)
router.register(r'bo-phan', BoPhanViewSet)
router.register(r'nhom', NhomViewSet)
router.register(r'factories', FactoryViewSet)
router.register(r'xi-nghiep', XiNghiepViewSet)
router.register(r'bo-phan-xi-nghiep', BoPhanXiNghiepViewSet)
router.register(r'nhom-xi-nghiep', NhomXiNghiepViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'document-categories', DocumentCategoryViewSet)
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'csrf', CsrfViewSet, basename='csrf')
router.register(r'company', CompanyViewSet, basename='company')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
    path('health-check/', HealthCheckView.as_view(), name='health-check'),

    # Include departments and factories API endpoints
    path('', include('departments.urls')),
    path('', include('factories.urls')),
    path('recruitment/', include('recruitment.urls')),
]
