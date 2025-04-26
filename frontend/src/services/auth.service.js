import api from './api.service'

class AuthService {
  // Lấy CSRF token
  getCsrfToken() {
    return api.get('/csrf/token/')
  }

  // Đăng nhập
  async login(username, password) {
    // Lấy CSRF token trước khi đăng nhập
    await this.getCsrfToken()

    return api.post('/auth/login/', {
      username,
      password
    })
  }

  async logout() {
    // Lấy CSRF token trước khi đăng xuất
    await this.getCsrfToken()

    return api.post('/auth/logout/')
  }

  getCurrentUser() {
    return api.get('/auth/user/')
  }

  updateProfile(userData) {
    return api.patch('/auth/update_profile/', userData)
  }

  async changePassword(oldPassword, newPassword, confirmPassword) {
    // Lấy CSRF token trước khi đổi mật khẩu
    await this.getCsrfToken()

    return api.post('/auth/change_password/', {
      old_password: oldPassword,
      new_password: newPassword,
      confirm_password: confirmPassword
    })
  }

  resetPassword(email) {
    return api.post('/auth/password/reset/', {
      email
    })
  }

  resetPasswordConfirm(uid, token, newPassword) {
    return api.post('/auth/password/reset/confirm/', {
      uid,
      token,
      new_password1: newPassword,
      new_password2: newPassword
    })
  }
}

export default new AuthService()
