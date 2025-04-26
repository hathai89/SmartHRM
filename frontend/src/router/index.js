import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'

// Lazy-load các component
const Login = () => import('@/views/auth/Login.vue')
const ForgotPassword = () => import('@/views/auth/ForgotPassword.vue')
const ResetPassword = () => import('@/views/auth/ResetPassword.vue')
const ChangePassword = () => import('@/views/auth/ChangePassword.vue')
const Profile = () => import('@/views/profile/Profile.vue')
const Dashboard = () => import('@/views/dashboard/Dashboard.vue')
const EmployeeList = () => import('@/views/employees/EmployeeList.vue')
const EmployeeDetail = () => import('@/views/employees/EmployeeDetail.vue')
const EmployeeForm = () => import('@/views/employees/EmployeeForm.vue')
const DepartmentList = () => import('@/views/departments/DepartmentList.vue')
const FactoryList = () => import('@/views/factories/FactoryList.vue')
const DocumentList = () => import('@/views/documents/DocumentList.vue')
const Settings = () => import('@/views/settings/Settings.vue')
const CompanyInfo = () => import('@/views/company/CompanyInfo.vue')
const NotFound = () => import('@/views/errors/NotFound.vue')

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: ForgotPassword,
    meta: { requiresAuth: false }
  },
  {
    path: '/reset-password',
    name: 'reset-password',
    component: ResetPassword,
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/employees',
    name: 'employees',
    component: EmployeeList,
    meta: { requiresAuth: true }
  },
  {
    path: '/employees/:id',
    name: 'employee-detail',
    component: EmployeeDetail,
    meta: { requiresAuth: true }
  },
  {
    path: '/employees/create',
    name: 'employee-create',
    component: EmployeeForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/employees/:id/edit',
    name: 'employee-edit',
    component: EmployeeForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/departments',
    name: 'departments',
    component: DepartmentList,
    meta: { requiresAuth: true }
  },
  {
    path: '/factories',
    name: 'factories',
    component: FactoryList,
    meta: { requiresAuth: true }
  },
  {
    path: '/documents',
    name: 'documents',
    component: DocumentList,
    meta: { requiresAuth: true }
  },
  {
    path: '/company',
    name: 'company',
    component: CompanyInfo,
    meta: { requiresAuth: true }
  },
  {
    path: '/change-password',
    name: 'change-password',
    component: ChangePassword,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'settings',
    component: Settings,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFound
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior() {
    // Luôn cuộn lên đầu trang khi chuyển trang
    return { top: 0 }
  }
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters['auth/isAuthenticated']

  // Kiểm tra xem route có yêu cầu xác thực không
  if (to.meta.requiresAuth && !isAuthenticated) {
    // Nếu route yêu cầu xác thực và người dùng chưa đăng nhập, chuyển hướng đến trang đăng nhập
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.name === 'login' && isAuthenticated) {
    // Nếu người dùng đã đăng nhập và cố gắng truy cập trang đăng nhập, chuyển hướng đến trang chủ
    next({ name: 'dashboard' })
  } else {
    // Trong các trường hợp khác, cho phép truy cập
    next()
  }
})

export default router
