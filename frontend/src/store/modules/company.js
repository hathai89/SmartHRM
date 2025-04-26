import companyService from '@/services/company.service';

// Initial state
const state = {
  company: null,
  loading: false,
  error: null
};

// Getters
const getters = {
  companyInfo: state => state.company,
  isLoading: state => state.loading,
  hasError: state => state.error !== null,
  errorMessage: state => state.error
};

// Actions
const actions = {
  /**
   * Lấy thông tin công ty
   */
  async fetchCompanyInfo({ commit }) {
    try {
      commit('SET_LOADING', true);
      const response = await companyService.getCompanyInfo();
      commit('SET_COMPANY', response.data);
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.message || 'Không thể tải thông tin công ty');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  }
};

// Mutations
const mutations = {
  SET_COMPANY(state, company) {
    state.company = company;
    state.error = null;
  },
  SET_LOADING(state, status) {
    state.loading = status;
  },
  SET_ERROR(state, error) {
    state.error = error;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
