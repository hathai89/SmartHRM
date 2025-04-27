import api from './api.service'
import { DEPARTMENT_ENDPOINTS } from '@/api/api'

class DepartmentService {
  getDepartments() {
    return api.get(DEPARTMENT_ENDPOINTS.LIST)
  }

  getDepartment(id) {
    return api.get(DEPARTMENT_ENDPOINTS.DETAIL(id))
  }

  createDepartment(data) {
    return api.post(DEPARTMENT_ENDPOINTS.CREATE, data)
  }

  updateDepartment(id, data) {
    return api.patch(DEPARTMENT_ENDPOINTS.UPDATE(id), data)
  }

  deleteDepartment(id) {
    return api.delete(DEPARTMENT_ENDPOINTS.DELETE(id))
  }

  getDepartmentEmployees(id) {
    return api.get(`/departments/${id}/employees/`)
  }
}

export default new DepartmentService()
