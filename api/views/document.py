from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from documents.models import Document, DocumentCategory, DocumentVersion
from api.serializers.document import (
    DocumentListSerializer, DocumentDetailSerializer, 
    DocumentCreateSerializer, DocumentUpdateSerializer,
    DocumentCategorySerializer, DocumentVersionSerializer
)

class DocumentCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho quản lý danh mục tài liệu
    """
    queryset = DocumentCategory.objects.all()
    serializer_class = DocumentCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'is_active']
    ordering = ['name']
    
    def get_queryset(self):
        queryset = DocumentCategory.objects.all()
        
        # Lọc theo danh mục cha
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

class DocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho quản lý tài liệu
    """
    queryset = Document.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'document_number', 'description', 'content']
    ordering_fields = ['title', 'document_number', 'category__name', 'document_type', 'version', 'access_level', 'is_active', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DocumentListSerializer
        elif self.action == 'create':
            return DocumentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return DocumentUpdateSerializer
        return DocumentDetailSerializer
    
    def get_queryset(self):
        queryset = Document.objects.all()
        
        # Lọc theo danh mục
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        # Lọc theo loại tài liệu
        document_type = self.request.query_params.get('document_type')
        if document_type:
            queryset = queryset.filter(document_type=document_type)
        
        # Lọc theo mức độ truy cập
        access_level = self.request.query_params.get('access_level')
        if access_level:
            queryset = queryset.filter(access_level=access_level)
        
        # Lọc theo trạng thái hoạt động
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def versions(self, request, pk=None):
        """
        Lấy danh sách phiên bản của tài liệu
        """
        document = self.get_object()
        versions = DocumentVersion.objects.filter(document=document).order_by('-created_at')
        serializer = DocumentVersionSerializer(versions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_version(self, request, pk=None):
        """
        Thêm phiên bản mới cho tài liệu
        """
        document = self.get_object()
        
        # Kiểm tra dữ liệu đầu vào
        version = request.data.get('version')
        content = request.data.get('content')
        change_summary = request.data.get('change_summary')
        
        if not version or not change_summary:
            return Response(
                {'detail': 'Vui lòng cung cấp phiên bản và tóm tắt thay đổi'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Kiểm tra xem phiên bản đã tồn tại chưa
        if DocumentVersion.objects.filter(document=document, version=version).exists():
            return Response(
                {'detail': 'Phiên bản này đã tồn tại'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Tạo phiên bản mới
        document_version = DocumentVersion.objects.create(
            document=document,
            version=version,
            content=content,
            change_summary=change_summary,
            created_by=request.user
        )
        
        # Cập nhật phiên bản hiện tại của tài liệu
        document.version = version
        if content:
            document.content = content
        document.save()
        
        serializer = DocumentVersionSerializer(document_version)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Phê duyệt tài liệu
        """
        document = self.get_object()
        
        # Kiểm tra quyền
        if not request.user.is_superuser and not request.user.is_staff:
            return Response(
                {'detail': 'Bạn không có quyền phê duyệt tài liệu'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Cập nhật thông tin phê duyệt
        document.approved_by = request.user
        document.approved_at = timezone.now()
        document.save()
        
        serializer = DocumentDetailSerializer(document)
        return Response(serializer.data)
