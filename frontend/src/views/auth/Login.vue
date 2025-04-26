<template>
  <div class="login-page">
    <div class="login-container">
      <div class="card shadow-lg">
        <div class="card-header text-center py-3">
          <img src="@/assets/images/logo.png" alt="Logo" class="img-fluid mb-2" style="max-height: 80px;">
          <h4 class="mb-0">CÔNG TY CỔ PHẦN DỆT MAY 29/3</h4>
        </div>
        <div class="card-body p-4">
          <h5 class="card-title text-center mb-4">Đăng nhập hệ thống</h5>

          <alert-message
            v-if="error"
            type="danger"
            :message="error"
            @dismissed="clearError"
          />

          <form @submit.prevent="handleLogin">
            <div class="mb-3">
              <label for="username" class="form-label">Tên đăng nhập</label>
              <div class="input-group">
                <span class="input-group-text">
                  <font-awesome-icon icon="user" />
                </span>
                <input
                  type="text"
                  id="username"
                  v-model="username"
                  class="form-control"
                  placeholder="Nhập tên đăng nhập"
                  required
                  autofocus
                />
              </div>
            </div>

            <div class="mb-3">
              <label for="password" class="form-label">Mật khẩu</label>
              <div class="input-group">
                <span class="input-group-text">
                  <font-awesome-icon icon="lock" />
                </span>
                <input
                  :type="showPassword ? 'text' : 'password'"
                  id="password"
                  v-model="password"
                  class="form-control"
                  placeholder="Nhập mật khẩu"
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
            </div>

            <div class="mb-3 form-check">
              <input
                type="checkbox"
                id="rememberMe"
                v-model="rememberMe"
                class="form-check-input"
              />
              <label class="form-check-label" for="rememberMe">
                Ghi nhớ đăng nhập
              </label>
            </div>

            <div class="d-grid">
              <button
                type="submit"
                class="btn btn-primary"
                :disabled="loading"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Đăng nhập
              </button>
            </div>

            <div class="text-center mt-3">
              <a href="#" @click.prevent="forgotPassword">Quên mật khẩu?</a>
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
  name: 'LoginPage',
  components: {
    AlertMessage
  },
  data() {
    return {
      username: '',
      password: '',
      rememberMe: false,
      showPassword: false,
      loading: false,
      error: null
    }
  },
  computed: {
    currentYear() {
      return new Date().getFullYear()
    }
  },
  methods: {
    ...mapActions({
      login: 'auth/login',
      setError: 'setError',
      clearError: 'clearError'
    }),
    async handleLogin() {
      this.loading = true
      this.error = null

      try {
        await this.login({
          username: this.username,
          password: this.password
        })

        // Chuyển hướng đến trang được yêu cầu hoặc trang chủ
        const redirectPath = this.$route.query.redirect || '/dashboard'
        this.$router.push(redirectPath)
      } catch (error) {
        this.error = error.response?.data?.detail || 'Tên đăng nhập hoặc mật khẩu không đúng. Vui lòng thử lại.'
      } finally {
        this.loading = false
      }
    },
    toggleShowPassword() {
      this.showPassword = !this.showPassword
    },
    forgotPassword() {
      // Chuyển hướng đến trang quên mật khẩu
      this.$router.push('/forgot-password')
    }
  }
}
</script>

<style lang="scss" scoped>
.login-page {
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

.login-container {
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
