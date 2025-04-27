#!/bin/bash

# Tạo thư mục ~/.local/lib nếu chưa tồn tại
mkdir -p ~/.local/lib

# Tạo symbolic link từ thư viện thực tế đến tên thư viện mà WeasyPrint đang tìm kiếm
ln -sf /opt/homebrew/lib/libgobject-2.0-0.dylib ~/.local/lib/libgobject-2.0-0.dylib

# Thiết lập biến môi trường
export DYLD_LIBRARY_PATH=~/.local/lib:/opt/homebrew/lib:$DYLD_LIBRARY_PATH
export PKG_CONFIG_PATH=/opt/homebrew/lib/pkgconfig:$PKG_CONFIG_PATH

echo "Đã thiết lập môi trường cho WeasyPrint"
echo "DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH"
echo "PKG_CONFIG_PATH=$PKG_CONFIG_PATH"
