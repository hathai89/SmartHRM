from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer

class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint để xem và chỉnh sửa thông tin công ty
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """
        Chỉ cho phép admin chỉnh sửa thông tin công ty
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def info(self, request):
        """
        Lấy thông tin công ty đầu tiên
        """
        company = Company.get_company_info()
        if company:
            serializer = self.get_serializer(company)
            return Response(serializer.data)
        return Response(
            {"detail": "Không tìm thấy thông tin công ty"},
            status=status.HTTP_404_NOT_FOUND
        )
