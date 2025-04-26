# SmartHRM Frontend

Frontend cho hệ thống quản lý nhân sự SmartHRM sử dụng Vue.js 3.

## Cài đặt

```bash
# Cài đặt các gói phụ thuộc
npm install

# Chạy môi trường phát triển với hot-reload
npm run serve

# Biên dịch và tối ưu hóa cho môi trường sản xuất
npm run build

# Kiểm tra và sửa lỗi
npm run lint
```

## Cấu trúc dự án

```
frontend/
├── public/                 # Tài nguyên tĩnh
├── src/
│   ├── assets/             # Tài nguyên (CSS, SCSS, images)
│   ├── components/         # Các component Vue
│   │   ├── common/         # Component dùng chung
│   │   ├── layout/         # Component layout
│   │   └── ...             # Component theo module
│   ├── locales/            # File ngôn ngữ
│   ├── router/             # Cấu hình router
│   ├── services/           # Service gọi API
│   ├── store/              # Vuex store
│   │   ├── modules/        # Các module store
│   │   └── index.js        # Cấu hình store
│   ├── utils/              # Các hàm tiện ích
│   ├── views/              # Các trang
│   ├── App.vue             # Component gốc
│   └── main.js             # Điểm khởi đầu
├── .eslintrc.js            # Cấu hình ESLint
├── babel.config.js         # Cấu hình Babel
├── package.json            # Cấu hình npm
└── vue.config.js           # Cấu hình Vue CLI
```

## Tính năng

- Xác thực người dùng (đăng nhập, đăng xuất, đổi mật khẩu)
- Quản lý nhân viên
- Quản lý phòng ban
- Quản lý xí nghiệp
- Quản lý tài liệu
- Thông báo thời gian thực
- Hỗ trợ đa ngôn ngữ (Tiếng Việt)
- Giao diện đáp ứng (responsive)

## Công nghệ sử dụng

- Vue.js 3
- Vue Router 4
- Vuex 4
- Bootstrap 5
- Axios
- Chart.js
- FontAwesome
- Vee-Validate
- Vue I18n
