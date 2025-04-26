<template>
  <div class="settings-page">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="h3">Cài đặt hệ thống</h1>
    </div>

    <div class="row">
      <div class="col-md-3 mb-4">
        <div class="card">
          <div class="card-body">
            <div class="nav flex-column nav-pills" role="tablist" aria-orientation="vertical">
              <button
                class="nav-link active mb-2"
                id="general-tab"
                data-bs-toggle="pill"
                data-bs-target="#general"
                type="button"
                role="tab"
                aria-controls="general"
                aria-selected="true"
              >
                <font-awesome-icon icon="cog" class="me-2" />
                Cài đặt chung
              </button>
              <button
                class="nav-link mb-2"
                id="company-tab"
                data-bs-toggle="pill"
                data-bs-target="#company"
                type="button"
                role="tab"
                aria-controls="company"
                aria-selected="false"
              >
                <font-awesome-icon icon="building" class="me-2" />
                Thông tin công ty
              </button>
              <button
                class="nav-link mb-2"
                id="email-tab"
                data-bs-toggle="pill"
                data-bs-target="#email"
                type="button"
                role="tab"
                aria-controls="email"
                aria-selected="false"
              >
                <font-awesome-icon icon="envelope" class="me-2" />
                Cấu hình email
              </button>
              <button
                class="nav-link mb-2"
                id="backup-tab"
                data-bs-toggle="pill"
                data-bs-target="#backup"
                type="button"
                role="tab"
                aria-controls="backup"
                aria-selected="false"
              >
                <font-awesome-icon icon="database" class="me-2" />
                Sao lưu & Phục hồi
              </button>
              <button
                class="nav-link"
                id="users-tab"
                data-bs-toggle="pill"
                data-bs-target="#users"
                type="button"
                role="tab"
                aria-controls="users"
                aria-selected="false"
              >
                <font-awesome-icon icon="users-cog" class="me-2" />
                Quản lý người dùng
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-9">
        <div class="tab-content">
          <!-- Cài đặt chung -->
          <div class="tab-pane fade show active" id="general" role="tabpanel" aria-labelledby="general-tab">
            <div class="card">
              <div class="card-header">
                <h5 class="mb-0">Cài đặt chung</h5>
              </div>
              <div class="card-body">
                <form @submit.prevent="saveGeneralSettings">
                  <div class="mb-3">
                    <label for="appName" class="form-label">Tên ứng dụng</label>
                    <input
                      type="text"
                      class="form-control"
                      id="appName"
                      v-model="generalSettings.appName"
                    >
                  </div>
                  <div class="mb-3">
                    <label for="language" class="form-label">Ngôn ngữ mặc định</label>
                    <select class="form-select" id="language" v-model="generalSettings.language">
                      <option value="vi">Tiếng Việt</option>
                      <option value="en">English</option>
                    </select>
                  </div>
                  <div class="mb-3">
                    <label for="timezone" class="form-label">Múi giờ</label>
                    <select class="form-select" id="timezone" v-model="generalSettings.timezone">
                      <option value="Asia/Ho_Chi_Minh">Asia/Ho_Chi_Minh (GMT+7)</option>
                      <option value="Asia/Bangkok">Asia/Bangkok (GMT+7)</option>
                      <option value="Asia/Singapore">Asia/Singapore (GMT+8)</option>
                      <option value="UTC">UTC</option>
                    </select>
                  </div>
                  <div class="mb-3">
                    <label for="dateFormat" class="form-label">Định dạng ngày</label>
                    <select class="form-select" id="dateFormat" v-model="generalSettings.dateFormat">
                      <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                      <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                      <option value="YYYY-MM-DD">YYYY-MM-DD</option>
                    </select>
                  </div>
                  <div class="mb-3">
                    <div class="form-check form-switch">
                      <input
                        class="form-check-input"
                        type="checkbox"
                        id="maintenanceMode"
                        v-model="generalSettings.maintenanceMode"
                      >
                      <label class="form-check-label" for="maintenanceMode">Chế độ bảo trì</label>
                    </div>
                  </div>
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="savingGeneral"
                  >
                    <span v-if="savingGeneral" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    Lưu cài đặt
                  </button>
                </form>
              </div>
            </div>
          </div>

          <!-- Thông tin công ty -->
          <div class="tab-pane fade" id="company" role="tabpanel" aria-labelledby="company-tab">
            <div class="card">
              <div class="card-header">
                <h5 class="mb-0">Thông tin công ty</h5>
              </div>
              <div class="card-body">
                <form @submit.prevent="saveCompanySettings">
                  <div class="mb-4 text-center">
                    <div class="company-logo-container mb-3">
                      <img
                        v-if="companySettings.logo"
                        :src="companySettings.logo"
                        alt="Company Logo"
                        class="company-logo"
                      >
                      <div v-else class="company-logo-placeholder">
                        <font-awesome-icon icon="building" size="2x" />
                      </div>
                    </div>
                    <div>
                      <button type="button" class="btn btn-outline-primary btn-sm" @click="$refs.logoInput.click()">
                        <font-awesome-icon icon="upload" class="me-2" />
                        {{ companySettings.logo ? 'Thay đổi logo' : 'Tải lên logo' }}
                      </button>
                      <input
                        type="file"
                        ref="logoInput"
                        class="d-none"
                        accept="image/*"
                        @change="handleLogoChange"
                      >
                    </div>
                  </div>

                  <div class="mb-3">
                    <label for="companyName" class="form-label">Tên công ty <span class="text-danger">*</span></label>
                    <input
                      type="text"
                      class="form-control"
                      id="companyName"
                      v-model="companySettings.name"
                      required
                    >
                  </div>
                  <div class="mb-3">
                    <label for="companyAddress" class="form-label">Địa chỉ</label>
                    <textarea
                      class="form-control"
                      id="companyAddress"
                      v-model="companySettings.address"
                      rows="2"
                    ></textarea>
                  </div>
                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label for="companyPhone" class="form-label">Số điện thoại</label>
                      <input
                        type="tel"
                        class="form-control"
                        id="companyPhone"
                        v-model="companySettings.phone"
                      >
                    </div>
                    <div class="col-md-6">
                      <label for="companyEmail" class="form-label">Email</label>
                      <input
                        type="email"
                        class="form-control"
                        id="companyEmail"
                        v-model="companySettings.email"
                      >
                    </div>
                  </div>
                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label for="companyWebsite" class="form-label">Website</label>
                      <input
                        type="url"
                        class="form-control"
                        id="companyWebsite"
                        v-model="companySettings.website"
                      >
                    </div>
                    <div class="col-md-6">
                      <label for="companyTaxCode" class="form-label">Mã số thuế</label>
                      <input
                        type="text"
                        class="form-control"
                        id="companyTaxCode"
                        v-model="companySettings.taxCode"
                      >
                    </div>
                  </div>
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="savingCompany"
                  >
                    <span v-if="savingCompany" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    Lưu thông tin
                  </button>
                </form>
              </div>
            </div>
          </div>

          <!-- Cấu hình email -->
          <div class="tab-pane fade" id="email" role="tabpanel" aria-labelledby="email-tab">
            <div class="card">
              <div class="card-header">
                <h5 class="mb-0">Cấu hình email</h5>
              </div>
              <div class="card-body">
                <form @submit.prevent="saveEmailSettings">
                  <div class="mb-3">
                    <label for="smtpServer" class="form-label">Máy chủ SMTP <span class="text-danger">*</span></label>
                    <input
                      type="text"
                      class="form-control"
                      id="smtpServer"
                      v-model="emailSettings.smtpServer"
                      required
                    >
                  </div>
                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label for="smtpPort" class="form-label">Cổng SMTP <span class="text-danger">*</span></label>
                      <input
                        type="number"
                        class="form-control"
                        id="smtpPort"
                        v-model="emailSettings.smtpPort"
                        required
                      >
                    </div>
                    <div class="col-md-6">
                      <label for="smtpEncryption" class="form-label">Mã hóa</label>
                      <select class="form-select" id="smtpEncryption" v-model="emailSettings.smtpEncryption">
                        <option value="tls">TLS</option>
                        <option value="ssl">SSL</option>
                        <option value="none">Không mã hóa</option>
                      </select>
                    </div>
                  </div>
                  <div class="mb-3">
                    <label for="smtpUsername" class="form-label">Tên đăng nhập SMTP <span class="text-danger">*</span></label>
                    <input
                      type="text"
                      class="form-control"
                      id="smtpUsername"
                      v-model="emailSettings.smtpUsername"
                      required
                    >
                  </div>
                  <div class="mb-3">
                    <label for="smtpPassword" class="form-label">Mật khẩu SMTP <span class="text-danger">*</span></label>
                    <div class="input-group">
                      <input
                        :type="showPassword ? 'text' : 'password'"
                        class="form-control"
                        id="smtpPassword"
                        v-model="emailSettings.smtpPassword"
                        required
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
                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label for="fromEmail" class="form-label">Email gửi đi <span class="text-danger">*</span></label>
                      <input
                        type="email"
                        class="form-control"
                        id="fromEmail"
                        v-model="emailSettings.fromEmail"
                        required
                      >
                    </div>
                    <div class="col-md-6">
                      <label for="fromName" class="form-label">Tên người gửi <span class="text-danger">*</span></label>
                      <input
                        type="text"
                        class="form-control"
                        id="fromName"
                        v-model="emailSettings.fromName"
                        required
                      >
                    </div>
                  </div>
                  <div class="d-flex gap-2">
                    <button
                      type="submit"
                      class="btn btn-primary"
                      :disabled="savingEmail"
                    >
                      <span v-if="savingEmail" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      Lưu cấu hình
                    </button>
                    <button
                      type="button"
                      class="btn btn-outline-secondary"
                      @click="testEmailConnection"
                    >
                      <font-awesome-icon icon="paper-plane" class="me-2" />
                      Kiểm tra kết nối
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>

          <!-- Sao lưu & Phục hồi -->
          <div class="tab-pane fade" id="backup" role="tabpanel" aria-labelledby="backup-tab">
            <div class="card">
              <div class="card-header">
                <h5 class="mb-0">Sao lưu & Phục hồi</h5>
              </div>
              <div class="card-body">
                <form @submit.prevent="saveBackupSettings">
                  <div class="mb-3">
                    <div class="form-check form-switch">
                      <input
                        class="form-check-input"
                        type="checkbox"
                        id="autoBackup"
                        v-model="backupSettings.autoBackup"
                      >
                      <label class="form-check-label" for="autoBackup">Tự động sao lưu</label>
                    </div>
                  </div>

                  <div v-if="backupSettings.autoBackup">
                    <div class="mb-3">
                      <label for="backupFrequency" class="form-label">Tần suất sao lưu</label>
                      <select class="form-select" id="backupFrequency" v-model="backupSettings.backupFrequency">
                        <option value="daily">Hàng ngày</option>
                        <option value="weekly">Hàng tuần</option>
                        <option value="monthly">Hàng tháng</option>
                      </select>
                    </div>
                    <div class="mb-3">
                      <label for="backupTime" class="form-label">Thời gian sao lưu</label>
                      <input
                        type="time"
                        class="form-control"
                        id="backupTime"
                        v-model="backupSettings.backupTime"
                      >
                    </div>
                    <div class="mb-3">
                      <label for="keepBackups" class="form-label">Số bản sao lưu giữ lại</label>
                      <input
                        type="number"
                        class="form-control"
                        id="keepBackups"
                        v-model="backupSettings.keepBackups"
                        min="1"
                      >
                    </div>
                    <div class="mb-3">
                      <label for="backupLocation" class="form-label">Vị trí lưu trữ</label>
                      <select class="form-select" id="backupLocation" v-model="backupSettings.backupLocation">
                        <option value="local">Máy chủ cục bộ</option>
                        <option value="cloud">Đám mây</option>
                      </select>
                    </div>
                  </div>

                  <div class="d-flex gap-2 mb-4">
                    <button
                      type="submit"
                      class="btn btn-primary"
                      :disabled="savingBackup"
                    >
                      <span v-if="savingBackup" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      Lưu cài đặt
                    </button>
                    <button
                      type="button"
                      class="btn btn-outline-primary"
                      @click="createBackup"
                    >
                      <font-awesome-icon icon="database" class="me-2" />
                      Tạo bản sao lưu ngay
                    </button>
                  </div>
                </form>

                <hr>

                <h6 class="mb-3">Phục hồi dữ liệu</h6>
                <div class="mb-3">
                  <label for="restoreFile" class="form-label">Chọn file sao lưu</label>
                  <input
                    type="file"
                    class="form-control"
                    id="restoreFile"
                    accept=".zip,.sql,.gz"
                  >
                </div>
                <button
                  type="button"
                  class="btn btn-warning"
                  @click="restoreBackup"
                >
                  <font-awesome-icon icon="undo" class="me-2" />
                  Phục hồi dữ liệu
                </button>
              </div>
            </div>
          </div>

          <!-- Quản lý người dùng -->
          <div class="tab-pane fade" id="users" role="tabpanel" aria-labelledby="users-tab">
            <div class="card">
              <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Quản lý người dùng</h5>
                <button
                  type="button"
                  class="btn btn-sm btn-primary"
                  data-bs-toggle="modal"
                  data-bs-target="#addUserModal"
                >
                  <font-awesome-icon icon="user-plus" class="me-2" />
                  Thêm người dùng
                </button>
              </div>
              <div class="card-body">
                <div class="table-responsive">
                  <table class="table table-hover">
                    <thead>
                      <tr>
                        <th>Tên đăng nhập</th>
                        <th>Họ tên</th>
                        <th>Email</th>
                        <th>Vai trò</th>
                        <th>Trạng thái</th>
                        <th>Đăng nhập cuối</th>
                        <th>Thao tác</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="user in users" :key="user.id">
                        <td>{{ user.username }}</td>
                        <td>{{ user.fullName }}</td>
                        <td>{{ user.email }}</td>
                        <td>
                          <span
                            class="badge"
                            :class="{
                              'bg-danger': user.role === 'admin',
                              'bg-warning': user.role === 'manager',
                              'bg-info': user.role === 'user'
                            }"
                          >
                            {{ user.role === 'admin' ? 'Quản trị viên' : user.role === 'manager' ? 'Quản lý' : 'Người dùng' }}
                          </span>
                        </td>
                        <td>
                          <span
                            class="badge"
                            :class="{
                              'bg-success': user.isActive,
                              'bg-secondary': !user.isActive
                            }"
                          >
                            {{ user.isActive ? 'Hoạt động' : 'Bị khóa' }}
                          </span>
                        </td>
                        <td>{{ formatDate(user.lastLogin) }}</td>
                        <td>
                          <div class="btn-group">
                            <button
                              type="button"
                              class="btn btn-sm btn-outline-primary"
                              @click="editUser(user)"
                            >
                              <font-awesome-icon icon="edit" />
                            </button>
                            <button
                              type="button"
                              class="btn btn-sm btn-outline-danger"
                              @click="confirmDeleteUser(user)"
                            >
                              <font-awesome-icon icon="trash-alt" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal thêm người dùng -->
  <div class="modal fade" id="addUserModal" tabindex="-1" aria-labelledby="addUserModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="addUserModalLabel">Thêm người dùng mới</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="addUser">
            <div class="mb-3">
              <label for="username" class="form-label">Tên đăng nhập <span class="text-danger">*</span></label>
              <input
                type="text"
                class="form-control"
                id="username"
                v-model="newUser.username"
                required
              >
            </div>
            <div class="mb-3">
              <label for="fullName" class="form-label">Họ tên <span class="text-danger">*</span></label>
              <input
                type="text"
                class="form-control"
                id="fullName"
                v-model="newUser.fullName"
                required
              >
            </div>
            <div class="mb-3">
              <label for="email" class="form-label">Email <span class="text-danger">*</span></label>
              <input
                type="email"
                class="form-control"
                id="email"
                v-model="newUser.email"
                required
              >
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Mật khẩu <span class="text-danger">*</span></label>
              <div class="input-group">
                <input
                  :type="showPassword ? 'text' : 'password'"
                  class="form-control"
                  id="password"
                  v-model="newUser.password"
                  required
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
              <label for="confirmPassword" class="form-label">Xác nhận mật khẩu <span class="text-danger">*</span></label>
              <input
                :type="showPassword ? 'text' : 'password'"
                class="form-control"
                id="confirmPassword"
                v-model="newUser.confirmPassword"
                required
              >
            </div>
            <div class="mb-3">
              <label for="role" class="form-label">Vai trò <span class="text-danger">*</span></label>
              <select class="form-select" id="role" v-model="newUser.role" required>
                <option value="user">Người dùng</option>
                <option value="manager">Quản lý</option>
                <option value="admin">Quản trị viên</option>
              </select>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Hủy</button>
          <button type="button" class="btn btn-primary" @click="addUser">Thêm người dùng</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.settings-page {
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

  .nav-pills {
    .nav-link {
      color: #495057;
      border-radius: 8px;
      padding: 0.75rem 1rem;
      transition: all 0.3s ease;

      &:hover {
        background-color: rgba(0, 0, 0, 0.05);
      }

      &.active {
        background: linear-gradient(90deg, var(--primary-color, #003366) 0%, var(--accent-color, #ff6600) 100%);
        color: white;
      }
    }
  }

  .company-logo-container {
    width: 150px;
    height: 150px;
    margin: 0 auto;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid rgba(0, 0, 0, 0.1);

    .company-logo {
      width: 100%;
      height: 100%;
      object-fit: contain;
    }

    .company-logo-placeholder {
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

  .table {
    th {
      background-color: #f8f9fa;
      font-weight: 600;
    }

    td {
      vertical-align: middle;
    }
  }
}
</style>

<script>
import { mapGetters, mapActions } from 'vuex'
import { breadcrumbMixin } from '@/utils/breadcrumb'
import { Modal } from 'bootstrap'

export default {
  name: 'SettingsPage',
  mixins: [breadcrumbMixin],
  data() {
    return {
      savingGeneral: false,
      savingCompany: false,
      savingEmail: false,
      savingBackup: false,
      generalSettings: {
        appName: 'SmartHRM',
        language: 'vi',
        timezone: 'Asia/Ho_Chi_Minh',
        dateFormat: 'DD/MM/YYYY',
        maintenanceMode: false
      },
      companySettings: {
        name: 'Công ty TNHH ABC',
        address: 'Số 123, Đường ABC, Quận XYZ, TP. Hồ Chí Minh',
        phone: '0987654321',
        email: 'info@abc.com',
        website: 'https://abc.com',
        taxCode: '1234567890',
        logo: null
      },
      emailSettings: {
        smtpServer: 'smtp.gmail.com',
        smtpPort: 587,
        smtpUsername: 'example@gmail.com',
        smtpPassword: '',
        smtpEncryption: 'tls',
        fromEmail: 'noreply@abc.com',
        fromName: 'SmartHRM'
      },
      backupSettings: {
        autoBackup: true,
        backupFrequency: 'daily',
        backupTime: '00:00',
        keepBackups: 7,
        backupLocation: 'local'
      },
      users: [
        {
          id: 1,
          username: 'admin',
          email: 'admin@example.com',
          fullName: 'Administrator',
          role: 'admin',
          lastLogin: '2023-05-15T08:30:00Z',
          isActive: true
        },
        {
          id: 2,
          username: 'manager',
          email: 'manager@example.com',
          fullName: 'Manager User',
          role: 'manager',
          lastLogin: '2023-05-14T10:15:00Z',
          isActive: true
        },
        {
          id: 3,
          username: 'user',
          email: 'user@example.com',
          fullName: 'Normal User',
          role: 'user',
          lastLogin: '2023-05-13T14:45:00Z',
          isActive: true
        }
      ],
      newUser: {
        username: '',
        email: '',
        fullName: '',
        password: '',
        confirmPassword: '',
        role: 'user'
      },
      showPassword: false,
      selectedUser: null,
      showDeleteUserConfirm: false
    }
  },
  computed: {
    ...mapGetters({
      // settings: 'settings/all',
      // isLoading: 'settings/isLoading'
    })
  },
  mounted() {
    this.fetchSettings()
  },
  methods: {
    ...mapActions({
      // fetchAllSettings: 'settings/fetchSettings',
      // updateSettings: 'settings/updateSettings',
      setSuccess: 'setSuccess',
      setError: 'setError'
    }),
    async fetchSettings() {
      try {
        // Trong thực tế, bạn sẽ gọi API để lấy dữ liệu
        // await this.fetchAllSettings()

        // Giả lập API call
        await new Promise(resolve => setTimeout(resolve, 1000))

        // Dữ liệu mẫu đã được khởi tạo trong data()
      } catch (error) {
        console.error('Error fetching settings:', error)
        this.setError('Không thể tải cài đặt. Vui lòng thử lại sau.')
      }
    },
    async saveGeneralSettings() {
      this.savingGeneral = true

      try {
        // Trong thực tế, bạn sẽ gọi API để lưu cài đặt
        // await this.updateSettings({ section: 'general', data: this.generalSettings })

        // Giả lập API call
        await new Promise(resolve => setTimeout(resolve, 1000))

        this.setSuccess('Đã lưu cài đặt chung thành công.')
      } catch (error) {
        console.error('Error saving general settings:', error)
        this.setError('Không thể lưu cài đặt chung. Vui lòng thử lại sau.')
      } finally {
        this.savingGeneral = false
      }
    },
    async saveCompanySettings() {
      this.savingCompany = true

      try {
        // Trong thực tế, bạn sẽ gọi API để lưu cài đặt
        // await this.updateSettings({ section: 'company', data: this.companySettings })

        // Giả lập API call
        await new Promise(resolve => setTimeout(resolve, 1000))

        this.setSuccess('Đã lưu thông tin công ty thành công.')
      } catch (error) {
        console.error('Error saving company settings:', error)
        this.setError('Không thể lưu thông tin công ty. Vui lòng thử lại sau.')
      } finally {
        this.savingCompany = false
      }
    },
    async saveEmailSettings() {
      this.savingEmail = true

      try {
        // Trong thực tế, bạn sẽ gọi API để lưu cài đặt
        // await this.updateSettings({ section: 'email', data: this.emailSettings })

        // Giả lập API call
        await new Promise(resolve => setTimeout(resolve, 1000))

        this.setSuccess('Đã lưu cấu hình email thành công.')
      } catch (error) {
        console.error('Error saving email settings:', error)
        this.setError('Không thể lưu cấu hình email. Vui lòng thử lại sau.')
      } finally {
        this.savingEmail = false
      }
    },
    async saveBackupSettings() {
      this.savingBackup = true

      try {
        // Trong thực tế, bạn sẽ gọi API để lưu cài đặt
        // await this.updateSettings({ section: 'backup', data: this.backupSettings })

        // Giả lập API call
        await new Promise(resolve => setTimeout(resolve, 1000))

        this.setSuccess('Đã lưu cài đặt sao lưu thành công.')
      } catch (error) {
        console.error('Error saving backup settings:', error)
        this.setError('Không thể lưu cài đặt sao lưu. Vui lòng thử lại sau.')
      } finally {
        this.savingBackup = false
      }
    },
    toggleShowPassword() {
      this.showPassword = !this.showPassword
    },
    formatDate(dateString) {
      if (!dateString) return null

      const date = new Date(dateString)
      return date.toLocaleDateString('vi-VN')
    },
    handleLogoChange(event) {
      const file = event.target.files[0]
      if (!file) return

      // Kiểm tra kích thước file (tối đa 2MB)
      if (file.size > 2 * 1024 * 1024) {
        this.setError('Kích thước file quá lớn. Vui lòng chọn file nhỏ hơn 2MB.')
        this.$refs.logoInput.value = ''
        return
      }

      // Kiểm tra loại file
      if (!file.type.match('image.*')) {
        this.setError('Vui lòng chọn file hình ảnh.')
        this.$refs.logoInput.value = ''
        return
      }

      // Tạo preview
      const reader = new FileReader()
      reader.onload = (e) => {
        this.companySettings.logo = e.target.result
      }
      reader.readAsDataURL(file)
    },
    testEmailConnection() {
      // Trong thực tế, bạn sẽ gọi API để kiểm tra kết nối
      this.setSuccess('Đang kiểm tra kết nối email...')

      // Giả lập API call
      setTimeout(() => {
        this.setSuccess('Kết nối email thành công!')
      }, 2000)
    },
    createBackup() {
      // Trong thực tế, bạn sẽ gọi API để tạo bản sao lưu
      this.setSuccess('Đang tạo bản sao lưu...')

      // Giả lập API call
      setTimeout(() => {
        this.setSuccess('Đã tạo bản sao lưu thành công!')
      }, 3000)
    },
    restoreBackup() {
      // Trong thực tế, bạn sẽ gọi API để phục hồi dữ liệu
      const restoreFile = document.getElementById('restoreFile').files[0]
      if (!restoreFile) {
        this.setError('Vui lòng chọn file sao lưu để phục hồi.')
        return
      }

      if (confirm('Bạn có chắc chắn muốn phục hồi dữ liệu? Dữ liệu hiện tại sẽ bị mất.')) {
        this.setSuccess('Đang phục hồi dữ liệu...')

        // Giả lập API call
        setTimeout(() => {
          this.setSuccess('Đã phục hồi dữ liệu thành công!')
        }, 3000)
      }
    },
    addUser() {
      // Kiểm tra mật khẩu xác nhận
      if (this.newUser.password !== this.newUser.confirmPassword) {
        this.setError('Mật khẩu xác nhận không khớp.')
        return
      }

      // Trong thực tế, bạn sẽ gọi API để thêm người dùng
      // Giả lập API call
      setTimeout(() => {
        // Thêm người dùng mới vào danh sách
        const newUserId = this.users.length + 1
        this.users.push({
          id: newUserId,
          username: this.newUser.username,
          email: this.newUser.email,
          fullName: this.newUser.fullName,
          role: this.newUser.role,
          lastLogin: null,
          isActive: true
        })

        // Reset form
        this.newUser = {
          username: '',
          email: '',
          fullName: '',
          password: '',
          confirmPassword: '',
          role: 'user'
        }

        // Đóng modal
        const modal = document.getElementById('addUserModal')
        const bootstrapModal = Modal.getInstance(modal)
        bootstrapModal.hide()

        this.setSuccess('Đã thêm người dùng mới thành công.')
      }, 1000)
    },
    editUser(user) {
      // Trong thực tế, bạn sẽ mở modal chỉnh sửa người dùng
      this.selectedUser = { ...user }

      // Giả lập mở modal
      alert(`Chỉnh sửa người dùng: ${user.username}`)
    },
    confirmDeleteUser(user) {
      this.selectedUser = user
      this.showDeleteUserConfirm = true

      // Giả lập xác nhận xóa
      if (confirm(`Bạn có chắc chắn muốn xóa người dùng ${user.username}?`)) {
        this.deleteUser()
      }
    },
    deleteUser() {
      if (!this.selectedUser) return

      // Trong thực tế, bạn sẽ gọi API để xóa người dùng
      // Giả lập API call
      setTimeout(() => {
        // Xóa người dùng khỏi danh sách
        this.users = this.users.filter(u => u.id !== this.selectedUser.id)

        this.setSuccess(`Đã xóa người dùng ${this.selectedUser.username} thành công.`)

        // Reset
        this.selectedUser = null
        this.showDeleteUserConfirm = false
      }, 1000)
    }
  }
}
</script>
