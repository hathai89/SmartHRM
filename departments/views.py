from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Department
from .forms import DepartmentForm
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from django.db import transaction
from django.db import models
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.serializers import serialize

# API Views
class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho phòng ban
    """
    queryset = Department.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from .serializers import DepartmentSerializer, DepartmentTreeSerializer

        if self.action == 'tree':
            return DepartmentTreeSerializer
        return DepartmentSerializer

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """
        Trả về cấu trúc cây phòng ban
        """
        # Lấy các phòng ban gốc (không có parent)
        root_departments = Department.objects.filter(parent=None)

        # Sử dụng serializer để chuyển đổi thành JSON
        from .serializers import DepartmentTreeSerializer
        serializer = DepartmentTreeSerializer(root_departments, many=True)

        # Trả về dữ liệu theo định dạng tương thích với frontend
        return Response({
            'success': True,
            'data': serializer.data
        })

    @action(detail=True, methods=['get'])
    def children(self, request, pk=None):
        """
        Trả về danh sách các phòng ban con trực tiếp
        """
        department = self.get_object()
        children = department.get_children()

        from .serializers import DepartmentSerializer
        serializer = DepartmentSerializer(children, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def move(self, request, pk=None):
        """
        Di chuyển phòng ban trong cây
        """
        department = self.get_object()
        parent_id = request.data.get('parent_id')
        position = request.data.get('position', 0)

        try:
            with transaction.atomic():
                if parent_id is None:
                    department.move_to(None, position)
                else:
                    parent = Department.objects.get(pk=parent_id)
                    department.move_to(parent, position)

                department.save()

                from .serializers import DepartmentSerializer
                serializer = DepartmentSerializer(department)

                return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Traditional Views
class DepartmentListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Department
    template_name = 'departments/department_list.html'
    context_object_name = 'departments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tree_departments'] = Department.objects.all()
        return context

class DepartmentDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Department
    template_name = 'departments/department_detail.html'
    context_object_name = 'department'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department = self.get_object()

        # Lấy tất cả các phòng ban con (bao gồm cả các phòng ban con của các phòng ban con)
        descendant_departments = department.get_descendants(include_self=True)

        # Lấy các phòng ban con trực tiếp
        context['direct_children'] = department.get_children()

        return context

class DepartmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/login/'
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/department_form.html'
    success_url = reverse_lazy('department-list')
    permission_required = 'departments.add_department'

    def form_valid(self, form):
        messages.success(self.request, f'Đơn vị {form.instance.name} đã được tạo thành công!')
        return super().form_valid(form)

class DepartmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/department_form.html'
    permission_required = 'departments.change_department'

    def get_success_url(self):
        return reverse_lazy('department-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, f'Đơn vị {form.instance.name} đã được cập nhật thành công!')
        return super().form_valid(form)

class DepartmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Department
    template_name = 'departments/department_confirm_delete.html'
    success_url = reverse_lazy('department-list')
    permission_required = 'departments.delete_department'

    def delete(self, request, *args, **kwargs):
        department = self.get_object()
        messages.success(request, f'Đơn vị {department.name} đã được xóa thành công!')
        return super().delete(request, *args, **kwargs)

# Chế độ xem tổng hợp phòng ban (cấu trúc + danh sách nhân viên)
@login_required(login_url='/login/')
@permission_required('departments.view_department', raise_exception=True)
def department_overview(request):
    """Hiển thị tổng quan phòng ban"""
    all_departments = Department.objects.all()

    context = {
        'all_departments': all_departments,
    }

    return render(request, 'departments/department_overview.html', context)

@login_required(login_url='/login/')
@permission_required('departments.view_department', raise_exception=True)
def department_tree_view(request):
    """Hiển thị cấu trúc cây phòng ban"""
    departments = Department.objects.all()

    context = {
        'departments': departments,
    }

    return render(request, 'departments/department_tree.html', context)

@require_http_methods(["POST"])
def update_department_position(request):
    """API để cập nhật vị trí của department trong cây phòng ban"""
    try:
        data = json.loads(request.body)
        department_id = data.get('department_id')
        parent_id = data.get('parent_id')
        position = data.get('position', 0)

        with transaction.atomic():
            department = get_object_or_404(Department, pk=department_id)

            # Nếu parent_id là None, di chuyển đến level cao nhất
            if parent_id is None:
                department.move_to(None, position)
            else:
                parent = get_object_or_404(Department, pk=parent_id)
                department.move_to(parent, position)

            department.save()

        return JsonResponse({
            'success': True,
            'message': f'Đã cập nhật vị trí cho phòng ban {department.name}'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

def get_department_tree_json(request):
    """API để lấy cấu trúc cây phòng ban dưới dạng JSON"""
    try:
        # Lấy các phòng ban gốc (không có parent)
        root_departments = Department.objects.filter(parent=None)

        # Hàm đệ quy để xây dựng cây
        def build_tree(departments):
            result = []
            for dept in departments:
                children = dept.get_children()
                # Lấy danh sách nhân viên thuộc phòng ban
                employees = dept.employees.all().values('id', 'code', 'full_name', 'avatar', 'job_title__name', 'status', 'join_date')

                # Chuyển đổi các trường để phù hợp với frontend
                employees_list = []
                for emp in employees:
                    employee_dict = {
                        'id': emp['id'],
                        'code': emp['code'],
                        'full_name': emp['full_name'],
                        'avatar': emp['avatar'],
                        'job_title_name': emp['job_title__name'],
                        'department_name': dept.name,
                        'status': emp['status'],
                        'join_date': emp['join_date']
                    }
                    employees_list.append(employee_dict)

                dept_dict = {
                    'id': dept.id,
                    'name': dept.name,
                    'code': dept.code,
                    'dept_type': dept.dept_type,
                    'type': dept.dept_type,  # Giữ lại để tương thích
                    'children': build_tree(children) if children else [],
                    'employees': employees_list
                }
                result.append(dept_dict)
            return result

        tree_data = build_tree(root_departments)

        return JsonResponse({
            'success': True,
            'data': tree_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

# API endpoint trực tiếp cho cấu trúc cây
def department_tree_api(request):
    """API endpoint trực tiếp cho cấu trúc cây phòng ban"""
    return get_department_tree_json(request)
