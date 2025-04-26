from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Employee, JobTitle
from .forms import EmployeeForm

@login_required
def employee_list(request):
    """
    Hiển thị danh sách nhân viên
    """
    employees = Employee.objects.all()
    context = {
        'title': 'Danh sách nhân viên',
        'employees': employees
    }
    return render(request, 'employees/employee_list.html', context)

@login_required
def employee_detail(request, pk):
    """
    Hiển thị chi tiết nhân viên
    """
    employee = get_object_or_404(Employee, pk=pk)
    context = {
        'title': f'Chi tiết nhân viên: {employee.full_name}',
        'employee': employee
    }
    return render(request, 'employees/employee_detail.html', context)

@login_required
def employee_create(request):
    """
    Tạo nhân viên mới
    """
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'Nhân viên {employee.full_name} đã được tạo thành công!')
            return redirect('employee-detail', pk=employee.pk)
    else:
        form = EmployeeForm()

    context = {
        'title': 'Thêm nhân viên mới',
        'form': form
    }
    return render(request, 'employees/employee_form.html', context)

@login_required
def employee_update(request, pk):
    """
    Cập nhật thông tin nhân viên
    """
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'Thông tin nhân viên {employee.full_name} đã được cập nhật!')
            return redirect('employee-detail', pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)

    context = {
        'title': f'Cập nhật nhân viên: {employee.full_name}',
        'form': form,
        'employee': employee
    }
    return render(request, 'employees/employee_form.html', context)
