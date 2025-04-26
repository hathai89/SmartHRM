/**
 * Breadcrumb utilities
 */

// Định nghĩa breadcrumbs cho các route
export const routeBreadcrumbs = {
  'dashboard': [
    { title: 'Bảng điều khiển', route: { name: 'dashboard' } }
  ],
  'employees': [
    { title: 'Nhân viên', route: { name: 'employees' } }
  ],
  'employee-detail': [
    { title: 'Nhân viên', route: { name: 'employees' } },
    { title: 'Chi tiết nhân viên', route: null }
  ],
  'employee-create': [
    { title: 'Nhân viên', route: { name: 'employees' } },
    { title: 'Thêm nhân viên', route: null }
  ],
  'employee-edit': [
    { title: 'Nhân viên', route: { name: 'employees' } },
    { title: 'Chỉnh sửa nhân viên', route: null }
  ],
  'departments': [
    { title: 'Phòng ban', route: { name: 'departments' } }
  ],
  'department-detail': [
    { title: 'Phòng ban', route: { name: 'departments' } },
    { title: 'Chi tiết phòng ban', route: null }
  ],
  'department-create': [
    { title: 'Phòng ban', route: { name: 'departments' } },
    { title: 'Thêm phòng ban', route: null }
  ],
  'department-edit': [
    { title: 'Phòng ban', route: { name: 'departments' } },
    { title: 'Chỉnh sửa phòng ban', route: null }
  ],
  'factories': [
    { title: 'Xí nghiệp', route: { name: 'factories' } }
  ],
  'factory-detail': [
    { title: 'Xí nghiệp', route: { name: 'factories' } },
    { title: 'Chi tiết xí nghiệp', route: null }
  ],
  'factory-create': [
    { title: 'Xí nghiệp', route: { name: 'factories' } },
    { title: 'Thêm xí nghiệp', route: null }
  ],
  'factory-edit': [
    { title: 'Xí nghiệp', route: { name: 'factories' } },
    { title: 'Chỉnh sửa xí nghiệp', route: null }
  ],
  'documents': [
    { title: 'Tài liệu', route: { name: 'documents' } }
  ],
  'document-detail': [
    { title: 'Tài liệu', route: { name: 'documents' } },
    { title: 'Chi tiết tài liệu', route: null }
  ],
  'document-create': [
    { title: 'Tài liệu', route: { name: 'documents' } },
    { title: 'Thêm tài liệu', route: null }
  ],
  'document-edit': [
    { title: 'Tài liệu', route: { name: 'documents' } },
    { title: 'Chỉnh sửa tài liệu', route: null }
  ],
  'company': [
    { title: 'Công ty', route: { name: 'company' } }
  ],
  'profile': [
    { title: 'Hồ sơ', route: { name: 'profile' } }
  ],
  'settings': [
    { title: 'Cài đặt', route: { name: 'settings' } }
  ],
  'notifications': [
    { title: 'Thông báo', route: { name: 'notifications' } }
  ],
  'change-password': [
    { title: 'Hồ sơ', route: { name: 'profile' } },
    { title: 'Đổi mật khẩu', route: null }
  ]
};

/**
 * Lấy breadcrumbs cho route hiện tại
 * @param {String} routeName - Tên route
 * @param {Object} params - Params của route
 * @returns {Array} - Mảng breadcrumbs
 */
export function getBreadcrumbs(routeName, params = {}) {
  const breadcrumbs = routeBreadcrumbs[routeName] || [];

  // Xử lý các trường hợp đặc biệt cần thông tin động
  if (routeName === 'employee-detail' || routeName === 'employee-edit') {
    if (params.employeeName) {
      breadcrumbs[breadcrumbs.length - 1].title = params.employeeName;
    }
  }

  return breadcrumbs;
}

/**
 * Mixin để thêm breadcrumbs vào component
 */
export const breadcrumbMixin = {
  computed: {
    breadcrumbs() {
      return getBreadcrumbs(this.$route.name, this.$route.params);
    }
  }
};
