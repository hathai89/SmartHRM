import api from './api.service'

class DepartmentService {
  getDepartments() {
    return api.get('/departments/')
  }

  getDepartment(id) {
    return api.get(`/departments/${id}/`)
  }

  createDepartment(data) {
    return api.post('/departments/', data)
  }

  updateDepartment(id, data) {
    return api.patch(`/departments/${id}/`, data)
  }

  deleteDepartment(id) {
    return api.delete(`/departments/${id}/`)
  }

  getDepartmentEmployees(id) {
    return api.get(`/departments/${id}/employees/`)
  }
}

export default new DepartmentService()
