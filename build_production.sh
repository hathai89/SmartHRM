#!/bin/bash

# Hiển thị banner
echo "====================================================="
echo "          BUILDING SMARTHRM FOR PRODUCTION          "
echo "====================================================="

# Kiểm tra môi trường ảo Python
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
else
    echo "Activating Python virtual environment..."
    source venv/bin/activate
fi

# Build Vue.js frontend
echo "Building Vue.js frontend..."
cd frontend
npm install
npm run build
cd ..

# Tạo thư mục static nếu chưa tồn tại
if [ ! -d "static" ]; then
    mkdir -p static
fi

# Thu thập static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Áp dụng migrations
echo "Applying database migrations..."
python manage.py migrate

# Tạo file .env cho production
echo "Creating .env file for production..."
cat > .env << EOL
DEBUG=False
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(50))")
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://ha:@localhost:5432/smarthrm
REDIS_URL=redis://localhost:6379/1
EOL

echo ""
echo "====================================================="
echo "  SmartHRM has been built for production!            "
echo "                                                     "
echo "  To run in production mode:                         "
echo "  1. Set DEBUG=False in settings.py                  "
echo "  2. Configure your web server (Nginx/Apache)        "
echo "  3. Run with gunicorn or uwsgi                      "
echo "                                                     "
echo "  Example with gunicorn:                             "
echo "  gunicorn smarthrm.wsgi:application --bind 0.0.0.0:8000"
echo "====================================================="
