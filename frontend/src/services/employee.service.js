import api from './api.service'
import { EMPLOYEE_ENDPOINTS } from '@/api/api'

class EmployeeService {
  getEmployees(page = 1, limit = 10, search = '', department = null, factory = null, status = null) {
    let url = `${EMPLOYEE_ENDPOINTS.LIST}?page=${page}&limit=${limit}`

    if (search) {
      url += `&search=${search}`
    }

    if (department) {
      url += `&department=${department}`
    }

    if (factory) {
      url += `&factory=${factory}`
    }

    if (status) {
      url += `&status=${status}`
    }

    return api.get(url)
  }

  getEmployee(id) {
    return api.get(EMPLOYEE_ENDPOINTS.DETAIL(id))
  }

  createEmployee(data) {
    // Sử dụng FormData để gửi dữ liệu multipart/form-data (cho upload file)
    const formData = new FormData()

    // Thêm các trường dữ liệu vào formData
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        if (key === 'avatar' || key === 'id_card_front_image' || key === 'id_card_back_image') {
          if (data[key] instanceof File) {
            formData.append(key, data[key])
          }
        } else {
          formData.append(key, data[key])
        }
      }
    })

    return api.post(EMPLOYEE_ENDPOINTS.CREATE, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }

  updateEmployee(id, data) {
    // Sử dụng FormData để gửi dữ liệu multipart/form-data (cho upload file)
    const formData = new FormData()

    // Thêm các trường dữ liệu vào formData
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        if (key === 'avatar' || key === 'id_card_front_image' || key === 'id_card_back_image') {
          if (data[key] instanceof File) {
            formData.append(key, data[key])
          }
        } else {
          formData.append(key, data[key])
        }
      }
    })

    return api.patch(EMPLOYEE_ENDPOINTS.UPDATE(id), formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }

  deleteEmployee(id) {
    return api.delete(EMPLOYEE_ENDPOINTS.DELETE(id))
  }

  getJobTitles() {
    return api.get('/job-titles/')
  }
}

export default new EmployeeService()
