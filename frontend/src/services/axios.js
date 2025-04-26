import axios from 'axios'
import store from '@/store'

// Tạo instance axios với cấu hình mặc định
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: true // Cho phép gửi cookies
})

// Thêm interceptor cho request
apiClient.interceptors.request.use(
  config => {
    // Lấy token từ store
    const token = store.getters['auth/token']
    
    // Nếu có token, thêm vào header
    if (token) {
      config.headers.Authorization = `Token ${token}`
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
    // Xử lý lỗi 401 (Unauthorized)
    if (error.response && error.response.status === 401) {
      // Đăng xuất nếu token hết hạn
      store.dispatch('auth/logout')
    }
    
    return Promise.reject(error)
  }
)

export default apiClient
