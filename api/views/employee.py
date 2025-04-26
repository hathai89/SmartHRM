from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from employees.models import Employee, JobTitle
from api.serializers.employee import (
    EmployeeListSerializer, EmployeeDetailSerializer, 
    EmployeeCreateSerializer, EmployeeUpdateSerializer,
    JobTitleSerializer
)

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho quản lý nhân viên
    """
    queryset = Employee.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['code', 'first_name', 'last_name', 'full_name', 'email', 'phone_number']
    ordering_fields = ['code', 'full_name', 'job_title__name', 'department__name', 'factory__name', 'status', 'is_active']
    ordering = ['code']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EmployeeListSerializer
        elif self.action == 'create':
            return EmployeeCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return EmployeeUpdateSerializer
        return EmployeeDetailSerializer
    
    def get_queryset(self):
        queryset = Employee.objects.all()
        
        # Lọc theo phòng ban
        department = self.request.query_params.get('department')
        if department:
            queryset = queryset.filter(department_id=department)
        
        # Lọc theo xí nghiệp
        factory = self.request.query_params.get('factory')
        if factory:
            queryset = queryset.filter(factory_id=factory)
        
        # Lọc theo trạng thái
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Lọc theo trạng thái hoạt động
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Lấy thông tin nhân viên của người dùng hiện tại
        """
        try:
            employee = request.user.employee
            serializer = EmployeeDetailSerializer(employee)
            return Response(serializer.data)
        except:
            return Response(
                {'detail': 'Không tìm thấy thông tin nhân viên'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def update_password_changed(self, request, pk=None):
        """
        Cập nhật trạng thái đã đổi mật khẩu
        """
        employee = self.get_object()
        
        # Kiểm tra quyền
        if not request.user.is_superuser and request.user != employee.user:
            return Response(
                {'detail': 'Bạn không có quyền thực hiện hành động này'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        employee.password_changed = True
        employee.save()
        
        return Response({'detail': 'Cập nhật trạng thái đổi mật khẩu thành công'})

class JobTitleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint cho chức danh
    """
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'department_type', 'position_type', 'is_active']
    ordering = ['name']
    
    def get_queryset(self):
        queryset = JobTitle.objects.all()
        
        # Lọc theo loại phòng ban
        department_type = self.request.query_params.get('department_type')
        if department_type:
            queryset = queryset.filter(department_type=department_type)
        
        # Lọc theo loại vị trí
        position_type = self.request.query_params.get('position_type')
        if position_type:
            queryset = queryset.filter(position_type=position_type)
        
        # Lọc theo trạng thái hoạt động
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        
        return queryset
