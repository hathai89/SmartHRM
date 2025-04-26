<template>
  <div class="employee-form">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="h3">{{ isEdit ? 'Chỉnh sửa nhân viên' : 'Thêm nhân viên mới' }}</h1>
      <div class="d-flex">
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
      <div class="card mb-4">
        <div class="card-body">
          <alert-message
            v-if="error"
            type="danger"
            :message="error"
            @dismissed="clearError"
          />

          <alert-message
            v-if="success"
            type="success"
            :message="success"
            @dismissed="clearSuccess"
          />

          <form @submit.prevent="saveEmployee">
            <div class="row">
              <div class="col-lg-8">
                <!-- Thông tin cơ bản -->
                <h5 class="mb-3">Thông tin cơ bản</h5>
                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="employeeId" class="form-label">Mã nhân viên <span class="text-danger">*</span></label>
                    <input
                      type="text"
                      id="employeeId"
                      v-model="formData.employee_id"
                      class="form-control"
                      required
                      :disabled="isEdit"
                    >
                  </div>
                  <div class="col-md-6">
                    <label for="status" class="form-label">Trạng thái <span class="text-danger">*</span></label>
                    <select
                      id="status"
                      v-model="formData.status"
                      class="form-select"
                      required
                    >
                      <option value="active">Đang làm việc</option>
                      <option value="probation">Thử việc</option>
                      <option value="terminated">Đã nghỉ việc</option>
                    </select>
                  </div>
                </div>

                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="firstName" class="form-label">Họ <span class="text-danger">*</span></label>
                    <input
                      type="text"
                      id="firstName"
                      v-model="formData.first_name"
                      class="form-control"
                      required
                    >
                  </div>
                  <div class="col-md-6">
                    <label for="lastName" class="form-label">Tên <span class="text-danger">*</span></label>
                    <input
                      type="text"
                      id="lastName"
                      v-model="formData.last_name"
                      class="form-control"
                      required
                    >
                  </div>
                </div>

                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="email" class="form-label">Email <span class="text-danger">*</span></label>
                    <input
                      type="email"
                      id="email"
                      v-model="formData.email"
                      class="form-control"
                      required
                    >
                  </div>
                  <div class="col-md-6">
                    <label for="phone" class="form-label">Số điện thoại</label>
                    <input
                      type="tel"
                      id="phone"
                      v-model="formData.phone"
                      class="form-control"
                    >
                  </div>
                </div>

                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="birthDate" class="form-label">Ngày sinh</label>
                    <input
                      type="date"
                      id="birthDate"
                      v-model="formData.birth_date"
                      class="form-control"
                    >
                  </div>
                  <div class="col-md-6">
                    <label for="gender" class="form-label">Giới tính</label>
                    <select
                      id="gender"
                      v-model="formData.gender"
                      class="form-select"
                    >
                      <option value="">-- Chọn giới tính --</option>
                      <option value="male">Nam</option>
                      <option value="female">Nữ</option>
                      <option value="other">Khác</option>
                    </select>
                  </div>
                </div>

                <div class="mb-3">
                  <label for="address" class="form-label">Địa chỉ</label>
                  <textarea
                    id="address"
                    v-model="formData.address"
                    class="form-control"
                    rows="3"
                  ></textarea>
                </div>

                <!-- Thông tin CMND/CCCD -->
                <h5 class="mb-3 mt-4">Thông tin CMND/CCCD</h5>
                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="idNumber" class="form-label">Số CMND/CCCD</label>
                    <input
                      type="text"
                      id="idNumber"
                      v-model="formData.id_number"
                      class="form-control"
                    >
                  </div>
                  <div class="col-md-6">
                    <label for="idIssueDate" class="form-label">Ngày cấp</label>
                    <input
                      type="date"
                      id="idIssueDate"
                      v-model="formData.id_issue_date"
                      class="form-control"
                    >
                  </div>
                </div>

                <div class="mb-3">
                  <label for="idIssuePlace" class="form-label">Nơi cấp</label>
                  <input
                    type="text"
                    id="idIssuePlace"
                    v-model="formData.id_issue_place"
                    class="form-control"
                  >
                </div>

                <!-- Thông tin công việc -->
                <h5 class="mb-3 mt-4">Thông tin công việc</h5>
                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="department" class="form-label">Phòng ban <span class="text-danger">*</span></label>
                    <select
                      id="department"
                      v-model="formData.department_id"
                      class="form-select"
                      required
                    >
                      <option value="">-- Chọn phòng ban --</option>
                      <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                        {{ dept.name }}
                      </option>
                    </select>
                  </div>
                  <div class="col-md-6">
                    <label for="factory" class="form-label">Xí nghiệp <span class="text-danger">*</span></label>
                    <select
                      id="factory"
                      v-model="formData.factory_id"
                      class="form-select"
                      required
                    >
                      <option value="">-- Chọn xí nghiệp --</option>
                      <option v-for="factory in factories" :key="factory.id" :value="factory.id">
                        {{ factory.name }}
                      </option>
                    </select>
                  </div>
                </div>

                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="jobTitle" class="form-label">Chức vụ <span class="text-danger">*</span></label>
                    <input
                      type="text"
                      id="jobTitle"
                      v-model="formData.job_title"
                      class="form-control"
                      required
                    >
                  </div>
                  <div class="col-md-6">
                    <label for="hireDate" class="form-label">Ngày vào làm <span class="text-danger">*</span></label>
                    <input
                      type="date"
                      id="hireDate"
                      v-model="formData.hire_date"
                      class="form-control"
                      required
                    >
                  </div>
                </div>

                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="contractType" class="form-label">Loại hợp đồng</label>
                    <input
                      type="text"
                      id="contractType"
                      v-model="formData.contract_type"
                      class="form-control"
                    >
                  </div>
                  <div class="col-md-6">
                    <label for="manager" class="form-label">Quản lý trực tiếp</label>
                    <input
                      type="text"
                      id="manager"
                      v-model="formData.manager"
                      class="form-control"
                    >
                  </div>
                </div>

                <!-- Thông tin liên hệ khẩn cấp -->
                <h5 class="mb-3 mt-4">Thông tin liên hệ khẩn cấp</h5>
                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="emergencyContact" class="form-label">Người liên hệ</label>
                    <input
                      type="text"
                      id="emergencyContact"
                      v-model="formData.emergency_contact"
                      class="form-control"
                    >
                  </div>
                  <div class="col-md-6">
                    <label for="emergencyPhone" class="form-label">Số điện thoại</label>
                    <input
                      type="tel"
                      id="emergencyPhone"
                      v-model="formData.emergency_phone"
                      class="form-control"
                    >
                  </div>
                </div>

                <div class="mb-3">
                  <label for="emergencyRelationship" class="form-label">Mối quan hệ</label>
                  <input
                    type="text"
                    id="emergencyRelationship"
                    v-model="formData.emergency_relationship"
                    class="form-control"
                  >
                </div>
              </div>

              <div class="col-lg-4">
                <!-- Ảnh đại diện -->
                <div class="card mb-4">
                  <div class="card-header">
                    <h5 class="mb-0">Ảnh đại diện</h5>
                  </div>
                  <div class="card-body text-center">
                    <div class="avatar-container mb-3">
                      <img
                        v-if="avatarPreview"
                        :src="avatarPreview"
                        alt="Avatar Preview"
                        class="avatar-img"
                      >
                      <div v-else class="avatar-placeholder">
                        <font-awesome-icon icon="user" size="2x" />
                      </div>
                    </div>
                    <div class="d-grid">
                      <button type="button" class="btn btn-outline-primary" @click="openAvatarUpload">
                        <font-awesome-icon icon="camera" class="me-2" />
                        {{ avatarPreview ? 'Thay đổi ảnh' : 'Tải lên ảnh' }}
                      </button>
                      <input
                        type="file"
                        ref="avatarInput"
                        class="d-none"
                        accept="image/*"
                        @change="handleAvatarChange"
                      >
                    </div>
                  </div>
                </div>

                <!-- Tài khoản -->
                <div class="card mb-4">
                  <div class="card-header">
                    <h5 class="mb-0">Tài khoản</h5>
                  </div>
                  <div class="card-body">
                    <div class="form-check form-switch mb-3">
                      <input
                        class="form-check-input"
                        type="checkbox"
                        id="createAccount"
                        v-model="createAccount"
                      >
                      <label class="form-check-label" for="createAccount">
                        Tạo tài khoản đăng nhập
                      </label>
                    </div>

                    <div v-if="createAccount">
                      <div class="mb-3">
                        <label for="username" class="form-label">Tên đăng nhập <span class="text-danger">*</span></label>
                        <input
                          type="text"
                          id="username"
                          v-model="accountData.username"
                          class="form-control"
                          :required="createAccount"
                        >
                      </div>

                      <div class="mb-3">
                        <label for="password" class="form-label">Mật khẩu <span class="text-danger">*</span></label>
                        <div class="input-group">
                          <input
                            :type="showPassword ? 'text' : 'password'"
                            id="password"
                            v-model="accountData.password"
                            class="form-control"
                            :required="createAccount"
                          >
                          <button
                            class="btn btn-outline-secondary"
                            type="button"
                            @click="toggleShowPassword"
                          >
                            <font-awesome-icon :icon="showPassword ? 'eye-slash' : 'eye'" />
                          </button>
                        </div>
                      </div>

                      <div class="mb-3">
                        <label for="role" class="form-label">Vai trò <span class="text-danger">*</span></label>
                        <select
                          id="role"
                          v-model="accountData.role"
                          class="form-select"
                          :required="createAccount"
                        >
                          <option value="">-- Chọn vai trò --</option>
                          <option value="user">Người dùng</option>
                          <option value="admin">Quản trị viên</option>
                          <option value="manager">Quản lý</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="d-flex gap-2 mt-4">
              <button
                type="submit"
                class="btn btn-primary"
                :disabled="saving"
              >
                <span v-if="saving" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                {{ isEdit ? 'Cập nhật' : 'Thêm mới' }}
              </button>
              <router-link to="/employees" class="btn btn-outline-secondary">
                Hủy
              </router-link>
            </div>
          </form>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import AlertMessage from '@/components/common/AlertMessage.vue'
import { breadcrumbMixin } from '@/utils/breadcrumb'

export default {
  name: 'EmployeeFormPage',
  components: {
    LoadingSpinner,
    AlertMessage
  },
  mixins: [breadcrumbMixin],
  data() {
    return {
      loading: false,
      saving: false,
      error: null,
      success: null,
      formData: {
        employee_id: '',
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        birth_date: '',
        gender: '',
        address: '',
        id_number: '',
        id_issue_date: '',
        id_issue_place: '',
        department_id: '',
        factory_id: '',
        job_title: '',
        hire_date: '',
        contract_type: '',
        manager: '',
        status: 'active',
        emergency_contact: '',
        emergency_phone: '',
        emergency_relationship: '',
        avatar: null
      },
      accountData: {
        username: '',
        password: '',
        role: ''
      },
      createAccount: false,
      showPassword: false,
      avatarPreview: null,
      avatarFile: null,
      // Dữ liệu mẫu
      departments: [
        { id: 1, name: 'Phòng Nhân sự' },
        { id: 2, name: 'Phòng Kế toán' },
        { id: 3, name: 'Phòng Kỹ thuật' },
        { id: 4, name: 'Phòng Kinh doanh' }
      ],
      factories: [
        { id: 1, name: 'Xí nghiệp 1' },
        { id: 2, name: 'Xí nghiệp 2' },
        { id: 3, name: 'Xí nghiệp 3' }
      ]
    }
  },
  computed: {
    ...mapGetters({
      // employeeData: 'employees/currentEmployee',
      // isLoading: 'employees/isLoading'
    }),
    isEdit() {
      return this.$route.name === 'employee-edit'
    },
    employeeId() {
      return this.isEdit ? this.$route.params.id : null
    }
  },
  created() {
    if (this.isEdit) {
      this.fetchEmployeeData()
    } else {
      // Tạo mã nhân viên mới
      this.generateEmployeeId()
    }
  },
  methods: {
    ...mapActions({
      // fetchEmployee: 'employees/fetchEmployee',
      // createEmployee: 'employees/createEmployee',
      // updateEmployee: 'employees/updateEmployee',
      setError: 'setError',
      clearError: 'clearError',
      setSuccess: 'setSuccess',
      clearSuccess: 'clearSuccess'
    }),
    async fetchEmployeeData() {
      this.loading = true

      try {
        // Trong thực tế, bạn sẽ gọi API để lấy dữ liệu
        // await this.fetchEmployee(this.employeeId)
        // this.formData = { ...this.employeeData }

        // Giả lập API call
        await new Promise(resolve => setTimeout(resolve, 1000))

        // Dữ liệu mẫu
        this.formData = {
          id: 1,
          employee_id: 'NV001',
          first_name: 'Nguyễn',
          last_name: 'Văn A',
          email: 'nguyenvana@example.com',
          phone: '0987654321',
          birth_date: '1990-01-01',
          gender: 'male',
          address: 'Số 123, Đường ABC, Quận XYZ, TP. Hồ Chí Minh',
          id_number: '123456789',
          id_issue_date: '2015-01-01',
          id_issue_place: 'Công an TP. Hồ Chí Minh',
          department_id: 1,
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

        // Nếu có avatar, hiển thị preview
        if (this.formData.avatar) {
          this.avatarPreview = this.formData.avatar
        }
      } catch (error) {
        console.error('Error fetching employee data:', error)
        this.error = 'Không thể tải thông tin nhân viên. Vui lòng thử lại sau.'
      } finally {
        this.loading = false
      }
    },
    generateEmployeeId() {
      // Trong thực tế, bạn sẽ gọi API để lấy mã nhân viên mới
      // Ở đây chúng ta giả lập
      const randomNum = Math.floor(Math.random() * 1000).toString().padStart(3, '0')
      this.formData.employee_id = `NV${randomNum}`
    },
    openAvatarUpload() {
      this.$refs.avatarInput.click()
    },
    handleAvatarChange(event) {
      const file = event.target.files[0]
      if (!file) return

      // Kiểm tra kích thước file (tối đa 5MB)
      if (file.size > 5 * 1024 * 1024) {
        this.error = 'Kích thước file quá lớn. Vui lòng chọn file nhỏ hơn 5MB.'
        return
      }

      // Kiểm tra loại file
      if (!file.type.match('image.*')) {
        this.error = 'Vui lòng chọn file hình ảnh.'
        return
      }

      this.avatarFile = file

      // Tạo preview
      const reader = new FileReader()
      reader.onload = (e) => {
        this.avatarPreview = e.target.result
      }
      reader.readAsDataURL(file)
    },
    toggleShowPassword() {
      this.showPassword = !this.showPassword
    },
    async saveEmployee() {
      this.saving = true
      this.error = null
      this.success = null

      try {
        // Chuẩn bị dữ liệu
        const employeeData = { ...this.formData }

        // Thêm thông tin tài khoản nếu cần
        if (this.createAccount) {
          employeeData.account = this.accountData
        }

        // Thêm avatar nếu có
        if (this.avatarFile) {
          // Trong thực tế, bạn sẽ upload file lên server
          // Ở đây chúng ta giả lập
          employeeData.avatar = this.avatarPreview
        }

        if (this.isEdit) {
          // Cập nhật nhân viên
          // await this.updateEmployee({ id: this.employeeId, data: employeeData })

          // Giả lập API call
          await new Promise(resolve => setTimeout(resolve, 1000))

          this.success = 'Cập nhật thông tin nhân viên thành công.'
        } else {
          // Thêm nhân viên mới
          // await this.createEmployee(employeeData)

          // Giả lập API call
          await new Promise(resolve => setTimeout(resolve, 1000))

          this.success = 'Thêm nhân viên mới thành công.'

          // Chuyển hướng đến trang danh sách nhân viên sau khi thêm thành công
          setTimeout(() => {
            this.$router.push('/employees')
          }, 2000)
        }
      } catch (error) {
        console.error('Error saving employee:', error)
        this.error = this.isEdit
          ? 'Không thể cập nhật thông tin nhân viên. Vui lòng thử lại sau.'
          : 'Không thể thêm nhân viên mới. Vui lòng thử lại sau.'
      } finally {
        this.saving = false
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.employee-form {
  .card {
    border: none;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);

    .card-header {
      background-color: #f8f9fa;
      border-bottom: 1px solid rgba(0, 0, 0, 0.1);
      padding: 1rem 1.5rem;
    }

    .card-body {
      padding: 1.5rem;
    }
  }

  .avatar-container {
    width: 150px;
    height: 150px;
    margin: 0 auto;
    border-radius: 50%;
    overflow: hidden;
    border: 1px solid rgba(0, 0, 0, 0.1);
    margin-bottom: 1rem;

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
      background-color: #f8f9fa;
      color: #6c757d;
    }
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

    &:disabled {
      background: #6c757d;
      transform: none;
      box-shadow: none;
    }
  }
}
</style>
