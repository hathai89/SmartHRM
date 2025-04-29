from django.core.management.base import BaseCommand
from recruitment.models import MaritalStatus, FamilyPolicyType, Gender, EducationLevel

class Command(BaseCommand):
    help = 'Seed data for recruitment models'

    def handle(self, *args, **options):
        self.stdout.write('Seeding recruitment data...')

        # Seed MaritalStatus
        marital_statuses = [
            {'code': 'single', 'name': 'Độc thân', 'order': 1},
            {'code': 'married', 'name': 'Đã kết hôn', 'order': 2},
            {'code': 'divorced', 'name': 'Đã ly hôn', 'order': 3},
            {'code': 'widowed', 'name': 'Góa phụ', 'order': 4},
        ]

        for status in marital_statuses:
            MaritalStatus.objects.get_or_create(
                code=status['code'],
                defaults={
                    'name': status['name'],
                    'order': status['order'],
                    'is_active': True
                }
            )

        self.stdout.write(self.style.SUCCESS(f'Added {len(marital_statuses)} marital statuses'))

        # Seed FamilyPolicyType
        policy_types = [
            {'code': 'war_invalid', 'name': 'Thương binh', 'order': 1},
            {'code': 'war_martyr', 'name': 'Liệt sĩ', 'order': 2},
            {'code': 'revolution_contributor', 'name': 'Người có công với cách mạng', 'order': 3},
            {'code': 'poor_household', 'name': 'Hộ nghèo', 'order': 4},
            {'code': 'near_poor_household', 'name': 'Hộ cận nghèo', 'order': 5},
            {'code': 'ethnic_minority', 'name': 'Dân tộc thiểu số', 'order': 6},
            {'code': 'other', 'name': 'Khác', 'order': 7},
        ]

        for policy in policy_types:
            FamilyPolicyType.objects.get_or_create(
                code=policy['code'],
                defaults={
                    'name': policy['name'],
                    'order': policy['order'],
                    'is_active': True
                }
            )

        self.stdout.write(self.style.SUCCESS(f'Added {len(policy_types)} family policy types'))

        # Seed Gender
        genders = [
            {'code': 'male', 'name': 'Nam', 'order': 1},
            {'code': 'female', 'name': 'Nữ', 'order': 2},
            {'code': 'other', 'name': 'Khác', 'order': 3},
        ]

        for gender in genders:
            Gender.objects.get_or_create(
                code=gender['code'],
                defaults={
                    'name': gender['name'],
                    'order': gender['order'],
                    'is_active': True
                }
            )

        self.stdout.write(self.style.SUCCESS(f'Added {len(genders)} genders'))

        # Seed EducationLevel
        education_levels = [
            {'code': 'primary', 'name': 'Tiểu học', 'order': 1},
            {'code': 'secondary', 'name': 'Trung học cơ sở', 'order': 2},
            {'code': 'high_school', 'name': 'Trung học phổ thông', 'order': 3},
            {'code': 'vocational', 'name': 'Trung cấp nghề', 'order': 4},
            {'code': 'college', 'name': 'Cao đẳng', 'order': 5},
            {'code': 'university', 'name': 'Đại học', 'order': 6},
            {'code': 'master', 'name': 'Thạc sĩ', 'order': 7},
            {'code': 'doctor', 'name': 'Tiến sĩ', 'order': 8},
            {'code': 'professor', 'name': 'Giáo sư', 'order': 9},
            {'code': 'other', 'name': 'Khác', 'order': 10},
        ]

        for level in education_levels:
            EducationLevel.objects.get_or_create(
                code=level['code'],
                defaults={
                    'name': level['name'],
                    'order': level['order'],
                    'is_active': True
                }
            )

        self.stdout.write(self.style.SUCCESS(f'Added {len(education_levels)} education levels'))

        self.stdout.write(self.style.SUCCESS('Recruitment data seeding completed!'))
