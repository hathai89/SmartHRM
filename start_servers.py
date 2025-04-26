#!/usr/bin/env python
"""
Script để chạy cả backend Django và frontend Vue.js cùng một lúc.
Hoạt động trên cả Windows và macOS/Linux.
"""

import os
import sys
import subprocess
import time
import signal
import platform
import webbrowser
from pathlib import Path

# Màu sắc cho terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Đường dẫn
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / 'frontend'
VENV_DIR = BASE_DIR / 'venv'
VENV_ACTIVATE = VENV_DIR / ('Scripts' if platform.system() == 'Windows' else 'bin') / 'activate'

# Các URL
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:8080"
API_URL = f"{BACKEND_URL}/api/"
ADMIN_URL = f"{BACKEND_URL}/admin/"

# Các tiến trình
processes = []

def print_banner():
    """In banner cho script"""
    print(f"{Colors.HEADER}{'=' * 53}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'STARTING SMARTHRM SERVERS':^53}{Colors.ENDC}")
    print(f"{Colors.HEADER}{'=' * 53}{Colors.ENDC}")

def print_urls():
    """In các URL cho người dùng"""
    print(f"\n{Colors.HEADER}{'=' * 53}{Colors.ENDC}")
    print(f"{Colors.BOLD}  SmartHRM servers are running:{Colors.ENDC}")
    print(f"  - Backend: {Colors.BLUE}{BACKEND_URL}{Colors.ENDC}")
    print(f"  - Frontend: {Colors.BLUE}{FRONTEND_URL}{Colors.ENDC}")
    print(f"  - API: {Colors.BLUE}{API_URL}{Colors.ENDC}")
    print(f"  - Admin: {Colors.BLUE}{ADMIN_URL}{Colors.ENDC}")
    print(f"{Colors.HEADER}{'=' * 53}{Colors.ENDC}")
    print(f"\n{Colors.BOLD}Press Ctrl+C to stop all servers{Colors.ENDC}\n")

def setup_environment():
    """Thiết lập môi trường phát triển"""
    # Kiểm tra và tạo môi trường ảo Python
    if not VENV_DIR.exists():
        print(f"{Colors.YELLOW}Creating Python virtual environment...{Colors.ENDC}")
        subprocess.run([sys.executable, "-m", "venv", "venv"], cwd=BASE_DIR, check=True)
        
        # Cài đặt các gói phụ thuộc
        print(f"{Colors.YELLOW}Installing Python dependencies...{Colors.ENDC}")
        if platform.system() == 'Windows':
            subprocess.run(["venv\\Scripts\\pip", "install", "-r", "requirements.txt"], cwd=BASE_DIR, check=True)
        else:
            subprocess.run(["./venv/bin/pip", "install", "-r", "requirements.txt"], cwd=BASE_DIR, check=True)
    
    # Kiểm tra và cài đặt các gói phụ thuộc Node.js
    node_modules = FRONTEND_DIR / 'node_modules'
    if not node_modules.exists():
        print(f"{Colors.YELLOW}Installing Node.js dependencies...{Colors.ENDC}")
        subprocess.run(["npm", "install"], cwd=FRONTEND_DIR, check=True)
    
    # Chạy migrations
    print(f"{Colors.YELLOW}Checking database migrations...{Colors.ENDC}")
    if platform.system() == 'Windows':
        subprocess.run(["venv\\Scripts\\python", "manage.py", "migrate"], cwd=BASE_DIR, check=True)
    else:
        subprocess.run(["./venv/bin/python", "manage.py", "migrate"], cwd=BASE_DIR, check=True)

def start_django_server():
    """Khởi động Django server"""
    print(f"{Colors.GREEN}Starting Django backend server...{Colors.ENDC}")
    
    if platform.system() == 'Windows':
        process = subprocess.Popen(["venv\\Scripts\\python", "manage.py", "runserver"], cwd=BASE_DIR)
    else:
        process = subprocess.Popen(["./venv/bin/python", "manage.py", "runserver"], cwd=BASE_DIR)
    
    processes.append(process)
    print(f"{Colors.GREEN}Django server running with PID: {process.pid}{Colors.ENDC}")
    return process

def start_vue_server():
    """Khởi động Vue.js server"""
    print(f"{Colors.GREEN}Starting Vue.js frontend server...{Colors.ENDC}")
    
    process = subprocess.Popen(["npm", "run", "serve"], cwd=FRONTEND_DIR)
    processes.append(process)
    print(f"{Colors.GREEN}Vue.js server running with PID: {process.pid}{Colors.ENDC}")
    return process

def open_browsers():
    """Mở trình duyệt với các URL"""
    print(f"{Colors.BLUE}Opening browsers...{Colors.ENDC}")
    time.sleep(5)  # Đợi server khởi động
    
    webbrowser.open(FRONTEND_URL)
    time.sleep(1)
    webbrowser.open(BACKEND_URL)

def cleanup(signum=None, frame=None):
    """Dọn dẹp khi thoát script"""
    print(f"\n{Colors.YELLOW}Stopping servers...{Colors.ENDC}")
    
    for process in processes:
        if platform.system() == 'Windows':
            process.terminate()
        else:
            process.send_signal(signal.SIGTERM)
    
    print(f"{Colors.YELLOW}Servers stopped.{Colors.ENDC}")
    sys.exit(0)

def main():
    """Hàm chính"""
    print_banner()
    
    try:
        # Thiết lập môi trường
        setup_environment()
        
        # Khởi động các server
        django_process = start_django_server()
        vue_process = start_vue_server()
        
        # In thông tin URL
        print_urls()
        
        # Mở trình duyệt
        open_browsers()
        
        # Đợi người dùng nhấn Ctrl+C
        signal.signal(signal.SIGINT, cleanup)
        signal.signal(signal.SIGTERM, cleanup)
        
        # Giữ script chạy
        while True:
            time.sleep(1)
            
            # Kiểm tra xem các tiến trình có còn chạy không
            if django_process.poll() is not None:
                print(f"{Colors.RED}Django server stopped unexpectedly!{Colors.ENDC}")
                cleanup()
            
            if vue_process.poll() is not None:
                print(f"{Colors.RED}Vue.js server stopped unexpectedly!{Colors.ENDC}")
                cleanup()
    
    except KeyboardInterrupt:
        cleanup()
    except Exception as e:
        print(f"{Colors.RED}Error: {str(e)}{Colors.ENDC}")
        cleanup()

if __name__ == "__main__":
    main()
