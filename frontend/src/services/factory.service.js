import api from './api.service'
import { FACTORY_ENDPOINTS } from '@/api/api'

// Thêm endpoints cho cấu trúc cây
const TREE_ENDPOINT = '/api/factories/tree/'
const UPDATE_POSITION_ENDPOINT = '/api/factories/update-position/'

class FactoryService {
  getFactories() {
    return api.get(FACTORY_ENDPOINTS.LIST)
  }

  getFactory(id) {
    return api.get(FACTORY_ENDPOINTS.DETAIL(id))
  }

  createFactory(data) {
    return api.post(FACTORY_ENDPOINTS.CREATE, data)
  }

  updateFactory(id, data) {
    return api.patch(FACTORY_ENDPOINTS.UPDATE(id), data)
  }

  deleteFactory(id) {
    return api.delete(FACTORY_ENDPOINTS.DELETE(id))
  }

  getFactoryEmployees(id) {
    return api.get(`/factories/${id}/employees/`)
  }

  // Các phương thức mới cho cấu trúc cây
  getFactoryTree() {
    return api.get(TREE_ENDPOINT)
  }

  getFactoryChildren(id) {
    return api.get(`/factories/${id}/children/`)
  }

  updateFactoryPosition(factoryId, parentId, position) {
    return api.post(UPDATE_POSITION_ENDPOINT, {
      factory_id: factoryId,
      parent_id: parentId,
      position: position
    })
  }
}

export default new FactoryService()
