import { mount } from '@vue/test-utils'
import Profile from '@/views/profile/Profile.vue'
import { createStore } from 'vuex'
import { createRouter, createMemoryHistory } from 'vue-router'

// Mock store
const createVuexStore = () => {
  return createStore({
    modules: {
      auth: {
        namespaced: true,
        state: {
          user: {
            id: 1,
            username: 'admin',
            email: 'admin@example.com',
            first_name: 'Admin',
            last_name: 'User',
            is_staff: true
          },
          token: 'fake-token'
        },
        getters: {
          isAuthenticated: () => true,
          user: state => state.user
        },
        actions: {
          updateProfile: jest.fn()
        }
      }
    },
    actions: {
      setSuccess: jest.fn(),
      setError: jest.fn(),
      clearSuccess: jest.fn(),
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
      { path: '/profile', name: 'profile', component: { template: '<div>Profile</div>' } },
      { path: '/change-password', name: 'change-password', component: { template: '<div>Change Password</div>' } }
    ]
  })
}

describe('Profile.vue', () => {
  let store
  let router
  
  beforeEach(() => {
    store = createVuexStore()
    router = createVueRouter()
    
    // Mock the updateProfile action
    store.dispatch = jest.fn()
  })
  
  test('renders correctly with user data', async () => {
    const wrapper = mount(Profile, {
      global: {
        plugins: [store, router],
        stubs: {
          FontAwesomeIcon: true,
          RouterLink: true,
          AlertMessage: true,
          LoadingSpinner: true
        },
        mocks: {
          $t: (key) => key
        }
      }
    })
    
    // Wait for component to mount
    await wrapper.vm.$nextTick()
    
    // Check if the profile form is rendered
    expect(wrapper.find('form').exists()).toBe(true)
  })
  
  test('calls updateProfile action when form is submitted', async () => {
    // Mock the updateProfile action to return a successful response
    store.dispatch.mockResolvedValue({
      data: {
        id: 1,
        username: 'admin',
        email: 'updated@example.com',
        first_name: 'Updated',
        last_name: 'User',
        is_staff: true
      }
    })
    
    const wrapper = mount(Profile, {
      global: {
        plugins: [store, router],
        stubs: {
          FontAwesomeIcon: true,
          RouterLink: true,
          AlertMessage: true,
          LoadingSpinner: true
        },
        mocks: {
          $t: (key) => key
        }
      }
    })
    
    // Wait for component to mount
    await wrapper.vm.$nextTick()
    
    // Update the form fields
    await wrapper.find('#email').setValue('updated@example.com')
    await wrapper.find('#first_name').setValue('Updated')
    
    // Submit the form
    await wrapper.find('form').trigger('submit.prevent')
    
    // Check if the updateProfile action was called
    expect(store.dispatch).toHaveBeenCalledWith('auth/updateProfile', expect.objectContaining({
      email: 'updated@example.com',
      first_name: 'Updated'
    }))
  })
  
  test('shows error when updateProfile fails', async () => {
    // Mock the updateProfile action to throw an error
    store.dispatch.mockRejectedValue(new Error('Update failed'))
    
    const wrapper = mount(Profile, {
      global: {
        plugins: [store, router],
        stubs: {
          FontAwesomeIcon: true,
          RouterLink: true,
          AlertMessage: true,
          LoadingSpinner: true
        },
        mocks: {
          $t: (key) => key
        }
      }
    })
    
    // Wait for component to mount
    await wrapper.vm.$nextTick()
    
    // Update the form fields
    await wrapper.find('#email').setValue('updated@example.com')
    
    // Submit the form
    await wrapper.find('form').trigger('submit.prevent')
    
    // Check if the setError action was called
    expect(store.dispatch).toHaveBeenCalledWith('setError', expect.any(String))
  })
})
