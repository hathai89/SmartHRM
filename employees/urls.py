from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Trang danh sách nhân viên
    path('', views.employee_list, name='employee-list'),

    # Trang chi tiết nhân viên
    path('<int:pk>/', views.employee_detail, name='employee-detail'),

    # Trang thêm nhân viên mới
    path('add/', views.employee_create, name='employee-create'),

    # Trang chỉnh sửa nhân viên
    path('<int:pk>/edit/', views.employee_update, name='employee-update'),

    # Trang đổi mật khẩu
    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='employees/change_password.html',
        success_url='/employees/change-password-done/'
    ), name='change_password'),

    # Trang đổi mật khẩu thành công
    path('change-password-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='employees/change_password_done.html'
    ), name='change_password_done'),
]
