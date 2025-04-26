import AuthService from '@/services/auth.service'

const user = JSON.parse(localStorage.getItem('user'))
const initialState = user
  ? { status: { loggedIn: true }, user }
  : { status: { loggedIn: false }, user: null }

export default {
  namespaced: true,
  state: initialState,
  getters: {
    isAuthenticated: state => state.status.loggedIn,
    currentUser: state => state.user,
    isAdmin: state => state.user && state.user.is_superuser
  },
  mutations: {
    LOGIN_SUCCESS(state, user) {
      state.status.loggedIn = true
      state.user = user
    },
    LOGIN_FAILURE(state) {
      state.status.loggedIn = false
      state.user = null
    },
    LOGOUT(state) {
      state.status.loggedIn = false
      state.user = null
    },
    UPDATE_USER(state, user) {
      state.user = { ...state.user, ...user }
    }
  },
  actions: {
    async login({ commit }, { username, password }) {
      try {
        const response = await AuthService.login(username, password)
        const user = response.data.user
        const token = response.data.token

        // Lưu token vào localStorage
        localStorage.setItem('token', token)
        localStorage.setItem('user', JSON.stringify(user))

        commit('LOGIN_SUCCESS', user)
        return Promise.resolve(user)
      } catch (error) {
        commit('LOGIN_FAILURE')
        return Promise.reject(error)
      }
    },

    logout({ commit }) {
      AuthService.logout()
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      commit('LOGOUT')
    },

    async checkAuth({ commit, state }) {
      // Nếu đã đăng nhập, không cần kiểm tra lại
      if (state.status.loggedIn) {
        return Promise.resolve(state.user)
      }

      try {
        const response = await AuthService.getCurrentUser()
        const user = response.data

        // Cập nhật thông tin người dùng trong localStorage
        localStorage.setItem('user', JSON.stringify(user))

        commit('LOGIN_SUCCESS', user)
        return Promise.resolve(user)
      } catch (error) {
        commit('LOGIN_FAILURE')
        return Promise.reject(error)
      }
    },

    async updateProfile({ commit }, userData) {
      try {
        const response = await AuthService.updateProfile(userData)
        const updatedUser = response.data

        // Cập nhật thông tin người dùng trong localStorage
        const currentUser = JSON.parse(localStorage.getItem('user'))
        const newUserData = { ...currentUser, ...updatedUser }
        localStorage.setItem('user', JSON.stringify(newUserData))

        commit('UPDATE_USER', updatedUser)
        return Promise.resolve(updatedUser)
      } catch (error) {
        return Promise.reject(error)
      }
    },

    async changePassword(_, { oldPassword, newPassword }) {
      try {
        await AuthService.changePassword(oldPassword, newPassword)
        return Promise.resolve()
      } catch (error) {
        return Promise.reject(error)
      }
    },

    updateUserAvatar({ commit }, avatarUrl) {
      try {
        // Cập nhật avatar trong localStorage
        const currentUser = JSON.parse(localStorage.getItem('user'))
        if (currentUser) {
          currentUser.avatar = avatarUrl
          localStorage.setItem('user', JSON.stringify(currentUser))
        }

        // Cập nhật avatar trong state
        commit('UPDATE_USER', { avatar: avatarUrl })
        return Promise.resolve()
      } catch (error) {
        return Promise.reject(error)
      }
    }
  }
}
