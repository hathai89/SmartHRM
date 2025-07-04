import DepartmentService from '@/services/department.service'

export default {
  namespaced: true,
  state: {
    departments: [],
    departmentTree: [],
    department: null,
    loading: false,
    error: null
  },
  getters: {
    allDepartments: state => state.departments,
    departmentTree: state => state.departmentTree,
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
    SET_DEPARTMENT_TREE(state, tree) {
      state.departmentTree = tree
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

        // Kiểm tra và xử lý dữ liệu trả về
        let departments = []
        if (response.data) {
          if (Array.isArray(response.data)) {
            departments = response.data
          } else if (response.data.results && Array.isArray(response.data.results)) {
            departments = response.data.results
          } else if (typeof response.data === 'object') {
            // Nếu là object, chuyển đổi thành mảng
            console.log('Chuyển đổi dữ liệu phòng ban từ object sang mảng')
            departments = Object.values(response.data).filter(item => item && typeof item === 'object')
          }
        }

        commit('SET_DEPARTMENTS', departments)
        return Promise.resolve(departments)
      } catch (error) {
        console.error('Lỗi khi tải danh sách phòng ban:', error)
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi tải danh sách phòng ban')
        commit('SET_DEPARTMENTS', []) // Đặt mảng rỗng khi có lỗi
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async fetchDepartmentTree({ commit }) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')

      try {
        const response = await DepartmentService.getDepartmentTree()
        console.log('API response:', response)

        let treeData = []
        if (response.data) {
          if (response.data.data && Array.isArray(response.data.data)) {
            treeData = response.data.data
          } else if (Array.isArray(response.data)) {
            treeData = response.data
          }
        }

        console.log('Tree data to commit:', treeData)
        commit('SET_DEPARTMENT_TREE', treeData)
        return Promise.resolve(treeData)
      } catch (error) {
        console.error('Lỗi khi tải cấu trúc cây phòng ban:', error)
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi tải cấu trúc cây phòng ban')
        commit('SET_DEPARTMENT_TREE', [])
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
    },

    async updateDepartmentPosition({ commit }, { departmentId, parentId, position }) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')

      try {
        const response = await DepartmentService.updateDepartmentPosition(departmentId, parentId, position)
        return Promise.resolve(response.data)
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi cập nhật vị trí phòng ban')
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    }
  }
}
