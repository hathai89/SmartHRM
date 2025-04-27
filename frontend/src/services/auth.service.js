import api from './api.service'
import { AUTH_ENDPOINTS } from '@/api/api'

class AuthService {
  // Lấy CSRF token
  getCsrfToken() {
    return api.get('/csrf/token/')
  }

  // Đăng nhập
  async login(username, password) {
    // Lấy CSRF token trước khi đăng nhập
    await this.getCsrfToken()

    return api.post(AUTH_ENDPOINTS.LOGIN, {
      username,
      password
    })
  }

  async logout() {
    // Lấy CSRF token trước khi đăng xuất
    await this.getCsrfToken()

    return api.post(AUTH_ENDPOINTS.LOGOUT)
  }

  getCurrentUser() {
    return api.get(AUTH_ENDPOINTS.USER_INFO)
  }

  updateProfile(userData) {
    return api.patch('/auth/update_profile/', userData)
  }

  async changePassword(oldPassword, newPassword, confirmPassword) {
    // Lấy CSRF token trước khi đổi mật khẩu
    await this.getCsrfToken()

    return api.post(AUTH_ENDPOINTS.CHANGE_PASSWORD, {
      old_password: oldPassword,
      new_password: newPassword,
      confirm_password: confirmPassword
    })
  }

  resetPassword(email) {
    return api.post(AUTH_ENDPOINTS.RESET_PASSWORD, {
      email
    })
  }

  resetPasswordConfirm(uid, token, newPassword) {
    return api.post(AUTH_ENDPOINTS.RESET_PASSWORD_CONFIRM, {
      uid,
      token,
      new_password1: newPassword,
      new_password2: newPassword
    })
  }
}

export default new AuthService()
