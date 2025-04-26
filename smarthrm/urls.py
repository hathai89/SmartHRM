# smarthrm/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Chuyển hướng trang chủ đến dashboard (middleware sẽ xử lý chuyển hướng cho nhân viên)
    path('', RedirectView.as_view(pattern_name='dashboard'), name='home'),

    # Thêm URLs cho dashboard
    path('dashboard/', include('dashboard.urls')),

    # URLs cho các ứng dụng
    path('company/', include('company.urls')),
    path('departments/', include('departments.urls')),
    path('factories/', include('factories.urls')),
    path('employees/', include('employees.urls')),
    path('documents/', include('documents.urls')),
    path('recruitment/', include('recruitment.urls')),
    path('assets/', include('assets.urls')),
    path('notifications/', include('notifications.urls')),

    # URLs cho authentication
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # URLs cho authentication (alias)
    path('accounts/login/', RedirectView.as_view(url='/login/'), name='accounts-login'),
    path('accounts/logout/', RedirectView.as_view(url='/logout/'), name='accounts-logout'),

    # CKEditor URLs
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # API URLs
    path('api/', include('api.urls')),

    # REST framework browsable API
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
