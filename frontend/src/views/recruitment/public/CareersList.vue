<template>
  <div class="container py-5">
    <div class="row mb-5">
      <div class="col-12 text-center">
        <h1 class="display-4 mb-3">Cơ hội việc làm</h1>
        <p class="lead">Khám phá các cơ hội nghề nghiệp hấp dẫn tại công ty chúng tôi</p>
      </div>
    </div>

    <!-- Bộ lọc -->
    <div class="row mb-4">
      <div class="col-md-12">
        <div class="card">
          <div class="card-body">
            <div class="row">
              <div class="col-md-3 mb-3">
                <label for="department" class="form-label">Phòng ban</label>
                <select id="department" v-model="filters.department" class="form-select" @change="applyFilters">
                  <option value="">Tất cả</option>
                  <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                    {{ dept.name }}
                  </option>
                </select>
              </div>
              <div class="col-md-3 mb-3">
                <label for="factory" class="form-label">Xí nghiệp</label>
                <select id="factory" v-model="filters.factory" class="form-select" @change="applyFilters">
                  <option value="">Tất cả</option>
                  <option v-for="factory in factories" :key="factory.id" :value="factory.id">
                    {{ factory.name }}
                  </option>
                </select>
              </div>
              <div class="col-md-3 mb-3">
                <label for="location" class="form-label">Địa điểm</label>
                <select id="location" v-model="filters.location" class="form-select" @change="applyFilters">
                  <option value="">Tất cả</option>
                  <option v-for="location in locations" :key="location" :value="location">
                    {{ location }}
                  </option>
                  <option v-if="locations.length === 0" disabled>Không có địa điểm nào</option>
                </select>
                <small v-if="locations.length === 0" class="text-muted">
                  Hiện chưa có thông tin về địa điểm làm việc
                </small>
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
                  <button class="btn btn-primary" type="button" @click="applyFilters">
                    <font-awesome-icon icon="search" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Danh sách việc làm -->
    <div class="row">
      <div class="col-md-12">
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Đang tải...</span>
          </div>
        </div>
        <div v-else-if="jobPostings.length === 0" class="text-center py-5">
          <div class="alert alert-info">
            <h4 class="alert-heading">Không có vị trí nào phù hợp</h4>
            <p>Hiện tại không có vị trí nào phù hợp với tiêu chí tìm kiếm của bạn.</p>
            <hr />
            <p class="mb-0">Vui lòng thử lại với các tiêu chí khác hoặc quay lại sau.</p>
          </div>
        </div>
        <div v-else>
          <div class="row">
            <div v-for="job in jobPostings" :key="job.id" class="col-md-6 mb-4">
              <div class="card h-100 job-card">
                <div class="card-body">
                  <h5 class="card-title">{{ job.title }}</h5>
                  <h6 class="card-subtitle mb-2 text-muted">{{ job.department_name || job.factory_name }}</h6>
                  <div class="mb-3">
                    <span class="badge bg-primary me-2">{{ job.employment_type_display }}</span>
                    <span class="badge bg-secondary me-2">{{ job.location }}</span>
                    <span class="badge bg-info">{{ job.experience_level_display }}</span>
                  </div>
                  <p class="card-text">{{ truncateText(job.description, 150) }}</p>
                  <div class="d-flex justify-content-between align-items-center">
                    <small class="text-muted">Hạn nộp: {{ formatDate(job.closing_date) }}</small>
                    <router-link :to="`/careers/${job.id}`" class="btn btn-outline-primary">
                      Xem chi tiết
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Phân trang -->
          <div class="d-flex justify-content-center mt-4">
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

    <!-- Giới thiệu công ty -->
    <div class="row mt-5">
      <div class="col-md-12">
        <div class="card">
          <div class="card-body">
            <h3 class="card-title">Về công ty chúng tôi</h3>
            <p class="card-text">
              Công ty chúng tôi là một trong những công ty hàng đầu trong lĩnh vực của mình, với môi trường làm việc năng động,
              chuyên nghiệp và nhiều cơ hội phát triển. Chúng tôi luôn tìm kiếm những ứng viên tài năng, đam mê và sáng tạo
              để cùng nhau phát triển và đạt được những thành công mới.
            </p>
            <h4>Tại sao nên làm việc với chúng tôi?</h4>
            <ul>
              <li>Môi trường làm việc chuyên nghiệp, năng động</li>
              <li>Cơ hội phát triển và thăng tiến</li>
              <li>Chế độ đãi ngộ hấp dẫn</li>
              <li>Đội ngũ nhân viên thân thiện, hỗ trợ</li>
              <li>Các hoạt động team building thường xuyên</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'CareersList',
  data() {
    return {
      filters: {
        department: '',
        factory: '',
        location: '',
        search: ''
      },
      currentPage: 1,
      itemsPerPage: 10,
      totalItems: 0,
      departments: [],
      factories: [],
      locations: []
    }
  },
  computed: {
    ...mapGetters('recruitment', ['jobPostings', 'loading', 'error']),

    totalPages() {
      return Math.ceil(this.totalItems / this.itemsPerPage)
    }
  },
  created() {
    this.fetchDepartments()
    this.fetchFactories()
    this.fetchJobPostings()
  },
  methods: {
    async fetchDepartments() {
      try {
        // Lấy danh sách phòng ban trực tiếp từ API public
        const response = await this.$store.dispatch('recruitment/fetchPublicDepartments')
        this.departments = response || []
        console.log(`Đã tải ${this.departments.length} phòng ban`)
      } catch (error) {
        console.error('Error fetching departments:', error)
        this.departments = []
      }
    },

    async fetchFactories() {
      try {
        // Lấy danh sách xí nghiệp trực tiếp từ API public
        const response = await this.$store.dispatch('recruitment/fetchPublicFactories')
        this.factories = response || []
        console.log(`Đã tải ${this.factories.length} xí nghiệp`)

        // Lấy danh sách địa điểm từ các tin tuyển dụng đã đăng
        await this.fetchLocations()
      } catch (error) {
        console.error('Error fetching factories:', error)
        this.factories = []
      }
    },

    async fetchLocations() {
      try {
        // Lấy danh sách tin tuyển dụng để trích xuất các địa điểm duy nhất
        const response = await this.$store.dispatch('recruitment/fetchPublicJobPostings', {
          params: {
            status: 'published',
            page_size: 1000 // Lấy tất cả tin để có đủ địa điểm
          }
        })

        // Lấy danh sách tin tuyển dụng
        let jobsList = []
        if (response && response.results) {
          jobsList = response.results
        } else if (Array.isArray(response)) {
          jobsList = response
        } else {
          jobsList = this.$store.getters['recruitment/jobPostings'] || []
        }

        // Trích xuất các địa điểm duy nhất
        const uniqueLocations = new Set()
        jobsList.forEach(job => {
          if (job.location && job.location.trim() !== '') {
            uniqueLocations.add(job.location)
          }
        })

        // Chuyển Set thành mảng và sắp xếp
        this.locations = Array.from(uniqueLocations).sort()

        // Log để debug
        console.log(`Đã tìm thấy ${this.locations.length} địa điểm từ ${jobsList.length} tin tuyển dụng`)

        // Nếu không có địa điểm nào từ API, sử dụng danh sách trống
        if (this.locations.length === 0) {
          console.log('Không tìm thấy địa điểm nào từ API')
          this.locations = []
        }
      } catch (error) {
        console.error('Error fetching locations:', error)
        this.locations = []
      }
    },

    async fetchJobPostings() {
      try {
        const params = {
          page: this.currentPage,
          page_size: this.itemsPerPage,
          status: 'published',
          ...this.getFilterParams()
        }

        // Lấy dữ liệu từ API thông qua store
        const response = await this.$store.dispatch('recruitment/fetchPublicJobPostings', params)

        // Cập nhật tổng số mục
        if (response && response.count !== undefined) {
          this.totalItems = response.count
        } else if (response && Array.isArray(response)) {
          this.totalItems = response.length
        } else {
          this.totalItems = 0
        }
      } catch (error) {
        console.error('Error fetching job postings:', error)
        this.totalItems = 0
      }
    },

    applyFilters() {
      this.currentPage = 1
      this.fetchJobPostings()
    },

    getFilterParams() {
      const params = {}

      if (this.filters.department) {
        params.department = this.filters.department
      }

      if (this.filters.factory) {
        params.factory = this.filters.factory
      }

      if (this.filters.location) {
        params.location = this.filters.location
      }

      if (this.filters.search) {
        params.search = this.filters.search
      }

      return params
    },

    changePage(page) {
      if (page < 1 || page > this.totalPages) {
        return
      }

      this.currentPage = page
      this.fetchJobPostings()
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('vi-VN')
    },

    truncateText(text, length) {
      if (!text) return ''
      if (text.length <= length) return text
      return text.substring(0, length) + '...'
    }
  }
}
</script>

<style scoped>
.job-card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.job-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.badge {
  font-size: 0.8rem;
  padding: 0.4em 0.6em;
}
</style>
