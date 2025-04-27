# Hướng dẫn triển khai SmartHRM cho môi trường production

Tài liệu này hướng dẫn cách triển khai SmartHRM cho môi trường production sử dụng Nginx, Gunicorn và PostgreSQL.

## Yêu cầu hệ thống

- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Redis 6+
- Nginx
- Gunicorn

## Các bước triển khai

### 1. Chuẩn bị môi trường

```bash
# Cài đặt các gói cần thiết
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql redis-server

# Tạo thư mục cho dự án
mkdir -p /var/www/smarthrm
cd /var/www/smarthrm

# Clone dự án từ repository
git clone https://github.com/your-username/smarthrm.git .
```

### 2. Cài đặt và cấu hình PostgreSQL

```bash
# Tạo database và user
sudo -u postgres psql

CREATE DATABASE smarthrm;
CREATE USER smarthrm_user WITH PASSWORD 'your_secure_password';
ALTER ROLE smarthrm_user SET client_encoding TO 'utf8';
ALTER ROLE smarthrm_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE smarthrm_user SET timezone TO 'Asia/Ho_Chi_Minh';
GRANT ALL PRIVILEGES ON DATABASE smarthrm TO smarthrm_user;
\q
```

### 3. Cài đặt và cấu hình Python

```bash
# Tạo môi trường ảo Python
python3 -m venv venv
source venv/bin/activate

# Cài đặt các gói Python
pip install -r requirements.txt
pip install gunicorn
```

### 4. Cài đặt và build frontend

```bash
# Cài đặt Node.js dependencies
cd frontend
npm install

# Build frontend cho production
npm run build
cd ..
```

### 5. Cấu hình Django cho production

Tạo file `.env` trong thư mục gốc của dự án:

```
DEBUG=False
SECRET_KEY=your_secure_secret_key
ALLOWED_HOSTS=your_domain.com,www.your_domain.com
DATABASE_URL=postgres://smarthrm_user:your_secure_password@localhost:5432/smarthrm
REDIS_URL=redis://localhost:6379/1
```

Thu thập static files:

```bash
python manage.py collectstatic --noinput
```

Áp dụng migrations:

```bash
python manage.py migrate
```

### 6. Cấu hình Gunicorn

Tạo file `/etc/systemd/system/smarthrm.service`:

```ini
[Unit]
Description=SmartHRM Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/smarthrm
ExecStart=/var/www/smarthrm/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/var/www/smarthrm/smarthrm.sock smarthrm.wsgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Khởi động và kích hoạt service:

```bash
sudo systemctl start smarthrm
sudo systemctl enable smarthrm
```

### 7. Cấu hình Nginx

Tạo file `/etc/nginx/sites-available/smarthrm`:

```nginx
server {
    listen 80;
    server_name your_domain.com www.your_domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/smarthrm;
    }
    
    location /media/ {
        root /var/www/smarthrm;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/smarthrm/smarthrm.sock;
    }
}
```

Kích hoạt cấu hình Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/smarthrm /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### 8. Cấu hình HTTPS (tùy chọn nhưng khuyến nghị)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain.com -d www.your_domain.com
```

### 9. Cấu hình Redis cho cache và Channels

Đảm bảo Redis đang chạy:

```bash
sudo systemctl status redis-server
```

### 10. Kiểm tra và hoàn tất

Truy cập trang web của bạn tại `https://your_domain.com` và đảm bảo mọi thứ hoạt động bình thường.

## Bảo trì và cập nhật

### Cập nhật code

```bash
cd /var/www/smarthrm
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart smarthrm
```

### Backup database

```bash
pg_dump -U smarthrm_user -d smarthrm > smarthrm_backup_$(date +%Y%m%d).sql
```

## Xử lý sự cố

### Kiểm tra logs

```bash
# Logs của Gunicorn
sudo journalctl -u smarthrm

# Logs của Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Khởi động lại các dịch vụ

```bash
sudo systemctl restart smarthrm
sudo systemctl restart nginx
sudo systemctl restart redis-server
```

## Kết luận

Bạn đã triển khai thành công SmartHRM trong môi trường production. Hệ thống sẽ phục vụ frontend Vue.js và backend Django API trên cùng một domain, giúp đơn giản hóa việc triển khai và bảo trì.
