import { mount } from '@vue/test-utils'
import Login from '@/views/auth/Login.vue'
import { createStore } from 'vuex'
import { createRouter, createMemoryHistory } from 'vue-router'

// Mock store
const createVuexStore = () => {
  return createStore({
    modules: {
      auth: {
        namespaced: true,
        state: {
          user: null,
          token: null,
          status: {
            loggedIn: false
          }
        },
        actions: {
          login: jest.fn()
        }
      }
    },
    actions: {
      setError: jest.fn(),
      clearError: jest.fn()
    }
  })
}

// Mock router
const createVueRouter = () => {
  return createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/', name: 'dashboard', component: { template: '<div>Dashboard</div>' } },
      { path: '/login', name: 'login', component: { template: '<div>Login</div>' } },
      { path: '/forgot-password', name: 'forgot-password', component: { template: '<div>Forgot Password</div>' } }
    ]
  })
}

describe('Login.vue', () => {
  let store
  let router
  
  beforeEach(() => {
    store = createVuexStore()
    router = createVueRouter()
    
    // Mock the login action
    store.modules = {
      auth: {
        namespaced: true,
        actions: {
          login: jest.fn()
        }
      }
    }
  })
  
  test('renders correctly', () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [store, router],
        stubs: {
          FontAwesomeIcon: true,
          RouterLink: true,
          AlertMessage: true
        },
        mocks: {
          $t: (key) => key
        }
      }
    })
    
    // Check if the login form is rendered
    expect(wrapper.find('form').exists()).toBe(true)
    
    // Check if the username input is rendered
    expect(wrapper.find('#username').exists()).toBe(true)
    
    // Check if the password input is rendered
    expect(wrapper.find('#password').exists()).toBe(true)
    
    // Check if the login button is rendered
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
  })
  
  test('calls login action when form is submitted', async () => {
    // Mock the login action
    const loginAction = jest.fn()
    store.dispatch = jest.fn()
    
    const wrapper = mount(Login, {
      global: {
        plugins: [store, router],
        stubs: {
          FontAwesomeIcon: true,
          RouterLink: true,
          AlertMessage: true
        },
        mocks: {
          $t: (key) => key
        }
      }
    })
    
    // Set the username and password
    await wrapper.find('#username').setValue('testuser')
    await wrapper.find('#password').setValue('password123')
    
    // Submit the form
    await wrapper.find('form').trigger('submit.prevent')
    
    // Check if the login action was called
    expect(store.dispatch).toHaveBeenCalledWith('auth/login', {
      username: 'testuser',
      password: 'password123'
    })
  })
  
  test('shows error when login fails', async () => {
    // Mock the login action to throw an error
    store.dispatch = jest.fn().mockRejectedValue(new Error('Invalid credentials'))
    
    const wrapper = mount(Login, {
      global: {
        plugins: [store, router],
        stubs: {
          FontAwesomeIcon: true,
          RouterLink: true,
          AlertMessage: true
        },
        mocks: {
          $t: (key) => key
        }
      }
    })
    
    // Set the username and password
    await wrapper.find('#username').setValue('testuser')
    await wrapper.find('#password').setValue('password123')
    
    // Submit the form
    await wrapper.find('form').trigger('submit.prevent')
    
    // Check if the setError action was called
    expect(store.dispatch).toHaveBeenCalledWith('setError', expect.any(String))
  })
})
