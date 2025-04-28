/**
 * Breadcrumb utilities
 */

// Định nghĩa breadcrumbs cho các route
export const routeBreadcrumbs = {
  'dashboard': [
    { title: 'Bảng điều khiển', route: { name: 'dashboard' } }
  ],
  'employees': [
    { title: 'Danh sách nhân viên', route: { name: 'employees' } }
  ],
  'employee-detail': [
    { title: 'Danh sách nhân viên', route: { name: 'employees' } },
    { title: 'Chi tiết nhân viên', route: null }
  ],
  'employee-create': [
    { title: 'Danh sách nhân viên', route: { name: 'employees' } },
    { title: 'Thêm nhân viên', route: null }
  ],
  'employee-edit': [
    { title: 'Danh sách nhân viên', route: { name: 'employees' } },
    { title: 'Chỉnh sửa nhân viên', route: null }
  ],
  'departments': [
    { title: 'Danh sách phòng ban', route: { name: 'departments' } }
  ],
  'department-detail': [
    { title: 'Danh sách phòng ban', route: { name: 'departments' } },
    { title: 'Chi tiết phòng ban', route: null }
  ],
  'department-create': [
    { title: 'Danh sách phòng ban', route: { name: 'departments' } },
    { title: 'Thêm phòng ban', route: null }
  ],
  'department-edit': [
    { title: 'Danh sách phòng ban', route: { name: 'departments' } },
    { title: 'Chỉnh sửa phòng ban', route: null }
  ],
  'factories': [
    { title: 'Danh sách xí nghiệp', route: { name: 'factories' } }
  ],
  'factory-detail': [
    { title: 'Danh sách xí nghiệp', route: { name: 'factories' } },
    { title: 'Chi tiết xí nghiệp', route: null }
  ],
  'factory-create': [
    { title: 'Danh sách xí nghiệp', route: { name: 'factories' } },
    { title: 'Thêm xí nghiệp', route: null }
  ],
  'factory-edit': [
    { title: 'Danh sách xí nghiệp', route: { name: 'factories' } },
    { title: 'Chỉnh sửa xí nghiệp', route: null }
  ],
  'documents': [
    { title: 'Danh sách tài liệu', route: { name: 'documents' } }
  ],
  'document-detail': [
    { title: 'Danh sách tài liệu', route: { name: 'documents' } },
    { title: 'Chi tiết tài liệu', route: null }
  ],
  'document-create': [
    { title: 'Danh sách tài liệu', route: { name: 'documents' } },
    { title: 'Thêm tài liệu', route: null }
  ],
  'document-edit': [
    { title: 'Danh sách tài liệu', route: { name: 'documents' } },
    { title: 'Chỉnh sửa tài liệu', route: null }
  ],
  'company': [
    { title: 'Thông tin công ty', route: { name: 'company' } }
  ],
  'profile': [
    { title: 'Hồ sơ cá nhân', route: { name: 'profile' } }
  ],
  'settings': [
    { title: 'Cài đặt hệ thống', route: { name: 'settings' } }
  ],
  'notifications': [
    { title: 'Thông báo hệ thống', route: { name: 'notifications' } }
  ],
  'change-password': [
    { title: 'Hồ sơ cá nhân', route: { name: 'profile' } },
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
