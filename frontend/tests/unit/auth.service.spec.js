import authService from '@/services/auth.service'
import api from '@/services/api.service'

// Mock the api service
jest.mock('@/services/api.service', () => ({
  get: jest.fn(),
  post: jest.fn(),
  patch: jest.fn(),
  delete: jest.fn()
}))

// Mock the router
jest.mock('@/router', () => ({
  push: jest.fn()
}))

describe('auth.service.js', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks()
    
    // Mock localStorage
    global.localStorage = {
      getItem: jest.fn(),
      setItem: jest.fn(),
      removeItem: jest.fn()
    }
    
    // Mock delete operator for headers
    delete api.defaults
    api.defaults = { headers: { common: {} } }
  })
  
  describe('login', () => {
    test('should call api.post with correct parameters', async () => {
      // Mock the getCsrfToken method
      authService.getCsrfToken = jest.fn().mockResolvedValue({})
      
      // Mock the api.post response
      api.post.mockResolvedValue({
        data: {
          token: 'fake-token',
          user: {
            id: 1,
            username: 'testuser',
            email: 'test@example.com'
          }
        }
      })
      
      // Call the login method
      await authService.login('testuser', 'password123')
      
      // Check if getCsrfToken was called
      expect(authService.getCsrfToken).toHaveBeenCalled()
      
      // Check if api.post was called with correct parameters
      expect(api.post).toHaveBeenCalledWith('/auth/login/', {
        username: 'testuser',
        password: 'password123'
      })
    })
    
    test('should throw an error when api.post fails', async () => {
      // Mock the getCsrfToken method
      authService.getCsrfToken = jest.fn().mockResolvedValue({})
      
      // Mock the api.post to throw an error
      const error = new Error('Login failed')
      api.post.mockRejectedValue(error)
      
      // Call the login method and expect it to throw an error
      await expect(authService.login('testuser', 'password123')).rejects.toThrow('Login failed')
      
      // Check if getCsrfToken was called
      expect(authService.getCsrfToken).toHaveBeenCalled()
      
      // Check if api.post was called with correct parameters
      expect(api.post).toHaveBeenCalledWith('/auth/login/', {
        username: 'testuser',
        password: 'password123'
      })
    })
  })
  
  describe('getCurrentUser', () => {
    test('should call api.get with correct parameters', async () => {
      // Mock the api.get response
      api.get.mockResolvedValue({
        data: {
          id: 1,
          username: 'testuser',
          email: 'test@example.com'
        }
      })
      
      // Call the getCurrentUser method
      await authService.getCurrentUser()
      
      // Check if api.get was called with correct parameters
      expect(api.get).toHaveBeenCalledWith('/auth/user/')
    })
  })
})
