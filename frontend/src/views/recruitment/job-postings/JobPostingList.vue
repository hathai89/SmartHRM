<template>
  <div class="container-fluid">
    <div class="d-flex justify-content-end align-items-center mb-4">
      <div class="d-flex">
        <button class="btn-flat btn-flat-secondary me-2" @click="refreshData">
          <font-awesome-icon icon="sync" :class="{ 'fa-spin': loading }" />
          Làm mới
        </button>
        <router-link to="/recruitment/job-postings/create" class="btn-flat btn-flat-primary">
          <font-awesome-icon icon="plus" class="me-2" />
          Tạo tin tuyển dụng
        </router-link>
      </div>
    </div>

    <!-- Bộ lọc -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="row">
          <div class="col-md-3 mb-3">
            <label for="status" class="form-label">Trạng thái</label>
            <select id="status" v-model="filters.status" class="form-select" @change="applyFilters">
              <option value="">Tất cả</option>
              <option value="draft">Nháp</option>
              <option value="published">Đang tuyển</option>
              <option value="closed">Đã kết thúc</option>
              <option value="on_hold">Tạm dừng</option>
            </select>
          </div>
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

    <!-- Danh sách tin tuyển dụng -->
    <div class="card">
      <div class="card-body">
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Đang tải...</span>
          </div>
        </div>
        <div v-else-if="filteredJobPostings.length === 0" class="text-center py-5">
          <p class="text-muted">Không có tin tuyển dụng nào</p>
          <router-link to="/recruitment/job-postings/create" class="btn btn-primary">
            <font-awesome-icon icon="plus" class="me-2" />
            Tạo tin tuyển dụng
          </router-link>
        </div>
        <div v-else>
          <div class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th @click="sortBy('title')">
                    Tiêu đề
                    <font-awesome-icon v-if="sortKey === 'title'" :icon="sortIcon" />
                  </th>
                  <th @click="sortBy('department_name')">
                    Phòng ban/Xí nghiệp
                    <font-awesome-icon v-if="sortKey === 'department_name'" :icon="sortIcon" />
                  </th>
                  <th @click="sortBy('positions')">
                    Số lượng
                    <font-awesome-icon v-if="sortKey === 'positions'" :icon="sortIcon" />
                  </th>
                  <th @click="sortBy('publish_date')">
                    Ngày đăng
                    <font-awesome-icon v-if="sortKey === 'publish_date'" :icon="sortIcon" />
                  </th>
                  <th @click="sortBy('closing_date')">
                    Hạn nộp
                    <font-awesome-icon v-if="sortKey === 'closing_date'" :icon="sortIcon" />
                  </th>
                  <th @click="sortBy('applications_count')">
                    Đơn ứng tuyển
                    <font-awesome-icon v-if="sortKey === 'applications_count'" :icon="sortIcon" />
                  </th>
                  <th @click="sortBy('status')">
                    Trạng thái
                    <font-awesome-icon v-if="sortKey === 'status'" :icon="sortIcon" />
                  </th>
                  <th>Thao tác</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="job in filteredJobPostings" :key="job.id">
                  <td>
                    <router-link :to="`/recruitment/job-postings/${job.id}`" class="text-decoration-none">
                      {{ job.title }}
                    </router-link>
                  </td>
                  <td>{{ job.department_name || job.factory_name }}</td>
                  <td>{{ job.positions }}</td>
                  <td>{{ formatDate(job.publish_date) }}</td>
                  <td>{{ formatDate(job.closing_date) }}</td>
                  <td>
                    <router-link
                      :to="`/recruitment/applications?job_posting_id=${job.id}`"
                      class="badge bg-info text-decoration-none"
                    >
                      {{ job.applications_count }}
                    </router-link>
                  </td>
                  <td>
                    <span :class="getStatusBadgeClass(job.status)">
                      {{ job.status_display }}
                    </span>
                  </td>
                  <td>
                    <div class="btn-group">
                      <router-link
                        :to="`/recruitment/job-postings/${job.id}`"
                        class="btn btn-sm btn-outline-primary"
                        title="Xem chi tiết"
                      >
                        <font-awesome-icon icon="eye" />
                      </router-link>
                      <router-link
                        :to="`/recruitment/job-postings/${job.id}/edit`"
                        class="btn btn-sm btn-outline-secondary"
                        title="Chỉnh sửa"
                      >
                        <font-awesome-icon icon="edit" />
                      </router-link>
                      <button
                        v-if="job.status === 'draft'"
                        class="btn btn-sm btn-outline-success"
                        title="Đăng tin"
                        @click="publishJobPosting(job.id)"
                      >
                        <font-awesome-icon icon="check" />
                      </button>
                      <button
                        v-if="job.status === 'published'"
                        class="btn btn-sm btn-outline-danger"
                        title="Đóng tin"
                        @click="closeJobPosting(job.id)"
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
              <span class="text-muted">Hiển thị {{ filteredJobPostings.length }} / {{ totalItems }} tin tuyển dụng</span>
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
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'JobPostingList',
  data() {
    return {
      filters: {
        status: '',
        department: '',
        factory: '',
        search: ''
      },
      sortKey: 'created_at',
      sortDirection: 'desc',
      currentPage: 1,
      itemsPerPage: 10,
      totalItems: 0,
      departments: [],
      factories: []
    }
  },
  computed: {
    ...mapGetters('recruitment', ['jobPostings', 'loading', 'error']),
    ...mapGetters('departments', ['allDepartments']),
    ...mapGetters('factories', ['allFactories']),

    filteredJobPostings() {
      // Lọc các phần tử null hoặc undefined và đảm bảo mỗi phần tử có id
      return this.jobPostings.filter(job => job && job.id)
    },

    sortIcon() {
      return this.sortDirection === 'asc' ? 'sort-up' : 'sort-down'
    },

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
      await this.$store.dispatch('departments/fetchDepartments')
      this.departments = this.allDepartments.filter(dept => dept.dept_type === 'department')
    },

    async fetchFactories() {
      await this.$store.dispatch('factories/fetchFactories')
      this.factories = this.allFactories.filter(factory => factory.factory_type === 'factory')
    },

    async fetchJobPostings() {
      try {
        const params = {
          page: this.currentPage,
          page_size: this.itemsPerPage,
          ordering: this.getSortParam(),
          ...this.getFilterParams()
        }

        const response = await this.$store.dispatch('recruitment/fetchJobPostings', params)

        // Lấy tổng số mục từ response nếu có
        if (response && response.count !== undefined) {
          this.totalItems = response.count
        } else {
          // Nếu không có thông tin phân trang, sử dụng độ dài của mảng đã lọc
          this.totalItems = this.filteredJobPostings.length
        }
      } catch (error) {
        console.error('Error fetching job postings:', error)
        this.totalItems = 0 // Đặt về 0 khi có lỗi
      }
    },

    refreshData() {
      this.fetchJobPostings()
    },

    applyFilters() {
      this.currentPage = 1
      this.fetchJobPostings()
    },

    getFilterParams() {
      const params = {}

      if (this.filters.status) {
        params.status = this.filters.status
      }

      if (this.filters.department) {
        params.department = this.filters.department
      }

      if (this.filters.factory) {
        params.factory = this.filters.factory
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

      this.fetchJobPostings()
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
      this.fetchJobPostings()
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('vi-VN')
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
        default:
          return 'badge bg-secondary'
      }
    },

    async publishJobPosting(id) {
      try {
        if (confirm('Bạn có chắc chắn muốn đăng tin tuyển dụng này?')) {
          await this.$store.dispatch('recruitment/publishJobPosting', id)
          this.$store.dispatch('app/setSuccess', 'Đăng tin tuyển dụng thành công')
          this.fetchJobPostings()
        }
      } catch (error) {
        this.$store.dispatch('app/setError', 'Đăng tin tuyển dụng thất bại')
        console.error('Error publishing job posting:', error)
      }
    },

    async closeJobPosting(id) {
      try {
        if (confirm('Bạn có chắc chắn muốn đóng tin tuyển dụng này?')) {
          await this.$store.dispatch('recruitment/closeJobPosting', id)
          this.$store.dispatch('app/setSuccess', 'Đóng tin tuyển dụng thành công')
          this.fetchJobPostings()
        }
      } catch (error) {
        this.$store.dispatch('app/setError', 'Đóng tin tuyển dụng thất bại')
        console.error('Error closing job posting:', error)
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
