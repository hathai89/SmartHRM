import DepartmentService from '@/services/department.service'

export default {
  namespaced: true,
  state: {
    departments: [],
    department: null,
    loading: false,
    error: null
  },
  getters: {
    allDepartments: state => state.departments,
    departmentById: state => id => state.departments.find(dept => dept.id === id),
    currentDepartment: state => state.department,
    isLoading: state => state.loading,
    hasError: state => !!state.error,
    error: state => state.error
  },
  mutations: {
    SET_DEPARTMENTS(state, departments) {
      state.departments = departments
    },
    SET_DEPARTMENT(state, department) {
      state.department = department
    },
    ADD_DEPARTMENT(state, department) {
      state.departments.push(department)
    },
    UPDATE_DEPARTMENT(state, updatedDepartment) {
      const index = state.departments.findIndex(d => d.id === updatedDepartment.id)
      if (index !== -1) {
        state.departments.splice(index, 1, updatedDepartment)
      }
      if (state.department && state.department.id === updatedDepartment.id) {
        state.department = updatedDepartment
      }
    },
    REMOVE_DEPARTMENT(state, id) {
      state.departments = state.departments.filter(d => d.id !== id)
      if (state.department && state.department.id === id) {
        state.department = null
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
    async fetchDepartments({ commit }) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      
      try {
        const response = await DepartmentService.getDepartments()
        commit('SET_DEPARTMENTS', response.data)
        return Promise.resolve(response.data)
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi tải danh sách phòng ban')
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchDepartment({ commit }, id) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      
      try {
        const response = await DepartmentService.getDepartment(id)
        commit('SET_DEPARTMENT', response.data)
        return Promise.resolve(response.data)
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi tải thông tin phòng ban')
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async createDepartment({ commit }, departmentData) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      
      try {
        const response = await DepartmentService.createDepartment(departmentData)
        commit('ADD_DEPARTMENT', response.data)
        return Promise.resolve(response.data)
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi tạo phòng ban mới')
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async updateDepartment({ commit }, { id, data }) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      
      try {
        const response = await DepartmentService.updateDepartment(id, data)
        commit('UPDATE_DEPARTMENT', response.data)
        return Promise.resolve(response.data)
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi cập nhật thông tin phòng ban')
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async deleteDepartment({ commit }, id) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      
      try {
        await DepartmentService.deleteDepartment(id)
        commit('REMOVE_DEPARTMENT', id)
        return Promise.resolve()
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi xóa phòng ban')
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    }
  }
}
