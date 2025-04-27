import { createStore } from 'vuex'
import auth from '@/store/modules/auth'
import AuthService from '@/services/auth.service'

// Mock the auth service
jest.mock('@/services/auth.service', () => ({
  login: jest.fn(),
  logout: jest.fn(),
  getCurrentUser: jest.fn(),
  updateProfile: jest.fn(),
  changePassword: jest.fn()
}))

// Mock the router
jest.mock('@/router', () => ({
  push: jest.fn()
}))

describe('auth.js (Vuex Store Module)', () => {
  let store
  
  beforeEach(() => {
    // Create a fresh store before each test
    store = createStore({
      modules: {
        auth: {
          namespaced: true,
          state: auth.state,
          getters: auth.getters,
          mutations: auth.mutations,
          actions: auth.actions
        }
      }
    })
    
    // Clear all mocks before each test
    jest.clearAllMocks()
  })
  
  describe('getters', () => {
    test('isAuthenticated should return true when user is logged in', () => {
      // Set the user and token
      store.state.auth.user = { id: 1, username: 'testuser' }
      store.state.auth.token = 'fake-token'
      store.state.auth.status.loggedIn = true
      
      expect(store.getters['auth/isAuthenticated']).toBe(true)
    })
    
    test('isAuthenticated should return false when user is not logged in', () => {
      // Make sure user and token are null
      store.state.auth.user = null
      store.state.auth.token = null
      store.state.auth.status.loggedIn = false
      
      expect(store.getters['auth/isAuthenticated']).toBe(false)
    })
    
    test('user should return the current user', () => {
      const user = { id: 1, username: 'testuser', email: 'test@example.com' }
      
      // Set the user
      store.state.auth.user = user
      
      expect(store.getters['auth/user']).toEqual(user)
    })
  })
  
  describe('actions', () => {
    test('login should call AuthService.login', async () => {
      const user = {
        id: 1,
        username: 'testuser',
        email: 'test@example.com'
      }
      const token = 'fake-token'
      
      // Mock the AuthService.login response
      AuthService.login.mockResolvedValue({
        data: { user, token }
      })
      
      // Call the login action
      await store.dispatch('auth/login', {
        username: 'testuser',
        password: 'password123'
      })
      
      // Check if AuthService.login was called with correct parameters
      expect(AuthService.login).toHaveBeenCalledWith('testuser', 'password123')
    })
    
    test('logout should call AuthService.logout', async () => {
      // Mock the AuthService.logout response
      AuthService.logout.mockResolvedValue({})
      
      // Call the logout action
      await store.dispatch('auth/logout')
      
      // Check if AuthService.logout was called
      expect(AuthService.logout).toHaveBeenCalled()
    })
  })
})
