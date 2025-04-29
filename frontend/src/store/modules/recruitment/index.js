import api from '@/services/api.service'

const state = {
  jobPostings: [],
  jobPosting: null,
  applications: [],
  application: null,
  interviews: [],
  interview: null,
  loading: false,
  error: null
}

const getters = {
  jobPostings: state => state.jobPostings,
  jobPosting: state => state.jobPosting,
  applications: state => state.applications,
  application: state => state.application,
  interviews: state => state.interviews,
  interview: state => state.interview,
  loading: state => state.loading,
  error: state => state.error
}

const actions = {
  // Job Postings
  async fetchJobPostings({ commit }, params = {}) {
    commit('SET_LOADING', true)
    try {
      const response = await api.get('/recruitment/job-postings/', { params })

      // Kiểm tra cấu trúc dữ liệu và đảm bảo jobPostings luôn là mảng
      if (response.data && response.data.results) {
        // Nếu API trả về dạng phân trang
        commit('SET_JOB_POSTINGS', response.data.results)
      } else if (Array.isArray(response.data)) {
        // Nếu API trả về mảng trực tiếp
        commit('SET_JOB_POSTINGS', response.data)
      } else {
        // Trường hợp khác, đặt mảng rỗng
        commit('SET_JOB_POSTINGS', [])
      }

      commit('SET_ERROR', null)
      return response.data // Trả về response.data để component có thể sử dụng
    } catch (error) {
      commit('SET_ERROR', error.response ? error.response.data : error.message)
      commit('SET_JOB_POSTINGS', []) // Đặt mảng rỗng khi có lỗi
      throw error // Ném lỗi để component có thể bắt
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async fetchJobPosting({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await api.get(`/recruitment/job-postings/${id}/`)
      commit('SET_JOB_POSTING', response.data)
      commit('SET_ERROR', null)
    } catch (error) {
      commit('SET_ERROR', error.response ? error.response.data : error.message)
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async createJobPosting({ commit }, jobPosting) {
    commit('SET_LOADING', true)
    try {
      const response = await api.post('/recruitment/job-postings/', jobPosting)
      commit('SET_JOB_POSTING', response.data)
      commit('SET_ERROR', null)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.response ? error.response.data : error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async updateJobPosting({ commit }, { id, data }) {
    commit('SET_LOADING', true)
    try {
      const response = await api.patch(`/recruitment/job-postings/${id}/`, data)
      commit('SET_JOB_POSTING', response.data)
      commit('SET_ERROR', null)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.response ? error.response.data : error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async publishJobPosting({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await api.post(`/recruitment/job-postings/${id}/publish/`)
      commit('SET_ERROR', null)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.response ? error.response.data : error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async closeJobPosting({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await api.post(`/recruitment/job-postings/${id}/close/`)
      commit('SET_ERROR', null)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.response ? error.response.data : error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async cancelJobPosting({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await api.post(`/recruitment/job-postings/${id}/cancel/`)
      commit('SET_ERROR', null)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.response ? error.response.data : error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // Applications
  async fetchApplications({ commit }, params = {}) {
    commit('SET_LOADING', true)
    try {
      const response = await api.get('/recruitment/applications/', { params })

      // Kiểm tra cấu trúc dữ liệu và đảm bảo applications luôn là mảng
      if (response.data && response.data.results) {
        // Nếu API trả về dạng phân trang
        commit('SET_APPLICATIONS', response.data)
      } else if (Array.isArray(response.data)) {
        // Nếu API trả về mảng trực tiếp
        commit('SET_APPLICATIONS', response.data)
      } else {
        // Trường hợp khác, đặt mảng rỗng
        commit('SET_APPLICATIONS', [])
      }

      commit('SET_ERROR', null)
      return response.data // Trả về response.data để component có thể sử dụng
    } catch (error) {
      console.error('Error fetching applications:', error)
      commit('SET_ERROR', error.response ? error.response.data : error.message)
      commit('SET_APPLICATIONS', []) // Đặt mảng rỗng khi có lỗi
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async fetchApplication({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await api.get(`/recruitment/applications/${id}/`)
      commit('SET_APPLICATION', response.data)
      commit('SET_ERROR', null)
    } catch (error) {
      commit('SET_ERROR', error.response ? error.response.data : error.message)
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async updateApplicationStatus({ commit }, { id, status, notes }) {
    commit('SET_LOADING', true)
    try {
      const response = await api.post(`/recruitment/applications/${id}/change_status/`, { status, notes })
      commit('SET_ERROR', null)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.response ? error.response.data : error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async scheduleInterview({ commit }, { id, data }) {
    commit('SET_LOADING', true)
    try {
      const response = await api.post(`/recruitment/applications/${id}/schedule_interview/`, data)
      commit('SET_ERROR', null)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.response ? error.response.data : error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // Interviews
  async fetchInterviews({ commit }, params = {}) {
    commit('SET_LOADING', true)
    try {
      const response = await api.get('/recruitment/interviews/', { params })
      commit('SET_INTERVIEWS', response.data)
      commit('SET_ERROR', null)
    } catch (error) {
      commit('SET_ERROR', error.response ? error.response.data : error.message)
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async fetchInterview({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await api.get(`/recruitment/interviews/${id}/`)
      commit('SET_INTERVIEW', response.data)
      commit('SET_ERROR', null)
    } catch (error) {
      commit('SET_ERROR', error.response ? error.response.data : error.message)
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async completeInterview({ commit }, { id, data }) {
    commit('SET_LOADING', true)
    try {
      const response = await api.post(`/recruitment/interviews/${id}/complete/`, data)
      commit('SET_ERROR', null)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.response ? error.response.data : error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async cancelInterview({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await api.post(`/recruitment/interviews/${id}/cancel/`)
      commit('SET_ERROR', null)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.response ? error.response.data : error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // Public API
  async fetchPublicJobPostings({ commit }, params = {}) {
    commit('SET_LOADING', true)
    try {
      const response = await api.get('/recruitment/public/job-postings/', { params })
      // Kiểm tra cấu trúc dữ liệu và đảm bảo jobPostings luôn là mảng
      if (response.data && response.data.results) {
        commit('SET_JOB_POSTINGS', response.data.results)
      } else if (Array.isArray(response.data)) {
        commit('SET_JOB_POSTINGS', response.data)
      } else {
        commit('SET_JOB_POSTINGS', [])
      }
      commit('SET_ERROR', null)
      return response.data // Trả về response.data để component có thể sử dụng
    } catch (error) {
      commit('SET_ERROR', error.response ? error.response.data : error.message)
      commit('SET_JOB_POSTINGS', [])
      throw error // Ném lỗi để component có thể bắt
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async fetchPublicJobPosting({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await api.get(`/recruitment/public/job-postings/${id}/`)
      commit('SET_JOB_POSTING', response.data)
      commit('SET_ERROR', null)
    } catch (error) {
      commit('SET_ERROR', error.response ? error.response.data : error.message)
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async submitApplication({ commit }, application) {
    commit('SET_LOADING', true)
    try {
      // Nếu application đã là FormData, sử dụng trực tiếp
      let formData = application

      // Nếu application là object thông thường, chuyển đổi thành FormData
      if (!(application instanceof FormData)) {
        formData = new FormData()

        // Append all fields to FormData
        Object.keys(application).forEach(key => {
          // Xử lý các trường file
          if ((key === 'resume' || key === 'avatar' ||
               key === 'id_card_front_image' || key === 'id_card_back_image') &&
              application[key] instanceof File) {
            formData.append(key, application[key])
          }
          // Xử lý các trường boolean
          else if (typeof application[key] === 'boolean') {
            formData.append(key, application[key] ? 'true' : 'false')
          }
          // Xử lý các trường khác
          else if (application[key] !== null && application[key] !== undefined) {
            formData.append(key, application[key])
          }
        })
      }

      const response = await api.post('/recruitment/public/applications/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      commit('SET_ERROR', null)
      return response.data
    } catch (error) {
      commit('SET_ERROR', error.response ? error.response.data : error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // Public Departments and Factories
  async fetchPublicDepartments({ commit }) {
    commit('SET_LOADING', true)
    try {
      const response = await api.get('/recruitment/public/departments/')
      commit('SET_ERROR', null)
      return response.data
    } catch (error) {
      console.error('Error fetching public departments:', error)
      commit('SET_ERROR', error.response ? error.response.data : error.message)
      return []
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async fetchPublicFactories({ commit }) {
    commit('SET_LOADING', true)
    try {
      const response = await api.get('/recruitment/public/factories/')
      commit('SET_ERROR', null)
      return response.data
    } catch (error) {
      console.error('Error fetching public factories:', error)
      commit('SET_ERROR', error.response ? error.response.data : error.message)
      return []
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // Marital Status and Family Policy Types
  async fetchMaritalStatus({ commit }) {
    commit('SET_LOADING', true)
    try {
      const response = await api.get('/recruitment/public/marital-status/')
      commit('SET_ERROR', null)
      console.log('API response for marital status:', response.data)
      return response.data
    } catch (error) {
      console.error('Error fetching marital status:', error)
      commit('SET_ERROR', error.response ? error.response.data : error.message)
      return { results: [] }
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async fetchFamilyPolicyTypes({ commit }) {
    commit('SET_LOADING', true)
    try {
      const response = await api.get('/recruitment/public/family-policy-types/')
      commit('SET_ERROR', null)
      console.log('API response for family policy types:', response.data)
      return response.data
    } catch (error) {
      console.error('Error fetching family policy types:', error)
      commit('SET_ERROR', error.response ? error.response.data : error.message)
      return { results: [] }
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // Gender and Education Level
  async fetchGenders({ commit }) {
    commit('SET_LOADING', true)
    try {
      const response = await api.get('/recruitment/public/genders/')
      commit('SET_ERROR', null)
      console.log('API response for genders:', response.data)
      return response.data
    } catch (error) {
      console.error('Error fetching genders:', error)
      commit('SET_ERROR', error.response ? error.response.data : error.message)
      return { results: [] }
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async fetchEducationLevels({ commit }) {
    commit('SET_LOADING', true)
    try {
      const response = await api.get('/recruitment/public/education-levels/')
      commit('SET_ERROR', null)
      console.log('API response for education levels:', response.data)
      return response.data
    } catch (error) {
      console.error('Error fetching education levels:', error)
      commit('SET_ERROR', error.response ? error.response.data : error.message)
      return { results: [] }
    } finally {
      commit('SET_LOADING', false)
    }
  }
}

const mutations = {
  SET_JOB_POSTINGS(state, jobPostings) {
    // Đảm bảo jobPostings là mảng và không chứa phần tử null hoặc undefined
    if (Array.isArray(jobPostings)) {
      state.jobPostings = jobPostings.filter(job => job && job.id)
    } else {
      state.jobPostings = []
    }
  },
  SET_JOB_POSTING(state, jobPosting) {
    state.jobPosting = jobPosting
  },
  SET_APPLICATIONS(state, applications) {
    // Đảm bảo applications là mảng và không chứa phần tử null hoặc undefined
    if (Array.isArray(applications)) {
      state.applications = applications.filter(app => app && app.id)
    } else if (applications && applications.results && Array.isArray(applications.results)) {
      // Nếu API trả về dạng phân trang
      state.applications = applications.results.filter(app => app && app.id)
    } else {
      state.applications = []
    }
  },
  SET_APPLICATION(state, application) {
    state.application = application
  },
  SET_INTERVIEWS(state, interviews) {
    state.interviews = interviews
  },
  SET_INTERVIEW(state, interview) {
    state.interview = interview
  },
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_ERROR(state, error) {
    state.error = error
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
