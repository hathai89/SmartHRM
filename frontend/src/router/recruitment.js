const recruitmentRoutes = [
  {
    path: '/recruitment',
    name: 'recruitment',
    component: () => import('@/views/recruitment/RecruitmentDashboard.vue'),
    meta: {
      requiresAuth: true,
      title: 'Tuyển dụng',
      breadcrumb: [
        { text: 'Trang chủ', to: '/' },
        { text: 'Tuyển dụng', active: true }
      ]
    }
  },
  {
    path: '/recruitment/job-postings',
    name: 'job-postings',
    component: () => import('@/views/recruitment/job-postings/JobPostingList.vue'),
    meta: {
      requiresAuth: true,
      title: 'Tin tuyển dụng',
      breadcrumb: [
        { text: 'Trang chủ', to: '/' },
        { text: 'Tuyển dụng', to: '/recruitment' },
        { text: 'Tin tuyển dụng', active: true }
      ]
    }
  },
  {
    path: '/recruitment/job-postings/create',
    name: 'create-job-posting',
    component: () => import('@/views/recruitment/job-postings/JobPostingForm.vue'),
    meta: {
      requiresAuth: true,
      title: 'Tạo tin tuyển dụng',
      breadcrumb: [
        { text: 'Trang chủ', to: '/' },
        { text: 'Tuyển dụng', to: '/recruitment' },
        { text: 'Tin tuyển dụng', to: '/recruitment/job-postings' },
        { text: 'Tạo tin tuyển dụng', active: true }
      ]
    }
  },
  {
    path: '/recruitment/job-postings/:id',
    name: 'job-posting-detail',
    component: () => import('@/views/recruitment/job-postings/JobPostingDetail.vue'),
    meta: {
      requiresAuth: true,
      title: 'Chi tiết tin tuyển dụng',
      breadcrumb: [
        { text: 'Trang chủ', to: '/' },
        { text: 'Tuyển dụng', to: '/recruitment' },
        { text: 'Tin tuyển dụng', to: '/recruitment/job-postings' },
        { text: 'Chi tiết tin tuyển dụng', active: true }
      ]
    }
  },
  {
    path: '/recruitment/job-postings/:id/edit',
    name: 'edit-job-posting',
    component: () => import('@/views/recruitment/job-postings/JobPostingForm.vue'),
    meta: {
      requiresAuth: true,
      title: 'Chỉnh sửa tin tuyển dụng',
      breadcrumb: [
        { text: 'Trang chủ', to: '/' },
        { text: 'Tuyển dụng', to: '/recruitment' },
        { text: 'Tin tuyển dụng', to: '/recruitment/job-postings' },
        { text: 'Chỉnh sửa tin tuyển dụng', active: true }
      ]
    }
  },
  {
    path: '/recruitment/applications',
    name: 'applications',
    component: () => import('@/views/recruitment/applications/ApplicationList.vue'),
    meta: {
      requiresAuth: true,
      title: 'Đơn ứng tuyển',
      breadcrumb: [
        { text: 'Trang chủ', to: '/' },
        { text: 'Tuyển dụng', to: '/recruitment' },
        { text: 'Đơn ứng tuyển', active: true }
      ]
    }
  },
  {
    path: '/recruitment/applications/:id',
    name: 'application-detail',
    component: () => import('@/views/recruitment/applications/ApplicationDetail.vue'),
    meta: {
      requiresAuth: true,
      title: 'Chi tiết đơn ứng tuyển',
      breadcrumb: [
        { text: 'Trang chủ', to: '/' },
        { text: 'Tuyển dụng', to: '/recruitment' },
        { text: 'Đơn ứng tuyển', to: '/recruitment/applications' },
        { text: 'Chi tiết đơn ứng tuyển', active: true }
      ]
    }
  },
  {
    path: '/recruitment/interviews',
    name: 'interviews',
    component: () => import('@/views/recruitment/interviews/InterviewList.vue'),
    meta: {
      requiresAuth: true,
      title: 'Phỏng vấn',
      breadcrumb: [
        { text: 'Trang chủ', to: '/' },
        { text: 'Tuyển dụng', to: '/recruitment' },
        { text: 'Phỏng vấn', active: true }
      ]
    }
  },
  {
    path: '/recruitment/interviews/:id',
    name: 'interview-detail',
    component: () => import('@/views/recruitment/interviews/InterviewDetail.vue'),
    meta: {
      requiresAuth: true,
      title: 'Chi tiết phỏng vấn',
      breadcrumb: [
        { text: 'Trang chủ', to: '/' },
        { text: 'Tuyển dụng', to: '/recruitment' },
        { text: 'Phỏng vấn', to: '/recruitment/interviews' },
        { text: 'Chi tiết phỏng vấn', active: true }
      ]
    }
  },
  // Public routes
  {
    path: '/careers',
    name: 'careers',
    component: () => import('@/views/recruitment/public/CareersList.vue'),
    meta: {
      requiresAuth: false,
      title: 'Cơ hội việc làm',
      breadcrumb: [
        { text: 'Trang chủ', to: '/' },
        { text: 'Cơ hội việc làm', active: true }
      ]
    }
  },
  {
    path: '/careers/:id',
    name: 'career-detail',
    component: () => import('@/views/recruitment/public/CareerDetail.vue'),
    meta: {
      requiresAuth: false,
      title: 'Chi tiết việc làm',
      breadcrumb: [
        { text: 'Trang chủ', to: '/' },
        { text: 'Cơ hội việc làm', to: '/careers' },
        { text: 'Chi tiết việc làm', active: true }
      ]
    }
  },
  {
    path: '/careers/:id/apply',
    name: 'career-apply',
    component: () => import('@/views/recruitment/public/ApplicationForm.vue'),
    meta: {
      requiresAuth: false,
      title: 'Ứng tuyển',
      breadcrumb: [
        { text: 'Trang chủ', to: '/' },
        { text: 'Cơ hội việc làm', to: '/careers' },
        { text: 'Ứng tuyển', active: true }
      ]
    }
  }
]

export default recruitmentRoutes
