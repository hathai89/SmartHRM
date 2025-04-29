from rest_framework import serializers
from .models import (
    JobPosting, JobApplication, Interview,
    MaritalStatus, FamilyPolicyType, Gender, EducationLevel
)
from departments.serializers import DepartmentSerializer
from factories.serializers import FactorySerializer
from django.contrib.auth.models import User

class MaritalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaritalStatus
        fields = ['id', 'code', 'name', 'is_active', 'order']


class FamilyPolicyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyPolicyType
        fields = ['id', 'code', 'name', 'description', 'is_active', 'order']


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'code', 'name', 'is_active', 'order']


class EducationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationLevel
        fields = ['id', 'code', 'name', 'description', 'is_active', 'order']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class JobPostingListSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    factory_name = serializers.SerializerMethodField()
    division_name = serializers.SerializerMethodField()
    team_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    applications_count = serializers.IntegerField(read_only=True)
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = JobPosting
        fields = [
            'id', 'title', 'job_code', 'department', 'department_name',
            'factory', 'factory_name', 'division', 'division_name',
            'team', 'team_name', 'positions', 'status', 'status_display',
            'publish_date', 'closing_date', 'created_by', 'created_by_name',
            'applications_count', 'created_at', 'updated_at'
        ]

    def get_department_name(self, obj):
        return obj.department.name if obj.department else None

    def get_factory_name(self, obj):
        return obj.factory.name if obj.factory else None

    def get_division_name(self, obj):
        return obj.division.name if obj.division else None

    def get_team_name(self, obj):
        return obj.team.name if obj.team else None

    def get_created_by_name(self, obj):
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip() or obj.created_by.username
        return None

    def get_status_display(self, obj):
        return obj.get_status_display()

class JobPostingDetailSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    factory = FactorySerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    approved_by = UserSerializer(read_only=True)
    applications_count = serializers.IntegerField(read_only=True)
    status_display = serializers.SerializerMethodField()
    division_name = serializers.SerializerMethodField()
    team_name = serializers.SerializerMethodField()
    employment_type_display = serializers.SerializerMethodField()
    experience_level_display = serializers.SerializerMethodField()
    education_required_display = serializers.SerializerMethodField()
    workplace_type_display = serializers.SerializerMethodField()

    class Meta:
        model = JobPosting
        fields = '__all__'

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_division_name(self, obj):
        from departments.models import Department
        if obj.division:
            try:
                # Ensure division is an integer ID
                division_id = obj.division.id if hasattr(obj.division, 'id') else obj.division
                division = Department.objects.get(id=division_id)
                return division.name
            except (Department.DoesNotExist, ValueError, AttributeError, TypeError):
                return None
        return None

    def get_team_name(self, obj):
        from departments.models import Department
        if obj.team:
            try:
                # Ensure team is an integer ID
                team_id = obj.team.id if hasattr(obj.team, 'id') else obj.team
                team = Department.objects.get(id=team_id)
                return team.name
            except (Department.DoesNotExist, ValueError, AttributeError, TypeError):
                return None
        return None

    def get_employment_type_display(self, obj):
        return obj.get_employment_type_display()

    def get_experience_level_display(self, obj):
        return obj.get_experience_level_display()

    def get_education_required_display(self, obj):
        return obj.get_education_required_display()

    def get_workplace_type_display(self, obj):
        return obj.get_workplace_type_display()

class JobPostingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = [
            'title', 'job_code', 'description', 'requirements', 'benefits',
            'positions', 'min_salary', 'max_salary', 'is_salary_visible', 'is_salary_negotiable', 'is_open_until_filled',
            'workplace_type', 'department', 'factory', 'division', 'team', 'location',
            'employment_type', 'experience_level', 'education_required',
            'publish_date', 'closing_date', 'status'
        ]

    def validate(self, data):
        # Kiểm tra xem đã chọn phòng ban hoặc xí nghiệp chưa
        if data.get('workplace_type') == 'department' and not data.get('department'):
            raise serializers.ValidationError({"department": "Vui lòng chọn phòng ban"})
        elif data.get('workplace_type') == 'factory' and not data.get('factory'):
            raise serializers.ValidationError({"factory": "Vui lòng chọn xí nghiệp"})

        # Kiểm tra ngày đăng và ngày hết hạn
        if data.get('publish_date') and data.get('closing_date'):
            if data['publish_date'] > data['closing_date']:
                raise serializers.ValidationError({"closing_date": "Ngày hết hạn phải sau ngày đăng"})

        # Kiểm tra mức lương
        if not data.get('is_salary_negotiable'):
            if data.get('min_salary') and data.get('max_salary'):
                if data['min_salary'] > data['max_salary']:
                    raise serializers.ValidationError({"max_salary": "Mức lương tối đa phải lớn hơn mức lương tối thiểu"})

        # Kiểm tra mã tin tuyển dụng nếu được cung cấp
        job_code = data.get('job_code')
        if job_code:
            # Kiểm tra xem mã tin tuyển dụng đã tồn tại chưa
            instance = self.instance  # Lấy instance hiện tại (nếu đang cập nhật)
            if instance:
                # Nếu đang cập nhật, kiểm tra xem mã có trùng với mã của tin tuyển dụng khác không
                if JobPosting.objects.filter(job_code=job_code).exclude(pk=instance.pk).exists():
                    raise serializers.ValidationError({"job_code": "Mã tin tuyển dụng này đã tồn tại"})
            else:
                # Nếu đang tạo mới, kiểm tra xem mã đã tồn tại chưa
                if JobPosting.objects.filter(job_code=job_code).exists():
                    raise serializers.ValidationError({"job_code": "Mã tin tuyển dụng này đã tồn tại"})

        return data

class JobApplicationListSerializer(serializers.ModelSerializer):
    job_title = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication
        fields = [
            'id', 'job_posting', 'job_title', 'full_name', 'email', 'phone',
            'status', 'status_display', 'created_at'
        ]

    def get_job_title(self, obj):
        return obj.job_posting.title

    def get_status_display(self, obj):
        return obj.get_status_display()

class JobApplicationDetailSerializer(serializers.ModelSerializer):
    job_posting = JobPostingListSerializer(read_only=True)
    status_display = serializers.SerializerMethodField()
    resume_url = serializers.SerializerMethodField()
    interviews = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication
        fields = '__all__'

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_resume_url(self, obj):
        if obj.resume:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.resume.url)
        return None

    def get_interviews(self, obj):
        interviews = obj.interviews.all().order_by('-scheduled_date')
        return InterviewListSerializer(interviews, many=True).data

class JobApplicationCreateSerializer(serializers.ModelSerializer):
    agree_terms = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = JobApplication
        fields = [
            # Thông tin cơ bản
            'job_posting', 'first_name', 'last_name', 'full_name', 'gender', 'date_of_birth',
            'email', 'phone', 'marital_status', 'nationality', 'birth_place', 'ethnicity', 'religion',

            # Thông tin CCCD/CMND
            'id_card_number', 'id_card_issue_date', 'id_card_issue_place',
            'id_card_front_image', 'id_card_back_image',

            # Thông tin địa chỉ
            'permanent_address', 'address',

            # Thông tin liên hệ khẩn cấp
            'emergency_contact_name', 'emergency_contact_relationship', 'emergency_contact_phone',

            # Thông tin gia đình
            'father_name', 'father_phone', 'mother_name', 'mother_phone',
            'is_family_policy', 'family_policy_type', 'family_policy_detail',

            # Thông tin nghĩa vụ quân sự
            'military_service', 'military_service_date', 'military_service_end_date', 'military_service_role',

            # Thông tin chuyên môn
            'education_level', 'education_detail', 'experience', 'skills', 'resume', 'avatar', 'cover_letter',

            # Thông tin bổ sung
            'portfolio_url', 'linkedin_profile', 'expected_salary', 'salary_currency',

            # Điều khoản
            'agree_terms'
        ]

    def validate(self, data):
        # Không kiểm tra điều khoản nữa

        # Tạo full_name từ first_name và last_name nếu không được cung cấp
        if not data.get('full_name') and data.get('first_name') and data.get('last_name'):
            data['full_name'] = f"{data['last_name']} {data['first_name']}"

        # Kiểm tra các trường bắt buộc
        required_fields = ['full_name', 'email', 'phone']

        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError({field: f"Trường này là bắt buộc"})

        # Đảm bảo các trường boolean có giá trị mặc định
        boolean_fields = ['is_party_member', 'is_family_policy', 'military_service']
        for field in boolean_fields:
            if field not in data:
                data[field] = False

        # Kiểm tra các trường phụ thuộc
        if data.get('is_family_policy'):
            if not data.get('family_policy_type'):
                raise serializers.ValidationError({"family_policy_type": "Vui lòng chọn loại chính sách"})
            # Chi tiết chính sách không bắt buộc
            # if not data.get('family_policy_detail'):
            #     raise serializers.ValidationError({"family_policy_detail": "Vui lòng nhập chi tiết chính sách"})

        if data.get('military_service'):
            # Ngày bắt đầu và kết thúc nghĩa vụ quân sự không bắt buộc
            pass
            # if not data.get('military_service_date'):
            #     raise serializers.ValidationError({"military_service_date": "Vui lòng nhập ngày bắt đầu"})
            # if not data.get('military_service_end_date'):
            #     raise serializers.ValidationError({"military_service_end_date": "Vui lòng nhập ngày kết thúc"})

        return data

    def validate_job_posting(self, value):
        if value.status != 'published':
            raise serializers.ValidationError("Tin tuyển dụng này không còn nhận hồ sơ")
        return value

    def create(self, validated_data):
        # Loại bỏ trường agree_terms khỏi validated_data
        validated_data.pop('agree_terms', None)
        return super().create(validated_data)

class JobApplicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = [
            'status', 'notes'
        ]

class InterviewListSerializer(serializers.ModelSerializer):
    application_name = serializers.SerializerMethodField()
    interview_type_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    result_display = serializers.SerializerMethodField()

    class Meta:
        model = Interview
        fields = [
            'id', 'application', 'application_name', 'interview_type',
            'interview_type_display', 'scheduled_date', 'location',
            'status', 'status_display', 'result', 'result_display'
        ]

    def get_application_name(self, obj):
        return obj.application.full_name

    def get_interview_type_display(self, obj):
        return obj.get_interview_type_display()

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_result_display(self, obj):
        return obj.get_result_display()

class InterviewDetailSerializer(serializers.ModelSerializer):
    application = JobApplicationListSerializer(read_only=True)
    interviewers = UserSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    interview_type_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    result_display = serializers.SerializerMethodField()

    class Meta:
        model = Interview
        fields = '__all__'

    def get_interview_type_display(self, obj):
        return obj.get_interview_type_display()

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_result_display(self, obj):
        return obj.get_result_display()

class InterviewCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = [
            'application', 'interview_type', 'interviewers', 'scheduled_date',
            'location', 'status', 'result', 'evaluation', 'notes'
        ]

    def validate(self, data):
        # Kiểm tra xem đơn ứng tuyển có hợp lệ không
        if data.get('application') and data.get('application').status == 'rejected':
            raise serializers.ValidationError({"application": "Không thể lên lịch phỏng vấn cho đơn đã bị từ chối"})

        return data
