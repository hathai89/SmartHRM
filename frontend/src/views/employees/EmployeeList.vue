<template>
  <div class="employee-list">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="h3">Danh sách nhân viên</h1>
      <div class="d-flex">
        <button class="btn btn-outline-secondary me-2" @click="refreshData">
          <font-awesome-icon icon="sync" :class="{ 'fa-spin': loading }" />
          Làm mới
        </button>
        <router-link to="/employees/create" class="btn btn-primary">
          <font-awesome-icon icon="plus" class="me-2" />
          Thêm nhân viên
        </router-link>
      </div>
    </div>

    <div class="card mb-4">
      <div class="card-body">
        <div class="row mb-3">
          <div class="col-md-3 mb-2">
            <div class="input-group">
              <span class="input-group-text">
                <font-awesome-icon icon="search" />
              </span>
              <input
                type="text"
                class="form-control"
                v-model="searchQuery"
                placeholder="Tìm kiếm nhân viên..."
                @input="handleSearch"
              >
            </div>
          </div>
          <div class="col-md-3 mb-2">
            <select class="form-select" v-model="departmentFilter" @change="applyFilters">
              <option value="">Tất cả phòng ban</option>
              <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                {{ dept.name }}
              </option>
            </select>
          </div>
          <div class="col-md-3 mb-2">
            <select class="form-select" v-model="factoryFilter" @change="applyFilters">
              <option value="">Tất cả xí nghiệp</option>
              <option v-for="factory in factories" :key="factory.id" :value="factory.id">
                {{ factory.name }}
              </option>
            </select>
          </div>
          <div class="col-md-3 mb-2">
            <select class="form-select" v-model="statusFilter" @change="applyFilters">
              <option value="">Tất cả trạng thái</option>
              <option value="active">Đang làm việc</option>
              <option value="probation">Thử việc</option>
              <option value="terminated">Đã nghỉ việc</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading">
      <loading-spinner />
    </div>

    <template v-else>
      <div class="card">
        <div class="table-responsive">
          <table class="table table-hover table-striped mb-0">
            <thead class="table-light">
              <tr>
                <th scope="col" @click="sortBy('employee_id')" class="sortable">
                  Mã NV
                  <font-awesome-icon
                    v-if="sortKey === 'employee_id'"
                    :icon="sortOrder === 'asc' ? 'sort-up' : 'sort-down'"
                  />
                </th>
                <th scope="col" @click="sortBy('full_name')" class="sortable">
                  Họ và tên
                  <font-awesome-icon
                    v-if="sortKey === 'full_name'"
                    :icon="sortOrder === 'asc' ? 'sort-up' : 'sort-down'"
                  />
                </th>
                <th scope="col">Phòng ban</th>
                <th scope="col">Xí nghiệp</th>
                <th scope="col">Chức vụ</th>
                <th scope="col" @click="sortBy('hire_date')" class="sortable">
                  Ngày vào làm
                  <font-awesome-icon
                    v-if="sortKey === 'hire_date'"
                    :icon="sortOrder === 'asc' ? 'sort-up' : 'sort-down'"
                  />
                </th>
                <th scope="col">Trạng thái</th>
                <th scope="col" class="text-center">Thao tác</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="filteredEmployees.length === 0">
                <td colspan="8" class="text-center py-4">
                  <p class="mb-0 text-muted">Không tìm thấy nhân viên nào</p>
                </td>
              </tr>
              <tr v-for="employee in paginatedEmployees" :key="employee.id">
                <td>{{ employee.employee_id }}</td>
                <td>
                  <div class="d-flex align-items-center">
                    <div class="avatar-sm me-2">
                      <img
                        v-if="employee.avatar"
                        :src="employee.avatar"
                        alt="Avatar"
                        class="avatar-img"
                      >
                      <div v-else class="avatar-placeholder">
                        <font-awesome-icon icon="user" />
                      </div>
                    </div>
                    {{ employee.full_name }}
                  </div>
                </td>
                <td>{{ employee.department }}</td>
                <td>{{ employee.factory }}</td>
                <td>{{ employee.job_title }}</td>
                <td>{{ formatDate(employee.hire_date) }}</td>
                <td>
                  <span
                    class="badge"
                    :class="{
                      'bg-success': employee.status === 'active',
                      'bg-warning': employee.status === 'probation',
                      'bg-danger': employee.status === 'terminated'
                    }"
                    style="border-radius: 4px; padding: 5px 8px;"
                  >
                    {{ getStatusText(employee.status) }}
                  </span>
                </td>
                <td class="text-center">
                  <div class="btn-group">
                    <router-link
                      :to="'/employees/' + employee.id"
                      class="btn btn-sm btn-outline-primary"
                      title="Xem chi tiết"
                    >
                      <font-awesome-icon icon="eye" />
                    </router-link>
                    <router-link
                      :to="'/employees/' + employee.id + '/edit'"
                      class="btn btn-sm btn-outline-secondary"
                      title="Chỉnh sửa"
                    >
                      <font-awesome-icon icon="edit" />
                    </router-link>
                    <button
                      class="btn btn-sm btn-outline-danger"
                      title="Xóa"
                      @click="confirmDelete(employee)"
                    >
                      <font-awesome-icon icon="trash-alt" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="card-footer d-flex justify-content-between align-items-center">
          <div>
            Hiển thị {{ paginationInfo.from }}-{{ paginationInfo.to }} trên {{ filteredEmployees.length }} nhân viên
          </div>
          <nav aria-label="Page navigation">
            <ul class="pagination mb-0">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <a class="page-link" href="#" @click.prevent="goToPage(1)">
                  <font-awesome-icon icon="angle-double-left" />
                </a>
              </li>
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <a class="page-link" href="#" @click.prevent="goToPage(currentPage - 1)">
                  <font-awesome-icon icon="angle-left" />
                </a>
              </li>
              <li
                v-for="page in displayedPages"
                :key="page"
                class="page-item"
                :class="{ active: currentPage === page }"
              >
                <a class="page-link" href="#" @click.prevent="goToPage(page)">{{ page }}</a>
              </li>
              <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <a class="page-link" href="#" @click.prevent="goToPage(currentPage + 1)">
                  <font-awesome-icon icon="angle-right" />
                </a>
              </li>
              <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <a class="page-link" href="#" @click.prevent="goToPage(totalPages)">
                  <font-awesome-icon icon="angle-double-right" />
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </template>

    <!-- Modal xác nhận xóa nhân viên -->
    <confirm-dialog
      v-if="showDeleteConfirm"
      title="Xác nhận xóa nhân viên"
      :message="'Bạn có chắc chắn muốn xóa nhân viên ' + (employeeToDelete ? employeeToDelete.full_name : '') + '?'"
      @confirm="deleteEmployee"
      @cancel="cancelDelete"
    />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import { breadcrumbMixin } from '@/utils/breadcrumb'
import debounce from 'lodash/debounce'

export default {
  name: 'EmployeeListPage',
  components: {
    LoadingSpinner,
    ConfirmDialog
  },
  mixins: [breadcrumbMixin],
  data() {
    return {
      loading: false,
      searchQuery: '',
      departmentFilter: '',
      factoryFilter: '',
      statusFilter: '',
      sortKey: 'employee_id',
      sortOrder: 'asc',
      currentPage: 1,
      perPage: 10,
      showDeleteConfirm: false,
      employeeToDelete: null,
      employees: [],
      departments: [],
      factories: []
    }
  },
  computed: {
    ...mapGetters({
      employeesData: 'employees/allEmployees',
      totalEmployees: 'employees/totalEmployees',
      isLoading: 'employees/isLoading',
      departmentsData: 'departments/allDepartments',
      factoriesData: 'factories/allFactories'
    }),
    filteredEmployees() {
      let result = [...this.employees]

      // Tìm kiếm
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        result = result.filter(employee =>
          employee.employee_id.toLowerCase().includes(query) ||
          employee.full_name.toLowerCase().includes(query) ||
          employee.email.toLowerCase().includes(query) ||
          employee.phone.toLowerCase().includes(query)
        )
      }

      // Lọc theo phòng ban
      if (this.departmentFilter) {
        result = result.filter(employee =>
          employee.department_id === parseInt(this.departmentFilter)
        )
      }

      // Lọc theo xí nghiệp
      if (this.factoryFilter) {
        result = result.filter(employee =>
          employee.factory_id === parseInt(this.factoryFilter)
        )
      }

      // Lọc theo trạng thái
      if (this.statusFilter) {
        result = result.filter(employee =>
          employee.status === this.statusFilter
        )
      }

      // Sắp xếp
      result.sort((a, b) => {
        let valueA = a[this.sortKey]
        let valueB = b[this.sortKey]

        // Xử lý các trường hợp đặc biệt
        if (this.sortKey === 'hire_date') {
          valueA = new Date(valueA)
          valueB = new Date(valueB)
        }

        if (this.sortOrder === 'asc') {
          return valueA > valueB ? 1 : -1
        } else {
          return valueA < valueB ? 1 : -1
        }
      })

      return result
    },
    paginatedEmployees() {
      const start = (this.currentPage - 1) * this.perPage
      const end = start + this.perPage
      return this.filteredEmployees.slice(start, end)
    },
    totalPages() {
      return Math.ceil(this.filteredEmployees.length / this.perPage)
    },
    displayedPages() {
      const pages = []
      const maxPagesToShow = 5

      if (this.totalPages <= maxPagesToShow) {
        // Hiển thị tất cả các trang nếu tổng số trang ít hơn hoặc bằng maxPagesToShow
        for (let i = 1; i <= this.totalPages; i++) {
          pages.push(i)
        }
      } else {
        // Hiển thị một số trang giới hạn
        let startPage = Math.max(1, this.currentPage - Math.floor(maxPagesToShow / 2))
        let endPage = startPage + maxPagesToShow - 1

        if (endPage > this.totalPages) {
          endPage = this.totalPages
          startPage = Math.max(1, endPage - maxPagesToShow + 1)
        }

        for (let i = startPage; i <= endPage; i++) {
          pages.push(i)
        }
      }

      return pages
    },
    paginationInfo() {
      const from = this.filteredEmployees.length === 0
        ? 0
        : (this.currentPage - 1) * this.perPage + 1

      const to = Math.min(from + this.perPage - 1, this.filteredEmployees.length)

      return { from, to }
    }
  },
  created() {
    this.fetchEmployees()
  },
  methods: {
    ...mapActions({
      fetchAllEmployees: 'employees/fetchEmployees',
      removeEmployee: 'employees/deleteEmployee',
      fetchAllDepartments: 'departments/fetchDepartments',
      fetchAllFactories: 'factories/fetchFactories'
    }),
    async fetchEmployees() {
      this.loading = true

      try {
        // Lấy danh sách nhân viên từ API
        await this.fetchAllEmployees({
          page: this.currentPage,
          limit: this.perPage,
          search: this.searchQuery,
          department: this.departmentFilter,
          factory: this.factoryFilter,
          status: this.statusFilter
        })

        // Lấy danh sách phòng ban và xí nghiệp
        await Promise.all([
          this.fetchAllDepartments(),
          this.fetchAllFactories()
        ])

        // Cập nhật dữ liệu local từ store
        this.employees = this.employeesData
        this.departments = this.departmentsData
        this.factories = this.factoriesData
      } catch (error) {
        console.error('Error fetching data:', error)
      } finally {
        this.loading = false
      }
    },
    refreshData() {
      this.fetchEmployees()
    },
    handleSearch: debounce(function() {
      this.currentPage = 1
    }, 300),
    applyFilters() {
      this.currentPage = 1
    },
    sortBy(key) {
      if (this.sortKey === key) {
        // Nếu đang sắp xếp theo key này, đảo ngược thứ tự
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc'
      } else {
        // Nếu sắp xếp theo key mới, mặc định là tăng dần
        this.sortKey = key
        this.sortOrder = 'asc'
      }
    },
    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
      }
    },
    formatDate(dateString) {
      if (!dateString) return null

      const date = new Date(dateString)
      return date.toLocaleDateString('vi-VN')
    },
    getStatusText(status) {
      switch (status) {
        case 'active':
          return 'Đang làm việc'
        case 'probation':
          return 'Thử việc'
        case 'terminated':
          return 'Đã nghỉ việc'
        default:
          return 'Không xác định'
      }
    },
    confirmDelete(employee) {
      this.employeeToDelete = employee
      this.showDeleteConfirm = true
    },
    async deleteEmployee() {
      if (!this.employeeToDelete) return

      this.loading = true

      try {
        // Gọi API để xóa nhân viên
        await this.removeEmployee(this.employeeToDelete.id)

        // Cập nhật lại danh sách nhân viên từ store
        this.employees = this.employeesData

        // Hiển thị thông báo thành công
        this.$store.dispatch('setSuccess', `Đã xóa nhân viên ${this.employeeToDelete.full_name} thành công`)
      } catch (error) {
        console.error('Error deleting employee:', error)
        this.$store.dispatch('setError', 'Không thể xóa nhân viên. Vui lòng thử lại sau.')
      } finally {
        this.loading = false
        this.showDeleteConfirm = false
        this.employeeToDelete = null
      }
    },
    cancelDelete() {
      this.showDeleteConfirm = false
      this.employeeToDelete = null
    }
  }
}
</script>

<style lang="scss" scoped>
.employee-list {
  .card {
    border: none;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  }

  .table {
    margin-bottom: 0;

    th.sortable {
      cursor: pointer;

      &:hover {
        background-color: rgba(0, 0, 0, 0.05);
      }
    }
  }

  .avatar-sm {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    overflow: hidden;

    .avatar-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .avatar-placeholder {
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: #e9ecef;
      color: #6c757d;
    }
  }

  .btn-primary {
    background: linear-gradient(90deg, var(--primary-color, #003366) 0%, var(--accent-color, #ff6600) 100%);
    border: none;
    padding: 0.5rem 1.5rem;
    font-weight: 500;
    transition: all 0.3s ease;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
  }

  .pagination {
    .page-link {
      color: var(--primary-color, #003366);
      border-color: #dee2e6;

      &:hover {
        background-color: #e9ecef;
      }
    }

    .active .page-link {
      background-color: var(--primary-color, #003366);
      border-color: var(--primary-color, #003366);
      color: white;
    }
  }
}
</style>
