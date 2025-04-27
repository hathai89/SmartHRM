<template>
  <div class="profile">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="h3">Hồ sơ cá nhân</h1>
      <div class="d-flex">
        <button class="btn btn-outline-secondary me-2" @click="refreshData">
          <font-awesome-icon icon="sync" :class="{ 'fa-spin': loading }" />
          Làm mới
        </button>
        <router-link to="/change-password" class="btn btn-outline-primary">
          <font-awesome-icon icon="key" class="me-2" />
          Đổi mật khẩu
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
                  v-if="profileData.avatar"
                  :src="profileData.avatar"
                  alt="Avatar"
                  class="avatar-img"
                >
                <div v-else class="avatar-placeholder">
                  <font-awesome-icon icon="user" size="2x" />
                </div>
              </div>
              <h5 class="mb-1">{{ profileData.full_name }}</h5>
              <p class="mb-0">{{ profileData.job_title }}</p>
            </div>
            <div class="card-body">
              <div class="info-item">
                <div class="info-label">
                  <font-awesome-icon icon="id-card" class="me-2" />
                  Mã nhân viên
                </div>
                <div class="info-value">{{ profileData.employee_id || 'Chưa cập nhật' }}</div>
              </div>
              <div class="info-item">
                <div class="info-label">
                  <font-awesome-icon icon="envelope" class="me-2" />
                  Email
                </div>
                <div class="info-value">{{ profileData.email || 'Chưa cập nhật' }}</div>
              </div>
              <div class="info-item">
                <div class="info-label">
                  <font-awesome-icon icon="phone" class="me-2" />
                  Số điện thoại
                </div>
                <div class="info-value">{{ profileData.phone || 'Chưa cập nhật' }}</div>
              </div>
              <div class="info-item">
                <div class="info-label">
                  <font-awesome-icon icon="building" class="me-2" />
                  Phòng ban
                </div>
                <div class="info-value">{{ profileData.department || 'Chưa cập nhật' }}</div>
              </div>
              <div class="info-item">
                <div class="info-label">
                  <font-awesome-icon icon="industry" class="me-2" />
                  Xí nghiệp
                </div>
                <div class="info-value">{{ profileData.factory || 'Chưa cập nhật' }}</div>
              </div>
              <div class="info-item">
                <div class="info-label">
                  <font-awesome-icon icon="calendar-alt" class="me-2" />
                  Ngày vào làm
                </div>
                <div class="info-value">{{ formatDate(profileData.hire_date) || 'Chưa cập nhật' }}</div>
              </div>
            </div>
            <div class="card-footer">
              <button class="btn btn-primary w-100" @click="openAvatarUpload">
                <font-awesome-icon icon="camera" class="me-2" />
                Thay đổi ảnh đại diện
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

        <div class="col-lg-8">
          <div class="card mb-4">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0">Thông tin cá nhân</h5>
              <button
                class="btn btn-sm btn-outline-primary"
                @click="toggleEditMode"
              >
                <font-awesome-icon :icon="isEditing ? 'times' : 'edit'" class="me-1" />
                {{ isEditing ? 'Hủy' : 'Chỉnh sửa' }}
              </button>
            </div>
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

              <form @submit.prevent="saveProfile">
                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="firstName" class="form-label">Họ</label>
                    <input
                      type="text"
                      id="firstName"
                      v-model="formData.first_name"
                      class="form-control"
                      :disabled="!isEditing"
                    >
                  </div>
                  <div class="col-md-6">
                    <label for="lastName" class="form-label">Tên</label>
                    <input
                      type="text"
                      id="lastName"
                      v-model="formData.last_name"
                      class="form-control"
                      :disabled="!isEditing"
                    >
                  </div>
                </div>

                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="email" class="form-label">Email</label>
                    <input
                      type="email"
                      id="email"
                      v-model="formData.email"
                      class="form-control"
                      :disabled="!isEditing"
                    >
                  </div>
                  <div class="col-md-6">
                    <label for="phone" class="form-label">Số điện thoại</label>
                    <input
                      type="tel"
                      id="phone"
                      v-model="formData.phone"
                      class="form-control"
                      :disabled="!isEditing"
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
                      :disabled="!isEditing"
                    >
                  </div>
                  <div class="col-md-6">
                    <label for="gender" class="form-label">Giới tính</label>
                    <select
                      id="gender"
                      v-model="formData.gender"
                      class="form-select"
                      :disabled="!isEditing"
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
                    :disabled="!isEditing"
                  ></textarea>
                </div>

                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="idNumber" class="form-label">Số CMND/CCCD</label>
                    <input
                      type="text"
                      id="idNumber"
                      v-model="formData.id_number"
                      class="form-control"
                      :disabled="!isEditing"
                    >
                  </div>
                  <div class="col-md-6">
                    <label for="idIssueDate" class="form-label">Ngày cấp</label>
                    <input
                      type="date"
                      id="idIssueDate"
                      v-model="formData.id_issue_date"
                      class="form-control"
                      :disabled="!isEditing"
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
                    :disabled="!isEditing"
                  >
                </div>

                <div class="mb-3">
                  <label for="emergencyContact" class="form-label">Người liên hệ khẩn cấp</label>
                  <input
                    type="text"
                    id="emergencyContact"
                    v-model="formData.emergency_contact"
                    class="form-control"
                    :disabled="!isEditing"
                  >
                </div>

                <div class="mb-3">
                  <label for="emergencyPhone" class="form-label">Số điện thoại liên hệ khẩn cấp</label>
                  <input
                    type="tel"
                    id="emergencyPhone"
                    v-model="formData.emergency_phone"
                    class="form-control"
                    :disabled="!isEditing"
                  >
                </div>

                <div v-if="isEditing" class="d-flex gap-2">
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="saving"
                  >
                    <span v-if="saving" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    Lưu thay đổi
                  </button>
                  <button
                    type="button"
                    class="btn btn-outline-secondary"
                    @click="cancelEdit"
                  >
                    Hủy
                  </button>
                </div>
              </form>
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
                    <label class="info-label">Mã nhân viên</label>
                    <div class="info-value">{{ profileData.employee_id || 'Chưa cập nhật' }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-group">
                    <label class="info-label">Chức vụ</label>
                    <div class="info-value">{{ profileData.job_title || 'Chưa cập nhật' }}</div>
                  </div>
                </div>
              </div>

              <div class="row mb-3">
                <div class="col-md-6">
                  <div class="info-group">
                    <label class="info-label">Phòng ban</label>
                    <div class="info-value">{{ profileData.department || 'Chưa cập nhật' }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-group">
                    <label class="info-label">Xí nghiệp</label>
                    <div class="info-value">{{ profileData.factory || 'Chưa cập nhật' }}</div>
                  </div>
                </div>
              </div>

              <div class="row mb-3">
                <div class="col-md-6">
                  <div class="info-group">
                    <label class="info-label">Ngày vào làm</label>
                    <div class="info-value">{{ formatDate(profileData.hire_date) || 'Chưa cập nhật' }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-group">
                    <label class="info-label">Loại hợp đồng</label>
                    <div class="info-value">{{ profileData.contract_type || 'Chưa cập nhật' }}</div>
                  </div>
                </div>
              </div>

              <div class="row">
                <div class="col-md-6">
                  <div class="info-group">
                    <label class="info-label">Quản lý trực tiếp</label>
                    <div class="info-value">{{ profileData.manager || 'Chưa cập nhật' }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-group">
                    <label class="info-label">Trạng thái</label>
                    <div class="info-value">
                      <span
                        class="badge"
                        :class="{
                          'bg-success': profileData.status === 'active',
                          'bg-warning': profileData.status === 'probation',
                          'bg-danger': profileData.status === 'terminated',
                          'bg-secondary': !profileData.status
                        }"
                      >
                        {{ getStatusText(profileData.status) }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Modal xác nhận thay đổi ảnh đại diện -->
    <confirm-dialog
      v-if="showAvatarConfirm"
      title="Xác nhận thay đổi ảnh đại diện"
      :message="'Bạn có chắc chắn muốn thay đổi ảnh đại diện?'"
      @confirm="confirmAvatarChange"
      @cancel="cancelAvatarChange"
    />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import AlertMessage from '@/components/common/AlertMessage.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import { breadcrumbMixin } from '@/utils/breadcrumb'

export default {
  name: 'ProfilePage',
  components: {
    LoadingSpinner,
    AlertMessage,
    ConfirmDialog
  },
  mixins: [breadcrumbMixin],
  data() {
    return {
      loading: false,
      saving: false,
      isEditing: false,
      error: null,
      success: null,
      profileData: {
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
        emergency_contact: 'Nguyễn Văn B',
        emergency_phone: '0987654322',
        job_title: 'Nhân viên',
        department: 'Phòng Nhân sự',
        factory: 'Xí nghiệp 1',
        hire_date: '2020-01-01',
        contract_type: 'Hợp đồng không xác định thời hạn',
        manager: 'Trần Văn C',
        status: 'active',
        avatar: null
      },
      formData: {},
      showAvatarConfirm: false,
      selectedAvatar: null
    }
  },
  computed: {
    ...mapGetters({
      currentUser: 'auth/currentUser'
    })
  },
  created() {
    this.fetchProfileData()
  },
  methods: {
    ...mapActions({
      setError: 'setError',
      clearError: 'clearError',
      setSuccess: 'setSuccess',
      clearSuccess: 'clearSuccess'
    }),
    async fetchProfileData() {
      this.loading = true

      try {
        // Trong thực tế, bạn sẽ gọi API để lấy dữ liệu
        // Ở đây chúng ta sử dụng dữ liệu mẫu
        await new Promise(resolve => setTimeout(resolve, 1000))

        // Nếu có currentUser, cập nhật profileData
        if (this.currentUser) {
          this.profileData = {
            ...this.profileData,
            username: this.currentUser.username,
            email: this.currentUser.email,
            full_name: this.currentUser.full_name || this.profileData.full_name,
            avatar: this.currentUser.avatar
          }
        }

        // Khởi tạo formData từ profileData
        this.resetFormData()
      } catch (error) {
        console.error('Error fetching profile data:', error)
        this.error = 'Không thể tải thông tin hồ sơ. Vui lòng thử lại sau.'
      } finally {
        this.loading = false
      }
    },
    refreshData() {
      this.fetchProfileData()
    },
    resetFormData() {
      this.formData = { ...this.profileData }
    },
    toggleEditMode() {
      if (this.isEditing) {
        this.cancelEdit()
      } else {
        this.isEditing = true
      }
    },
    cancelEdit() {
      this.isEditing = false
      this.resetFormData()
    },
    async saveProfile() {
      this.saving = true
      this.error = null
      this.success = null

      try {
        // Trong thực tế, bạn sẽ gọi API để lưu dữ liệu
        // Ở đây chúng ta giả lập API call
        await new Promise(resolve => setTimeout(resolve, 1000))

        // Cập nhật profileData từ formData
        this.profileData = { ...this.formData }

        // Cập nhật full_name
        this.profileData.full_name = `${this.profileData.first_name} ${this.profileData.last_name}`

        this.success = 'Thông tin hồ sơ đã được cập nhật thành công.'
        this.isEditing = false
      } catch (error) {
        console.error('Error saving profile data:', error)
        this.error = 'Không thể lưu thông tin hồ sơ. Vui lòng thử lại sau.'
      } finally {
        this.saving = false
      }
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

      this.selectedAvatar = file
      this.showAvatarConfirm = true
    },
    async confirmAvatarChange() {
      if (!this.selectedAvatar) return

      this.loading = true
      this.error = null

      try {
        // Trong thực tế, bạn sẽ gọi API để upload ảnh
        // Ở đây chúng ta giả lập API call và tạo URL cho ảnh
        await new Promise(resolve => setTimeout(resolve, 1000))

        const reader = new FileReader()
        reader.onload = (e) => {
          this.profileData.avatar = e.target.result
          this.success = 'Ảnh đại diện đã được cập nhật thành công.'
          this.loading = false
        }
        reader.readAsDataURL(this.selectedAvatar)
      } catch (error) {
        console.error('Error uploading avatar:', error)
        this.error = 'Không thể cập nhật ảnh đại diện. Vui lòng thử lại sau.'
        this.loading = false
      } finally {
        this.showAvatarConfirm = false
        this.selectedAvatar = null
      }
    },
    cancelAvatarChange() {
      this.showAvatarConfirm = false
      this.selectedAvatar = null
      this.$refs.avatarInput.value = null
    }
  }
}
</script>

<style lang="scss" scoped>
.profile {
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

    .card-footer {
      background-color: #f8f9fa;
      border-top: 1px solid rgba(0, 0, 0, 0.1);
      padding: 1rem 1.5rem;
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

    &:disabled {
      background: #6c757d;
      transform: none;
      box-shadow: none;
    }
  }
}
</style>
