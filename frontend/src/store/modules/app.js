// App state module
const state = {
  isOffline: false,
  showOfflineNotification: false,
  error: null,
  success: null
};

const getters = {
  isOffline: state => state.isOffline,
  showOfflineNotification: state => state.showOfflineNotification,
  error: state => state.error,
  success: state => state.success
};

const mutations = {
  SET_OFFLINE_STATUS(state, status) {
    state.isOffline = status;
  },
  SET_SHOW_OFFLINE_NOTIFICATION(state, show) {
    state.showOfflineNotification = show;
  },
  SET_ERROR(state, error) {
    state.error = error;
  },
  SET_SUCCESS(state, success) {
    state.success = success;
  },
  CLEAR_ERROR(state) {
    state.error = null;
  },
  CLEAR_SUCCESS(state) {
    state.success = null;
  }
};

const actions = {
  /**
   * Đặt trạng thái offline
   */
  setOfflineStatus({ commit }, status) {
    commit('SET_OFFLINE_STATUS', status);
    if (status) {
      // Khi chuyển sang chế độ offline, hiển thị thông báo
      commit('SET_SHOW_OFFLINE_NOTIFICATION', true);
    }
  },

  /**
   * Ẩn thông báo offline
   */
  hideOfflineNotification({ commit }) {
    commit('SET_SHOW_OFFLINE_NOTIFICATION', false);
  },

  /**
   * Kiểm tra kết nối đến backend
   */
  async checkBackendConnection({ dispatch }) {
    try {
      // Gửi request đến health-check endpoint
      const response = await fetch('/api/health-check/');
      if (response.ok) {
        // Backend hoạt động
        dispatch('setOfflineStatus', false);
        return true;
      } else {
        // Backend không hoạt động đúng cách
        dispatch('setOfflineStatus', true);
        return false;
      }
    } catch (error) {
      // Không thể kết nối đến backend
      dispatch('setOfflineStatus', true);
      return false;
    }
  },

  /**
   * Đặt thông báo lỗi
   */
  setError({ commit }, error) {
    commit('SET_ERROR', error);
  },

  /**
   * Đặt thông báo thành công
   */
  setSuccess({ commit }, success) {
    commit('SET_SUCCESS', success);
  },

  /**
   * Xóa thông báo lỗi
   */
  clearError({ commit }) {
    commit('CLEAR_ERROR');
  },

  /**
   * Xóa thông báo thành công
   */
  clearSuccess({ commit }) {
    commit('CLEAR_SUCCESS');
  },

  /**
   * Xóa tất cả thông báo
   */
  clearMessages({ commit }) {
    commit('CLEAR_ERROR');
    commit('CLEAR_SUCCESS');
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
