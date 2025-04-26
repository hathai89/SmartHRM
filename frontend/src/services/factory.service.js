import api from './api.service'

class FactoryService {
  getFactories() {
    return api.get('/factories/')
  }

  getFactory(id) {
    return api.get(`/factories/${id}/`)
  }

  createFactory(data) {
    return api.post('/factories/', data)
  }

  updateFactory(id, data) {
    return api.patch(`/factories/${id}/`, data)
  }

  deleteFactory(id) {
    return api.delete(`/factories/${id}/`)
  }

  getFactoryEmployees(id) {
    return api.get(`/factories/${id}/employees/`)
  }
}

export default new FactoryService()
