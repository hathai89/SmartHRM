@echo off
echo =====================================================
echo           STARTING SMARTHRM SERVERS                  
echo =====================================================

REM Kiểm tra môi trường ảo Python
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    echo Installing Python dependencies...
    pip install -r requirements.txt
) else (
    echo Activating Python virtual environment...
    call venv\Scripts\activate
)

REM Kiểm tra node_modules trong thư mục frontend
if not exist frontend\node_modules (
    echo Installing Node.js dependencies...
    cd frontend
    npm install
    cd ..
)

REM Kiểm tra cơ sở dữ liệu
echo Checking database migrations...
python manage.py migrate

REM Chạy Django server trong một cửa sổ mới
echo Starting Django backend server...
start "Django Backend" cmd /k "venv\Scripts\activate && python manage.py runserver 8000"

REM Chạy Vue.js server trong một cửa sổ mới
echo Starting Vue.js frontend server...
start "Vue.js Frontend" cmd /k "cd frontend && npm run serve"

echo.
echo =====================================================
echo   SmartHRM servers are running:                      
echo   - Backend: http://localhost:8000                   
echo   - Frontend: http://localhost:8080                  
echo   - API: http://localhost:8000/api/                  
echo   - Admin: http://localhost:8000/admin/              
echo =====================================================
echo.
echo Close the command windows to stop the servers
echo.

REM Giữ cửa sổ chính mở
pause
