import EmployeeService from '@/services/employee.service'

export default {
  namespaced: true,
  state: {
    employees: [],
    employee: null,
    totalItems: 0,
    loading: false,
    error: null
  },
  getters: {
    allEmployees: state => state.employees,
    employeeById: state => id => state.employees.find(employee => employee.id === id),
    currentEmployee: state => state.employee,
    totalEmployees: state => state.totalItems,
    isLoading: state => state.loading,
    hasError: state => !!state.error,
    error: state => state.error
  },
  mutations: {
    SET_EMPLOYEES(state, employees) {
      state.employees = employees
    },
    SET_EMPLOYEE(state, employee) {
      state.employee = employee
    },
    SET_TOTAL_ITEMS(state, total) {
      state.totalItems = total
    },
    ADD_EMPLOYEE(state, employee) {
      state.employees.push(employee)
    },
    UPDATE_EMPLOYEE(state, updatedEmployee) {
      const index = state.employees.findIndex(e => e.id === updatedEmployee.id)
      if (index !== -1) {
        state.employees.splice(index, 1, updatedEmployee)
      }
      if (state.employee && state.employee.id === updatedEmployee.id) {
        state.employee = updatedEmployee
      }
    },
    REMOVE_EMPLOYEE(state, id) {
      state.employees = state.employees.filter(e => e.id !== id)
      if (state.employee && state.employee.id === id) {
        state.employee = null
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
    async fetchEmployees({ commit }, { page = 1, limit = 10, search = '', department = null, factory = null, status = null }) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')

      try {
        const response = await EmployeeService.getEmployees(page, limit, search, department, factory, status)
        commit('SET_EMPLOYEES', response.data.results)
        commit('SET_TOTAL_ITEMS', response.data.count)
        return Promise.resolve(response.data)
      } catch (error) {
        console.error('Lỗi khi tải danh sách nhân viên:', error)

        // Sử dụng mảng rỗng khi không thể lấy danh sách nhân viên
        commit('SET_EMPLOYEES', [])
        commit('SET_TOTAL_ITEMS', 0)

        // Hiển thị thông báo lỗi thân thiện
        commit('SET_ERROR', 'Không thể tải danh sách nhân viên. Vui lòng thử lại sau.')

        // Trả về dữ liệu mặc định thay vì reject promise
        return Promise.resolve({ results: [], count: 0 })
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async fetchEmployee({ commit }, id) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')

      try {
        const response = await EmployeeService.getEmployee(id)
        commit('SET_EMPLOYEE', response.data)
        return Promise.resolve(response.data)
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi tải thông tin nhân viên')
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async createEmployee({ commit }, employeeData) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')

      try {
        const response = await EmployeeService.createEmployee(employeeData)
        commit('ADD_EMPLOYEE', response.data)
        return Promise.resolve(response.data)
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi tạo nhân viên mới')
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async updateEmployee({ commit }, { id, data }) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')

      try {
        const response = await EmployeeService.updateEmployee(id, data)
        commit('UPDATE_EMPLOYEE', response.data)
        return Promise.resolve(response.data)
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi cập nhật thông tin nhân viên')
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async deleteEmployee({ commit }, id) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')

      try {
        await EmployeeService.deleteEmployee(id)
        commit('REMOVE_EMPLOYEE', id)
        return Promise.resolve()
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi xóa nhân viên')
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
    }
  }
}
