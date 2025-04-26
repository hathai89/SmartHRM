# SmartHRM - Hệ thống Quản lý Nhân sự Thông minh

SmartHRM là một hệ thống quản lý nhân sự toàn diện được phát triển bằng Django và Vue.js, giúp doanh nghiệp quản lý hiệu quả các quy trình nhân sự từ tuyển dụng, quản lý nhân viên, hợp đồng, đến quản lý tài sản công ty.

## Cấu trúc dự án

Dự án được chia thành hai phần chính:

- **Backend**: Django REST framework API
- **Frontend**: Vue.js 3 SPA (Single Page Application)

## Tính năng chính

### Quản lý cơ cấu tổ chức
- Quản lý thông tin công ty
- Quản lý phòng ban theo cấu trúc phân cấp (Phòng ban > Bộ phận > Nhóm)
- Quản lý xí nghiệp theo cấu trúc phân cấp (Xí nghiệp > Bộ phận > Nhóm)

### Quản lý nhân sự
- Quản lý thông tin nhân viên chi tiết (thông tin cá nhân, công việc, gia đình, CCCD, bảo hiểm...)
- Quản lý hồ sơ nhân viên
- Quản lý thẻ nhân viên
- Quản lý hợp đồng thử việc
- Quản lý quyết định nhận chính thức
- Quản lý hợp đồng chính thức

### Quản lý tuyển dụng
- Quản lý tin tuyển dụng
- Quản lý đơn ứng tuyển
- Theo dõi quy trình tuyển dụng
- Quản lý trạng thái ứng viên

### Quản lý tài sản
- Quản lý danh mục tài sản
- Quản lý cấp phát tài sản cho nhân viên
- Quản lý bảo trì tài sản
- Quản lý kiểm kê tài sản

### Hệ thống thông báo
- Thông báo qua WebSocket
- Thông báo qua email

## Yêu cầu hệ thống

### Backend
- Python 3.8+
- Django 5.1+
- PostgreSQL
- Redis (cho WebSocket và cache)

### Frontend
- Node.js 14+
- npm 6+
- Vue.js 3
- Vue CLI 5

## Cài đặt

### Backend

1. Clone repository:
```
git clone https://github.com/yourusername/smarthrm.git
cd smarthrm
```

2. Tạo và kích hoạt môi trường ảo:
```
python -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate
```

3. Cài đặt các gói phụ thuộc:
```
pip install -r requirements.txt
```

4. Tạo cơ sở dữ liệu PostgreSQL:
```
createdb smarthrm
```

5. Cấu hình cơ sở dữ liệu trong `smarthrm/settings.py`

6. Chạy migration:
```
python manage.py migrate
```

7. Tạo tài khoản admin:
```
python manage.py createsuperuser
```

8. Chạy server:
```
python manage.py runserver
```

### Frontend

1. Di chuyển vào thư mục frontend:
```
cd frontend
```

2. Cài đặt các gói phụ thuộc:
```
npm install
```

3. Chạy server phát triển:
```
npm run serve
```

4. Biên dịch cho môi trường sản xuất:
```
npm run build
```

## Đóng góp

Chúng tôi rất hoan nghênh mọi đóng góp cho dự án. Vui lòng tạo issue hoặc pull request trên GitHub.

## Giấy phép

Dự án này được phân phối dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.
