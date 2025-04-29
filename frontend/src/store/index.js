import { createStore } from 'vuex'
import auth from './modules/auth'
import employees from './modules/employees'
import departments from './modules/departments'
import factories from './modules/factories'
import documents from './modules/documents'
import notifications from './modules/notifications'
import company from './modules/company'
import profile from './modules/profile'
import app from './modules/app'
import recruitment from './modules/recruitment'

export default createStore({
  state: {
    loading: false,
    error: null,
    success: null,
    appTitle: 'CÔNG TY CỔ PHẦN DỆT MAY 29/3'
  },
  getters: {
    isLoading: state => state.loading,
    hasError: state => !!state.error,
    error: state => state.error,
    hasSuccess: state => !!state.success,
    success: state => state.success,
    appTitle: state => state.appTitle
  },
  mutations: {
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    CLEAR_ERROR(state) {
      state.error = null
    },
    SET_SUCCESS(state, success) {
      state.success = success
    },
    CLEAR_SUCCESS(state) {
      state.success = null
    }
  },
  actions: {
    setLoading({ commit }, loading) {
      commit('SET_LOADING', loading)
    },
    setError({ commit }, error) {
      commit('SET_ERROR', error)
    },
    clearError({ commit }) {
      commit('CLEAR_ERROR')
    },
    setSuccess({ commit }, success) {
      commit('SET_SUCCESS', success)
    },
    clearSuccess({ commit }) {
      commit('CLEAR_SUCCESS')
    },
    clearMessages({ commit }) {
      commit('CLEAR_ERROR')
      commit('CLEAR_SUCCESS')
    }
  },
  modules: {
    auth,
    employees,
    departments,
    factories,
    documents,
    notifications,
    company,
    profile,
    app,
    recruitment
  }
})
