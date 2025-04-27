<template>
  <div class="forgot-password-page">
    <div class="forgot-password-container">
      <div class="card shadow-lg">
        <div class="card-header text-center py-3">
          <img src="@/assets/images/logo.png" alt="Logo" class="img-fluid mb-2" style="max-height: 80px;">
          <h4 class="mb-0">CÔNG TY CỔ PHẦN DỆT MAY 29/3</h4>
        </div>
        <div class="card-body p-4">
          <h5 class="card-title text-center mb-4">Quên mật khẩu</h5>

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

          <p class="text-muted mb-4">
            Vui lòng nhập địa chỉ email của bạn. Chúng tôi sẽ gửi cho bạn một liên kết để đặt lại mật khẩu.
          </p>

          <form @submit.prevent="handleSubmit">
            <div class="mb-3">
              <label for="email" class="form-label">Email</label>
              <div class="input-group">
                <span class="input-group-text">
                  <font-awesome-icon icon="envelope" />
                </span>
                <input
                  type="email"
                  id="email"
                  v-model="email"
                  class="form-control"
                  placeholder="Nhập địa chỉ email"
                  required
                  autofocus
                />
              </div>
            </div>

            <div class="d-grid gap-2">
              <button
                type="submit"
                class="btn btn-primary"
                :disabled="loading"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Gửi yêu cầu
              </button>
              <router-link to="/login" class="btn btn-outline-secondary">
                Quay lại đăng nhập
              </router-link>
            </div>
          </form>
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
  name: 'ForgotPasswordPage',
  components: {
    AlertMessage
  },
  data() {
    return {
      email: '',
      loading: false,
      error: null,
      success: null
    }
  },
  computed: {
    currentYear() {
      return new Date().getFullYear()
    }
  },
  methods: {
    ...mapActions({
      setError: 'setError',
      clearError: 'clearError',
      setSuccess: 'setSuccess',
      clearSuccess: 'clearSuccess'
    }),
    async handleSubmit() {
      this.loading = true
      this.error = null
      this.success = null

      try {
        // Gọi API để gửi email đặt lại mật khẩu
        // Trong thực tế, bạn sẽ gọi API để gửi email đặt lại mật khẩu
        // await authService.resetPassword(this.email)

        // Giả lập API call thành công
        await new Promise(resolve => setTimeout(resolve, 1000))

        this.success = 'Một email đã được gửi đến địa chỉ của bạn với hướng dẫn đặt lại mật khẩu.'
        this.email = '' // Xóa email sau khi gửi thành công
      } catch (error) {
        this.error = error.response?.data?.detail || 'Không thể gửi email đặt lại mật khẩu. Vui lòng thử lại sau.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.forgot-password-page {
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

.forgot-password-container {
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
