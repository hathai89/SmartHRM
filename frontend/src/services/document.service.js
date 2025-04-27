import api from './api.service'
import { DOCUMENT_ENDPOINTS } from '@/api/api'

class DocumentService {
  getDocuments(category = null, type = null, search = '') {
    let url = DOCUMENT_ENDPOINTS.LIST
    const params = []

    if (category) {
      params.push(`category=${category}`)
    }

    if (type) {
      params.push(`document_type=${type}`)
    }

    if (search) {
      params.push(`search=${search}`)
    }

    if (params.length > 0) {
      url += `?${params.join('&')}`
    }

    return api.get(url)
  }

  getDocument(id) {
    return api.get(DOCUMENT_ENDPOINTS.DETAIL(id))
  }

  getCategories() {
    return api.get('/document-categories/')
  }

  createDocument(data) {
    // Sử dụng FormData để gửi dữ liệu multipart/form-data (cho upload file)
    const formData = new FormData()

    // Thêm các trường dữ liệu vào formData
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        if (key === 'file') {
          if (data[key] instanceof File) {
            formData.append(key, data[key])
          }
        } else {
          formData.append(key, data[key])
        }
      }
    })

    return api.post(DOCUMENT_ENDPOINTS.CREATE, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }

  updateDocument(id, data) {
    // Sử dụng FormData để gửi dữ liệu multipart/form-data (cho upload file)
    const formData = new FormData()

    // Thêm các trường dữ liệu vào formData
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        if (key === 'file') {
          if (data[key] instanceof File) {
            formData.append(key, data[key])
          }
        } else {
          formData.append(key, data[key])
        }
      }
    })

    return api.patch(DOCUMENT_ENDPOINTS.UPDATE(id), formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }

  deleteDocument(id) {
    return api.delete(DOCUMENT_ENDPOINTS.DELETE(id))
  }

  createCategory(data) {
    return api.post('/document-categories/', data)
  }

  updateCategory(id, data) {
    return api.patch(`/document-categories/${id}/`, data)
  }

  deleteCategory(id) {
    return api.delete(`/document-categories/${id}/`)
  }
}

export default new DocumentService()
