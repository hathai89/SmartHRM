import axios from 'axios'
import router from '@/router'
import { API_BASE_URL } from '@/api/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
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
    // Kiểm tra xem URL có phải là public API không
    const isPublicApi = config.url.includes('/public/') || config.url.includes('/careers')

    // Thêm token xác thực chỉ khi không phải là public API
    if (!isPublicApi) {
      const token = localStorage.getItem('token')
      if (token) {
        config.headers['Authorization'] = `Token ${token}`
      }
    }

    // Thêm CSRF token cho các phương thức không an toàn
    if (config.method !== 'get' && config.method !== 'options') {
      const csrfToken = getCsrfToken()
      if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken
      }
    }

    // Đặt Content-Type cho multipart/form-data
    if (config.data instanceof FormData) {
      config.headers['Content-Type'] = 'multipart/form-data'
    }

    // Thêm debug log
    console.log(`API Request to ${config.url} - Public API: ${isPublicApi}`)

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
    // Tạo biến để lưu thông báo lỗi
    let errorMessage = '';

    if (error.response) {
      // Xử lý lỗi 401 Unauthorized
      if (error.response.status === 401) {
        // Kiểm tra xem URL có phải là public API không
        const isPublicApi = error.config.url.includes('/public/') ||
                           error.config.url.includes('/careers') ||
                           router.currentRoute.value.meta.requiresAuth === false;

        console.log(`401 Error for ${error.config.url} - Public API: ${isPublicApi}, Current route: ${router.currentRoute.value.name}`);

        if (!isPublicApi) {
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          errorMessage = 'Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.';

          // Chuyển hướng đến trang đăng nhập nếu không phải đang ở trang đăng nhập
          if (router.currentRoute.value.name !== 'login') {
            router.push({
              name: 'login',
              query: { redirect: router.currentRoute.value.fullPath }
            })
          }
        } else {
          // Đối với public API, không cần chuyển hướng đến trang đăng nhập
          errorMessage = 'Không thể truy cập tài nguyên này.';
          console.error(errorMessage);
        }
      }

      // Xử lý lỗi 403 Forbidden
      if (error.response.status === 403) {
        errorMessage = 'Bạn không có quyền truy cập vào tài nguyên này.';
        console.error(errorMessage);
      }

      // Xử lý lỗi 404 Not Found
      if (error.response.status === 404) {
        errorMessage = 'Không tìm thấy tài nguyên yêu cầu.';
        console.error(errorMessage);
        // Có thể chuyển hướng đến trang 404
        // router.push({ name: 'not-found' })
      }

      // Xử lý lỗi 500 Internal Server Error
      if (error.response.status === 500) {
        errorMessage = 'Lỗi máy chủ nội bộ. Vui lòng thử lại sau.';
        console.error(errorMessage);
      }
    } else if (error.code === 'ECONNABORTED') {
      // Xử lý lỗi timeout
      errorMessage = 'Yêu cầu đã hết thời gian chờ. Vui lòng thử lại sau.';
      console.error(errorMessage);
    } else if (error.code === 'ERR_NETWORK' || error.code === 'ECONNREFUSED' || error.message.includes('Network Error') || !error.response) {
      // Xử lý lỗi kết nối mạng
      errorMessage = 'Không thể kết nối đến máy chủ. Vui lòng kiểm tra kết nối mạng của bạn.';
      console.error(errorMessage);
    } else {
      // Có lỗi khi thiết lập yêu cầu
      errorMessage = `Đã xảy ra lỗi: ${error.message}`;
      console.error(errorMessage);
    }

    // Dispatch action để hiển thị thông báo lỗi trong store
    if (errorMessage && window.store) {
      window.store.dispatch('setError', errorMessage);
    }

    return Promise.reject(error)
  }
)

export default apiClient
