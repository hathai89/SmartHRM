from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    """
    Hiển thị trang dashboard
    """
    # Thêm breadcrumbs
    request.breadcrumbs = [
        {'title': 'Bảng điều khiển', 'url': '#'}
    ]

    context = {
        'title': 'Bảng điều khiển',
        'breadcrumbs': request.breadcrumbs,
    }
    return render(request, 'dashboard/index.html', context)
