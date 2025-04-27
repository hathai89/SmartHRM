import api from './api.service'
import { FACTORY_ENDPOINTS } from '@/api/api'

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
}

export default new FactoryService()
