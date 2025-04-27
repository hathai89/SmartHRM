<template>
  <div class="reset-password-page">
    <div class="reset-password-container">
      <div class="card shadow-lg">
        <div class="card-header text-center py-3">
          <img src="@/assets/images/logo.png" alt="Logo" class="img-fluid mb-2" style="max-height: 80px;">
          <h4 class="mb-0">CÔNG TY CỔ PHẦN DỆT MAY 29/3</h4>
        </div>
        <div class="card-body p-4">
          <h5 class="card-title text-center mb-4">Đặt lại mật khẩu</h5>

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

          <p class="text-muted mb-4" v-if="!success">
            Vui lòng nhập mật khẩu mới của bạn.
          </p>

          <form @submit.prevent="handleSubmit" v-if="!success">
            <div class="mb-3">
              <label for="password" class="form-label">Mật khẩu mới</label>
              <div class="input-group">
                <span class="input-group-text">
                  <font-awesome-icon icon="lock" />
                </span>
                <input
                  :type="showPassword ? 'text' : 'password'"
                  id="password"
                  v-model="password"
                  class="form-control"
                  placeholder="Nhập mật khẩu mới"
                  required
                />
                <button
                  class="btn btn-outline-secondary"
                  type="button"
                  @click="toggleShowPassword"
                >
                  <font-awesome-icon :icon="showPassword ? 'eye-slash' : 'eye'" />
                </button>
              </div>
              <div class="form-text" v-if="password">
                <div :class="{'text-success': isStrongPassword, 'text-danger': !isStrongPassword}">
                  <font-awesome-icon :icon="isStrongPassword ? 'check' : 'times'" />
                  Mật khẩu phải có ít nhất 8 ký tự, bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt
                </div>
              </div>
            </div>

            <div class="mb-4">
              <label for="confirmPassword" class="form-label">Xác nhận mật khẩu</label>
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

            <div class="d-grid gap-2">
              <button
                type="submit"
                class="btn btn-primary"
                :disabled="loading || !isFormValid"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Đặt lại mật khẩu
              </button>
              <router-link to="/login" class="btn btn-outline-secondary">
                Quay lại đăng nhập
              </router-link>
            </div>
          </form>

          <div v-if="success" class="text-center">
            <font-awesome-icon icon="check-circle" class="text-success fa-3x mb-3" />
            <p>Mật khẩu của bạn đã được đặt lại thành công.</p>
            <router-link to="/login" class="btn btn-primary mt-3">
              Đăng nhập với mật khẩu mới
            </router-link>
          </div>
        </div>
      </div>

      <div class="text-center text-muted mt-3">
        <small>&copy; {{ currentYear }} CÔNG TY CỔ PHẦN DỆT MAY 29/3</small>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import AlertMessage from '@/components/common/AlertMessage.vue'

export default {
  name: 'ResetPasswordPage',
  components: {
    AlertMessage
  },
  data() {
    return {
      password: '',
      confirmPassword: '',
      showPassword: false,
      showConfirmPassword: false,
      loading: false,
      error: null,
      success: null,
      token: '',
      uid: ''
    }
  },
  computed: {
    currentYear() {
      return new Date().getFullYear()
    },
    isStrongPassword() {
      const strongRegex = new RegExp(
        '^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*])(?=.{8,})'
      )
      return strongRegex.test(this.password)
    },
    passwordsMatch() {
      return this.password === this.confirmPassword && this.confirmPassword !== ''
    },
    isFormValid() {
      return this.isStrongPassword && this.passwordsMatch
    }
  },
  created() {
    // Lấy token và uid từ URL
    const { token, uid } = this.$route.query
    if (!token || !uid) {
      this.error = 'Liên kết đặt lại mật khẩu không hợp lệ hoặc đã hết hạn.'
    } else {
      this.token = token
      this.uid = uid
    }
  },
  methods: {
    ...mapActions({
      setError: 'setError',
      clearError: 'clearError',
      setSuccess: 'setSuccess',
      clearSuccess: 'clearSuccess'
    }),
    toggleShowPassword() {
      this.showPassword = !this.showPassword
    },
    toggleShowConfirmPassword() {
      this.showConfirmPassword = !this.showConfirmPassword
    },
    async handleSubmit() {
      if (!this.isFormValid) return

      this.loading = true
      this.error = null

      try {
        // Gọi API để đặt lại mật khẩu
        // Trong thực tế, bạn sẽ gọi API để đặt lại mật khẩu
        // await authService.resetPasswordConfirm(
        //   this.uid,
        //   this.token,
        //   this.password
        // )

        // Giả lập API call thành công
        await new Promise(resolve => setTimeout(resolve, 1000))

        this.success = 'Mật khẩu của bạn đã được đặt lại thành công.'
        this.password = ''
        this.confirmPassword = ''
      } catch (error) {
        this.error = error.response?.data?.detail || 'Không thể đặt lại mật khẩu. Liên kết có thể đã hết hạn.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.reset-password-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary-color, #003366) 0%, var(--primary-light, #0066cc) 100%);

  .card {
    border: none;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);

    .card-header {
      background: white;
      border-bottom: 1px solid rgba(0, 0, 0, 0.1);

      h4 {
        color: var(--primary-color, #003366);
        font-size: 1.2rem;
        font-weight: 600;
      }
    }

    .card-body {
      background: white;
    }
  }
}

.reset-password-container {
  width: 100%;
  max-width: 400px;
  padding: 15px;

  .btn-primary {
    background: linear-gradient(90deg, var(--primary-color, #003366) 0%, var(--accent-color, #ff6600) 100%);
    border: none;
    padding: 0.75rem;
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

  a {
    color: var(--accent-color, #ff6600);
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }
}
</style>
