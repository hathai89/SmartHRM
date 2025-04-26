#!/bin/bash

# Hiển thị banner
echo "====================================================="
echo "          STARTING SMARTHRM SERVERS                  "
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

# Kiểm tra node_modules trong thư mục frontend
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing Node.js dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Kiểm tra cơ sở dữ liệu
echo "Checking database migrations..."
python manage.py migrate

# Chạy Django server trong background
echo "Starting Django backend server..."
python manage.py runserver 8000 &
DJANGO_PID=$!
echo "Django server running with PID: $DJANGO_PID"

# Chạy Vue.js server trong background
echo "Starting Vue.js frontend server..."
cd frontend
npm run serve &
VUE_PID=$!
echo "Vue.js server running with PID: $VUE_PID"
cd ..

echo ""
echo "====================================================="
echo "  SmartHRM servers are running:                      "
echo "  - Backend: http://localhost:8000                   "
echo "  - Frontend: http://localhost:8080                  "
echo "  - API: http://localhost:8000/api/                  "
echo "  - Admin: http://localhost:8000/admin/              "
echo "====================================================="
echo ""
echo "Press Ctrl+C to stop all servers"

# Xử lý khi người dùng nhấn Ctrl+C
trap "echo 'Stopping servers...'; kill $DJANGO_PID; kill $VUE_PID; echo 'Servers stopped.'; exit" INT

# Giữ script chạy
wait
