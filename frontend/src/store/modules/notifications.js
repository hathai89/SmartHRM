import NotificationService from '@/services/notification.service'

export default {
  namespaced: true,
  state: {
    notifications: [],
    unreadCount: 0,
    loading: false,
    error: null,
    socket: null
  },
  getters: {
    allNotifications: state => state.notifications || [],
    unreadNotifications: state => (state.notifications || []).filter(n => !n.is_read),
    unreadCount: state => state.unreadCount || 0,
    isLoading: state => state.loading,
    hasError: state => !!state.error,
    error: state => state.error,
    socket: state => state.socket
  },
  mutations: {
    SET_NOTIFICATIONS(state, notifications) {
      state.notifications = notifications
    },
    SET_UNREAD_COUNT(state, count) {
      state.unreadCount = count
    },
    ADD_NOTIFICATION(state, notification) {
      state.notifications.unshift(notification)
      if (!notification.is_read) {
        state.unreadCount++
      }
    },
    MARK_AS_READ(state, id) {
      const notification = state.notifications.find(n => n.id === id)
      if (notification && !notification.is_read) {
        notification.is_read = true
        state.unreadCount = Math.max(0, state.unreadCount - 1)
      }
    },
    MARK_ALL_AS_READ(state) {
      state.notifications.forEach(n => {
        n.is_read = true
      })
      state.unreadCount = 0
    },
    REMOVE_NOTIFICATION(state, id) {
      const notification = state.notifications.find(n => n.id === id)
      if (notification && !notification.is_read) {
        state.unreadCount = Math.max(0, state.unreadCount - 1)
      }
      state.notifications = state.notifications.filter(n => n.id !== id)
    },
    SET_SOCKET(state, socket) {
      state.socket = socket
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
    async fetchNotifications({ commit }) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')

      try {
        const response = await NotificationService.getNotifications()
        commit('SET_NOTIFICATIONS', response.data.results)
        commit('SET_UNREAD_COUNT', response.data.unread_count)
        return Promise.resolve(response.data)
      } catch (error) {
        console.error('Lỗi khi tải thông báo:', error)

        // Sử dụng mảng rỗng khi không thể lấy thông báo
        commit('SET_NOTIFICATIONS', [])
        commit('SET_UNREAD_COUNT', 0)

        // Không hiển thị lỗi cho người dùng vì đây không phải là lỗi quan trọng
        // commit('SET_ERROR', 'Không thể tải thông báo. Vui lòng thử lại sau.')

        // Trả về dữ liệu mặc định thay vì reject promise
        return Promise.resolve({ results: [], unread_count: 0 })
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async markAsRead({ commit }, id) {
      try {
        await NotificationService.markAsRead(id)
        commit('MARK_AS_READ', id)
        return Promise.resolve()
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi đánh dấu đã đọc')
        return Promise.reject(error)
      }
    },

    async markAllAsRead({ commit }) {
      try {
        await NotificationService.markAllAsRead()
        commit('MARK_ALL_AS_READ')
        return Promise.resolve()
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi đánh dấu tất cả đã đọc')
        return Promise.reject(error)
      }
    },

    async deleteNotification({ commit }, id) {
      try {
        await NotificationService.deleteNotification(id)
        commit('REMOVE_NOTIFICATION', id)
        return Promise.resolve()
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Có lỗi xảy ra khi xóa thông báo')
        return Promise.reject(error)
      }
    },

    setupWebSocket({ commit, dispatch }) {
      const token = localStorage.getItem('token')
      if (!token) return

      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const socket = new WebSocket(`${protocol}//${window.location.host}/ws/notifications/?token=${token}`)

      socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)

          if (data.type === 'notification') {
            commit('ADD_NOTIFICATION', data.notification)
          } else if (data.type === 'unread_count') {
            commit('SET_UNREAD_COUNT', data.count)
          }
        } catch (error) {
          console.error('Lỗi khi parse dữ liệu từ WebSocket:', error)
        }
      }

      socket.onclose = () => {
        // Thử kết nối lại sau 5 giây
        setTimeout(() => {
          dispatch('setupWebSocket')
        }, 5000)
      }

      commit('SET_SOCKET', socket)
    },

    closeWebSocket({ state }) {
      if (state.socket) {
        state.socket.close()
      }
    }
  }
}
