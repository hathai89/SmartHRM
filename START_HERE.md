# Hướng dẫn khởi động SmartHRM

Dự án SmartHRM bao gồm hai phần: backend (Django) và frontend (Vue.js). Bạn có thể khởi động cả hai phần cùng một lúc bằng cách sử dụng một trong các script sau đây.

## Cách 1: Sử dụng script Python (Khuyến nghị)

Script Python hoạt động trên cả Windows và macOS/Linux:

```bash
python start_servers.py
```

Script này sẽ:
1. Tự động tạo môi trường ảo Python nếu chưa tồn tại
2. Cài đặt các gói phụ thuộc Python nếu cần
3. Cài đặt các gói phụ thuộc Node.js nếu cần
4. Chạy migrations cho cơ sở dữ liệu
5. Khởi động Django backend server
6. Khởi động Vue.js frontend server
7. Mở trình duyệt với các URL tương ứng

## Cách 2: Sử dụng script shell (macOS/Linux)

```bash
./start_servers.sh
```

## Cách 3: Sử dụng script batch (Windows)

```
start_servers.bat
```

## Các URL quan trọng

Sau khi khởi động, bạn có thể truy cập:

- Frontend: http://localhost:8080
- Backend: http://localhost:8000
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

## Dừng các server

- Nếu sử dụng script Python hoặc shell: Nhấn `Ctrl+C` trong terminal
- Nếu sử dụng script batch: Đóng các cửa sổ command prompt

## Khắc phục sự cố

Nếu bạn gặp lỗi khi chạy các script:

1. Đảm bảo bạn đã cài đặt Python 3.8+ và Node.js 14+
2. Đảm bảo PostgreSQL đã được cài đặt và đang chạy
3. Đảm bảo cơ sở dữ liệu `smarthrm` đã được tạo
4. Kiểm tra cấu hình cơ sở dữ liệu trong `smarthrm/settings.py`

Nếu vẫn gặp vấn đề, bạn có thể khởi động các server riêng biệt:

### Khởi động backend:

```bash
cd SmartHRM
python -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Khởi động frontend:

```bash
cd SmartHRM/frontend
npm install
npm run serve
```
