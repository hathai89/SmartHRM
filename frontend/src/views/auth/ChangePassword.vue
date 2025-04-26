<template>
  <div class="change-password">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="h3">Đổi mật khẩu</h1>
    </div>

    <div class="card">
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

        <form @submit.prevent="handleSubmit">
          <div class="mb-3">
            <label for="currentPassword" class="form-label">Mật khẩu hiện tại</label>
            <div class="input-group">
              <span class="input-group-text">
                <font-awesome-icon icon="lock" />
              </span>
              <input
                :type="showCurrentPassword ? 'text' : 'password'"
                id="currentPassword"
                v-model="currentPassword"
                class="form-control"
                placeholder="Nhập mật khẩu hiện tại"
                required
              />
              <button
                class="btn btn-outline-secondary"
                type="button"
                @click="toggleShowCurrentPassword"
              >
                <font-awesome-icon :icon="showCurrentPassword ? 'eye-slash' : 'eye'" />
              </button>
            </div>
          </div>

          <div class="mb-3">
            <label for="newPassword" class="form-label">Mật khẩu mới</label>
            <div class="input-group">
              <span class="input-group-text">
                <font-awesome-icon icon="lock" />
              </span>
              <input
                :type="showNewPassword ? 'text' : 'password'"
                id="newPassword"
                v-model="newPassword"
                class="form-control"
                placeholder="Nhập mật khẩu mới"
                required
              />
              <button
                class="btn btn-outline-secondary"
                type="button"
                @click="toggleShowNewPassword"
              >
                <font-awesome-icon :icon="showNewPassword ? 'eye-slash' : 'eye'" />
              </button>
            </div>
            <div class="form-text" v-if="newPassword">
              <div :class="{'text-success': isStrongPassword, 'text-danger': !isStrongPassword}">
                <font-awesome-icon :icon="isStrongPassword ? 'check' : 'times'" /> 
                Mật khẩu phải có ít nhất 8 ký tự, bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt
              </div>
            </div>
          </div>

          <div class="mb-4">
            <label for="confirmPassword" class="form-label">Xác nhận mật khẩu mới</label>
            <div class="input-group">
              <span class="input-group-text">
                <font-awesome-icon icon="lock" />
              </span>
              <input
                :type="showConfirmPassword ? 'text' : 'password'"
                id="confirmPassword"
                v-model="confirmPassword"
                class="form-control"
                placeholder="Nhập lại mật khẩu mới"
                required
              />
              <button
                class="btn btn-outline-secondary"
                type="button"
                @click="toggleShowConfirmPassword"
              >
                <font-awesome-icon :icon="showConfirmPassword ? 'eye-slash' : 'eye'" />
              </button>
            </div>
            <div class="form-text" v-if="confirmPassword">
              <div :class="{'text-success': passwordsMatch, 'text-danger': !passwordsMatch}">
                <font-awesome-icon :icon="passwordsMatch ? 'check' : 'times'" /> 
                Mật khẩu xác nhận phải trùng khớp
              </div>
            </div>
          </div>

          <div class="d-flex gap-2">
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="loading || !isFormValid"
            >
              <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Đổi mật khẩu
            </button>
            <router-link to="/dashboard" class="btn btn-outline-secondary">
              Hủy
            </router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import AlertMessage from '@/components/common/AlertMessage.vue'
import { breadcrumbMixin } from '@/utils/breadcrumb'

export default {
  name: 'ChangePasswordPage',
  components: {
    AlertMessage
  },
  mixins: [breadcrumbMixin],
  data() {
    return {
      currentPassword: '',
      newPassword: '',
      confirmPassword: '',
      showCurrentPassword: false,
      showNewPassword: false,
      showConfirmPassword: false,
      loading: false,
      error: null,
      success: null
    }
  },
  computed: {
    isStrongPassword() {
      const strongRegex = new RegExp(
        '^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*])(?=.{8,})'
      )
      return strongRegex.test(this.newPassword)
    },
    passwordsMatch() {
      return this.newPassword === this.confirmPassword && this.confirmPassword !== ''
    },
    isFormValid() {
      return this.currentPassword && this.isStrongPassword && this.passwordsMatch
    }
  },
  methods: {
    ...mapActions({
      setError: 'setError',
      clearError: 'clearError',
      setSuccess: 'setSuccess',
      clearSuccess: 'clearSuccess'
    }),
    toggleShowCurrentPassword() {
      this.showCurrentPassword = !this.showCurrentPassword
    },
    toggleShowNewPassword() {
      this.showNewPassword = !this.showNewPassword
    },
    toggleShowConfirmPassword() {
      this.showConfirmPassword = !this.showConfirmPassword
    },
    async handleSubmit() {
      if (!this.isFormValid) return

      this.loading = true
      this.error = null
      this.success = null

      try {
        // Gọi API để đổi mật khẩu
        // await authService.changePassword({
        //   old_password: this.currentPassword,
        //   new_password: this.newPassword
        // })
        
        // Giả lập API call thành công
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        this.success = 'Mật khẩu của bạn đã được thay đổi thành công.'
        this.currentPassword = ''
        this.newPassword = ''
        this.confirmPassword = ''
      } catch (error) {
        this.error = error.response?.data?.detail || 'Không thể đổi mật khẩu. Vui lòng kiểm tra lại mật khẩu hiện tại.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.change-password {
  .card {
    border: none;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
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
