from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from employees.models import Employee
from departments.models import Department
from factories.models import Factory
from documents.models import Document
from django.utils import timezone
from datetime import timedelta

class DashboardViewSet(viewsets.ViewSet):
    """
    API endpoint cho bảng điều khiển
    """
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Lấy thống kê tổng quan
        """
        stats = {
            'totalEmployees': Employee.objects.count(),
            'totalDepartments': Department.objects.count(),
            'totalFactories': Factory.objects.count(),
            'totalDocuments': Document.objects.count(),
            'newEmployeesThisMonth': Employee.objects.filter(
                date_joined__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0)
            ).count(),
        }

        return Response(stats)

    @action(detail=False, methods=['get'])
    def activities(self, request):
        """
        Lấy danh sách hoạt động gần đây
        """
        # Lấy các hoạt động gần đây từ các model
        activities = []

        # Nhân viên mới
        new_employees = Employee.objects.filter(
            join_date__gte=timezone.now().date() - timedelta(days=30)
        ).order_by('-join_date')[:5]

        for employee in new_employees:
            activities.append({
                'type': 'employee',
                'description': f'Nhân viên {employee.first_name} {employee.last_name} đã được thêm mới',
                'timestamp': employee.created_at,
                'user': employee.user.username if employee.user else None
            })

        # Tài liệu mới
        new_documents = Document.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).order_by('-created_at')[:5]

        for document in new_documents:
            activities.append({
                'type': 'document',
                'description': f'Tài liệu "{document.title}" đã được thêm mới',
                'timestamp': document.created_at,
                'user': document.created_by.username if document.created_by else None
            })

        # Sắp xếp theo thời gian giảm dần
        activities.sort(key=lambda x: x['timestamp'], reverse=True)

        return Response({
            'count': len(activities),
            'results': activities[:10]  # Chỉ trả về 10 hoạt động gần nhất
        })

    @action(detail=False, methods=['get'])
    def charts(self, request):
        """
        Lấy dữ liệu cho các biểu đồ
        """
        # Thống kê nhân viên theo phòng ban
        departments = Department.objects.all()
        department_stats = []

        for dept in departments:
            department_stats.append({
                'name': dept.name,
                'count': Employee.objects.filter(department=dept).count()
            })

        # Thống kê nhân viên theo xí nghiệp
        factories = Factory.objects.all()
        factory_stats = []

        for factory in factories:
            factory_stats.append({
                'name': factory.name,
                'count': Employee.objects.filter(factory=factory).count()
            })

        # Thống kê nhân viên theo giới tính
        gender_stats = {
            'male': Employee.objects.filter(gender='M').count(),
            'female': Employee.objects.filter(gender='F').count(),
            'other': Employee.objects.filter(gender='O').count()
        }

        return Response({
            'departmentStats': department_stats,
            'factoryStats': factory_stats,
            'genderStats': gender_stats
        })
