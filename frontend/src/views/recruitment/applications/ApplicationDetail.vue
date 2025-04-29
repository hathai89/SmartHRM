<template>
  <div class="container-fluid">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Đang tải...</span>
      </div>
    </div>
    <div v-else-if="!application" class="text-center py-5">
      <div class="alert alert-danger">
        <h4 class="alert-heading">Không tìm thấy đơn ứng tuyển</h4>
        <p>Đơn ứng tuyển này không tồn tại hoặc đã bị xóa.</p>
        <hr />
        <router-link to="/recruitment/applications" class="btn btn-primary">
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
              <h1 class="h3 mb-2">{{ application.full_name }}</h1>
              <p class="text-muted mb-0">
                Ứng tuyển vị trí: {{ application.job_title }}
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
                  <li v-if="application.status === 'new'">
                    <a class="dropdown-item" href="#" @click.prevent="changeStatus('screening')">
                      <font-awesome-icon icon="clipboard-check" class="me-2" />
                      Bắt đầu xem xét
                    </a>
                  </li>
                  <li v-if="application.status === 'screening'">
                    <a class="dropdown-item" href="#" @click.prevent="scheduleInterview">
                      <font-awesome-icon icon="calendar-plus" class="me-2" />
                      Lên lịch phỏng vấn
                    </a>
                  </li>
                  <li v-if="['screening', 'interview_scheduled'].includes(application.status)">
                    <a class="dropdown-item" href="#" @click.prevent="changeStatus('offered')">
                      <font-awesome-icon icon="check" class="me-2" />
                      Đề nghị
                    </a>
                  </li>
                  <li v-if="application.status === 'offered'">
                    <a class="dropdown-item" href="#" @click.prevent="changeStatus('hired')">
                      <font-awesome-icon icon="user-plus" class="me-2" />
                      Tuyển dụng
                    </a>
                  </li>
                  <li v-if="!['rejected', 'hired'].includes(application.status)">
                    <a class="dropdown-item" href="#" @click.prevent="changeStatus('rejected')">
                      <font-awesome-icon icon="times" class="me-2" />
                      Từ chối
                    </a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="#" @click.prevent="downloadResume">
                      <font-awesome-icon icon="download" class="me-2" />
                      Tải CV
                    </a>
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
              <span :class="getStatusBadgeClass(application.status)">
                {{ application.status_display }}
              </span>
            </div>
            <div class="col-md-3 col-6 py-2">
              <div class="text-muted small">Ngày nộp</div>
              <span>{{ formatDate(application.created_at) }}</span>
            </div>
            <div class="col-md-3 col-6 py-2">
              <div class="text-muted small">Nguồn</div>
              <span>{{ application.source || 'Trực tiếp' }}</span>
            </div>
            <div class="col-md-3 col-6 py-2">
              <div class="text-muted small">Đánh giá</div>
              <div class="rating">
                <span v-for="i in 5" :key="i" :class="{ 'text-warning': i <= application.rating }">
                  <font-awesome-icon icon="star" />
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <ul class="nav nav-tabs mb-4">
        <li class="nav-item">
          <a
            class="nav-link"
            :class="{ active: activeTab === 'profile' }"
            href="#"
            @click.prevent="activeTab = 'profile'"
          >
            <font-awesome-icon icon="user" class="me-1" />
            Hồ sơ
          </a>
        </li>
        <li class="nav-item">
          <a
            class="nav-link"
            :class="{ active: activeTab === 'interviews' }"
            href="#"
            @click.prevent="activeTab = 'interviews'"
          >
            <font-awesome-icon icon="calendar-check" class="me-1" />
            Phỏng vấn
            <span v-if="interviews.length > 0" class="badge bg-info ms-1">{{ interviews.length }}</span>
          </a>
        </li>
        <li class="nav-item">
          <a
            class="nav-link"
            :class="{ active: activeTab === 'notes' }"
            href="#"
            @click.prevent="activeTab = 'notes'"
          >
            <font-awesome-icon icon="sticky-note" class="me-1" />
            Ghi chú
            <span v-if="notes.length > 0" class="badge bg-info ms-1">{{ notes.length }}</span>
          </a>
        </li>
      </ul>

      <!-- Tab content -->
      <div v-if="activeTab === 'profile'">
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
                    <h6>Thông tin cá nhân</h6>
                    <ul class="list-group list-group-flush">
                      <li class="list-group-item d-flex justify-content-between align-items-center">
                        <span>Họ tên</span>
                        <span>{{ application.full_name }}</span>
                      </li>
                      <li class="list-group-item d-flex justify-content-between align-items-center">
                        <span>Email</span>
                        <span>{{ application.email }}</span>
                      </li>
                      <li class="list-group-item d-flex justify-content-between align-items-center">
                        <span>Số điện thoại</span>
                        <span>{{ application.phone }}</span>
                      </li>
                      <li class="list-group-item d-flex justify-content-between align-items-center">
                        <span>Địa chỉ</span>
                        <span>{{ application.address }}</span>
                      </li>
                      <li class="list-group-item d-flex justify-content-between align-items-center">
                        <span>Ngày sinh</span>
                        <span>{{ formatDate(application.date_of_birth) }}</span>
                      </li>
                    </ul>
                  </div>
                  <div class="col-md-6">
                    <h6>Thông tin ứng tuyển</h6>
                    <ul class="list-group list-group-flush">
                      <li class="list-group-item d-flex justify-content-between align-items-center">
                        <span>Vị trí ứng tuyển</span>
                        <span>{{ application.job_title }}</span>
                      </li>
                      <li class="list-group-item d-flex justify-content-between align-items-center">
                        <span>Kinh nghiệm</span>
                        <span>{{ application.experience_years }} năm</span>
                      </li>
                      <li class="list-group-item d-flex justify-content-between align-items-center">
                        <span>Học vấn</span>
                        <span>{{ application.education }}</span>
                      </li>
                      <li class="list-group-item d-flex justify-content-between align-items-center">
                        <span>Mức lương mong muốn</span>
                        <span>{{ formatSalary(application.expected_salary) }}</span>
                      </li>
                      <li class="list-group-item d-flex justify-content-between align-items-center">
                        <span>Ngày có thể bắt đầu</span>
                        <span>{{ formatDate(application.available_start_date) }}</span>
                      </li>
                    </ul>
                  </div>
                </div>

                <h6>Kỹ năng</h6>
                <div class="mb-4">
                  <span
                    v-for="skill in application.skills"
                    :key="skill"
                    class="badge bg-light text-dark me-2 mb-2"
                  >
                    {{ skill }}
                  </span>
                </div>

                <h6>Giới thiệu bản thân</h6>
                <div class="mb-4">
                  <p>{{ application.cover_letter }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-4">
            <!-- Thông tin CV -->
            <div class="card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">CV</h5>
              </div>
              <div class="card-body text-center">
                <div v-if="application.resume">
                  <div class="mb-3">
                    <font-awesome-icon icon="file-pdf" class="text-danger fa-4x" />
                  </div>
                  <a href="#" class="btn btn-primary" @click.prevent="downloadResume">
                    <font-awesome-icon icon="download" class="me-1" />
                    Tải CV
                  </a>
                </div>
                <div v-else class="text-muted">
                  <p>Không có CV</p>
                </div>
              </div>
            </div>

            <!-- Đánh giá -->
            <div class="card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">Đánh giá</h5>
              </div>
              <div class="card-body">
                <div class="mb-3">
                  <label class="form-label">Đánh giá tổng quan</label>
                  <div class="rating-input">
                    <span
                      v-for="i in 5"
                      :key="i"
                      :class="{ 'text-warning': i <= rating }"
                      @click="setRating(i)"
                      style="cursor: pointer; font-size: 1.5rem;"
                    >
                      <font-awesome-icon icon="star" />
                    </span>
                  </div>
                </div>
                <div class="mb-3">
                  <label for="rating_notes" class="form-label">Ghi chú đánh giá</label>
                  <textarea
                    id="rating_notes"
                    v-model="ratingNotes"
                    class="form-control"
                    rows="3"
                  ></textarea>
                </div>
                <button class="btn btn-primary w-100" @click="saveRating">
                  <font-awesome-icon icon="save" class="me-1" />
                  Lưu đánh giá
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="activeTab === 'interviews'">
        <!-- Danh sách phỏng vấn -->
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="card-title mb-0">Lịch phỏng vấn</h5>
            <button class="btn btn-primary btn-sm" @click="scheduleInterview">
              <font-awesome-icon icon="plus" class="me-1" />
              Lên lịch phỏng vấn
            </button>
          </div>
          <div class="card-body">
            <div v-if="loadingInterviews" class="text-center py-3">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Đang tải...</span>
              </div>
            </div>
            <div v-else-if="interviews.length === 0" class="text-center py-3">
              <p class="text-muted">Chưa có lịch phỏng vấn nào</p>
              <button class="btn btn-primary" @click="scheduleInterview">
                <font-awesome-icon icon="plus" class="me-1" />
                Lên lịch phỏng vấn
              </button>
            </div>
            <div v-else>
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Thời gian</th>
                      <th>Địa điểm</th>
                      <th>Loại phỏng vấn</th>
                      <th>Người phỏng vấn</th>
                      <th>Trạng thái</th>
                      <th>Thao tác</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="interview in interviews" :key="interview.id">
                      <td>{{ formatDateTime(interview.scheduled_date) }}</td>
                      <td>{{ interview.location }}</td>
                      <td>{{ interview.interview_type_display }}</td>
                      <td>{{ interview.interviewers }}</td>
                      <td>
                        <span :class="getInterviewStatusBadgeClass(interview.status)">
                          {{ interview.status_display }}
                        </span>
                      </td>
                      <td>
                        <div class="btn-group">
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
                          <button
                            class="btn btn-sm btn-outline-info"
                            title="Xem chi tiết"
                            @click="viewInterviewDetails(interview)"
                          >
                            <font-awesome-icon icon="eye" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="activeTab === 'notes'">
        <!-- Ghi chú -->
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="card-title mb-0">Ghi chú</h5>
            <button class="btn btn-primary btn-sm" @click="addNote">
              <font-awesome-icon icon="plus" class="me-1" />
              Thêm ghi chú
            </button>
          </div>
          <div class="card-body">
            <div v-if="loadingNotes" class="text-center py-3">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Đang tải...</span>
              </div>
            </div>
            <div v-else-if="notes.length === 0" class="text-center py-3">
              <p class="text-muted">Chưa có ghi chú nào</p>
              <button class="btn btn-primary" @click="addNote">
                <font-awesome-icon icon="plus" class="me-1" />
                Thêm ghi chú
              </button>
            </div>
            <div v-else>
              <div class="timeline">
                <div v-for="note in notes" :key="note.id" class="timeline-item">
                  <div class="timeline-badge">
                    <font-awesome-icon icon="sticky-note" />
                  </div>
                  <div class="timeline-content">
                    <div class="d-flex justify-content-between">
                      <h6>{{ note.created_by }}</h6>
                      <small class="text-muted">{{ formatDateTime(note.created_at) }}</small>
                    </div>
                    <p>{{ note.content }}</p>
                  </div>
                </div>
              </div>
            </div>
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

    <!-- Modal thêm ghi chú -->
    <div class="modal fade" id="addNoteModal" tabindex="-1" aria-labelledby="addNoteModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="addNoteModalLabel">Thêm ghi chú</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitNote">
              <div class="mb-3">
                <label for="note_content" class="form-label">Nội dung</label>
                <textarea
                  id="note_content"
                  v-model="noteForm.content"
                  class="form-control"
                  rows="5"
                  required
                ></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Hủy</button>
            <button type="button" class="btn btn-primary" @click="submitNote">Lưu</button>
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
  name: 'ApplicationDetail',
  data() {
    return {
      activeTab: 'profile',
      loadingInterviews: false,
      loadingNotes: false,
      interviews: [],
      notes: [],
      rating: 0,
      ratingNotes: '',
      interviewForm: {
        scheduled_date: '',
        scheduled_time: '',
        location: '',
        interview_type: 'in_person',
        interviewers: '',
        notes: ''
      },
      completeInterviewForm: {
        id: null,
        result: 'passed',
        feedback: ''
      },
      noteForm: {
        content: ''
      }
    }
  },
  computed: {
    ...mapGetters('recruitment', ['application', 'loading', 'error']),

    applicationId() {
      return this.$route.params.id
    }
  },
  created() {
    this.fetchApplication()
  },
  methods: {
    async fetchApplication() {
      try {
        await this.$store.dispatch('recruitment/fetchApplication', this.applicationId)

        if (this.application) {
          this.rating = this.application.rating || 0
          this.ratingNotes = this.application.rating_notes || ''
          this.fetchInterviews()
          this.fetchNotes()
        }
      } catch (error) {
        console.error('Error fetching application:', error)
      }
    },

    async fetchInterviews() {
      try {
        this.loadingInterviews = true
        // In a real app, this would be an API call
        // For now, we'll use dummy data
        this.interviews = [
          {
            id: 1,
            scheduled_date: new Date().toISOString(),
            location: 'Văn phòng công ty',
            interview_type: 'in_person',
            interview_type_display: 'Trực tiếp',
            interviewers: 'Nguyễn Văn A, Trần Thị B',
            status: 'scheduled',
            status_display: 'Đã lên lịch',
            notes: 'Phỏng vấn vòng 1'
          }
        ]
      } catch (error) {
        console.error('Error fetching interviews:', error)
      } finally {
        this.loadingInterviews = false
      }
    },

    async fetchNotes() {
      try {
        this.loadingNotes = true
        // In a real app, this would be an API call
        // For now, we'll use dummy data
        this.notes = [
          {
            id: 1,
            content: 'Ứng viên có kinh nghiệm tốt và phù hợp với vị trí.',
            created_at: new Date().toISOString(),
            created_by: 'Admin'
          }
        ]
      } catch (error) {
        console.error('Error fetching notes:', error)
      } finally {
        this.loadingNotes = false
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

    formatSalary(salary) {
      if (!salary) return 'Thỏa thuận'
      return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(salary)
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

    getInterviewStatusBadgeClass(status) {
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

    async changeStatus(status) {
      try {
        if (confirm(`Bạn có chắc chắn muốn chuyển trạng thái thành "${this.getStatusDisplay(status)}"?`)) {
          await this.$store.dispatch('recruitment/updateApplicationStatus', {
            id: this.applicationId,
            status,
            notes: `Chuyển trạng thái thành ${this.getStatusDisplay(status)}`
          })
          this.$store.dispatch('app/setSuccess', 'Cập nhật trạng thái thành công')
          this.fetchApplication()
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

    setRating(value) {
      this.rating = value
    },

    async saveRating() {
      try {
        // In a real app, this would be an API call
        // For now, we'll just show a success message
        this.$store.dispatch('app/setSuccess', 'Lưu đánh giá thành công')
      } catch (error) {
        this.$store.dispatch('app/setError', 'Lưu đánh giá thất bại')
        console.error('Error saving rating:', error)
      }
    },

    downloadResume() {
      // In a real app, this would download the resume
      // For now, we'll just show a message
      this.$store.dispatch('app/setSuccess', 'Tải CV thành công')
    },

    scheduleInterview() {
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
        // In a real app, this would be an API call
        // For now, we'll just show a success message and update the UI
        this.$store.dispatch('app/setSuccess', 'Lên lịch phỏng vấn thành công')

        // Hide modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('scheduleInterviewModal'))
        modal.hide()

        // Add the new interview to the list
        const newInterview = {
          id: Date.now(), // Use timestamp as ID for now
          scheduled_date: `${this.interviewForm.scheduled_date}T${this.interviewForm.scheduled_time}:00`,
          location: this.interviewForm.location,
          interview_type: this.interviewForm.interview_type,
          interview_type_display: this.getInterviewTypeDisplay(this.interviewForm.interview_type),
          interviewers: this.interviewForm.interviewers,
          status: 'scheduled',
          status_display: 'Đã lên lịch',
          notes: this.interviewForm.notes
        }

        this.interviews.push(newInterview)

        // Update application status
        await this.$store.dispatch('recruitment/updateApplicationStatus', {
          id: this.applicationId,
          status: 'interview_scheduled',
          notes: 'Đã lên lịch phỏng vấn'
        })

        // Refresh application data
        this.fetchApplication()
      } catch (error) {
        this.$store.dispatch('app/setError', 'Lên lịch phỏng vấn thất bại')
        console.error('Error scheduling interview:', error)
      }
    },

    getInterviewTypeDisplay(type) {
      switch (type) {
        case 'in_person':
          return 'Trực tiếp'
        case 'phone':
          return 'Điện thoại'
        case 'video':
          return 'Video'
        default:
          return type
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
        // In a real app, this would be an API call
        // For now, we'll just show a success message and update the UI
        this.$store.dispatch('app/setSuccess', 'Hoàn thành phỏng vấn thành công')

        // Hide modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('completeInterviewModal'))
        modal.hide()

        // Update the interview in the list
        const index = this.interviews.findIndex(i => i.id === this.completeInterviewForm.id)
        if (index !== -1) {
          this.interviews[index].status = 'completed'
          this.interviews[index].status_display = 'Đã hoàn thành'
          this.interviews[index].result = this.completeInterviewForm.result
          this.interviews[index].feedback = this.completeInterviewForm.feedback
        }

        // Add a note about the interview
        const resultText = this.completeInterviewForm.result === 'passed' ? 'Đạt' :
                          this.completeInterviewForm.result === 'failed' ? 'Không đạt' : 'Chưa quyết định'

        this.notes.push({
          id: Date.now(),
          content: `Kết quả phỏng vấn: ${resultText}. ${this.completeInterviewForm.feedback}`,
          created_at: new Date().toISOString(),
          created_by: 'Admin'
        })
      } catch (error) {
        this.$store.dispatch('app/setError', 'Hoàn thành phỏng vấn thất bại')
        console.error('Error completing interview:', error)
      }
    },

    async cancelInterview(id) {
      try {
        if (confirm('Bạn có chắc chắn muốn hủy phỏng vấn này?')) {
          // In a real app, this would be an API call
          // For now, we'll just show a success message and update the UI
          this.$store.dispatch('app/setSuccess', 'Hủy phỏng vấn thành công')

          // Update the interview in the list
          const index = this.interviews.findIndex(i => i.id === id)
          if (index !== -1) {
            this.interviews[index].status = 'cancelled'
            this.interviews[index].status_display = 'Đã hủy'
          }
        }
      } catch (error) {
        this.$store.dispatch('app/setError', 'Hủy phỏng vấn thất bại')
        console.error('Error cancelling interview:', error)
      }
    },

    viewInterviewDetails(interview) {
      // In a real app, this would show a modal with interview details
      // For now, we'll just show an alert
      alert(`Chi tiết phỏng vấn:\n\nThời gian: ${this.formatDateTime(interview.scheduled_date)}\nĐịa điểm: ${interview.location}\nLoại phỏng vấn: ${interview.interview_type_display}\nNgười phỏng vấn: ${interview.interviewers}\nGhi chú: ${interview.notes}`)
    },

    addNote() {
      this.noteForm.content = ''

      // Show modal
      const modal = new bootstrap.Modal(document.getElementById('addNoteModal'))
      modal.show()
    },

    async submitNote() {
      try {
        if (!this.noteForm.content.trim()) {
          this.$store.dispatch('app/setError', 'Vui lòng nhập nội dung ghi chú')
          return
        }

        // In a real app, this would be an API call
        // For now, we'll just show a success message and update the UI
        this.$store.dispatch('app/setSuccess', 'Thêm ghi chú thành công')

        // Hide modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('addNoteModal'))
        modal.hide()

        // Add the new note to the list
        this.notes.push({
          id: Date.now(),
          content: this.noteForm.content,
          created_at: new Date().toISOString(),
          created_by: 'Admin'
        })
      } catch (error) {
        this.$store.dispatch('app/setError', 'Thêm ghi chú thất bại')
        console.error('Error adding note:', error)
      }
    }
  }
}
</script>

<style scoped>
.nav-tabs .nav-link {
  color: #6c757d;
}

.nav-tabs .nav-link.active {
  color: #0d6efd;
  font-weight: 500;
}

.badge {
  font-size: 0.85rem;
  padding: 0.35em 0.65em;
}

.list-group-item {
  padding: 0.75rem 1.25rem;
}

.rating {
  font-size: 1.25rem;
  color: #e0e0e0;
}

.rating .text-warning {
  color: #ffc107 !important;
}

.timeline {
  position: relative;
  padding: 20px 0;
}

.timeline-item {
  position: relative;
  padding-left: 40px;
  margin-bottom: 20px;
}

.timeline-badge {
  position: absolute;
  left: 0;
  top: 0;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #dee2e6;
}

.timeline-content {
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 4px;
  border-left: 3px solid #0d6efd;
}
</style>
