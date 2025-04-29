<template>
  <div class="container-fluid">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Đang tải...</span>
      </div>
    </div>
    <div v-else-if="!jobPosting" class="text-center py-5">
      <div class="alert alert-danger">
        <h4 class="alert-heading">Không tìm thấy tin tuyển dụng</h4>
        <p>Tin tuyển dụng này không tồn tại hoặc đã bị xóa.</p>
        <hr />
        <router-link to="/recruitment/job-postings" class="btn btn-primary">
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
              <h1 class="h3 mb-2">{{ jobPosting.title }}</h1>
              <p class="text-muted mb-0">
                {{ jobPosting.department?.name || jobPosting.factory?.name }}
                <span v-if="jobPosting.division?.name" class="ms-1">
                  &raquo; {{ jobPosting.division.name }}
                </span>
                <span v-if="jobPosting.team?.name" class="ms-1">
                  &raquo; {{ jobPosting.team.name }}
                </span>
                <span v-if="jobPosting.job_code" class="ms-2">
                  <font-awesome-icon icon="hashtag" />
                  {{ jobPosting.job_code }}
                </span>
              </p>
            </div>
            <div class="d-flex">
              <router-link
                :to="`/recruitment/job-postings/${jobPosting.id}/edit`"
                class="btn btn-outline-primary me-2"
              >
                <font-awesome-icon icon="edit" class="me-1" />
                Chỉnh sửa
              </router-link>
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
                  <li v-if="jobPosting.status === 'draft'">
                    <a class="dropdown-item" href="#" @click.prevent="publishJobPosting">
                      <font-awesome-icon icon="check" class="me-2" />
                      Đăng tin
                    </a>
                  </li>
                  <li v-if="jobPosting.status === 'published'">
                    <a class="dropdown-item" href="#" @click.prevent="closeJobPosting">
                      <font-awesome-icon icon="times" class="me-2" />
                      Đóng tin
                    </a>
                  </li>
                  <li v-if="jobPosting.status !== 'cancelled'">
                    <a class="dropdown-item" href="#" @click.prevent="cancelJobPosting">
                      <font-awesome-icon icon="ban" class="me-2" />
                      Hủy tin
                    </a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="#" @click.prevent="previewJobPosting">
                      <font-awesome-icon icon="eye" class="me-2" />
                      Xem trước
                    </a>
                  </li>
                  <li>
                    <router-link
                      :to="`/recruitment/applications?job_posting_id=${jobPosting.id}`"
                      class="dropdown-item"
                    >
                      <font-awesome-icon icon="users" class="me-2" />
                      Xem đơn ứng tuyển
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
              <span :class="getStatusBadgeClass(jobPosting.status)">
                {{ jobPosting.status_display }}
              </span>
            </div>
            <div class="col-md-3 col-6 py-2">
              <div class="text-muted small">Số lượng cần tuyển</div>
              <span class="fw-bold">{{ jobPosting.positions }}</span>
            </div>
            <div class="col-md-3 col-6 py-2">
              <div class="text-muted small">Đơn ứng tuyển</div>
              <router-link
                :to="`/recruitment/applications?job_posting_id=${jobPosting.id}`"
                class="badge bg-info text-decoration-none"
              >
                {{ jobPosting.applications_count }}
              </router-link>
            </div>
            <div class="col-md-3 col-6 py-2">
              <div class="text-muted small">Hạn nộp hồ sơ</div>
              <span
                :class="{
                  'text-danger': isExpired(jobPosting.closing_date),
                  'text-success': !isExpired(jobPosting.closing_date)
                }"
              >
                {{ formatDate(jobPosting.closing_date) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <ul class="nav nav-tabs mb-4">
        <li class="nav-item">
          <a
            class="nav-link"
            :class="{ active: activeTab === 'details' }"
            href="#"
            @click.prevent="activeTab = 'details'"
          >
            <font-awesome-icon icon="info-circle" class="me-1" />
            Chi tiết
          </a>
        </li>
        <li class="nav-item">
          <a
            class="nav-link"
            :class="{ active: activeTab === 'applications' }"
            href="#"
            @click.prevent="activeTab = 'applications'"
          >
            <font-awesome-icon icon="users" class="me-1" />
            Đơn ứng tuyển
            <span class="badge bg-info ms-1">{{ jobPosting.applications_count }}</span>
          </a>
        </li>
      </ul>

      <!-- Tab content -->
      <div v-if="activeTab === 'details'">
        <div class="row">
          <div class="col-md-8">
            <!-- Thông tin chi tiết -->
            <div class="card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">Thông tin chi tiết</h5>
              </div>
              <div class="card-body">
                <h5>Mô tả công việc</h5>
                <div class="mb-4" v-html="jobPosting.description"></div>

                <h5>Yêu cầu ứng viên</h5>
                <div class="mb-4" v-html="jobPosting.requirements"></div>

                <h5>Quyền lợi</h5>
                <div v-html="jobPosting.benefits"></div>
              </div>
            </div>
          </div>

          <div class="col-md-4">
            <!-- Thông tin cơ bản -->
            <div class="card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">Thông tin cơ bản</h5>
              </div>
              <div class="card-body">
                <ul class="list-group list-group-flush">
                  <!-- Thông tin đơn vị -->
                  <li v-if="jobPosting.department" class="list-group-item d-flex justify-content-between align-items-center">
                    <span>Phòng ban</span>
                    <span class="badge bg-light text-dark">
                      {{ jobPosting.department.name }}
                    </span>
                  </li>
                  <li v-if="jobPosting.factory" class="list-group-item d-flex justify-content-between align-items-center">
                    <span>Xí nghiệp</span>
                    <span class="badge bg-light text-dark">
                      {{ jobPosting.factory.name }}
                    </span>
                  </li>
                  <li v-if="jobPosting.division_name || jobPosting.division" class="list-group-item d-flex justify-content-between align-items-center">
                    <span>Bộ phận</span>
                    <span class="badge bg-light text-dark">
                      {{ jobPosting.division_name || (jobPosting.division ? jobPosting.division.name : '') }}
                    </span>
                  </li>
                  <li v-if="jobPosting.team_name || jobPosting.team" class="list-group-item d-flex justify-content-between align-items-center">
                    <span>Nhóm</span>
                    <span class="badge bg-light text-dark">
                      {{ jobPosting.team_name || (jobPosting.team ? jobPosting.team.name : '') }}
                    </span>
                  </li>

                  <!-- Thông tin khác -->
                  <li class="list-group-item d-flex justify-content-between align-items-center">
                    <span>Hình thức làm việc</span>
                    <span class="badge bg-light text-dark">
                      {{ jobPosting.employment_type_display }}
                    </span>
                  </li>
                  <li class="list-group-item d-flex justify-content-between align-items-center">
                    <span>Kinh nghiệm</span>
                    <span class="badge bg-light text-dark">
                      {{ jobPosting.experience_level_display }}
                    </span>
                  </li>
                  <li class="list-group-item d-flex justify-content-between align-items-center">
                    <span>Học vấn</span>
                    <span class="badge bg-light text-dark">
                      {{ jobPosting.education_required_display }}
                    </span>
                  </li>
                  <li class="list-group-item d-flex justify-content-between align-items-center">
                    <span>Mức lương</span>
                    <span v-if="jobPosting.is_salary_visible && !jobPosting.is_salary_negotiable" class="badge bg-light text-dark">
                      {{ formatSalary(jobPosting.min_salary, jobPosting.max_salary) }}
                    </span>
                    <span v-else-if="jobPosting.is_salary_visible && jobPosting.is_salary_negotiable" class="badge bg-light text-dark">
                      Thỏa thuận
                    </span>
                    <span v-else class="badge bg-light text-dark">Không công khai</span>
                  </li>
                  <li class="list-group-item d-flex justify-content-between align-items-center">
                    <span>Địa điểm làm việc</span>
                    <span class="badge bg-light text-dark">
                      {{ jobPosting.location }}
                    </span>
                  </li>
                  <li class="list-group-item d-flex justify-content-between align-items-center">
                    <span>Loại nơi làm việc</span>
                    <span class="badge bg-light text-dark">
                      {{ jobPosting.workplace_type_display }}
                    </span>
                  </li>
                </ul>
              </div>
            </div>

            <!-- Thông tin đăng tin -->
            <div class="card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">Thông tin đăng tin</h5>
              </div>
              <div class="card-body">
                <ul class="list-group list-group-flush">
                  <li class="list-group-item d-flex justify-content-between align-items-center">
                    <span>Người tạo</span>
                    <span>{{ jobPosting.created_by?.first_name }} {{ jobPosting.created_by?.last_name }}</span>
                  </li>
                  <li class="list-group-item d-flex justify-content-between align-items-center">
                    <span>Ngày tạo</span>
                    <span>{{ formatDate(jobPosting.created_at) }}</span>
                  </li>
                  <li class="list-group-item d-flex justify-content-between align-items-center">
                    <span>Ngày đăng</span>
                    <span>{{ formatDate(jobPosting.publish_date) }}</span>
                  </li>
                  <li class="list-group-item d-flex justify-content-between align-items-center">
                    <span>Hạn nộp hồ sơ</span>
                    <span
                      :class="{
                        'text-danger': isExpired(jobPosting.closing_date),
                        'text-success': !isExpired(jobPosting.closing_date)
                      }"
                    >
                      {{ formatDate(jobPosting.closing_date) }}
                    </span>
                  </li>
                  <li class="list-group-item d-flex justify-content-between align-items-center">
                    <span>Cập nhật lần cuối</span>
                    <span>{{ formatDate(jobPosting.updated_at) }}</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="activeTab === 'applications'">
        <!-- Danh sách đơn ứng tuyển -->
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="card-title mb-0">Danh sách đơn ứng tuyển</h5>
            <router-link
              :to="`/recruitment/applications?job_posting_id=${jobPosting.id}`"
              class="btn btn-sm btn-outline-primary"
            >
              Xem tất cả
            </router-link>
          </div>
          <div class="card-body">
            <div v-if="loadingApplications" class="text-center py-3">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Đang tải...</span>
              </div>
            </div>
            <div v-else-if="applications.length === 0" class="text-center py-3">
              <p class="text-muted">Chưa có đơn ứng tuyển nào</p>
            </div>
            <div v-else>
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Họ tên</th>
                      <th>Email</th>
                      <th>Số điện thoại</th>
                      <th>Ngày nộp</th>
                      <th>Trạng thái</th>
                      <th>Thao tác</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="application in applications || []" :key="application?.id">
                      <td>{{ application?.full_name }}</td>
                      <td>{{ application?.email }}</td>
                      <td>{{ application?.phone }}</td>
                      <td>{{ formatDate(application?.created_at) }}</td>
                      <td>
                        <span :class="getApplicationStatusBadgeClass(application?.status)">
                          {{ application?.status_display }}
                        </span>
                      </td>
                      <td>
                        <router-link
                          :to="`/recruitment/applications/${application?.id}`"
                          class="btn btn-sm btn-outline-primary"
                        >
                          <font-awesome-icon icon="eye" />
                        </router-link>
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
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'JobPostingDetail',
  data() {
    return {
      activeTab: 'details',
      loadingApplications: false,
      applications: []
    }
  },
  computed: {
    ...mapGetters('recruitment', ['jobPosting', 'loading', 'error']),

    jobId() {
      return this.$route.params.id
    }
  },
  created() {
    this.fetchJobPosting()
  },
  methods: {
    async fetchJobPosting() {
      try {
        await this.$store.dispatch('recruitment/fetchJobPosting', this.jobId)
        this.fetchApplications()
      } catch (error) {
        console.error('Error fetching job posting:', error)
      }
    },

    async fetchApplications() {
      try {
        this.loadingApplications = true
        await this.$store.dispatch('recruitment/fetchApplications', { job_posting_id: this.jobId })
        this.applications = this.$store.getters['recruitment/applications']
      } catch (error) {
        console.error('Error fetching applications:', error)
      } finally {
        this.loadingApplications = false
      }
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A'
      try {
        const date = new Date(dateString)
        return date.toLocaleDateString('vi-VN')
      } catch (error) {
        console.error('Error formatting date:', error)
        return 'N/A'
      }
    },

    isExpired(dateString) {
      if (!dateString) return false
      const today = new Date()
      const date = new Date(dateString)
      return date < today
    },

    formatSalary(min, max) {
      if (!min && !max) return 'Không có thông tin'

      const formatNumber = (num) => {
        return new Intl.NumberFormat('vi-VN').format(num)
      }

      if (min && max) {
        return `${formatNumber(min)} - ${formatNumber(max)} VNĐ`
      } else if (min) {
        return `Từ ${formatNumber(min)} VNĐ`
      } else if (max) {
        return `Đến ${formatNumber(max)} VNĐ`
      }

      return 'Không có thông tin'
    },

    getStatusBadgeClass(status) {
      switch (status) {
        case 'draft':
          return 'badge bg-secondary'
        case 'published':
          return 'badge bg-success'
        case 'closed':
          return 'badge bg-danger'
        case 'on_hold':
          return 'badge bg-warning'
        case 'cancelled':
          return 'badge bg-dark'
        default:
          return 'badge bg-secondary'
      }
    },

    getApplicationStatusBadgeClass(status) {
      if (!status) return 'badge bg-secondary'

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

    async publishJobPosting() {
      try {
        if (confirm('Bạn có chắc chắn muốn đăng tin tuyển dụng này?')) {
          await this.$store.dispatch('recruitment/publishJobPosting', this.jobId)
          this.$store.dispatch('app/setSuccess', 'Đăng tin tuyển dụng thành công')
          this.fetchJobPosting()
        }
      } catch (error) {
        this.$store.dispatch('app/setError', 'Đăng tin tuyển dụng thất bại')
        console.error('Error publishing job posting:', error)
      }
    },

    async closeJobPosting() {
      try {
        if (confirm('Bạn có chắc chắn muốn đóng tin tuyển dụng này?')) {
          await this.$store.dispatch('recruitment/closeJobPosting', this.jobId)
          this.$store.dispatch('app/setSuccess', 'Đóng tin tuyển dụng thành công')
          this.fetchJobPosting()
        }
      } catch (error) {
        this.$store.dispatch('app/setError', 'Đóng tin tuyển dụng thất bại')
        console.error('Error closing job posting:', error)
      }
    },

    async cancelJobPosting() {
      try {
        if (confirm('Bạn có chắc chắn muốn hủy tin tuyển dụng này?')) {
          await this.$store.dispatch('recruitment/cancelJobPosting', this.jobId)
          this.$store.dispatch('app/setSuccess', 'Hủy tin tuyển dụng thành công')
          this.fetchJobPosting()
        }
      } catch (error) {
        this.$store.dispatch('app/setError', 'Hủy tin tuyển dụng thất bại')
        console.error('Error cancelling job posting:', error)
      }
    },

    previewJobPosting() {
      window.open(`/careers/${this.jobId}`, '_blank')
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
</style>
