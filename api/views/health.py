from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HealthCheckView(APIView):
    """
    API endpoint để kiểm tra trạng thái hoạt động của backend
    """
    permission_classes = []  # Không yêu cầu xác thực
    
    def get(self, request, format=None):
        """
        Trả về trạng thái hoạt động của backend
        """
        return Response(
            {
                "status": "ok",
                "message": "Backend is running"
            },
            status=status.HTTP_200_OK
        )
