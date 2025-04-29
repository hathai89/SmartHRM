<template>
  <div class="container-fluid">
    <div class="d-flex justify-content-end align-items-center mb-4">
      <button class="btn-flat btn-flat-secondary" @click="refreshData">
        <font-awesome-icon icon="sync" :class="{ 'fa-spin': loading }" />
        Làm mới
      </button>
    </div>

    <!-- Bộ lọc -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="row">
          <div class="col-md-3 mb-3">
            <label for="status" class="form-label">Trạng thái</label>
            <select id="status" v-model="filters.status" class="form-select" @change="applyFilters">
              <option value="">Tất cả</option>
              <option value="new">Mới</option>
              <option value="screening">Đang xem xét</option>
              <option value="interview_scheduled">Đã lên lịch phỏng vấn</option>
              <option value="offered">Đã đề nghị</option>
              <option value="hired">Đã tuyển</option>
              <option value="rejected">Từ chối</option>
            </select>
          </div>
          <div class="col-md-3 mb-3">
            <label for="job_posting" class="form-label">Tin tuyển dụng</label>
            <select id="job_posting" v-model="filters.job_posting" class="form-select" @change="applyFilters">
              <option value="">Tất cả</option>
              <option v-for="job in jobPostings" :key="job.id" :value="job.id">
                {{ job.title }}
              </option>
            </select>
          </div>
          <div class="col-md-3 mb-3">
            <label for="date_range" class="form-label">Thời gian</label>
            <select id="date_range" v-model="filters.date_range" class="form-select" @change="applyFilters">
              <option value="">Tất cả</option>
              <option value="today">Hôm nay</option>
              <option value="yesterday">Hôm qua</option>
              <option value="last_week">Tuần trước</option>
              <option value="last_month">Tháng trước</option>
            </select>
          </div>
          <div class="col-md-3 mb-3">
            <label for="search" class="form-label">Tìm kiếm</label>
            <div class="input-group">
              <input
                id="search"
                v-model="filters.search"
                type="text"
                class="form-control"
                placeholder="Tìm kiếm..."
                @keyup.enter="applyFilters"
              />
              <button class="btn btn-outline-secondary" type="button" @click="applyFilters">
                <font-awesome-icon icon="search" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Danh sách đơn ứng tuyển -->
    <div class="card">
      <div class="card-body">
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Đang tải...</span>
          </div>
        </div>
        <div v-else-if="applications.length === 0" class="text-center py-5">
          <p class="text-muted">Không có đơn ứng tuyển nào</p>
        </div>
        <div v-else>
          <div class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th @click="sortBy('full_name')">
                    Họ tên
                    <font-awesome-icon v-if="sortKey === 'full_name'" :icon="sortIcon" />
                  </th>
                  <th @click="sortBy('email')">
                    Email
                    <font-awesome-icon v-if="sortKey === 'email'" :icon="sortIcon" />
                  </th>
                  <th @click="sortBy('phone')">
                    Số điện thoại
                    <font-awesome-icon v-if="sortKey === 'phone'" :icon="sortIcon" />
                  </th>
                  <th @click="sortBy('job_posting.title')">
                    Vị trí ứng tuyển
                    <font-awesome-icon v-if="sortKey === 'job_posting.title'" :icon="sortIcon" />
                  </th>
                  <th @click="sortBy('created_at')">
                    Ngày nộp
                    <font-awesome-icon v-if="sortKey === 'created_at'" :icon="sortIcon" />
                  </th>
                  <th @click="sortBy('status')">
                    Trạng thái
                    <font-awesome-icon v-if="sortKey === 'status'" :icon="sortIcon" />
                  </th>
                  <th>Thao tác</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="application in applications" :key="application.id">
                  <td>{{ application.full_name }}</td>
                  <td>{{ application.email }}</td>
                  <td>{{ application.phone }}</td>
                  <td>{{ application.job_title }}</td>
                  <td>{{ formatDate(application.created_at) }}</td>
                  <td>
                    <span :class="getStatusBadgeClass(application.status)">
                      {{ application.status_display }}
                    </span>
                  </td>
                  <td>
                    <div class="btn-group">
                      <router-link
                        :to="`/recruitment/applications/${application.id}`"
                        class="btn btn-sm btn-outline-primary"
                        title="Xem chi tiết"
                      >
                        <font-awesome-icon icon="eye" />
                      </router-link>
                      <button
                        v-if="application.status === 'new'"
                        class="btn btn-sm btn-outline-info"
                        title="Bắt đầu xem xét"
                        @click="changeStatus(application.id, 'screening')"
                      >
                        <font-awesome-icon icon="clipboard-check" />
                      </button>
                      <button
                        v-if="application.status === 'screening'"
                        class="btn btn-sm btn-outline-warning"
                        title="Lên lịch phỏng vấn"
                        @click="scheduleInterview(application.id)"
                      >
                        <font-awesome-icon icon="calendar-plus" />
                      </button>
                      <button
                        v-if="['screening', 'interview_scheduled'].includes(application.status)"
                        class="btn btn-sm btn-outline-success"
                        title="Đề nghị"
                        @click="changeStatus(application.id, 'offered')"
                      >
                        <font-awesome-icon icon="check" />
                      </button>
                      <button
                        v-if="application.status === 'offered'"
                        class="btn btn-sm btn-outline-success"
                        title="Tuyển dụng"
                        @click="changeStatus(application.id, 'hired')"
                      >
                        <font-awesome-icon icon="user-plus" />
                      </button>
                      <button
                        v-if="!['rejected', 'hired'].includes(application.status)"
                        class="btn btn-sm btn-outline-danger"
                        title="Từ chối"
                        @click="changeStatus(application.id, 'rejected')"
                      >
                        <font-awesome-icon icon="times" />
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Phân trang -->
          <div class="d-flex justify-content-between align-items-center mt-3">
            <div>
              <span class="text-muted">Hiển thị {{ applications.length }} / {{ totalItems }} đơn ứng tuyển</span>
            </div>
            <nav aria-label="Page navigation">
              <ul class="pagination">
                <li :class="['page-item', { disabled: currentPage === 1 }]">
                  <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">
                    <font-awesome-icon icon="chevron-left" />
                  </a>
                </li>
                <li
                  v-for="page in totalPages"
                  :key="page"
                  :class="['page-item', { active: currentPage === page }]"
                >
                  <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
                </li>
                <li :class="['page-item', { disabled: currentPage === totalPages }]">
                  <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">
                    <font-awesome-icon icon="chevron-right" />
                  </a>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal lên lịch phỏng vấn -->
    <div class="modal fade" id="scheduleInterviewModal" tabindex="-1" aria-labelledby="scheduleInterviewModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="scheduleInterviewModalLabel">Lên lịch phỏng vấn</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitInterviewSchedule">
              <div class="mb-3">
                <label for="scheduled_date" class="form-label">Ngày phỏng vấn</label>
                <input
                  id="scheduled_date"
                  v-model="interviewForm.scheduled_date"
                  type="date"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="scheduled_time" class="form-label">Giờ phỏng vấn</label>
                <input
                  id="scheduled_time"
                  v-model="interviewForm.scheduled_time"
                  type="time"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="location" class="form-label">Địa điểm</label>
                <input
                  id="location"
                  v-model="interviewForm.location"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="interview_type" class="form-label">Loại phỏng vấn</label>
                <select id="interview_type" v-model="interviewForm.interview_type" class="form-select" required>
                  <option value="in_person">Trực tiếp</option>
                  <option value="phone">Điện thoại</option>
                  <option value="video">Video</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="interviewers" class="form-label">Người phỏng vấn</label>
                <input
                  id="interviewers"
                  v-model="interviewForm.interviewers"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="notes" class="form-label">Ghi chú</label>
                <textarea
                  id="notes"
                  v-model="interviewForm.notes"
                  class="form-control"
                  rows="3"
                ></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Hủy</button>
            <button type="button" class="btn btn-primary" @click="submitInterviewSchedule">Lưu</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import * as bootstrap from 'bootstrap'

export default {
  name: 'ApplicationList',
  data() {
    return {
      filters: {
        status: '',
        job_posting: '',
        date_range: '',
        search: ''
      },
      sortKey: 'created_at',
      sortDirection: 'desc',
      currentPage: 1,
      itemsPerPage: 10,
      totalItems: 0,
      jobPostings: [],
      interviewForm: {
        application_id: null,
        scheduled_date: '',
        scheduled_time: '',
        location: '',
        interview_type: 'in_person',
        interviewers: '',
        notes: ''
      }
    }
  },
  computed: {
    ...mapGetters('recruitment', ['applications', 'loading', 'error']),

    sortIcon() {
      return this.sortDirection === 'asc' ? 'sort-up' : 'sort-down'
    },

    totalPages() {
      return Math.ceil(this.totalItems / this.itemsPerPage)
    }
  },
  created() {
    this.fetchJobPostings()
    this.fetchApplications()

    // Check if there's a job_posting_id in the query params
    const jobPostingId = this.$route.query.job_posting_id
    if (jobPostingId) {
      this.filters.job_posting = jobPostingId
    }
  },
  methods: {
    async fetchJobPostings() {
      try {
        const response = await this.$store.dispatch('recruitment/fetchJobPostings')
        this.jobPostings = response.results || response
      } catch (error) {
        console.error('Error fetching job postings:', error)
      }
    },

    async fetchApplications() {
      try {
        const params = {
          page: this.currentPage,
          page_size: this.itemsPerPage,
          ordering: this.getSortParam(),
          ...this.getFilterParams()
        }

        await this.$store.dispatch('recruitment/fetchApplications', params)

        // In a real app, the total count would come from the API
        this.totalItems = 25 // Dummy value for now
      } catch (error) {
        console.error('Error fetching applications:', error)
      }
    },

    refreshData() {
      this.fetchApplications()
    },

    applyFilters() {
      this.currentPage = 1
      this.fetchApplications()
    },

    getFilterParams() {
      const params = {}

      if (this.filters.status) {
        params.status = this.filters.status
      }

      if (this.filters.job_posting) {
        params.job_posting = this.filters.job_posting
      }

      if (this.filters.date_range) {
        params.date_range = this.filters.date_range
      }

      if (this.filters.search) {
        params.search = this.filters.search
      }

      return params
    },

    sortBy(key) {
      if (this.sortKey === key) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortKey = key
        this.sortDirection = 'asc'
      }

      this.fetchApplications()
    },

    getSortParam() {
      const prefix = this.sortDirection === 'desc' ? '-' : ''
      return `${prefix}${this.sortKey}`
    },

    changePage(page) {
      if (page < 1 || page > this.totalPages) {
        return
      }

      this.currentPage = page
      this.fetchApplications()
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('vi-VN')
    },

    getStatusBadgeClass(status) {
      switch (status) {
        case 'new':
          return 'badge bg-primary'
        case 'screening':
          return 'badge bg-info'
        case 'interview_scheduled':
          return 'badge bg-warning'
        case 'offered':
          return 'badge bg-success'
        case 'hired':
          return 'badge bg-success'
        case 'rejected':
          return 'badge bg-danger'
        default:
          return 'badge bg-secondary'
      }
    },

    async changeStatus(id, status) {
      try {
        if (confirm(`Bạn có chắc chắn muốn chuyển trạng thái thành "${this.getStatusDisplay(status)}"?`)) {
          await this.$store.dispatch('recruitment/updateApplicationStatus', {
            id,
            status,
            notes: `Chuyển trạng thái thành ${this.getStatusDisplay(status)}`
          })
          this.$store.dispatch('app/setSuccess', 'Cập nhật trạng thái thành công')
          this.fetchApplications()
        }
      } catch (error) {
        this.$store.dispatch('app/setError', 'Cập nhật trạng thái thất bại')
        console.error('Error updating application status:', error)
      }
    },

    getStatusDisplay(status) {
      switch (status) {
        case 'new':
          return 'Mới'
        case 'screening':
          return 'Đang xem xét'
        case 'interview_scheduled':
          return 'Đã lên lịch phỏng vấn'
        case 'offered':
          return 'Đã đề nghị'
        case 'hired':
          return 'Đã tuyển'
        case 'rejected':
          return 'Từ chối'
        default:
          return status
      }
    },

    scheduleInterview(id) {
      this.interviewForm.application_id = id
      this.interviewForm.scheduled_date = new Date().toISOString().split('T')[0]
      this.interviewForm.scheduled_time = '09:00'
      this.interviewForm.location = 'Văn phòng công ty'
      this.interviewForm.interview_type = 'in_person'
      this.interviewForm.interviewers = ''
      this.interviewForm.notes = ''

      // Show modal
      const modal = new bootstrap.Modal(document.getElementById('scheduleInterviewModal'))
      modal.show()
    },

    async submitInterviewSchedule() {
      try {
        const { application_id, scheduled_date, scheduled_time, ...rest } = this.interviewForm

        // Combine date and time
        const scheduledDateTime = `${scheduled_date}T${scheduled_time}:00`

        await this.$store.dispatch('recruitment/scheduleInterview', {
          id: application_id,
          data: {
            scheduled_date: scheduledDateTime,
            ...rest
          }
        })

        this.$store.dispatch('app/setSuccess', 'Lên lịch phỏng vấn thành công')

        // Hide modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('scheduleInterviewModal'))
        modal.hide()

        // Refresh data
        this.fetchApplications()
      } catch (error) {
        this.$store.dispatch('app/setError', 'Lên lịch phỏng vấn thất bại')
        console.error('Error scheduling interview:', error)
      }
    }
  }
}
</script>

<style scoped>
th {
  cursor: pointer;
  user-select: none;
}

.table th, .table td {
  vertical-align: middle;
}

.badge {
  font-size: 0.85rem;
  padding: 0.35em 0.65em;
}
</style>
