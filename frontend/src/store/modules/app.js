// App state module
const state = {
  isOffline: false,
  showOfflineNotification: false
};

const getters = {
  isOffline: state => state.isOffline,
  showOfflineNotification: state => state.showOfflineNotification
};

const mutations = {
  SET_OFFLINE_STATUS(state, status) {
    state.isOffline = status;
  },
  SET_SHOW_OFFLINE_NOTIFICATION(state, show) {
    state.showOfflineNotification = show;
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
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
