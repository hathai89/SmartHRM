#!/usr/bin/env python
"""
Script để kiểm tra xem WeasyPrint có hoạt động không
"""
import os
import sys

# Thiết lập môi trường
os.environ['DYLD_LIBRARY_PATH'] = os.path.expanduser('~/.local/lib') + ':' + os.environ.get('DYLD_LIBRARY_PATH', '')
os.environ['PKG_CONFIG_PATH'] = '/opt/homebrew/lib/pkgconfig:' + os.environ.get('PKG_CONFIG_PATH', '')

try:
    from weasyprint import HTML
    print("WeasyPrint đã được import thành công!")
    
    # Tạo một file PDF đơn giản
    html = HTML(string="<h1>Hello, WeasyPrint!</h1>")
    pdf_bytes = html.write_pdf()
    print(f"Đã tạo PDF thành công với kích thước {len(pdf_bytes)} bytes")
    
    # Lưu file PDF
    with open('test_weasyprint.pdf', 'wb') as f:
        f.write(pdf_bytes)
    print(f"Đã lưu file PDF tại {os.path.abspath('test_weasyprint.pdf')}")
    
    print("WeasyPrint hoạt động tốt!")
    sys.exit(0)
except Exception as e:
    print(f"Lỗi khi sử dụng WeasyPrint: {e}")
    sys.exit(1)
