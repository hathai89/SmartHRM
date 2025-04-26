import DocumentService from '@/services/document.service'

export default {
  namespaced: true,
  state: {
    documents: [],
    document: null,
    categories: [],
    loading: false,
    error: null
  },
  getters: {
    allDocuments: state => state.documents,
    documentById: state => id => state.documents.find(doc => doc.id === id),
    currentDocument: state => state.document,
    allCategories: state => state.categories,
    isLoading: state => state.loading,
    hasError: state => !!state.error,
    error: state => state.error
  },
  mutations: {
    SET_DOCUMENTS(state, documents) {
      state.documents = documents
    },
    SET_DOCUMENT(state, document) {
      state.document = document
    },
    SET_CATEGORIES(state, categories) {
      state.categories = categories
    },
    ADD_DOCUMENT(state, document) {
      state.documents.push(document)
    },
    UPDATE_DOCUMENT(state, updatedDocument) {
      const index = state.documents.findIndex(d => d.id === updatedDocument.id)
      if (index !== -1) {
        state.documents.splice(index, 1, updatedDocument)
      }
      if (state.document && state.document.id === updatedDocument.id) {
        state.document = updatedDocument
      }
    },
    REMOVE_DOCUMENT(state, id) {
      state.documents = state.documents.filter(d => d.id !== id)
      if (state.document && state.document.id === id) {
        state.document = null
      }
    },
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    CLEAR_ERROR(state) {
      state.error = null
    }
  },
  actions: {
    async fetchDocuments({ commit }, { category = null, type = null, search = '' }) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      
      try {
        const response = await DocumentService.getDocuments(category, type, search)
        commit('SET_DOCUMENTS', response.data)
        return Promise.resolve(response.data)
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi tải danh sách tài liệu')
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchDocument({ commit }, id) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      
      try {
        const response = await DocumentService.getDocument(id)
        commit('SET_DOCUMENT', response.data)
        return Promise.resolve(response.data)
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi tải thông tin tài liệu')
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchCategories({ commit }) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      
      try {
        const response = await DocumentService.getCategories()
        commit('SET_CATEGORIES', response.data)
        return Promise.resolve(response.data)
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi tải danh mục tài liệu')
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async createDocument({ commit }, documentData) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      
      try {
        const response = await DocumentService.createDocument(documentData)
        commit('ADD_DOCUMENT', response.data)
        return Promise.resolve(response.data)
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi tạo tài liệu mới')
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async updateDocument({ commit }, { id, data }) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      
      try {
        const response = await DocumentService.updateDocument(id, data)
        commit('UPDATE_DOCUMENT', response.data)
        return Promise.resolve(response.data)
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi cập nhật thông tin tài liệu')
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async deleteDocument({ commit }, id) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      
      try {
        await DocumentService.deleteDocument(id)
        commit('REMOVE_DOCUMENT', id)
        return Promise.resolve()
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi xóa tài liệu')
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    }
  }
}
