# smarthrm/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView, TemplateView
# Imports for views are now handled in their respective apps
from django.views.decorators.csrf import ensure_csrf_cookie

urlpatterns = [
    path('admin/', admin.site.urls),

    # Serve Vue.js SPA
    path('', ensure_csrf_cookie(TemplateView.as_view(template_name='vue_index.html')), name='vue-index'),

    # Catch all routes for Vue.js router
    path('dashboard/', ensure_csrf_cookie(TemplateView.as_view(template_name='vue_index.html')), name='vue-dashboard'),
    path('company/', ensure_csrf_cookie(TemplateView.as_view(template_name='vue_index.html')), name='vue-company'),
    path('departments/', ensure_csrf_cookie(TemplateView.as_view(template_name='vue_index.html')), name='vue-departments'),
    path('factories/', ensure_csrf_cookie(TemplateView.as_view(template_name='vue_index.html')), name='vue-factories'),
    path('employees/', ensure_csrf_cookie(TemplateView.as_view(template_name='vue_index.html')), name='vue-employees'),
    path('documents/', ensure_csrf_cookie(TemplateView.as_view(template_name='vue_index.html')), name='vue-documents'),
    path('recruitment/', ensure_csrf_cookie(TemplateView.as_view(template_name='vue_index.html')), name='vue-recruitment'),
    path('assets/', ensure_csrf_cookie(TemplateView.as_view(template_name='vue_index.html')), name='vue-assets'),
    path('notifications/', ensure_csrf_cookie(TemplateView.as_view(template_name='vue_index.html')), name='vue-notifications'),
    path('profile/', ensure_csrf_cookie(TemplateView.as_view(template_name='vue_index.html')), name='vue-profile'),
    path('settings/', ensure_csrf_cookie(TemplateView.as_view(template_name='vue_index.html')), name='vue-settings'),
    path('login/', ensure_csrf_cookie(TemplateView.as_view(template_name='vue_index.html')), name='vue-login'),

    # Legacy URLs for API compatibility
    path('accounts/login/', RedirectView.as_view(url='/login/'), name='accounts-login'),
    path('accounts/logout/', RedirectView.as_view(url='/logout/'), name='accounts-logout'),

    # CKEditor URLs
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # API URLs
    path('api/', include('api.urls')),

    # App URLs
    path('', include('departments.urls')),
    path('', include('factories.urls')),
    path('', include('recruitment.urls')),

    # Direct API endpoints for tree structures are now defined in their respective apps

    # REST framework browsable API
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
