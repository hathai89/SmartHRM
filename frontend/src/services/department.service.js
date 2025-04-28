import api from './api.service'
import { DEPARTMENT_ENDPOINTS } from '@/api/api'

// Thêm endpoints cho cấu trúc cây
const TREE_ENDPOINT = '/api/departments/tree/'
const UPDATE_POSITION_ENDPOINT = '/api/departments/update-position/'

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

  // Các phương thức mới cho cấu trúc cây
  getDepartmentTree() {
    return api.get(TREE_ENDPOINT)
  }

  getDepartmentChildren(id) {
    return api.get(`/departments/${id}/children/`)
  }

  updateDepartmentPosition(departmentId, parentId, position) {
    return api.post(UPDATE_POSITION_ENDPOINT, {
      department_id: departmentId,
      parent_id: parentId,
      position: position
    })
  }
}

export default new DepartmentService()
