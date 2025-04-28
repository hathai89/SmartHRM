import FactoryService from '@/services/factory.service'

export default {
  namespaced: true,
  state: {
    factories: [],
    factory: null,
    loading: false,
    error: null
  },
  getters: {
    allFactories: state => state.factories,
    factoryById: state => id => state.factories.find(factory => factory.id === id),
    currentFactory: state => state.factory,
    isLoading: state => state.loading,
    hasError: state => !!state.error,
    error: state => state.error
  },
  mutations: {
    SET_FACTORIES(state, factories) {
      state.factories = factories
    },
    SET_FACTORY(state, factory) {
      state.factory = factory
    },
    ADD_FACTORY(state, factory) {
      state.factories.push(factory)
    },
    UPDATE_FACTORY(state, updatedFactory) {
      const index = state.factories.findIndex(f => f.id === updatedFactory.id)
      if (index !== -1) {
        state.factories.splice(index, 1, updatedFactory)
      }
      if (state.factory && state.factory.id === updatedFactory.id) {
        state.factory = updatedFactory
      }
    },
    REMOVE_FACTORY(state, id) {
      state.factories = state.factories.filter(f => f.id !== id)
      if (state.factory && state.factory.id === id) {
        state.factory = null
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
    async fetchFactories({ commit }) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')

      try {
        const response = await FactoryService.getFactories()

        // Kiểm tra và xử lý dữ liệu trả về
        let factories = []
        if (response.data) {
          if (Array.isArray(response.data)) {
            factories = response.data
          } else if (response.data.results && Array.isArray(response.data.results)) {
            factories = response.data.results
          } else if (typeof response.data === 'object') {
            // Nếu là object, chuyển đổi thành mảng
            console.log('Chuyển đổi dữ liệu xí nghiệp từ object sang mảng')
            factories = Object.values(response.data).filter(item => item && typeof item === 'object')
          }
        }

        commit('SET_FACTORIES', factories)
        return Promise.resolve(factories)
      } catch (error) {
        console.error('Lỗi khi tải danh sách xí nghiệp:', error)
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi tải danh sách xí nghiệp')
        commit('SET_FACTORIES', []) // Đặt mảng rỗng khi có lỗi
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async fetchFactory({ commit }, id) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')

      try {
        const response = await FactoryService.getFactory(id)
        commit('SET_FACTORY', response.data)
        return Promise.resolve(response.data)
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi tải thông tin xí nghiệp')
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async createFactory({ commit }, factoryData) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')

      try {
        const response = await FactoryService.createFactory(factoryData)
        commit('ADD_FACTORY', response.data)
        return Promise.resolve(response.data)
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi tạo xí nghiệp mới')
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async updateFactory({ commit }, { id, data }) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')

      try {
        const response = await FactoryService.updateFactory(id, data)
        commit('UPDATE_FACTORY', response.data)
        return Promise.resolve(response.data)
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi cập nhật thông tin xí nghiệp')
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async deleteFactory({ commit }, id) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')

      try {
        await FactoryService.deleteFactory(id)
        commit('REMOVE_FACTORY', id)
        return Promise.resolve()
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi xóa xí nghiệp')
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    }
  }
}
