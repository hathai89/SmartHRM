import os
import uuid
import unicodedata
import re
from django.utils.text import slugify

def get_upload_path(instance, filename, folder='uploads'):
    """Tạo đường dẫn upload file với UUID để tránh trùng tên"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join(folder, filename)

def employee_avatar_path(instance, filename):
    """Tạo đường dẫn lưu trữ avatar nhân viên"""
    return get_upload_path(instance, filename, folder='employees/avatars')

def employee_id_card_path(instance, filename):
    """Tạo đường dẫn lưu trữ ảnh CCCD/CMND nhân viên"""
    return get_upload_path(instance, filename, folder='employees/id_cards')

def company_logo_path(instance, filename):
    """Tạo đường dẫn lưu trữ logo công ty"""
    return get_upload_path(instance, filename, folder='company/logo')

def normalize_filename(filename):
    """Chuẩn hóa tên file, loại bỏ dấu tiếng Việt và ký tự đặc biệt"""
    # Loại bỏ dấu tiếng Việt
    filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode('ASCII')
    # Thay thế khoảng trắng bằng dấu gạch dưới
    filename = re.sub(r'\s+', '_', filename)
    # Loại bỏ các ký tự không phải chữ cái, số, dấu gạch dưới, dấu chấm
    filename = re.sub(r'[^\w\-\.]', '', filename)
    return filename
