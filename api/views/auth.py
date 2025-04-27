from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from api.serializers.user import UserSerializer, UserUpdateSerializer, PasswordChangeSerializer

class AuthViewSet(viewsets.ViewSet):
    """
    API endpoint cho xác thực người dùng
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    @csrf_exempt
    def login(self, request):
        """
        Đăng nhập và lấy token
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'detail': 'Vui lòng cung cấp tên đăng nhập và mật khẩu'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {'detail': 'Tên đăng nhập hoặc mật khẩu không đúng'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {'detail': 'Tài khoản đã bị vô hiệu hóa'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Đăng nhập người dùng
        login(request, user)

        # Lấy hoặc tạo token
        token, created = Token.objects.get_or_create(user=user)

        # Trả về thông tin người dùng và token
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })

    @action(detail=False, methods=['post'])
    @csrf_exempt
    def logout(self, request):
        """
        Đăng xuất và xóa token
        """
        # Kiểm tra xem người dùng đã đăng nhập chưa
        if request.user.is_authenticated:
            # Xóa token
            try:
                request.user.auth_token.delete()
            except:
                pass

            # Đăng xuất
            logout(request)

        return Response({'detail': 'Đăng xuất thành công'})

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def user(self, request):
        """
        Lấy thông tin người dùng hiện tại
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request):
        """
        Cập nhật thông tin cá nhân
        """
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(request.user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    @csrf_exempt
    def change_password(self, request):
        """
        Đổi mật khẩu
        """
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Đổi mật khẩu
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            # Cập nhật trạng thái đã đổi mật khẩu cho nhân viên
            try:
                if hasattr(user, 'employee'):
                    user.employee.password_changed = True
                    user.employee.save()
            except:
                pass

            # Cập nhật token
            try:
                request.user.auth_token.delete()
            except:
                pass
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'detail': 'Đổi mật khẩu thành công',
                'token': token.key
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
