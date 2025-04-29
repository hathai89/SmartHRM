from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Q, Sum
from django.utils import timezone
from .models import (
    JobPosting, JobApplication, Interview,
    MaritalStatus, FamilyPolicyType, Gender, EducationLevel
)
from .serializers import (
    JobPostingListSerializer, JobPostingDetailSerializer, JobPostingCreateUpdateSerializer,
    JobApplicationListSerializer, JobApplicationDetailSerializer, JobApplicationCreateSerializer, JobApplicationUpdateSerializer,
    InterviewListSerializer, InterviewDetailSerializer, InterviewCreateUpdateSerializer,
    MaritalStatusSerializer, FamilyPolicyTypeSerializer, GenderSerializer, EducationLevelSerializer
)
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from notifications.services import create_notification

class JobPostingViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho tin tuyển dụng
    """
    queryset = JobPosting.objects.all().annotate(
        applications_count=Count('applications')
    )
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'job_code', 'description']
    ordering_fields = ['created_at', 'publish_date', 'closing_date', 'applications_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return JobPostingListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return JobPostingCreateUpdateSerializer
        return JobPostingDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Lọc theo trạng thái
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Lọc theo phòng ban
        department = self.request.query_params.get('department')
        if department:
            queryset = queryset.filter(department_id=department)

        # Lọc theo xí nghiệp
        factory = self.request.query_params.get('factory')
        if factory:
            queryset = queryset.filter(factory_id=factory)

        # Lọc theo người tạo
        created_by = self.request.query_params.get('created_by')
        if created_by:
            queryset = queryset.filter(created_by_id=created_by)

        # Lọc theo thời gian
        date_from = self.request.query_params.get('date_from')
        if date_from:
            queryset = queryset.filter(publish_date__gte=date_from)

        date_to = self.request.query_params.get('date_to')
        if date_to:
            queryset = queryset.filter(publish_date__lte=date_to)

        return queryset

    def perform_create(self, serializer):
        print("Request data:", self.request.data)
        try:
            # Kiểm tra xem job_code có được cung cấp không
            job_code = self.request.data.get('job_code')
            if not job_code:
                # Nếu không có job_code, tạo mã tự động
                job_code = JobPosting.generate_job_code()
                serializer.save(created_by=self.request.user, job_code=job_code)
            else:
                # Nếu có job_code, sử dụng mã đã cung cấp
                serializer.save(created_by=self.request.user)
        except Exception as e:
            print("Error creating job posting:", e)
            print("Serializer errors:", serializer.errors)
            raise

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """
        Đăng tin tuyển dụng
        """
        job_posting = self.get_object()

        if job_posting.status != 'draft' and job_posting.status != 'pending':
            return Response(
                {"detail": "Chỉ có thể đăng tin ở trạng thái nháp hoặc chờ duyệt"},
                status=status.HTTP_400_BAD_REQUEST
            )

        job_posting.status = 'published'
        job_posting.approved_by = request.user
        job_posting.approved_at = timezone.now()
        job_posting.save()

        # Gửi thông báo cho người tạo tin
        if job_posting.created_by and job_posting.created_by != request.user:
            create_notification(
                recipient=job_posting.created_by,
                title="Tin tuyển dụng đã được đăng",
                message=f"Tin tuyển dụng '{job_posting.title}' đã được đăng",
                notification_type="recruitment",
                priority="normal",
                link=f"/recruitment/jobs/{job_posting.id}/",
                related_object=job_posting
            )

        return Response(
            {"detail": "Tin tuyển dụng đã được đăng thành công"},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """
        Đóng tin tuyển dụng
        """
        job_posting = self.get_object()

        if job_posting.status != 'published':
            return Response(
                {"detail": "Chỉ có thể đóng tin đang được đăng"},
                status=status.HTTP_400_BAD_REQUEST
            )

        job_posting.status = 'closed'
        job_posting.save()

        # Gửi thông báo cho người tạo tin
        if job_posting.created_by and job_posting.created_by != request.user:
            create_notification(
                recipient=job_posting.created_by,
                title="Tin tuyển dụng đã đóng",
                message=f"Tin tuyển dụng '{job_posting.title}' đã được đóng",
                notification_type="recruitment",
                priority="normal",
                link=f"/recruitment/jobs/{job_posting.id}/",
                related_object=job_posting
            )

        return Response(
            {"detail": "Tin tuyển dụng đã được đóng thành công"},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Hủy tin tuyển dụng
        """
        job_posting = self.get_object()

        if job_posting.status == 'closed' or job_posting.status == 'cancelled':
            return Response(
                {"detail": "Không thể hủy tin đã đóng hoặc đã hủy"},
                status=status.HTTP_400_BAD_REQUEST
            )

        job_posting.status = 'cancelled'
        job_posting.save()

        # Gửi thông báo cho người tạo tin
        if job_posting.created_by and job_posting.created_by != request.user:
            create_notification(
                recipient=job_posting.created_by,
                title="Tin tuyển dụng đã bị hủy",
                message=f"Tin tuyển dụng '{job_posting.title}' đã bị hủy",
                notification_type="recruitment",
                priority="normal",
                link=f"/recruitment/jobs/{job_posting.id}/",
                related_object=job_posting
            )

        return Response(
            {"detail": "Tin tuyển dụng đã được hủy thành công"},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """
        Lấy danh sách đơn ứng tuyển cho tin tuyển dụng
        """
        job_posting = self.get_object()
        applications = job_posting.applications.all()

        # Lọc theo trạng thái
        status_param = request.query_params.get('status')
        if status_param:
            applications = applications.filter(status=status_param)

        serializer = JobApplicationListSerializer(applications, many=True)
        return Response(serializer.data)

class JobApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho đơn ứng tuyển
    """
    queryset = JobApplication.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'email', 'phone']
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return JobApplicationListSerializer
        elif self.action == 'create':
            return JobApplicationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return JobApplicationUpdateSerializer
        return JobApplicationDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Lọc theo tin tuyển dụng
        job_posting_id = self.request.query_params.get('job_posting_id')
        if job_posting_id:
            queryset = queryset.filter(job_posting_id=job_posting_id)

        # Lọc theo trạng thái
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Lọc theo phòng ban hoặc xí nghiệp
        department_id = self.request.query_params.get('department_id')
        if department_id:
            queryset = queryset.filter(job_posting__department_id=department_id)

        factory_id = self.request.query_params.get('factory_id')
        if factory_id:
            queryset = queryset.filter(job_posting__factory_id=factory_id)

        # Tìm kiếm
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(full_name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search)
            )

        return queryset

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """
        Thay đổi trạng thái đơn ứng tuyển
        """
        application = self.get_object()
        new_status = request.data.get('status')
        notes = request.data.get('notes')

        if not new_status:
            return Response(
                {"detail": "Vui lòng cung cấp trạng thái mới"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Kiểm tra trạng thái hợp lệ
        valid_statuses = [status_choice[0] for status_choice in JobApplication.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response(
                {"detail": "Trạng thái không hợp lệ"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Cập nhật trạng thái
        application.status = new_status
        if notes:
            application.notes = notes
        application.save()

        return Response(
            {"detail": "Đã cập nhật trạng thái đơn ứng tuyển thành công"},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def schedule_interview(self, request, pk=None):
        """
        Lên lịch phỏng vấn cho đơn ứng tuyển
        """
        application = self.get_object()

        # Kiểm tra trạng thái đơn
        if application.status == 'rejected' or application.status == 'cancelled':
            return Response(
                {"detail": "Không thể lên lịch phỏng vấn cho đơn đã bị từ chối hoặc hủy"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Lấy dữ liệu từ request
        interview_type = request.data.get('interview_type')
        scheduled_date = request.data.get('scheduled_date')
        location = request.data.get('location')
        interviewer_ids = request.data.get('interviewers', [])

        # Kiểm tra dữ liệu
        if not all([interview_type, scheduled_date, location]):
            return Response(
                {"detail": "Vui lòng cung cấp đầy đủ thông tin phỏng vấn"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Tạo phỏng vấn mới
        interview = Interview.objects.create(
            application=application,
            interview_type=interview_type,
            scheduled_date=scheduled_date,
            location=location,
            status='scheduled',
            created_by=request.user
        )

        # Thêm người phỏng vấn
        if interviewer_ids:
            interviewers = User.objects.filter(id__in=interviewer_ids)
            interview.interviewers.set(interviewers)

        # Cập nhật trạng thái đơn ứng tuyển
        if interview_type == 'department':
            application.status = 'interview_department'
        elif interview_type == 'factory':
            application.status = 'interview_factory'
        else:
            application.status = 'screening'
        application.save()

        # Gửi thông báo cho người phỏng vấn
        for interviewer in interview.interviewers.all():
            create_notification(
                recipient=interviewer,
                title="Lịch phỏng vấn mới",
                message=f"Bạn được phân công phỏng vấn {application.full_name} vào lúc {scheduled_date}",
                notification_type="recruitment",
                priority="high",
                link=f"/recruitment/interviews/{interview.id}/",
                related_object=interview
            )

        serializer = InterviewDetailSerializer(interview)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class InterviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho phỏng vấn
    """
    queryset = Interview.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['scheduled_date', 'status']
    ordering = ['-scheduled_date']

    def get_serializer_class(self):
        if self.action == 'list':
            return InterviewListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return InterviewCreateUpdateSerializer
        return InterviewDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Lọc theo đơn ứng tuyển
        application_id = self.request.query_params.get('application_id')
        if application_id:
            queryset = queryset.filter(application_id=application_id)

        # Lọc theo loại phỏng vấn
        interview_type = self.request.query_params.get('interview_type')
        if interview_type:
            queryset = queryset.filter(interview_type=interview_type)

        # Lọc theo trạng thái
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Lọc theo kết quả
        result = self.request.query_params.get('result')
        if result:
            queryset = queryset.filter(result=result)

        # Lọc theo người phỏng vấn
        interviewer_id = self.request.query_params.get('interviewer_id')
        if interviewer_id:
            queryset = queryset.filter(interviewers__id=interviewer_id)

        # Lọc theo thời gian
        date_from = self.request.query_params.get('date_from')
        if date_from:
            queryset = queryset.filter(scheduled_date__gte=date_from)

        date_to = self.request.query_params.get('date_to')
        if date_to:
            queryset = queryset.filter(scheduled_date__lte=date_to)

        # Lọc theo người tạo
        created_by = self.request.query_params.get('created_by')
        if created_by:
            queryset = queryset.filter(created_by_id=created_by)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        Hoàn thành phỏng vấn và cập nhật kết quả
        """
        interview = self.get_object()

        if interview.status == 'completed':
            return Response(
                {"detail": "Phỏng vấn đã được hoàn thành trước đó"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Lấy dữ liệu từ request
        result = request.data.get('result')
        evaluation = request.data.get('evaluation')
        notes = request.data.get('notes')

        # Kiểm tra dữ liệu
        if not result:
            return Response(
                {"detail": "Vui lòng cung cấp kết quả phỏng vấn"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Cập nhật phỏng vấn
        interview.status = 'completed'
        interview.result = result
        if evaluation:
            interview.evaluation = evaluation
        if notes:
            interview.notes = notes
        interview.save()

        # Cập nhật trạng thái đơn ứng tuyển nếu cần
        application = interview.application
        if result == 'passed':
            # Kiểm tra xem đã có phỏng vấn tiếp theo chưa
            next_interview = application.interviews.filter(
                scheduled_date__gt=interview.scheduled_date
            ).exists()

            if not next_interview:
                application.status = 'offered'
                application.save()
        elif result == 'failed':
            application.status = 'rejected'
            application.save()

        # Gửi thông báo cho người tạo đơn
        if application.job_posting.created_by:
            create_notification(
                recipient=application.job_posting.created_by,
                title="Kết quả phỏng vấn",
                message=f"Phỏng vấn của {application.full_name} đã hoàn thành với kết quả: {interview.get_result_display()}",
                notification_type="recruitment",
                priority="normal",
                link=f"/recruitment/interviews/{interview.id}/",
                related_object=interview
            )

        serializer = InterviewDetailSerializer(interview)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Hủy phỏng vấn
        """
        interview = self.get_object()

        if interview.status == 'completed' or interview.status == 'cancelled':
            return Response(
                {"detail": "Không thể hủy phỏng vấn đã hoàn thành hoặc đã hủy"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Cập nhật phỏng vấn
        interview.status = 'cancelled'
        interview.save()

        # Gửi thông báo cho người phỏng vấn
        for interviewer in interview.interviewers.all():
            create_notification(
                recipient=interviewer,
                title="Phỏng vấn đã bị hủy",
                message=f"Phỏng vấn với {interview.application.full_name} vào lúc {interview.scheduled_date} đã bị hủy",
                notification_type="recruitment",
                priority="high",
                link=f"/recruitment/interviews/{interview.id}/",
                related_object=interview
            )

        return Response(
            {"detail": "Phỏng vấn đã được hủy thành công"},
            status=status.HTTP_200_OK
        )

# Public views for job seekers
class PublicJobPostingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint công khai cho tin tuyển dụng
    """
    queryset = JobPosting.objects.filter(status='published')
    serializer_class = JobPostingDetailSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['publish_date', 'closing_date']
    ordering = ['-publish_date']

    def get_serializer_class(self):
        """
        Sử dụng serializer khác nhau cho list và detail
        """
        if self.action == 'list':
            return JobPostingListSerializer
        return JobPostingDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Chỉ lấy các tin đang mở và chưa hết hạn
        today = timezone.now().date()
        queryset = queryset.filter(
            Q(closing_date__gte=today) | Q(is_open_until_filled=True)
        )

        # Lọc theo phòng ban
        department = self.request.query_params.get('department')
        if department:
            queryset = queryset.filter(department_id=department)

        # Lọc theo xí nghiệp
        factory = self.request.query_params.get('factory')
        if factory:
            queryset = queryset.filter(factory_id=factory)

        return queryset

class PublicJobApplicationCreateView(viewsets.ModelViewSet):
    """
    API endpoint công khai cho việc nộp đơn ứng tuyển
    """
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationCreateSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post']  # Chỉ cho phép phương thức POST

    def create(self, request, *args, **kwargs):
        # In ra dữ liệu request để debug
        print("Request data:", request.data)
        print("Request data type:", type(request.data))

        # In ra các trường bắt buộc trong mô hình
        from recruitment.models import JobApplication
        required_fields = [field.name for field in JobApplication._meta.fields if not field.null and not field.blank and not field.auto_created]
        print("Required fields in model:", required_fields)

        # Kiểm tra các trường bắt buộc trong request
        for field in required_fields:
            print(f"Field {field} in request: {field in request.data}")

        # Lấy tin tuyển dụng
        job_posting_id = request.data.get('job_posting')
        job_posting = get_object_or_404(JobPosting, id=job_posting_id)

        # Kiểm tra xem tin tuyển dụng có đang mở không
        if job_posting.status != 'published':
            return Response(
                {"detail": "Tin tuyển dụng này không còn nhận hồ sơ"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Kiểm tra xem tin tuyển dụng có hết hạn không
        today = timezone.now().date()
        if not job_posting.is_open_until_filled and job_posting.closing_date < today:
            return Response(
                {"detail": "Tin tuyển dụng này đã hết hạn"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Tạo đơn ứng tuyển
        serializer = self.get_serializer(data=request.data)

        # Kiểm tra dữ liệu hợp lệ và in ra lỗi nếu có
        if not serializer.is_valid():
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)

        # Gửi thông báo cho người tạo tin tuyển dụng
        if job_posting.created_by:
            create_notification(
                recipient=job_posting.created_by,
                title="Đơn ứng tuyển mới",
                message=f"Có đơn ứng tuyển mới cho tin '{job_posting.title}' từ {serializer.validated_data['full_name']}",
                notification_type="recruitment",
                priority="normal",
                link=f"/recruitment/applications/{serializer.instance.id}/",
                related_object=serializer.instance
            )

        # Gửi thông báo cho admin
        admin_users = User.objects.filter(is_superuser=True)
        for admin in admin_users:
            if admin != job_posting.created_by:
                create_notification(
                    recipient=admin,
                    title="Đơn ứng tuyển mới",
                    message=f"Có đơn ứng tuyển mới cho tin '{job_posting.title}' từ {serializer.validated_data['full_name']}",
                    notification_type="recruitment",
                    priority="normal",
                    link=f"/recruitment/applications/{serializer.instance.id}/",
                    related_object=serializer.instance
                )

        headers = self.get_success_headers(serializer.data)
        return Response(
            {"detail": "Đơn ứng tuyển của bạn đã được gửi thành công"},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    """
    API endpoint để lấy thống kê cho dashboard recruitment
    """
    # Lấy thống kê tin tuyển dụng
    job_postings_count = JobPosting.objects.count()
    active_job_postings = JobPosting.objects.filter(status='published').count()
    closed_job_postings = JobPosting.objects.filter(status='closed').count()

    # Lấy thống kê đơn ứng tuyển
    applications_count = JobApplication.objects.count()
    new_applications = JobApplication.objects.filter(status='new').count()
    processed_applications = applications_count - new_applications

    # Lấy thống kê phỏng vấn
    interviews_count = Interview.objects.count()
    upcoming_interviews = Interview.objects.filter(
        status='scheduled',
        scheduled_date__gte=timezone.now()
    ).count()
    completed_interviews = Interview.objects.filter(status='completed').count()

    # Lấy thống kê tuyển dụng
    hired_count = JobApplication.objects.filter(status='accepted').count()
    rejected_count = JobApplication.objects.filter(status='rejected').count()

    # Tính tỷ lệ tuyển dụng
    total_processed = hired_count + rejected_count
    hire_rate = round((hired_count / total_processed) * 100) if total_processed > 0 else 0

    # Lấy tin tuyển dụng gần đây
    recent_job_postings = JobPostingListSerializer(
        JobPosting.objects.all().order_by('-created_at')[:5],
        many=True
    ).data

    # Lấy đơn ứng tuyển gần đây
    recent_applications = JobApplicationListSerializer(
        JobApplication.objects.all().order_by('-created_at')[:5],
        many=True
    ).data

    # Lấy phỏng vấn sắp tới
    upcoming_interviews_list = InterviewListSerializer(
        Interview.objects.filter(
            status='scheduled',
            scheduled_date__gte=timezone.now()
        ).order_by('scheduled_date')[:10],
        many=True
    ).data

    return Response({
        'jobPostings': job_postings_count,
        'activeJobPostings': active_job_postings,
        'closedJobPostings': closed_job_postings,
        'applications': applications_count,
        'newApplications': new_applications,
        'processedApplications': processed_applications,
        'interviews': interviews_count,
        'upcomingInterviews': upcoming_interviews,
        'completedInterviews': completed_interviews,
        'hireRate': hire_rate,
        'hired': hired_count,
        'rejected': rejected_count,
        'recentJobPostings': recent_job_postings,
        'recentApplications': recent_applications,
        'upcomingInterviews': upcoming_interviews_list
    })

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_departments(request):
    """
    API endpoint công khai để lấy danh sách phòng ban cho trang tuyển dụng
    """
    from departments.models import Department
    from departments.serializers import DepartmentSerializer

    # Lấy danh sách phòng ban đang hoạt động
    departments = Department.objects.filter(is_active=True)
    serializer = DepartmentSerializer(departments, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_factories(request):
    """
    API endpoint công khai để lấy danh sách xí nghiệp cho trang tuyển dụng
    """
    from factories.models import Factory
    from factories.serializers import FactorySerializer

    # Lấy danh sách xí nghiệp đang hoạt động
    factories = Factory.objects.filter(is_active=True)
    serializer = FactorySerializer(factories, many=True)

    return Response(serializer.data)


class MaritalStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint để lấy danh sách tình trạng hôn nhân
    """
    queryset = MaritalStatus.objects.filter(is_active=True)
    serializer_class = MaritalStatusSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'name']
    ordering = ['order', 'name']


class FamilyPolicyTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint để lấy danh sách loại chính sách gia đình
    """
    queryset = FamilyPolicyType.objects.filter(is_active=True)
    serializer_class = FamilyPolicyTypeSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'name']
    ordering = ['order', 'name']


class GenderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint để lấy danh sách giới tính
    """
    queryset = Gender.objects.filter(is_active=True)
    serializer_class = GenderSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'name']
    ordering = ['order', 'name']


class EducationLevelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint để lấy danh sách trình độ học vấn
    """
    queryset = EducationLevel.objects.filter(is_active=True)
    serializer_class = EducationLevelSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'name']
    ordering = ['order', 'name']