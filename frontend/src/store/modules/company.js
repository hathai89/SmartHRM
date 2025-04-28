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
      console.error('Lỗi khi tải thông tin công ty:', error);

      // Sử dụng dữ liệu mặc định khi không thể lấy từ API
      const defaultCompany = {
        name: 'CÔNG TY CỔ PHẦN DỆT MAY 29/3',
        logo: null,
        address: 'Địa chỉ công ty',
        phone: 'Số điện thoại',
        email: 'email@company.com',
        website: 'https://company.com'
      };

      commit('SET_COMPANY', defaultCompany);
      commit('SET_ERROR', 'Đang sử dụng thông tin công ty mặc định.');

      // Không throw error để không làm gián đoạn luồng ứng dụng
      return defaultCompany;
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
