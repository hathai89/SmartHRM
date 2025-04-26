from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from notifications.models import Notification
from api.serializers.notification import NotificationSerializer

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint cho quản lý thông báo
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'is_read', 'priority']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Chỉ lấy thông báo của người dùng hiện tại
        queryset = Notification.objects.filter(recipient=self.request.user, is_deleted=False)
        
        # Lọc theo trạng thái đã đọc
        is_read = self.request.query_params.get('is_read')
        if is_read is not None:
            is_read = is_read.lower() == 'true'
            queryset = queryset.filter(is_read=is_read)
        
        # Lọc theo loại thông báo
        notification_type = self.request.query_params.get('notification_type')
        if notification_type:
            queryset = queryset.filter(notification_type=notification_type)
        
        # Lọc theo mức độ ưu tiên
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            response = Response(serializer.data)
        
        # Thêm số lượng thông báo chưa đọc vào response
        unread_count = Notification.objects.filter(recipient=request.user, is_read=False, is_deleted=False).count()
        response.data['unread_count'] = unread_count
        
        return response
    
    @action(detail=True, methods=['post'])
    def read(self, request, pk=None):
        """
        Đánh dấu thông báo đã đọc
        """
        notification = self.get_object()
        
        # Kiểm tra quyền
        if notification.recipient != request.user:
            return Response(
                {'detail': 'Bạn không có quyền thực hiện hành động này'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        notification.is_read = True
        notification.save()
        
        return Response({'detail': 'Đánh dấu đã đọc thành công'})
    
    @action(detail=False, methods=['post'])
    def read_all(self, request):
        """
        Đánh dấu tất cả thông báo đã đọc
        """
        Notification.objects.filter(recipient=request.user, is_read=False, is_deleted=False).update(is_read=True)
        return Response({'detail': 'Đánh dấu tất cả đã đọc thành công'})
    
    @action(detail=True, methods=['delete'])
    def delete(self, request, pk=None):
        """
        Xóa thông báo
        """
        notification = self.get_object()
        
        # Kiểm tra quyền
        if notification.recipient != request.user:
            return Response(
                {'detail': 'Bạn không có quyền thực hiện hành động này'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        notification.is_deleted = True
        notification.save()
        
        return Response({'detail': 'Xóa thông báo thành công'})
    
    @action(detail=False, methods=['delete'])
    def delete_all(self, request):
        """
        Xóa tất cả thông báo
        """
        Notification.objects.filter(recipient=request.user, is_deleted=False).update(is_deleted=True)
        return Response({'detail': 'Xóa tất cả thông báo thành công'})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """
        Lấy số lượng thông báo chưa đọc
        """
        count = Notification.objects.filter(recipient=request.user, is_read=False, is_deleted=False).count()
        return Response({'count': count})
