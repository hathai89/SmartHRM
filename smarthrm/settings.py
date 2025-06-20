"""
Django settings for smarthrm project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Import cấu hình REST framework và CORS
from .settings_rest import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@9!d(kf1ybc@k#wxz08+j-^+47s8njq+7yk0$n68=mw%00v7bk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps của bên thứ ba
    'mptt',  # Để quản lý cấu trúc cây phân cấp
    'crispy_forms',
    'crispy_bootstrap5',
    'channels',  # Django Channels cho WebSocket
    'ckeditor',   # CKEditor cho trình soạn thảo văn bản
    'ckeditor_uploader',  # Cho phép upload ảnh trong CKEditor
    'rest_framework',  # Django REST framework
    'rest_framework.authtoken',  # Token authentication
    'corsheaders',  # CORS headers

    # App chính của dự án
    'smarthrm',
    'app_settings',  # App cấu hình hệ thống

    # Apps của dự án
    'company',
    'departments',
    'factories',
    'employees',
    'documents',
    'dashboard',
    'recruitment',

    # Apps mới
    'assets',
    'notifications',
    'api',  # API endpoints
]

# Cấu hình Crispy Forms sử dụng Bootstrap 5
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'employees.middleware.FirstLoginMiddleware',  # Middleware kiểm tra đăng nhập lần đầu
    'api.middleware.CsrfTokenMiddleware',  # Middleware để thêm CSRF token vào response header
    'smarthrm.middleware.BreadcrumbMiddleware',  # Middleware để cung cấp breadcrumbs
]

# CSRF settings
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
CSRF_COOKIE_HTTPONLY = False  # Set to True in production
CSRF_USE_SESSIONS = False  # Store CSRF token in cookie instead of session
CSRF_COOKIE_SAMESITE = None  # Allow cross-site requests in development
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8080',
    'http://127.0.0.1:8080',
    'http://localhost:8081',
    'http://127.0.0.1:8081',
    'http://localhost:8082',
    'http://127.0.0.1:8082',
    'http://localhost:8083',
    'http://127.0.0.1:8083',
    'http://localhost:8084',
    'http://127.0.0.1:8084',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

ROOT_URLCONF = 'smarthrm.urls'

# Cấu hình templates và static files
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'app_settings.context_processors.export_settings',
                'company.context_processors.company_info',
                'smarthrm.context_processors.vue_settings',
            ],
            'builtins': [
                'django.templatetags.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'smarthrm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# Cấu hình kết nối SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Cấu hình Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 1


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'vi'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'static/vue',  # Vue.js build output
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Cấu hình để phục vụ Vue.js SPA
VUE_STATIC_DIR = BASE_DIR / 'static/vue'
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'



# Cấu hình Channels
ASGI_APPLICATION = 'smarthrm.asgi.application'

# Cấu hình Channel Layers
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

# Cấu hình email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Development
DEFAULT_FROM_EMAIL = 'noreply@smarthrm.com'
SITE_URL = 'http://127.0.0.1:8000'

# Cấu hình Redis cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}',
    }
}

# Thời gian cache
CACHE_TTL = 60 * 15  # 15 phút

# Cấu hình thông báo (messages)
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'primary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# Cấu hình CKEditor
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_JQUERY_URL = 'https://code.jquery.com/jquery-3.6.0.min.js'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['Image', 'Table', 'HorizontalRule'],
            ['TextColor', 'BGColor'],
            ['Smiley', 'SpecialChar'],
            ['Source'],
        ],
        'height': 300,
        'width': '100%',
        'language': 'vi',
        'extraPlugins': 'justify,font,colorbutton,colordialog',
        'customConfig': '/static/js/ckeditor_config.js',
    },
    'probation_contract': {
        'toolbar': 'Full',
        'toolbar_Full': [
            ['Format', 'Font', 'FontSize'],
            ['Bold', 'Italic', 'Underline', 'Strike', '-',
                'TextColor', 'BGColor', '-', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['Image', 'Table', 'HorizontalRule'],
            ['Maximize', 'Source'],
        ],
        'height': 600,
        'width': '100%',
        'language': 'vi',
        'font_names': 'Times New Roman/Times New Roman, Times, serif;' +
                      'Arial/Arial, Helvetica, sans-serif;' +
                      'Courier New/Courier New, Courier, monospace;' +
                      'Georgia/Georgia, serif;' +
                      'Verdana/Verdana, Geneva, sans-serif',
        'fontSize_sizes': '8/8px;9/9px;10/10px;11/11px;12/12px;14/14px;16/16px;18/18px;20/20px;22/22px;24/24px;26/26px;28/28px;36/36px;48/48px;72/72px',
        'extraPlugins': 'justify,font,colorbutton,colordialog,tableresize,tabletools',
        'customConfig': '/static/js/ckeditor_config.js',
    },
    'custom_terms': {
        'toolbar': 'Basic',
        'toolbar_Basic': [
            ['Bold', 'Italic', 'Underline', 'Strike', '-', 'TextColor'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['Table', 'HorizontalRule'],
            ['Source'],
        ],
        'height': 300,
        'width': '100%',
        'language': 'vi',
        'extraPlugins': 'justify,colorbutton',
        'customConfig': '/static/js/ckeditor_config.js',
    },
}
