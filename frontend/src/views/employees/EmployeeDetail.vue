<template>
  <div class="employee-detail">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="h3">Chi tiết nhân viên</h1>
      <div class="d-flex">
        <button class="btn btn-outline-secondary me-2" @click="refreshData">
          <font-awesome-icon icon="sync" :class="{ 'fa-spin': loading }" />
          Làm mới
        </button>
        <router-link :to="'/employees/' + $route.params.id + '/edit'" class="btn btn-primary me-2">
          <font-awesome-icon icon="edit" class="me-2" />
          Chỉnh sửa
        </router-link>
        <router-link to="/employees" class="btn btn-outline-secondary">
          <font-awesome-icon icon="arrow-left" class="me-2" />
          Quay lại
        </router-link>
      </div>
    </div>

    <div v-if="loading">
      <loading-spinner />
    </div>

    <template v-else>
      <div class="row">
        <div class="col-lg-4 mb-4">
          <div class="card card-profile">
            <div class="card-header bg-gradient-primary text-white text-center py-4">
              <div class="avatar-container mb-3">
                <img
                  v-if="employee.avatar"
                  :src="employee.avatar"
                  alt="Avatar"
                  class="avatar-img"
                >
                <div v-else class="avatar-placeholder">
                  <font-awesome-icon icon="user" size="2x" />
                </div>
              </div>
              <h5 class="mb-1">{{ employee.full_name }}</h5>
              <p class="mb-0">{{ employee.job_title }}</p>
            </div>
            <div class="card-body">
              <div class="info-item">
                <div class="info-label">
                  <font-awesome-icon icon="id-card" class="me-2" />
                  Mã nhân viên
                </div>
                <div class="info-value">{{ employee.employee_id || 'Chưa cập nhật' }}</div>
              </div>
              <div class="info-item">
                <div class="info-label">
                  <font-awesome-icon icon="envelope" class="me-2" />
                  Email
                </div>
                <div class="info-value">{{ employee.email || 'Chưa cập nhật' }}</div>
              </div>
              <div class="info-item">
                <div class="info-label">
                  <font-awesome-icon icon="phone" class="me-2" />
                  Số điện thoại
                </div>
                <div class="info-value">{{ employee.phone || 'Chưa cập nhật' }}</div>
              </div>
              <div class="info-item">
                <div class="info-label">
                  <font-awesome-icon icon="building" class="me-2" />
                  Phòng ban
                </div>
                <div class="info-value">{{ employee.department || 'Chưa cập nhật' }}</div>
              </div>
              <div class="info-item">
                <div class="info-label">
                  <font-awesome-icon icon="industry" class="me-2" />
                  Xí nghiệp
                </div>
                <div class="info-value">{{ employee.factory || 'Chưa cập nhật' }}</div>
              </div>
              <div class="info-item">
                <div class="info-label">
                  <font-awesome-icon icon="calendar-alt" class="me-2" />
                  Ngày vào làm
                </div>
                <div class="info-value">{{ formatDate(employee.hire_date) || 'Chưa cập nhật' }}</div>
              </div>
            </div>
          </div>

          <div class="card mt-4">
            <div class="card-header">
              <h5 class="mb-0">Trạng thái</h5>
            </div>
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center">
                <span>Trạng thái làm việc:</span>
                <span
                  class="badge"
                  :class="{
                    'bg-success': employee.status === 'active',
                    'bg-warning': employee.status === 'probation',
                    'bg-danger': employee.status === 'terminated'
                  }"
                >
                  {{ getStatusText(employee.status) }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-8">
          <div class="card mb-4">
            <div class="card-header">
              <h5 class="mb-0">Thông tin cá nhân</h5>
            </div>
            <div class="card-body">
              <div class="row mb-3">
                <div class="col-md-6">
                  <div class="info-group">
                    <label class="info-label">Họ</label>
                    <div class="info-value">{{ employee.first_name || 'Chưa cập nhật' }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-group">
                    <label class="info-label">Tên</label>
                    <div class="info-value">{{ employee.last_name || 'Chưa cập nhật' }}</div>
                  </div>
                </div>
              </div>

              <div class="row mb-3">
                <div class="col-md-6">
                  <div class="info-group">
                    <label class="info-label">Ngày sinh</label>
                    <div class="info-value">{{ formatDate(employee.birth_date) || 'Chưa cập nhật' }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-group">
                    <label class="info-label">Giới tính</label>
                    <div class="info-value">{{ getGenderText(employee.gender) || 'Chưa cập nhật' }}</div>
                  </div>
                </div>
              </div>

              <div class="mb-3">
                <div class="info-group">
                  <label class="info-label">Địa chỉ</label>
                  <div class="info-value">{{ employee.address || 'Chưa cập nhật' }}</div>
                </div>
              </div>

              <div class="row mb-3">
                <div class="col-md-6">
                  <div class="info-group">
                    <label class="info-label">Số CMND/CCCD</label>
                    <div class="info-value">{{ employee.id_number || 'Chưa cập nhật' }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-group">
                    <label class="info-label">Ngày cấp</label>
                    <div class="info-value">{{ formatDate(employee.id_issue_date) || 'Chưa cập nhật' }}</div>
                  </div>
                </div>
              </div>

              <div class="mb-3">
                <div class="info-group">
                  <label class="info-label">Nơi cấp</label>
                  <div class="info-value">{{ employee.id_issue_place || 'Chưa cập nhật' }}</div>
                </div>
              </div>
            </div>
          </div>

          <div class="card mb-4">
            <div class="card-header">
              <h5 class="mb-0">Thông tin công việc</h5>
            </div>
            <div class="card-body">
              <div class="row mb-3">
                <div class="col-md-6">
                  <div class="info-group">
                    <label class="info-label">Chức vụ</label>
                    <div class="info-value">{{ employee.job_title || 'Chưa cập nhật' }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-group">
                    <label class="info-label">Loại hợp đồng</label>
                    <div class="info-value">{{ employee.contract_type || 'Chưa cập nhật' }}</div>
                  </div>
                </div>
              </div>

              <div class="row mb-3">
                <div class="col-md-6">
                  <div class="info-group">
                    <label class="info-label">Ngày vào làm</label>
                    <div class="info-value">{{ formatDate(employee.hire_date) || 'Chưa cập nhật' }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-group">
                    <label class="info-label">Quản lý trực tiếp</label>
                    <div class="info-value">{{ employee.manager || 'Chưa cập nhật' }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="card mb-4">
            <div class="card-header">
              <h5 class="mb-0">Thông tin liên hệ khẩn cấp</h5>
            </div>
            <div class="card-body">
              <div class="row mb-3">
                <div class="col-md-6">
                  <div class="info-group">
                    <label class="info-label">Người liên hệ</label>
                    <div class="info-value">{{ employee.emergency_contact || 'Chưa cập nhật' }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-group">
                    <label class="info-label">Số điện thoại</label>
                    <div class="info-value">{{ employee.emergency_phone || 'Chưa cập nhật' }}</div>
                  </div>
                </div>
              </div>

              <div class="mb-3">
                <div class="info-group">
                  <label class="info-label">Mối quan hệ</label>
                  <div class="info-value">{{ employee.emergency_relationship || 'Chưa cập nhật' }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import { breadcrumbMixin } from '@/utils/breadcrumb'

export default {
  name: 'EmployeeDetailPage',
  components: {
    LoadingSpinner
  },
  mixins: [breadcrumbMixin],
  data() {
    return {
      loading: false,
      employee: {
        id: 1,
        employee_id: 'NV001',
        first_name: 'Nguyễn',
        last_name: 'Văn A',
        full_name: 'Nguyễn Văn A',
        email: 'nguyenvana@example.com',
        phone: '0987654321',
        birth_date: '1990-01-01',
        gender: 'male',
        address: 'Số 123, Đường ABC, Quận XYZ, TP. Hồ Chí Minh',
        id_number: '123456789',
        id_issue_date: '2015-01-01',
        id_issue_place: 'Công an TP. Hồ Chí Minh',
        department: 'Phòng Nhân sự',
        department_id: 1,
        factory: 'Xí nghiệp 1',
        factory_id: 1,
        job_title: 'Trưởng phòng',
        hire_date: '2020-01-01',
        contract_type: 'Hợp đồng không xác định thời hạn',
        manager: 'Trần Văn C',
        status: 'active',
        emergency_contact: 'Nguyễn Văn B',
        emergency_phone: '0987654322',
        emergency_relationship: 'Anh trai',
        avatar: null
      }
    }
  },
  computed: {
    ...mapGetters({
      // employeeData: 'employees/currentEmployee',
      // isLoading: 'employees/isLoading'
    }),
    employeeId() {
      return this.$route.params.id
    }
  },
  created() {
    this.fetchEmployeeData()
  },
  methods: {
    ...mapActions({
      // fetchEmployee: 'employees/fetchEmployee'
    }),
    async fetchEmployeeData() {
      this.loading = true

      try {
        // Trong thực tế, bạn sẽ gọi API để lấy dữ liệu
        // await this.fetchEmployee(this.employeeId)
        // this.employee = this.employeeData

        // Giả lập API call
        await new Promise(resolve => setTimeout(resolve, 1000))

        // Dữ liệu mẫu đã được khởi tạo trong data()
      } catch (error) {
        console.error('Error fetching employee data:', error)
        this.$store.dispatch('setError', 'Không thể tải thông tin nhân viên. Vui lòng thử lại sau.')
      } finally {
        this.loading = false
      }
    },
    refreshData() {
      this.fetchEmployeeData()
    },
    formatDate(dateString) {
      if (!dateString) return null

      const date = new Date(dateString)
      return date.toLocaleDateString('vi-VN')
    },
    getStatusText(status) {
      switch (status) {
        case 'active':
          return 'Đang làm việc'
        case 'probation':
          return 'Thử việc'
        case 'terminated':
          return 'Đã nghỉ việc'
        default:
          return 'Không xác định'
      }
    },
    getGenderText(gender) {
      switch (gender) {
        case 'male':
          return 'Nam'
        case 'female':
          return 'Nữ'
        case 'other':
          return 'Khác'
        default:
          return null
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.employee-detail {
  .card {
    border: none;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    margin-bottom: 1.5rem;

    .card-header {
      background-color: #f8f9fa;
      border-bottom: 1px solid rgba(0, 0, 0, 0.1);
      padding: 1rem 1.5rem;
    }

    .card-body {
      padding: 1.5rem;
    }
  }

  .card-profile {
    .avatar-container {
      width: 120px;
      height: 120px;
      margin: 0 auto;
      border-radius: 50%;
      overflow: hidden;
      border: 4px solid rgba(255, 255, 255, 0.3);
    }

    .avatar-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .avatar-placeholder {
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: rgba(255, 255, 255, 0.2);
      color: white;
    }

    .info-item {
      padding: 0.75rem 0;
      border-bottom: 1px solid rgba(0, 0, 0, 0.05);

      &:last-child {
        border-bottom: none;
      }

      .info-label {
        font-size: 0.875rem;
        color: #6c757d;
        margin-bottom: 0.25rem;
      }

      .info-value {
        font-weight: 500;
      }
    }
  }

  .info-group {
    margin-bottom: 0.5rem;

    .info-label {
      font-size: 0.875rem;
      color: #6c757d;
      margin-bottom: 0.25rem;
    }

    .info-value {
      font-weight: 500;
    }
  }

  .bg-gradient-primary {
    background: linear-gradient(135deg, var(--primary-color, #003366) 0%, var(--primary-light, #0066cc) 100%);
  }

  .btn-primary {
    background: linear-gradient(90deg, var(--primary-color, #003366) 0%, var(--accent-color, #ff6600) 100%);
    border: none;
    padding: 0.5rem 1.5rem;
    font-weight: 500;
    transition: all 0.3s ease;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
  }
}
</style>
