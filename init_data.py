#!/usr/bin/env python
"""
Script để khởi tạo dữ liệu mẫu cho hệ thống SmartHRM
"""
import os
import django
import random
from datetime import datetime, timedelta

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smarthrm.settings')
django.setup()

# Import các models
from django.contrib.auth.models import User
from django.utils import timezone
from company.models import Company
from departments.models import Department
from factories.models import Factory
from employees.models import Employee, JobTitle
from documents.models import DocumentCategory, Document
from notifications.models import Notification

def create_superuser():
    """Tạo tài khoản superuser"""
    if not User.objects.filter(username='admin').exists():
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print(f"Đã tạo superuser: {user.username}")
    else:
        print("Superuser đã tồn tại")

def create_company():
    """Tạo thông tin công ty"""
    if not Company.objects.exists():
        company = Company.objects.create(
            name="Công ty Cổ phần Dệt May 29/3",
            short_name="Hachiba",
            address="60 Mê Linh, Thanh Khê Tây, Thanh Khê, Đà Nẵng",
            phone="02363756999",
            email="hcb@hachiba.com.vn",
            website="https://hachiba.com.vn",
            tax_code="0400101531",
            representative="Nguyễn Văn A",
            position="Tổng Giám đốc",
            description="Công ty Cổ phần Dệt May 29/3 (Hachiba) là một trong những doanh nghiệp dệt may hàng đầu tại Việt Nam.",
            foundation_date=datetime(1975, 3, 29).date()
        )
        print(f"Đã tạo thông tin công ty: {company.name}")
    else:
        print("Thông tin công ty đã tồn tại")

def create_departments():
    """Tạo các phòng ban"""
    departments = [
        {"name": "Ban Giám đốc", "code": "BGD", "description": "Ban lãnh đạo công ty"},
        {"name": "Phòng Nhân sự", "code": "PNS", "description": "Quản lý nhân sự và tuyển dụng"},
        {"name": "Phòng Kế toán", "code": "PKT", "description": "Quản lý tài chính và kế toán"},
        {"name": "Phòng Kinh doanh", "code": "PKD", "description": "Quản lý kinh doanh và bán hàng"},
        {"name": "Phòng Kỹ thuật", "code": "PKY", "description": "Quản lý kỹ thuật và công nghệ"},
        {"name": "Phòng Chất lượng", "code": "PCL", "description": "Quản lý và đảm bảo chất lượng sản phẩm"},
    ]

    for dept_data in departments:
        if not Department.objects.filter(code=dept_data["code"]).exists():
            dept = Department.objects.create(**dept_data)
            print(f"Đã tạo phòng ban: {dept.name}")
        else:
            print(f"Phòng ban {dept_data['name']} đã tồn tại")

def create_factories():
    """Tạo các xí nghiệp"""
    factories = [
        {"name": "Xí nghiệp May 1", "code": "XNM1", "description": "Xí nghiệp may xuất khẩu số 1"},
        {"name": "Xí nghiệp May 2", "code": "XNM2", "description": "Xí nghiệp may xuất khẩu số 2"},
        {"name": "Xí nghiệp Dệt", "code": "XND", "description": "Xí nghiệp dệt"},
        {"name": "Xí nghiệp Nhuộm", "code": "XNN", "description": "Xí nghiệp nhuộm"},
    ]

    for factory_data in factories:
        if not Factory.objects.filter(code=factory_data["code"]).exists():
            factory = Factory.objects.create(**factory_data)
            print(f"Đã tạo xí nghiệp: {factory.name}")
        else:
            print(f"Xí nghiệp {factory_data['name']} đã tồn tại")

def create_job_titles():
    """Tạo các chức danh công việc"""
    job_titles = [
        {"name": "Giám đốc", "code": "GD", "description": "Giám đốc điều hành"},
        {"name": "Phó Giám đốc", "code": "PGD", "description": "Phó Giám đốc"},
        {"name": "Trưởng phòng", "code": "TP", "description": "Trưởng phòng"},
        {"name": "Phó phòng", "code": "PP", "description": "Phó phòng"},
        {"name": "Nhân viên", "code": "NV", "description": "Nhân viên"},
        {"name": "Công nhân", "code": "CN", "description": "Công nhân"},
        {"name": "Quản đốc", "code": "QD", "description": "Quản đốc xí nghiệp"},
        {"name": "Phó Quản đốc", "code": "PQD", "description": "Phó Quản đốc xí nghiệp"},
    ]

    for job_data in job_titles:
        if not JobTitle.objects.filter(code=job_data["code"]).exists():
            job = JobTitle.objects.create(**job_data)
            print(f"Đã tạo chức danh: {job.name}")
        else:
            print(f"Chức danh {job_data['name']} đã tồn tại")

def create_employees():
    """Tạo nhân viên mẫu"""
    # Lấy các phòng ban, xí nghiệp và chức danh
    departments = list(Department.objects.all())
    factories = list(Factory.objects.all())
    job_titles = list(JobTitle.objects.all())

    # Tạo nhân viên cho các phòng ban
    employees_data = [
        {
            "first_name": "Nguyễn Văn",
            "last_name": "A",
            "email": "nguyenvana@example.com",
            "phone_number": "0901234567",
            "date_of_birth": datetime(1980, 1, 15).date(),
            "gender": "male",
            "permanent_address": "123 Đường ABC, Quận XYZ, Đà Nẵng",
            "current_address": "123 Đường ABC, Quận XYZ, Đà Nẵng",
            "id_card_number": "123456789012",
            "job_title": JobTitle.objects.get(code="GD"),
            "department": Department.objects.get(code="BGD"),
            "factory": None,
            "join_date": datetime(2010, 5, 10).date(),
            "is_active": True
        },
        {
            "first_name": "Trần Thị",
            "last_name": "B",
            "email": "tranthib@example.com",
            "phone_number": "0901234568",
            "date_of_birth": datetime(1985, 3, 20).date(),
            "gender": "female",
            "permanent_address": "456 Đường DEF, Quận UVW, Đà Nẵng",
            "current_address": "456 Đường DEF, Quận UVW, Đà Nẵng",
            "id_card_number": "123456789013",
            "job_title": JobTitle.objects.get(code="TP"),
            "department": Department.objects.get(code="PNS"),
            "factory": None,
            "join_date": datetime(2012, 7, 15).date(),
            "is_active": True
        },
        {
            "first_name": "Lê Văn",
            "last_name": "C",
            "email": "levanc@example.com",
            "phone_number": "0901234569",
            "date_of_birth": datetime(1990, 5, 25).date(),
            "gender": "male",
            "permanent_address": "789 Đường GHI, Quận RST, Đà Nẵng",
            "current_address": "789 Đường GHI, Quận RST, Đà Nẵng",
            "id_card_number": "123456789014",
            "job_title": JobTitle.objects.get(code="QD"),
            "department": None,
            "factory": Factory.objects.get(code="XNM1"),
            "join_date": datetime(2015, 9, 20).date(),
            "is_active": True
        },
    ]

    # Tạo thêm 20 nhân viên ngẫu nhiên
    first_names = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Đặng", "Bùi"]
    middle_names = ["Văn", "Thị", "Đức", "Minh", "Quang", "Thành", "Hữu", "Công", "Thanh", "Thị"]
    last_names = ["An", "Bình", "Cường", "Dũng", "Em", "Phương", "Giang", "Hùng", "Linh", "Minh"]

    for i in range(20):
        first_name = random.choice(middle_names) + " " + random.choice(last_names)
        last_name = random.choice(first_names)
        email = f"{last_name.lower()}{i+1}@example.com"
        phone = f"090{random.randint(1000000, 9999999)}"
        date_of_birth = datetime(random.randint(1970, 2000), random.randint(1, 12), random.randint(1, 28)).date()
        gender = random.choice(["male", "female"])
        address = f"{random.randint(1, 999)} Đường {random.choice(['A', 'B', 'C', 'D', 'E'])}, Quận {random.choice(['X', 'Y', 'Z'])}, Đà Nẵng"
        id_number = f"{random.randint(100000000000, 999999999999)}"
        job_title = random.choice(job_titles)

        # Quyết định ngẫu nhiên nhân viên thuộc phòng ban hay xí nghiệp
        if random.choice([True, False]):
            department = random.choice(departments)
            factory = None
            workplace_type = 'department'
        else:
            department = None
            factory = random.choice(factories)
            workplace_type = 'factory'

        join_date = datetime(random.randint(2010, 2023), random.randint(1, 12), random.randint(1, 28)).date()

        employees_data.append({
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone,
            "date_of_birth": date_of_birth,
            "gender": gender,
            "permanent_address": address,
            "current_address": address,
            "id_card_number": id_number,
            "job_title": job_title,
            "department": department,
            "factory": factory,
            "workplace_type": workplace_type,
            "join_date": join_date,
            "is_active": True
        })

    # Tạo nhân viên và tài khoản người dùng
    for emp_data in employees_data:
        email = emp_data.get("email")
        if not Employee.objects.filter(email=email).exists():
            # Tạo tài khoản người dùng
            username = email.split("@")[0]
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password="password123",
                    first_name=emp_data["first_name"],
                    last_name=emp_data["last_name"]
                )

                # Tạo nhân viên
                employee = Employee.objects.create(
                    user=user,
                    **emp_data
                )
                print(f"Đã tạo nhân viên: {employee.first_name} {employee.last_name}")
            else:
                print(f"Tài khoản {username} đã tồn tại")
        else:
            print(f"Nhân viên với email {email} đã tồn tại")

def create_document_categories():
    """Tạo các loại tài liệu"""
    categories = [
        {"name": "Quy chế", "code": "QC", "description": "Các quy chế của công ty"},
        {"name": "Quy định", "code": "QD", "description": "Các quy định của công ty"},
        {"name": "Quy trình", "code": "QT", "description": "Các quy trình làm việc"},
        {"name": "Biểu mẫu", "code": "BM", "description": "Các biểu mẫu"},
        {"name": "Hợp đồng", "code": "HD", "description": "Các loại hợp đồng"},
        {"name": "Tài liệu khác", "code": "TL", "description": "Các tài liệu khác"},
    ]

    for cat_data in categories:
        if not DocumentCategory.objects.filter(code=cat_data["code"]).exists():
            category = DocumentCategory.objects.create(**cat_data)
            print(f"Đã tạo loại tài liệu: {category.name}")
        else:
            print(f"Loại tài liệu {cat_data['name']} đã tồn tại")

def create_documents():
    """Tạo các tài liệu mẫu"""
    # Lấy các loại tài liệu
    categories = list(DocumentCategory.objects.all())

    documents_data = [
        {
            "title": "Quy chế làm việc",
            "document_number": "QC-LV-01",
            "category": DocumentCategory.objects.get(code="QC"),
            "document_type": "policy",
            "description": "Quy chế làm việc của công ty",
            "content": "Nội dung quy chế làm việc...",
            "version": "1.0",
            "access_level": "internal",
            "created_by": User.objects.get(username="admin")
        },
        {
            "title": "Quy định về trang phục",
            "document_number": "QD-TP-01",
            "category": DocumentCategory.objects.get(code="QD"),
            "document_type": "policy",
            "description": "Quy định về trang phục làm việc",
            "content": "Nội dung quy định về trang phục...",
            "version": "1.0",
            "access_level": "internal",
            "created_by": User.objects.get(username="admin")
        },
        {
            "title": "Quy trình tuyển dụng",
            "document_number": "QT-TD-01",
            "category": DocumentCategory.objects.get(code="QT"),
            "document_type": "procedure",
            "description": "Quy trình tuyển dụng nhân sự",
            "content": "Nội dung quy trình tuyển dụng...",
            "version": "1.0",
            "access_level": "internal",
            "created_by": User.objects.get(username="admin")
        },
    ]

    # Tạo thêm 10 tài liệu ngẫu nhiên
    titles = [
        "Biểu mẫu đánh giá nhân viên",
        "Hợp đồng lao động",
        "Quy định về chấm công",
        "Quy trình đào tạo",
        "Quy chế lương thưởng",
        "Biểu mẫu đề xuất mua sắm",
        "Quy định về an toàn lao động",
        "Quy trình kiểm soát chất lượng",
        "Hợp đồng thử việc",
        "Quy định về bảo mật thông tin"
    ]

    document_types = ["policy", "procedure", "form", "contract", "other"]
    access_levels = ["public", "internal", "restricted"]

    for i, title in enumerate(titles):
        category = random.choice(categories)
        document_number = f"{category.code}-{i+1:02d}"
        document_type = random.choice(document_types)
        access_level = random.choice(access_levels)

        documents_data.append({
            "title": title,
            "document_number": document_number,
            "category": category,
            "document_type": document_type,
            "description": f"Mô tả về {title.lower()}",
            "content": f"Nội dung {title.lower()}...",
            "version": "1.0",
            "access_level": access_level,
            "created_by": User.objects.get(username="admin")
        })

    for doc_data in documents_data:
        if not Document.objects.filter(document_number=doc_data["document_number"]).exists():
            document = Document.objects.create(**doc_data)
            print(f"Đã tạo tài liệu: {document.title}")
        else:
            print(f"Tài liệu {doc_data['title']} đã tồn tại")

def create_notifications():
    """Tạo thông báo mẫu"""
    # Lấy danh sách người dùng
    users = list(User.objects.all())

    # Các loại thông báo
    notification_types = ['system', 'document', 'task', 'message', 'approval', 'other']
    priority_levels = ['low', 'normal', 'high', 'urgent']
    display_types = ['popup', 'toast', 'badge']

    # Tạo 15 thông báo ngẫu nhiên
    for i in range(15):
        recipient = random.choice(users)
        sender = random.choice(users) if random.choice([True, False]) else None
        title = f"Thông báo {i+1}"
        message = f"Nội dung thông báo {i+1}. Đây là thông báo tự động được tạo bởi hệ thống."
        notification_type = random.choice(notification_types)
        priority = random.choice(priority_levels)
        display_type = random.choice(display_types)
        is_read = random.choice([True, False])
        requires_action = random.choice([True, False])

        # Tạo thông báo
        notification = Notification.objects.create(
            recipient=recipient,
            sender=sender,
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            display_type=display_type,
            is_read=is_read,
            requires_action=requires_action,
            link=f"/notifications/{i+1}/" if requires_action else None,
            action_text="Xem chi tiết" if requires_action else None
        )

        # Nếu thông báo đã đọc, cập nhật thời gian đọc
        if is_read:
            notification.read_at = timezone.now() - timedelta(days=random.randint(0, 5))
            notification.save(update_fields=['read_at'])

        print(f"Đã tạo thông báo: {notification.title}")

def main():
    """Hàm chính để khởi tạo dữ liệu"""
    print("Bắt đầu khởi tạo dữ liệu mẫu...")

    # Tạo superuser
    create_superuser()

    # Tạo thông tin công ty
    create_company()

    # Tạo các phòng ban
    create_departments()

    # Tạo các xí nghiệp
    create_factories()

    # Tạo các chức danh công việc
    create_job_titles()

    # Tạo nhân viên
    create_employees()

    # Tạo các loại tài liệu
    create_document_categories()

    # Tạo các tài liệu
    create_documents()

    # Tạo thông báo
    create_notifications()

    print("Hoàn thành khởi tạo dữ liệu mẫu!")

if __name__ == "__main__":
    main()
