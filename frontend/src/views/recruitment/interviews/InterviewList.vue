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
              <option value="scheduled">Đã lên lịch</option>
              <option value="completed">Đã hoàn thành</option>
              <option value="cancelled">Đã hủy</option>
            </select>
          </div>
          <div class="col-md-3 mb-3">
            <label for="date_range" class="form-label">Thời gian</label>
            <select id="date_range" v-model="filters.date_range" class="form-select" @change="applyFilters">
              <option value="">Tất cả</option>
              <option value="today">Hôm nay</option>
              <option value="tomorrow">Ngày mai</option>
              <option value="this_week">Tuần này</option>
              <option value="next_week">Tuần sau</option>
              <option value="this_month">Tháng này</option>
            </select>
          </div>
          <div class="col-md-3 mb-3">
            <label for="interview_type" class="form-label">Loại phỏng vấn</label>
            <select id="interview_type" v-model="filters.interview_type" class="form-select" @change="applyFilters">
              <option value="">Tất cả</option>
              <option value="in_person">Trực tiếp</option>
              <option value="phone">Điện thoại</option>
              <option value="video">Video</option>
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

    <!-- Danh sách phỏng vấn -->
    <div class="card">
      <div class="card-body">
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Đang tải...</span>
          </div>
        </div>
        <div v-else-if="interviews.length === 0" class="text-center py-5">
          <p class="text-muted">Không có lịch phỏng vấn nào</p>
        </div>
        <div v-else>
          <div class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th @click="sortBy('application.full_name')">
                    Ứng viên
                    <font-awesome-icon v-if="sortKey === 'application.full_name'" :icon="sortIcon" />
                  </th>
                  <th @click="sortBy('application.job_posting.title')">
                    Vị trí ứng tuyển
                    <font-awesome-icon v-if="sortKey === 'application.job_posting.title'" :icon="sortIcon" />
                  </th>
                  <th @click="sortBy('scheduled_date')">
                    Thời gian
                    <font-awesome-icon v-if="sortKey === 'scheduled_date'" :icon="sortIcon" />
                  </th>
                  <th @click="sortBy('location')">
                    Địa điểm
                    <font-awesome-icon v-if="sortKey === 'location'" :icon="sortIcon" />
                  </th>
                  <th @click="sortBy('interview_type')">
                    Loại phỏng vấn
                    <font-awesome-icon v-if="sortKey === 'interview_type'" :icon="sortIcon" />
                  </th>
                  <th @click="sortBy('interviewers')">
                    Người phỏng vấn
                    <font-awesome-icon v-if="sortKey === 'interviewers'" :icon="sortIcon" />
                  </th>
                  <th @click="sortBy('status')">
                    Trạng thái
                    <font-awesome-icon v-if="sortKey === 'status'" :icon="sortIcon" />
                  </th>
                  <th>Thao tác</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="interview in interviews" :key="interview.id">
                  <td>
                    <router-link :to="`/recruitment/applications/${interview.application_id}`" class="text-decoration-none">
                      {{ interview.application_name }}
                    </router-link>
                  </td>
                  <td>{{ interview.job_title }}</td>
                  <td>{{ formatDateTime(interview.scheduled_date) }}</td>
                  <td>{{ interview.location }}</td>
                  <td>{{ interview.interview_type_display }}</td>
                  <td>{{ interview.interviewers }}</td>
                  <td>
                    <span :class="getStatusBadgeClass(interview.status)">
                      {{ interview.status_display }}
                    </span>
                  </td>
                  <td>
                    <div class="btn-group">
                      <router-link
                        :to="`/recruitment/interviews/${interview.id}`"
                        class="btn btn-sm btn-outline-primary"
                        title="Xem chi tiết"
                      >
                        <font-awesome-icon icon="eye" />
                      </router-link>
                      <button
                        v-if="interview.status === 'scheduled'"
                        class="btn btn-sm btn-outline-success"
                        title="Hoàn thành phỏng vấn"
                        @click="completeInterview(interview.id)"
                      >
                        <font-awesome-icon icon="check" />
                      </button>
                      <button
                        v-if="interview.status === 'scheduled'"
                        class="btn btn-sm btn-outline-danger"
                        title="Hủy phỏng vấn"
                        @click="cancelInterview(interview.id)"
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
              <span class="text-muted">Hiển thị {{ interviews.length }} / {{ totalItems }} lịch phỏng vấn</span>
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

    <!-- Modal hoàn thành phỏng vấn -->
    <div class="modal fade" id="completeInterviewModal" tabindex="-1" aria-labelledby="completeInterviewModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="completeInterviewModalLabel">Hoàn thành phỏng vấn</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitCompleteInterview">
              <div class="mb-3">
                <label for="interview_result" class="form-label">Kết quả</label>
                <select id="interview_result" v-model="completeInterviewForm.result" class="form-select" required>
                  <option value="passed">Đạt</option>
                  <option value="failed">Không đạt</option>
                  <option value="pending">Chưa quyết định</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="interview_feedback" class="form-label">Đánh giá</label>
                <textarea
                  id="interview_feedback"
                  v-model="completeInterviewForm.feedback"
                  class="form-control"
                  rows="5"
                  required
                ></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Hủy</button>
            <button type="button" class="btn btn-primary" @click="submitCompleteInterview">Lưu</button>
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
  name: 'InterviewList',
  data() {
    return {
      filters: {
        status: '',
        date_range: '',
        interview_type: '',
        search: ''
      },
      sortKey: 'scheduled_date',
      sortDirection: 'asc',
      currentPage: 1,
      itemsPerPage: 10,
      totalItems: 0,
      completeInterviewForm: {
        id: null,
        result: 'passed',
        feedback: ''
      }
    }
  },
  computed: {
    ...mapGetters('recruitment', ['interviews', 'loading', 'error']),

    sortIcon() {
      return this.sortDirection === 'asc' ? 'sort-up' : 'sort-down'
    },

    totalPages() {
      return Math.ceil(this.totalItems / this.itemsPerPage)
    }
  },
  created() {
    this.fetchInterviews()
  },
  methods: {
    async fetchInterviews() {
      try {
        const params = {
          page: this.currentPage,
          page_size: this.itemsPerPage,
          ordering: this.getSortParam(),
          ...this.getFilterParams()
        }

        await this.$store.dispatch('recruitment/fetchInterviews', params)

        // In a real app, the total count would come from the API
        this.totalItems = 25 // Dummy value for now
      } catch (error) {
        console.error('Error fetching interviews:', error)
      }
    },

    refreshData() {
      this.fetchInterviews()
    },

    applyFilters() {
      this.currentPage = 1
      this.fetchInterviews()
    },

    getFilterParams() {
      const params = {}

      if (this.filters.status) {
        params.status = this.filters.status
      }

      if (this.filters.date_range) {
        params.date_range = this.filters.date_range
      }

      if (this.filters.interview_type) {
        params.interview_type = this.filters.interview_type
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

      this.fetchInterviews()
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
      this.fetchInterviews()
    },

    formatDateTime(dateTimeString) {
      if (!dateTimeString) return 'N/A'
      const date = new Date(dateTimeString)
      return `${date.toLocaleTimeString('vi-VN', {hour: '2-digit', minute:'2-digit'})} - ${date.toLocaleDateString('vi-VN')}`
    },

    getStatusBadgeClass(status) {
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

    completeInterview(id) {
      this.completeInterviewForm.id = id
      this.completeInterviewForm.result = 'passed'
      this.completeInterviewForm.feedback = ''

      // Show modal
      const modal = new bootstrap.Modal(document.getElementById('completeInterviewModal'))
      modal.show()
    },

    async submitCompleteInterview() {
      try {
        await this.$store.dispatch('recruitment/completeInterview', {
          id: this.completeInterviewForm.id,
          data: {
            result: this.completeInterviewForm.result,
            feedback: this.completeInterviewForm.feedback
          }
        })

        this.$store.dispatch('app/setSuccess', 'Hoàn thành phỏng vấn thành công')

        // Hide modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('completeInterviewModal'))
        modal.hide()

        // Refresh data
        this.fetchInterviews()
      } catch (error) {
        this.$store.dispatch('app/setError', 'Hoàn thành phỏng vấn thất bại')
        console.error('Error completing interview:', error)
      }
    },

    async cancelInterview(id) {
      try {
        if (confirm('Bạn có chắc chắn muốn hủy phỏng vấn này?')) {
          await this.$store.dispatch('recruitment/cancelInterview', id)
          this.$store.dispatch('app/setSuccess', 'Hủy phỏng vấn thành công')
          this.fetchInterviews()
        }
      } catch (error) {
        this.$store.dispatch('app/setError', 'Hủy phỏng vấn thất bại')
        console.error('Error cancelling interview:', error)
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
