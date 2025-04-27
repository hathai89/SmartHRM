import { mount } from '@vue/test-utils'
import AppHeader from '@/components/layout/AppHeader.vue'
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
          user: state => state.user,
          currentUser: state => state.user
        },
        actions: {
          logout: jest.fn()
        }
      },
      notifications: {
        namespaced: true,
        state: {
          notifications: [],
          unreadCount: 5
        },
        getters: {
          unreadCount: state => state.unreadCount,
          allNotifications: state => state.notifications
        },
        actions: {
          fetchNotifications: jest.fn()
        }
      }
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
      { path: '/notifications', name: 'notifications', component: { template: '<div>Notifications</div>' } },
      { path: '/login', name: 'login', component: { template: '<div>Login</div>' } }
    ]
  })
}

describe('AppHeader.vue', () => {
  let store
  let router
  
  beforeEach(() => {
    store = createVuexStore()
    router = createVueRouter()
  })
  
  test('renders correctly when user is authenticated', () => {
    const wrapper = mount(AppHeader, {
      global: {
        plugins: [store, router],
        stubs: {
          FontAwesomeIcon: true,
          RouterLink: true
        },
        mocks: {
          $t: (key) => key
        }
      }
    })
    
    // Check if the logo is rendered
    expect(wrapper.find('.navbar-brand').exists()).toBe(true)
    
    // Check if the user dropdown is rendered
    expect(wrapper.find('.user-dropdown').exists()).toBe(true)
    
    // Check if the user name is rendered correctly
    expect(wrapper.find('.user-name').text()).toContain('Admin User')
    
    // Check if the notification badge shows the correct count
    expect(wrapper.find('.notification-badge').text()).toBe('5')
  })
  
  test('logout action is called when logout button is clicked', async () => {
    const wrapper = mount(AppHeader, {
      global: {
        plugins: [store, router],
        stubs: {
          FontAwesomeIcon: true,
          RouterLink: true
        },
        mocks: {
          $t: (key) => key
        }
      }
    })
    
    // Find and click the logout button
    await wrapper.find('.logout-button').trigger('click')
    
    // Check if the logout action was called
    expect(store.state.auth.actions.logout).toHaveBeenCalled()
  })
})
