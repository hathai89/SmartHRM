<template>
  <div class="container py-5">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Đang tải...</span>
      </div>
    </div>
    <div v-else-if="!jobPosting" class="text-center py-5">
      <div class="alert alert-danger">
        <h4 class="alert-heading">Không tìm thấy vị trí</h4>
        <p>Vị trí này không tồn tại hoặc đã hết hạn.</p>
        <hr />
        <router-link to="/careers" class="btn btn-primary">
          Xem các vị trí khác
        </router-link>
      </div>
    </div>
    <div v-else>
      <div class="row mb-4">
        <div class="col-md-8">
          <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
              <li class="breadcrumb-item"><router-link to="/">Trang chủ</router-link></li>
              <li class="breadcrumb-item"><router-link to="/careers">Cơ hội việc làm</router-link></li>
              <li class="breadcrumb-item active" aria-current="page">{{ jobPosting.title }}</li>
            </ol>
          </nav>
          <h1 class="mb-2">{{ jobPosting.title }}</h1>
          <h5 class="text-muted mb-2">{{ jobPosting.department_name || jobPosting.factory_name }}</h5>
          <div class="text-muted mb-4">
            <span v-if="jobPosting.division_name">Bộ phận: {{ jobPosting.division_name }}</span>
            <span v-if="jobPosting.division_name && jobPosting.team_name"> | </span>
            <span v-if="jobPosting.team_name">Nhóm: {{ jobPosting.team_name }}</span>
          </div>

          <div class="mb-4">
            <span class="badge bg-primary me-2">{{ jobPosting.employment_type_display }}</span>
            <span class="badge bg-secondary me-2">{{ jobPosting.location }}</span>
            <span class="badge bg-info me-2">{{ jobPosting.experience_level_display }}</span>
            <span class="badge bg-success">{{ jobPosting.education_required_display }}</span>
          </div>

          <div class="alert" :class="{'alert-warning': daysRemaining > 0, 'alert-danger': daysRemaining === 0 && !jobPosting.is_open_until_filled, 'alert-info': jobPosting.is_open_until_filled}">
            <div class="d-flex align-items-center">
              <font-awesome-icon :icon="daysRemaining > 0 ? 'clock' : (jobPosting.is_open_until_filled ? 'calendar-check' : 'exclamation-triangle')" class="me-2" />
              <div>
                <strong>Hạn nộp hồ sơ:</strong> {{ jobPosting.is_open_until_filled ? 'Tuyển dụng đến khi đủ' : formatDate(jobPosting.closing_date) }}
                <div v-if="daysRemaining > 0" class="small">
                  Còn {{ daysRemaining }} ngày để ứng tuyển
                </div>
                <div v-else-if="jobPosting.is_open_until_filled" class="small">
                  Vẫn còn nhận hồ sơ ứng tuyển
                </div>
                <div v-else class="small text-danger">
                  Đã hết hạn ứng tuyển
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-4 text-end">
          <router-link
            v-if="jobPosting.is_open_until_filled || daysRemaining > 0"
            :to="`/careers/${jobPosting.id}/apply`"
            class="btn btn-primary btn-lg">
            <font-awesome-icon icon="paper-plane" class="me-2" />
            Ứng tuyển ngay
          </router-link>
          <button
            v-else
            class="btn btn-secondary btn-lg"
            disabled>
            <font-awesome-icon icon="times" class="me-2" />
            Đã hết hạn ứng tuyển
          </button>
        </div>
      </div>

      <div class="row">
        <div class="col-md-8">
          <div class="card mb-4">
            <div class="card-body">
              <h3 class="card-title">Mô tả công việc</h3>
              <div class="card-text" v-html="jobPosting.description"></div>

              <h3 class="card-title mt-4">Yêu cầu ứng viên</h3>
              <div class="card-text" v-html="jobPosting.requirements"></div>

              <h3 class="card-title mt-4">Quyền lợi</h3>
              <div class="card-text" v-html="jobPosting.benefits"></div>

              <div class="mt-4">
                <router-link
                  v-if="jobPosting.is_open_until_filled || daysRemaining > 0"
                  :to="`/careers/${jobPosting.id}/apply`"
                  class="btn btn-primary">
                  <font-awesome-icon icon="paper-plane" class="me-2" />
                  Ứng tuyển ngay
                </router-link>
                <button
                  v-else
                  class="btn btn-secondary"
                  disabled>
                  <font-awesome-icon icon="times" class="me-2" />
                  Đã hết hạn ứng tuyển
                </button>
                <button class="btn btn-outline-secondary ms-2" @click="shareJob">
                  <font-awesome-icon icon="share" class="me-2" />
                  Chia sẻ
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card mb-4">
            <div class="card-header">
              <h5 class="card-title mb-0">Thông tin vị trí</h5>
            </div>
            <div class="card-body">
              <ul class="list-group list-group-flush">
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Phòng ban/Xí nghiệp</span>
                  <span class="badge bg-light text-dark">{{ jobPosting.department_name || jobPosting.factory_name }}</span>
                </li>
                <li v-if="jobPosting.division_name" class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Bộ phận</span>
                  <span class="badge bg-light text-dark">{{ jobPosting.division_name }}</span>
                </li>
                <li v-if="jobPosting.team_name" class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Nhóm</span>
                  <span class="badge bg-light text-dark">{{ jobPosting.team_name }}</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Địa điểm làm việc</span>
                  <span class="badge bg-light text-dark">{{ jobPosting.location }}</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Hình thức làm việc</span>
                  <span class="badge bg-light text-dark">{{ jobPosting.employment_type_display }}</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Kinh nghiệm</span>
                  <span class="badge bg-light text-dark">{{ jobPosting.experience_level_display }}</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Học vấn</span>
                  <span class="badge bg-light text-dark">{{ jobPosting.education_required_display }}</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Số lượng tuyển</span>
                  <span class="badge bg-light text-dark">{{ jobPosting.positions }}</span>
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
                  <span>Ngày đăng</span>
                  <span class="badge bg-light text-dark">{{ formatDate(jobPosting.publish_date) }}</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Hạn nộp hồ sơ</span>
                  <span class="badge bg-light text-dark">{{ jobPosting.is_open_until_filled ? 'Tuyển dụng đến khi đủ' : formatDate(jobPosting.closing_date) }}</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Trạng thái</span>
                  <span v-if="jobPosting.is_open_until_filled || daysRemaining > 0" class="badge bg-success">
                    <font-awesome-icon icon="check" class="me-1" />
                    Đang nhận hồ sơ
                  </span>
                  <span v-else class="badge bg-danger">
                    <font-awesome-icon icon="times" class="me-1" />
                    Đã hết hạn
                  </span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Loại nơi làm việc</span>
                  <span class="badge bg-light text-dark">{{ jobPosting.workplace_type_display }}</span>
                </li>
              </ul>
            </div>
          </div>

          <div class="card mb-4">
            <div class="card-header">
              <h5 class="card-title mb-0">Vị trí tương tự</h5>
            </div>
            <div class="card-body">
              <div v-if="similarJobs.length === 0" class="text-center py-3">
                <p class="text-muted">Không có vị trí tương tự</p>
              </div>
              <div v-else>
                <div v-for="job in similarJobs" :key="job.id" class="mb-3">
                  <router-link :to="`/careers/${job.id}`" class="text-decoration-none">
                    <h6 class="mb-1">{{ job.title }}</h6>
                  </router-link>
                  <div class="small text-muted">
                    {{ job.department_name || job.factory_name }}
                    <span v-if="job.division_name"> | {{ job.division_name }}</span>
                    <span v-if="job.team_name"> | {{ job.team_name }}</span>
                    <br>{{ job.location }}
                  </div>
                </div>
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
  name: 'CareerDetail',
  data() {
    return {
      similarJobs: []
    }
  },
  computed: {
    ...mapGetters('recruitment', ['jobPosting', 'loading', 'error']),

    jobId() {
      return this.$route.params.id
    },

    daysRemaining() {
      if (!this.jobPosting) return 0

      // Nếu tuyển dụng đến khi đủ, trả về 1 để hiển thị là còn nhận hồ sơ
      if (this.jobPosting.is_open_until_filled) return 1

      // Nếu không có ngày hết hạn, trả về 0
      if (!this.jobPosting.closing_date) return 0

      const today = new Date()
      const closingDate = new Date(this.jobPosting.closing_date)
      const diffTime = closingDate - today
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

      return diffDays > 0 ? diffDays : 0
    },

    isExpired() {
      return !this.jobPosting.is_open_until_filled && this.daysRemaining === 0
    }
  },
  created() {
    this.fetchJobPosting()
  },
  methods: {
    async fetchJobPosting() {
      try {
        await this.$store.dispatch('recruitment/fetchPublicJobPosting', this.jobId)

        if (this.jobPosting) {
          this.fetchSimilarJobs()
        }
      } catch (error) {
        console.error('Error fetching job posting:', error)
      }
    },

    async fetchSimilarJobs() {
      try {
        // Lấy các việc làm tương tự dựa trên phòng ban hoặc xí nghiệp
        const params = {
          status: 'published',
          page_size: 5
        }

        // Thêm điều kiện lọc theo phòng ban hoặc xí nghiệp
        if (this.jobPosting.department) {
          params.department = this.jobPosting.department
        } else if (this.jobPosting.factory) {
          params.factory = this.jobPosting.factory
        }

        const response = await this.$store.dispatch('recruitment/fetchPublicJobPostings', params)

        // Lọc ra các việc làm khác với việc làm hiện tại
        let jobs = []
        if (response && response.results) {
          jobs = response.results
        } else if (Array.isArray(response)) {
          jobs = response
        } else {
          jobs = this.$store.getters['recruitment/jobPostings'] || []
        }

        // Lọc bỏ việc làm hiện tại và giới hạn số lượng
        this.similarJobs = jobs
          .filter(job => job.id !== parseInt(this.jobId))
          .slice(0, 3)
      } catch (error) {
        console.error('Error fetching similar jobs:', error)
        this.similarJobs = []
      }
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('vi-VN')
    },

    formatSalary(min, max) {
      if (!min && !max) return 'Thỏa thuận'

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

      return 'Thỏa thuận'
    },

    shareJob() {
      // In a real app, this would open a share dialog
      // For now, we'll just copy the URL to clipboard
      const url = window.location.href
      navigator.clipboard.writeText(url)
        .then(() => {
          this.$store.dispatch('app/setSuccess', 'Đã sao chép đường dẫn vào clipboard')
        })
        .catch(() => {
          this.$store.dispatch('app/setError', 'Không thể sao chép đường dẫn')
        })
    }
  }
}
</script>

<style scoped>
.badge {
  font-size: 0.8rem;
  padding: 0.4em 0.6em;
}

.list-group-item {
  padding: 0.75rem 1.25rem;
}
</style>
