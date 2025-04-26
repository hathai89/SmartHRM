import profileService from '@/services/profile.service';

// Initial state
const state = {
  profile: null,
  loading: false,
  error: null
};

// Getters
const getters = {
  profileData: state => state.profile,
  isLoading: state => state.loading,
  hasError: state => state.error !== null,
  errorMessage: state => state.error
};

// Actions
const actions = {
  /**
   * Lấy thông tin hồ sơ cá nhân
   */
  async fetchProfile({ commit }) {
    try {
      commit('SET_LOADING', true);
      const response = await profileService.getProfile();
      commit('SET_PROFILE', response.data);
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.message || 'Không thể tải thông tin hồ sơ');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },
  
  /**
   * Cập nhật thông tin hồ sơ cá nhân
   * @param {Object} profileData - Dữ liệu hồ sơ cần cập nhật
   */
  async updateProfile({ commit }, profileData) {
    try {
      commit('SET_LOADING', true);
      const response = await profileService.updateProfile(profileData);
      commit('SET_PROFILE', response.data);
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.message || 'Không thể cập nhật thông tin hồ sơ');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },
  
  /**
   * Upload ảnh đại diện
   * @param {File} file - File ảnh đại diện
   */
  async uploadAvatar({ commit, dispatch }, file) {
    try {
      commit('SET_LOADING', true);
      const response = await profileService.uploadAvatar(file);
      
      // Cập nhật avatar trong profile
      commit('UPDATE_AVATAR', response.data.avatar);
      
      // Cập nhật avatar trong thông tin người dùng
      dispatch('auth/updateUserAvatar', response.data.avatar, { root: true });
      
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.message || 'Không thể cập nhật ảnh đại diện');
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  }
};

// Mutations
const mutations = {
  SET_PROFILE(state, profile) {
    state.profile = profile;
    state.error = null;
  },
  UPDATE_AVATAR(state, avatarUrl) {
    if (state.profile) {
      state.profile.avatar = avatarUrl;
    }
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
