from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from departments.models import Department, PhongBan, BoPhan, Nhom
from api.serializers.department import (
    DepartmentSerializer, DepartmentDetailSerializer,
    PhongBanSerializer, BoPhanSerializer, NhomSerializer
)
from api.serializers.employee import EmployeeListSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho quản lý phòng ban
    """
    queryset = Department.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'dept_type', 'is_active']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DepartmentDetailSerializer
        return DepartmentSerializer
    
    def get_queryset(self):
        queryset = Department.objects.all()
        
        # Lọc theo loại phòng ban
        dept_type = self.request.query_params.get('dept_type')
        if dept_type:
            queryset = queryset.filter(dept_type=dept_type)
        
        # Lọc theo phòng ban cha
        parent = self.request.query_params.get('parent')
        if parent:
            if parent == 'null':
                queryset = queryset.filter(parent__isnull=True)
            else:
                queryset = queryset.filter(parent_id=parent)
        
        # Lọc theo trạng thái hoạt động
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """
        Lấy danh sách nhân viên thuộc phòng ban
        """
        department = self.get_object()
        employees = department.employees.all()
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)

class PhongBanViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho quản lý phòng ban (PhongBan)
    """
    queryset = PhongBan.objects.all()
    serializer_class = PhongBanSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'is_active']
    ordering = ['name']
    
    def get_queryset(self):
        queryset = PhongBan.objects.all()
        
        # Lọc theo phòng ban cha
        parent = self.request.query_params.get('parent')
        if parent:
            if parent == 'null':
                queryset = queryset.filter(parent__isnull=True)
            else:
                queryset = queryset.filter(parent_id=parent)
        
        # Lọc theo trạng thái hoạt động
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """
        Lấy danh sách nhân viên thuộc phòng ban
        """
        phongban = self.get_object()
        employees = phongban.employees.all()
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)

class BoPhanViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho quản lý bộ phận (BoPhan)
    """
    queryset = BoPhan.objects.all()
    serializer_class = BoPhanSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'is_active']
    ordering = ['name']
    
    def get_queryset(self):
        queryset = BoPhan.objects.all()
        
        # Lọc theo phòng ban cha
        parent = self.request.query_params.get('parent')
        if parent:
            if parent == 'null':
                queryset = queryset.filter(parent__isnull=True)
            else:
                queryset = queryset.filter(parent_id=parent)
        
        # Lọc theo trạng thái hoạt động
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """
        Lấy danh sách nhân viên thuộc bộ phận
        """
        bophan = self.get_object()
        employees = bophan.employees.all()
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)

class NhomViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho quản lý nhóm (Nhom)
    """
    queryset = Nhom.objects.all()
    serializer_class = NhomSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'is_active']
    ordering = ['name']
    
    def get_queryset(self):
        queryset = Nhom.objects.all()
        
        # Lọc theo bộ phận cha
        parent = self.request.query_params.get('parent')
        if parent:
            if parent == 'null':
                queryset = queryset.filter(parent__isnull=True)
            else:
                queryset = queryset.filter(parent_id=parent)
        
        # Lọc theo trạng thái hoạt động
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """
        Lấy danh sách nhân viên thuộc nhóm
        """
        nhom = self.get_object()
        employees = nhom.employees.all()
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)
