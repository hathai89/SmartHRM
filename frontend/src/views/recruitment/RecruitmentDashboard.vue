<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-end align-items-center mb-4">
          <router-link to="/recruitment/job-postings/create" class="btn-flat btn-flat-primary">
            <font-awesome-icon icon="plus" class="me-2" />
            Tạo tin tuyển dụng
          </router-link>
        </div>
      </div>
    </div>

    <div class="row">
      <!-- Thống kê -->
      <div class="col-md-3 mb-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Tin tuyển dụng</h5>
            <div class="d-flex align-items-center">
              <div class="display-4 me-3">{{ stats.jobPostings }}</div>
              <div>
                <div class="text-success">{{ stats.activeJobPostings }} đang mở</div>
                <div class="text-muted">{{ stats.closedJobPostings }} đã đóng</div>
              </div>
            </div>
          </div>
          <div class="card-footer bg-transparent">
            <router-link to="/recruitment/job-postings" class="text-decoration-none">
              Xem tất cả <font-awesome-icon icon="arrow-right" />
            </router-link>
          </div>
        </div>
      </div>

      <div class="col-md-3 mb-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Đơn ứng tuyển</h5>
            <div class="d-flex align-items-center">
              <div class="display-4 me-3">{{ stats.applications }}</div>
              <div>
                <div class="text-primary">{{ stats.newApplications }} mới</div>
                <div class="text-muted">{{ stats.processedApplications }} đã xử lý</div>
              </div>
            </div>
          </div>
          <div class="card-footer bg-transparent">
            <router-link to="/recruitment/applications" class="text-decoration-none">
              Xem tất cả <font-awesome-icon icon="arrow-right" />
            </router-link>
          </div>
        </div>
      </div>

      <div class="col-md-3 mb-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Phỏng vấn</h5>
            <div class="d-flex align-items-center">
              <div class="display-4 me-3">{{ stats.interviews }}</div>
              <div>
                <div class="text-warning">{{ stats.upcomingInterviews }} sắp tới</div>
                <div class="text-muted">{{ stats.completedInterviews }} đã hoàn thành</div>
              </div>
            </div>
          </div>
          <div class="card-footer bg-transparent">
            <router-link to="/recruitment/interviews" class="text-decoration-none">
              Xem tất cả <font-awesome-icon icon="arrow-right" />
            </router-link>
          </div>
        </div>
      </div>

      <div class="col-md-3 mb-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Tỷ lệ tuyển dụng</h5>
            <div class="d-flex align-items-center">
              <div class="display-4 me-3">{{ stats.hireRate }}%</div>
              <div>
                <div class="text-success">{{ stats.hired }} đã tuyển</div>
                <div class="text-danger">{{ stats.rejected }} từ chối</div>
              </div>
            </div>
          </div>
          <div class="card-footer bg-transparent">
            <router-link to="/recruitment/applications?status=hired" class="text-decoration-none">
              Xem chi tiết <font-awesome-icon icon="arrow-right" />
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <!-- Tin tuyển dụng gần đây -->
      <div class="col-md-6 mb-4">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="card-title mb-0">Tin tuyển dụng gần đây</h5>
            <router-link to="/recruitment/job-postings" class="btn btn-sm btn-outline-primary">
              Xem tất cả
            </router-link>
          </div>
          <div class="card-body">
            <div v-if="loading" class="text-center py-3">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Đang tải...</span>
              </div>
            </div>
            <div v-else-if="recentJobPostings.length === 0" class="text-center py-3">
              <p class="text-muted">Chưa có tin tuyển dụng nào</p>
            </div>
            <div v-else class="list-group list-group-flush">
              <router-link
                v-for="job in recentJobPostings"
                :key="job.id"
                :to="`/recruitment/job-postings/${job.id}`"
                class="list-group-item list-group-item-action"
              >
                <div class="d-flex w-100 justify-content-between">
                  <h6 class="mb-1">{{ job.title }}</h6>
                  <small :class="getStatusClass(job.status)">{{ job.status_display }}</small>
                </div>
                <p class="mb-1">{{ job.department_name || job.factory_name }}</p>
                <small class="text-muted">
                  <font-awesome-icon icon="calendar" class="me-1" />
                  {{ formatDate(job.publish_date) }} - {{ formatDate(job.closing_date) }}
                </small>
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Đơn ứng tuyển gần đây -->
      <div class="col-md-6 mb-4">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="card-title mb-0">Đơn ứng tuyển gần đây</h5>
            <router-link to="/recruitment/applications" class="btn btn-sm btn-outline-primary">
              Xem tất cả
            </router-link>
          </div>
          <div class="card-body">
            <div v-if="loading" class="text-center py-3">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Đang tải...</span>
              </div>
            </div>
            <div v-else-if="recentApplications.length === 0" class="text-center py-3">
              <p class="text-muted">Chưa có đơn ứng tuyển nào</p>
            </div>
            <div v-else class="list-group list-group-flush">
              <router-link
                v-for="application in recentApplications"
                :key="application.id"
                :to="`/recruitment/applications/${application.id}`"
                class="list-group-item list-group-item-action"
              >
                <div class="d-flex w-100 justify-content-between">
                  <h6 class="mb-1">{{ application.full_name }}</h6>
                  <small :class="getApplicationStatusClass(application.status)">
                    {{ application.status_display }}
                  </small>
                </div>
                <p class="mb-1">{{ application.job_title }}</p>
                <small class="text-muted">
                  <font-awesome-icon icon="calendar" class="me-1" />
                  {{ formatDate(application.created_at) }}
                </small>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <!-- Phỏng vấn sắp tới -->
      <div class="col-12 mb-4">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="card-title mb-0">Lịch phỏng vấn sắp tới</h5>
            <router-link to="/recruitment/interviews" class="btn btn-sm btn-outline-primary">
              Xem tất cả
            </router-link>
          </div>
          <div class="card-body">
            <div v-if="loading" class="text-center py-3">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Đang tải...</span>
              </div>
            </div>
            <div v-else-if="upcomingInterviews.length === 0" class="text-center py-3">
              <p class="text-muted">Không có lịch phỏng vấn nào sắp tới</p>
            </div>
            <div v-else class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>Ứng viên</th>
                    <th>Vị trí</th>
                    <th>Thời gian</th>
                    <th>Địa điểm</th>
                    <th>Loại phỏng vấn</th>
                    <th>Trạng thái</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="interview in upcomingInterviews"
                    :key="interview.id"
                    @click="goToInterview(interview.id)"
                    style="cursor: pointer"
                  >
                    <td>{{ interview.application_name }}</td>
                    <td>{{ interview.application.job_posting.title }}</td>
                    <td>{{ formatDateTime(interview.scheduled_date) }}</td>
                    <td>{{ interview.location }}</td>
                    <td>{{ interview.interview_type_display }}</td>
                    <td>
                      <span :class="getInterviewStatusClass(interview.status)">
                        {{ interview.status_display }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import axios from 'axios'
import { API_URL } from '@/config'

export default {
  name: 'RecruitmentDashboard',
  data() {
    return {
      stats: {
        jobPostings: 0,
        activeJobPostings: 0,
        closedJobPostings: 0,
        applications: 0,
        newApplications: 0,
        processedApplications: 0,
        interviews: 0,
        upcomingInterviews: 0,
        completedInterviews: 0,
        hireRate: 0,
        hired: 0,
        rejected: 0
      },
      recentJobPostings: [],
      recentApplications: [],
      upcomingInterviews: []
    }
  },
  computed: {
    ...mapGetters('recruitment', ['loading', 'error'])
  },
  created() {
    this.fetchDashboardData()
  },
  methods: {
    async fetchDashboardData() {
      try {
        // Fetch job postings
        await this.$store.dispatch('recruitment/fetchJobPostings', { limit: 5, ordering: '-created_at' })
        this.recentJobPostings = this.$store.getters['recruitment/jobPostings'].slice(0, 5)

        // Fetch applications
        await this.$store.dispatch('recruitment/fetchApplications', { limit: 5, ordering: '-created_at' })
        this.recentApplications = this.$store.getters['recruitment/applications'].slice(0, 5)

        // Fetch upcoming interviews
        const today = new Date().toISOString().split('T')[0]
        await this.$store.dispatch('recruitment/fetchInterviews', {
          scheduled_date_from: today,
          status: 'scheduled',
          ordering: 'scheduled_date',
          limit: 10
        })
        this.upcomingInterviews = this.$store.getters['recruitment/interviews'].slice(0, 10)

        // Calculate stats
        this.calculateStats()
      } catch (error) {
        console.error('Error fetching dashboard data:', error)
      }
    },
    async calculateStats() {
      try {
        // Fetch stats from API
        const response = await axios.get(`${API_URL}/recruitment/dashboard/stats/`)
        this.stats = response.data
      } catch (error) {
        console.error('Error fetching dashboard stats:', error)
        // Fallback to calculated stats from current data
        const jobPostings = this.$store.getters['recruitment/jobPostings']
        const applications = this.$store.getters['recruitment/applications']
        const interviews = this.$store.getters['recruitment/interviews']

        // Calculate stats based on available data
        const activeJobPostings = jobPostings.filter(job => job.status === 'published').length
        const closedJobPostings = jobPostings.filter(job => job.status === 'closed').length
        const newApplications = applications.filter(app => app.status === 'new').length
        const processedApplications = applications.length - newApplications
        const upcomingInterviews = interviews.filter(interview => interview.status === 'scheduled').length
        const completedInterviews = interviews.filter(interview => interview.status === 'completed').length
        const hired = applications.filter(app => app.status === 'hired').length
        const rejected = applications.filter(app => app.status === 'rejected').length
        const hireRate = applications.length > 0 ? Math.round((hired / applications.length) * 100) : 0

        this.stats = {
          jobPostings: jobPostings.length,
          activeJobPostings,
          closedJobPostings,
          applications: applications.length,
          newApplications,
          processedApplications,
          interviews: interviews.length,
          upcomingInterviews,
          completedInterviews,
          hireRate,
          hired,
          rejected
        }
      }
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('vi-VN')
    },
    formatDateTime(dateTimeString) {
      if (!dateTimeString) return 'N/A'
      const date = new Date(dateTimeString)
      return `${date.toLocaleTimeString('vi-VN', {hour: '2-digit', minute:'2-digit'})} - ${date.toLocaleDateString('vi-VN')}`
    },
    getStatusClass(status) {
      switch (status) {
        case 'draft':
          return 'text-secondary'
        case 'published':
          return 'text-success'
        case 'closed':
          return 'text-danger'
        case 'on_hold':
          return 'text-warning'
        default:
          return 'text-muted'
      }
    },
    getApplicationStatusClass(status) {
      switch (status) {
        case 'new':
          return 'text-primary'
        case 'screening':
          return 'text-info'
        case 'interview_scheduled':
          return 'text-warning'
        case 'offered':
          return 'text-success'
        case 'hired':
          return 'text-success'
        case 'rejected':
          return 'text-danger'
        default:
          return 'text-muted'
      }
    },
    getInterviewStatusClass(status) {
      switch (status) {
        case 'scheduled':
          return 'badge bg-warning'
        case 'completed':
          return 'badge bg-success'
        case 'cancelled':
          return 'badge bg-danger'
        default:
          return 'badge bg-secondary'
      }
    },
    goToInterview(id) {
      this.$router.push(`/recruitment/interviews/${id}`)
    }
  }
}
</script>

<style scoped>
.card {
  height: 100%;
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.display-4 {
  font-weight: 600;
  font-size: 2.5rem;
}

.list-group-item-action:hover {
  background-color: #f8f9fa;
}
</style>
