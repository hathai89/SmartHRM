import axios from 'axios'
import router from '@/router'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
  },
  withCredentials: true // Cho phép gửi cookies
})

// Hàm để lấy CSRF token từ cookie
function getCsrfToken() {
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1]
  return cookieValue
}

// Thêm interceptor cho request
apiClient.interceptors.request.use(
  config => {
    // Thêm token xác thực
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Token ${token}`
    }

    // Thêm CSRF token cho các phương thức không an toàn
    if (config.method !== 'get' && config.method !== 'options') {
      const csrfToken = getCsrfToken()
      if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken
      }
    }

    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Thêm interceptor cho response
apiClient.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response) {
      // Xử lý lỗi 401 Unauthorized
      if (error.response.status === 401) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')

        // Chuyển hướng đến trang đăng nhập nếu không phải đang ở trang đăng nhập
        if (router.currentRoute.value.name !== 'login') {
          router.push({
            name: 'login',
            query: { redirect: router.currentRoute.value.fullPath }
          })
        }
      }

      // Xử lý lỗi 403 Forbidden
      if (error.response.status === 403) {
        // Hiển thị thông báo lỗi quyền truy cập
        console.error('Bạn không có quyền truy cập vào tài nguyên này')
      }

      // Xử lý lỗi 404 Not Found
      if (error.response.status === 404) {
        // Có thể chuyển hướng đến trang 404
        // router.push({ name: 'not-found' })
      }

      // Xử lý lỗi 500 Internal Server Error
      if (error.response.status === 500) {
        console.error('Lỗi máy chủ nội bộ')
      }
    } else if (error.request) {
      // Yêu cầu đã được gửi nhưng không nhận được phản hồi
      console.error('Không thể kết nối đến máy chủ')
    } else {
      // Có lỗi khi thiết lập yêu cầu
      console.error('Lỗi:', error.message)
    }

    return Promise.reject(error)
  }
)

export default apiClient
