<template>
  <div class="container-fluid">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Đang tải...</span>
      </div>
    </div>
    <div v-else-if="!interview" class="text-center py-5">
      <div class="alert alert-danger">
        <h4 class="alert-heading">Không tìm thấy lịch phỏng vấn</h4>
        <p>Lịch phỏng vấn này không tồn tại hoặc đã bị xóa.</p>
        <hr />
        <router-link to="/recruitment/interviews" class="btn btn-primary">
          Quay lại danh sách
        </router-link>
      </div>
    </div>
    <div v-else>
      <!-- Header -->
      <div class="card mb-4">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h1 class="h3 mb-2">Phỏng vấn: {{ interview.application_name }}</h1>
              <p class="text-muted mb-0">
                Vị trí: {{ interview.job_title }}
              </p>
            </div>
            <div class="d-flex">
              <div class="dropdown">
                <button
                  class="btn btn-outline-secondary dropdown-toggle"
                  type="button"
                  id="dropdownMenuButton"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  <font-awesome-icon icon="ellipsis-v" />
                </button>
                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton">
                  <li v-if="interview.status === 'scheduled'">
                    <a class="dropdown-item" href="#" @click.prevent="completeInterview">
                      <font-awesome-icon icon="check" class="me-2" />
                      Hoàn thành phỏng vấn
                    </a>
                  </li>
                  <li v-if="interview.status === 'scheduled'">
                    <a class="dropdown-item" href="#" @click.prevent="rescheduleInterview">
                      <font-awesome-icon icon="calendar-alt" class="me-2" />
                      Đổi lịch phỏng vấn
                    </a>
                  </li>
                  <li v-if="interview.status === 'scheduled'">
                    <a class="dropdown-item" href="#" @click.prevent="cancelInterview">
                      <font-awesome-icon icon="times" class="me-2" />
                      Hủy phỏng vấn
                    </a>
                  </li>
                  <li>
                    <router-link :to="`/recruitment/applications/${interview.application_id}`" class="dropdown-item">
                      <font-awesome-icon icon="user" class="me-2" />
                      Xem hồ sơ ứng viên
                    </router-link>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        <div class="card-footer bg-transparent">
          <div class="row text-center">
            <div class="col-md-3 col-6 py-2">
              <div class="text-muted small">Trạng thái</div>
              <span :class="getStatusBadgeClass(interview.status)">
                {{ interview.status_display }}
              </span>
            </div>
            <div class="col-md-3 col-6 py-2">
              <div class="text-muted small">Thời gian</div>
              <span>{{ formatDateTime(interview.scheduled_date) }}</span>
            </div>
            <div class="col-md-3 col-6 py-2">
              <div class="text-muted small">Loại phỏng vấn</div>
              <span>{{ interview.interview_type_display }}</span>
            </div>
            <div class="col-md-3 col-6 py-2">
              <div class="text-muted small">Địa điểm</div>
              <span>{{ interview.location }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-md-8">
          <!-- Thông tin chi tiết -->
          <div class="card mb-4">
            <div class="card-header">
              <h5 class="card-title mb-0">Thông tin chi tiết</h5>
            </div>
            <div class="card-body">
              <div class="row mb-4">
                <div class="col-md-6">
                  <h6>Thông tin ứng viên</h6>
                  <ul class="list-group list-group-flush">
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                      <span>Họ tên</span>
                      <span>{{ interview.application_name }}</span>
                    </li>
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                      <span>Email</span>
                      <span>{{ interview.application_email }}</span>
                    </li>
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                      <span>Số điện thoại</span>
                      <span>{{ interview.application_phone }}</span>
                    </li>
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                      <span>Vị trí ứng tuyển</span>
                      <span>{{ interview.job_title }}</span>
                    </li>
                  </ul>
                </div>
                <div class="col-md-6">
                  <h6>Thông tin phỏng vấn</h6>
                  <ul class="list-group list-group-flush">
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                      <span>Thời gian</span>
                      <span>{{ formatDateTime(interview.scheduled_date) }}</span>
                    </li>
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                      <span>Địa điểm</span>
                      <span>{{ interview.location }}</span>
                    </li>
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                      <span>Loại phỏng vấn</span>
                      <span>{{ interview.interview_type_display }}</span>
                    </li>
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                      <span>Người phỏng vấn</span>
                      <span>{{ interview.interviewers }}</span>
                    </li>
                  </ul>
                </div>
              </div>

              <h6>Ghi chú</h6>
              <div class="mb-4">
                <p>{{ interview.notes || 'Không có ghi chú' }}</p>
              </div>

              <div v-if="interview.status === 'completed'">
                <h6>Kết quả phỏng vấn</h6>
                <div class="mb-4">
                  <div class="alert" :class="getResultAlertClass(interview.result)">
                    <h6 class="alert-heading">{{ getResultText(interview.result) }}</h6>
                    <p>{{ interview.feedback || 'Không có đánh giá' }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <!-- Thông tin hồ sơ -->
          <div class="card mb-4">
            <div class="card-header">
              <h5 class="card-title mb-0">Hồ sơ ứng viên</h5>
            </div>
            <div class="card-body">
              <div class="text-center mb-3">
                <font-awesome-icon icon="user-circle" class="fa-4x text-primary" />
              </div>
              <div class="d-grid gap-2">
                <router-link :to="`/recruitment/applications/${interview.application_id}`" class="btn btn-primary">
                  <font-awesome-icon icon="user" class="me-1" />
                  Xem hồ sơ ứng viên
                </router-link>
                <a href="#" class="btn btn-outline-secondary" @click.prevent="downloadResume">
                  <font-awesome-icon icon="download" class="me-1" />
                  Tải CV
                </a>
              </div>
            </div>
          </div>

          <!-- Thao tác -->
          <div class="card mb-4">
            <div class="card-header">
              <h5 class="card-title mb-0">Thao tác</h5>
            </div>
            <div class="card-body">
              <div class="d-grid gap-2">
                <button
                  v-if="interview.status === 'scheduled'"
                  class="btn btn-success"
                  @click="completeInterview"
                >
                  <font-awesome-icon icon="check" class="me-1" />
                  Hoàn thành phỏng vấn
                </button>
                <button
                  v-if="interview.status === 'scheduled'"
                  class="btn btn-warning"
                  @click="rescheduleInterview"
                >
                  <font-awesome-icon icon="calendar-alt" class="me-1" />
                  Đổi lịch phỏng vấn
                </button>
                <button
                  v-if="interview.status === 'scheduled'"
                  class="btn btn-danger"
                  @click="cancelInterview"
                >
                  <font-awesome-icon icon="times" class="me-1" />
                  Hủy phỏng vấn
                </button>
              </div>
            </div>
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

    <!-- Modal đổi lịch phỏng vấn -->
    <div class="modal fade" id="rescheduleInterviewModal" tabindex="-1" aria-labelledby="rescheduleInterviewModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="rescheduleInterviewModalLabel">Đổi lịch phỏng vấn</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitRescheduleInterview">
              <div class="mb-3">
                <label for="scheduled_date" class="form-label">Ngày phỏng vấn</label>
                <input
                  id="scheduled_date"
                  v-model="rescheduleForm.scheduled_date"
                  type="date"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="scheduled_time" class="form-label">Giờ phỏng vấn</label>
                <input
                  id="scheduled_time"
                  v-model="rescheduleForm.scheduled_time"
                  type="time"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="location" class="form-label">Địa điểm</label>
                <input
                  id="location"
                  v-model="rescheduleForm.location"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="interview_type" class="form-label">Loại phỏng vấn</label>
                <select id="interview_type" v-model="rescheduleForm.interview_type" class="form-select" required>
                  <option value="in_person">Trực tiếp</option>
                  <option value="phone">Điện thoại</option>
                  <option value="video">Video</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="interviewers" class="form-label">Người phỏng vấn</label>
                <input
                  id="interviewers"
                  v-model="rescheduleForm.interviewers"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="notes" class="form-label">Ghi chú</label>
                <textarea
                  id="notes"
                  v-model="rescheduleForm.notes"
                  class="form-control"
                  rows="3"
                ></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Hủy</button>
            <button type="button" class="btn btn-primary" @click="submitRescheduleInterview">Lưu</button>
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
  name: 'InterviewDetail',
  data() {
    return {
      completeInterviewForm: {
        result: 'passed',
        feedback: ''
      },
      rescheduleForm: {
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
    ...mapGetters('recruitment', ['interview', 'loading', 'error']),

    interviewId() {
      return this.$route.params.id
    }
  },
  created() {
    this.fetchInterview()
  },
  methods: {
    async fetchInterview() {
      try {
        await this.$store.dispatch('recruitment/fetchInterview', this.interviewId)

        if (this.interview) {
          // Initialize reschedule form with current values
          const scheduledDate = new Date(this.interview.scheduled_date)
          this.rescheduleForm.scheduled_date = scheduledDate.toISOString().split('T')[0]
          this.rescheduleForm.scheduled_time = scheduledDate.toTimeString().slice(0, 5)
          this.rescheduleForm.location = this.interview.location
          this.rescheduleForm.interview_type = this.interview.interview_type
          this.rescheduleForm.interviewers = this.interview.interviewers
          this.rescheduleForm.notes = this.interview.notes
        }
      } catch (error) {
        console.error('Error fetching interview:', error)
      }
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

    getResultAlertClass(result) {
      switch (result) {
        case 'passed':
          return 'alert-success'
        case 'failed':
          return 'alert-danger'
        case 'pending':
          return 'alert-warning'
        default:
          return 'alert-secondary'
      }
    },

    getResultText(result) {
      switch (result) {
        case 'passed':
          return 'Đạt'
        case 'failed':
          return 'Không đạt'
        case 'pending':
          return 'Chưa quyết định'
        default:
          return result
      }
    },

    completeInterview() {
      this.completeInterviewForm.result = 'passed'
      this.completeInterviewForm.feedback = ''

      // Show modal
      const modal = new bootstrap.Modal(document.getElementById('completeInterviewModal'))
      modal.show()
    },

    async submitCompleteInterview() {
      try {
        await this.$store.dispatch('recruitment/completeInterview', {
          id: this.interviewId,
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
        this.fetchInterview()
      } catch (error) {
        this.$store.dispatch('app/setError', 'Hoàn thành phỏng vấn thất bại')
        console.error('Error completing interview:', error)
      }
    },

    rescheduleInterview() {
      // Show modal
      const modal = new bootstrap.Modal(document.getElementById('rescheduleInterviewModal'))
      modal.show()
    },

    async submitRescheduleInterview() {
      try {
        const { scheduled_date, scheduled_time, ...rest } = this.rescheduleForm

        // Combine date and time
        const scheduledDateTime = `${scheduled_date}T${scheduled_time}:00`

        await this.$store.dispatch('recruitment/updateInterview', {
          id: this.interviewId,
          data: {
            scheduled_date: scheduledDateTime,
            ...rest
          }
        })

        this.$store.dispatch('app/setSuccess', 'Đổi lịch phỏng vấn thành công')

        // Hide modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('rescheduleInterviewModal'))
        modal.hide()

        // Refresh data
        this.fetchInterview()
      } catch (error) {
        this.$store.dispatch('app/setError', 'Đổi lịch phỏng vấn thất bại')
        console.error('Error rescheduling interview:', error)
      }
    },

    async cancelInterview() {
      try {
        if (confirm('Bạn có chắc chắn muốn hủy phỏng vấn này?')) {
          await this.$store.dispatch('recruitment/cancelInterview', this.interviewId)
          this.$store.dispatch('app/setSuccess', 'Hủy phỏng vấn thành công')
          this.fetchInterview()
        }
      } catch (error) {
        this.$store.dispatch('app/setError', 'Hủy phỏng vấn thất bại')
        console.error('Error cancelling interview:', error)
      }
    },

    downloadResume() {
      // In a real app, this would download the resume
      // For now, we'll just show a message
      this.$store.dispatch('app/setSuccess', 'Tải CV thành công')
    }
  }
}
</script>

<style scoped>
.badge {
  font-size: 0.85rem;
  padding: 0.35em 0.65em;
}

.list-group-item {
  padding: 0.75rem 1.25rem;
}
</style>
