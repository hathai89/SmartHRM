from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from factories.models import Factory, XiNghiep, BoPhanXiNghiep, NhomXiNghiep
from api.serializers.factory import (
    FactorySerializer, FactoryDetailSerializer,
    XiNghiepSerializer, BoPhanXiNghiepSerializer, NhomXiNghiepSerializer
)
from api.serializers.employee import EmployeeListSerializer

class FactoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho quản lý xí nghiệp
    """
    queryset = Factory.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'factory_type', 'is_active']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FactoryDetailSerializer
        return FactorySerializer
    
    def get_queryset(self):
        queryset = Factory.objects.all()
        
        # Lọc theo loại xí nghiệp
        factory_type = self.request.query_params.get('factory_type')
        if factory_type:
            queryset = queryset.filter(factory_type=factory_type)
        
        # Lọc theo xí nghiệp cha
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
        Lấy danh sách nhân viên thuộc xí nghiệp
        """
        factory = self.get_object()
        employees = factory.employees.all()
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)

class XiNghiepViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho quản lý xí nghiệp (XiNghiep)
    """
    queryset = XiNghiep.objects.all()
    serializer_class = XiNghiepSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'is_active']
    ordering = ['name']
    
    def get_queryset(self):
        queryset = XiNghiep.objects.all()
        
        # Lọc theo xí nghiệp cha
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
        Lấy danh sách nhân viên thuộc xí nghiệp
        """
        xinghiep = self.get_object()
        employees = xinghiep.employees.all()
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)

class BoPhanXiNghiepViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho quản lý bộ phận xí nghiệp (BoPhanXiNghiep)
    """
    queryset = BoPhanXiNghiep.objects.all()
    serializer_class = BoPhanXiNghiepSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'is_active']
    ordering = ['name']
    
    def get_queryset(self):
        queryset = BoPhanXiNghiep.objects.all()
        
        # Lọc theo xí nghiệp cha
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
        Lấy danh sách nhân viên thuộc bộ phận xí nghiệp
        """
        bophan = self.get_object()
        employees = bophan.employees.all()
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)

class NhomXiNghiepViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho quản lý nhóm xí nghiệp (NhomXiNghiep)
    """
    queryset = NhomXiNghiep.objects.all()
    serializer_class = NhomXiNghiepSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'is_active']
    ordering = ['name']
    
    def get_queryset(self):
        queryset = NhomXiNghiep.objects.all()
        
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
        Lấy danh sách nhân viên thuộc nhóm xí nghiệp
        """
        nhom = self.get_object()
        employees = nhom.employees.all()
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)
