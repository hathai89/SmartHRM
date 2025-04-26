from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User

class FirstLoginMiddleware:
    """
    Middleware kiểm tra đăng nhập lần đầu của nhân viên
    Nếu nhân viên đăng nhập lần đầu, chuyển hướng đến trang đổi mật khẩu
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Kiểm tra nếu người dùng đã đăng nhập
        if request.user.is_authenticated:
            # Kiểm tra nếu người dùng có liên kết với nhân viên
            try:
                employee = request.user.employee
                # Kiểm tra nếu nhân viên chưa đổi mật khẩu
                if not employee.password_changed:
                    # Nếu không phải đang ở trang đổi mật khẩu, chuyển hướng đến trang đổi mật khẩu
                    if request.path != reverse('change_password'):
                        return redirect('change_password')
            except:
                # Nếu người dùng không có liên kết với nhân viên, bỏ qua
                pass

        response = self.get_response(request)
        return response
