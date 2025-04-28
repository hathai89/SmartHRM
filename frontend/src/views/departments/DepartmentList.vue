<template>
  <div class="department-list">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="h3">Danh sách phòng ban</h1>
      <div class="d-flex">
        <button class="btn btn-outline-secondary me-2" @click="refreshData">
          <font-awesome-icon icon="sync" :class="{ 'fa-spin': loading }" />
          Làm mới
        </button>
        <button class="btn btn-primary" @click="openCreateModal">
          <font-awesome-icon icon="plus" class="me-2" />
          Thêm phòng ban
        </button>
      </div>
    </div>

    <div class="card mb-4">
      <div class="card-body">
        <div class="row mb-3">
          <div class="col-md-6 mb-2">
            <div class="input-group">
              <span class="input-group-text">
                <font-awesome-icon icon="search" />
              </span>
              <input
                type="text"
                class="form-control"
                v-model="searchQuery"
                placeholder="Tìm kiếm phòng ban..."
                @input="handleSearch"
              >
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading">
      <loading-spinner />
    </div>

    <template v-else>
      <div class="row">
        <div class="col-lg-4 mb-4" v-for="(department, index) in validFilteredDepartments" :key="department.id || index">
          <div class="card h-100 department-card">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0">{{ department.name }}</h5>
              <div class="dropdown">
                <button class="btn btn-sm btn-outline-secondary" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
                  <font-awesome-icon icon="ellipsis-v" />
                </button>
                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton">
                  <li>
                    <a class="dropdown-item" href="#" @click.prevent="openEditModal(department)">
                      <font-awesome-icon icon="edit" class="me-2" />
                      Chỉnh sửa
                    </a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="#" @click.prevent="openViewModal(department)">
                      <font-awesome-icon icon="eye" class="me-2" />
                      Xem chi tiết
                    </a>
                  </li>
                  <li><hr class="dropdown-divider"></li>
                  <li>
                    <a class="dropdown-item text-danger" href="#" @click.prevent="confirmDelete(department)">
                      <font-awesome-icon icon="trash-alt" class="me-2" />
                      Xóa
                    </a>
                  </li>
                </ul>
              </div>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <div class="text-muted small mb-1">Mã phòng ban</div>
                <div>{{ department.code }}</div>
              </div>
              <div class="mb-3">
                <div class="text-muted small mb-1">Trưởng phòng</div>
                <div>{{ department.manager || 'Chưa có' }}</div>
              </div>
              <div class="mb-3">
                <div class="text-muted small mb-1">Số nhân viên</div>
                <div>{{ department.employee_count || 0 }}</div>
              </div>
              <div>
                <div class="text-muted small mb-1">Mô tả</div>
                <div class="description-text">{{ department.description || 'Không có mô tả' }}</div>
              </div>
            </div>
            <div class="card-footer">
              <button class="btn btn-sm btn-outline-primary w-100" @click="viewEmployees(department)">
                <font-awesome-icon icon="users" class="me-2" />
                Xem danh sách nhân viên
              </button>
            </div>
          </div>
        </div>

        <div class="col-12" v-if="filteredDepartments.length === 0">
          <div class="alert alert-info text-center">
            Không tìm thấy phòng ban nào
          </div>
        </div>
      </div>
    </template>

    <!-- Modal thêm/chỉnh sửa phòng ban -->
    <div class="modal fade" id="departmentModal" tabindex="-1" aria-labelledby="departmentModalLabel" aria-hidden="true" ref="departmentModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="departmentModalLabel">{{ isEdit ? 'Chỉnh sửa phòng ban' : 'Thêm phòng ban mới' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <alert-message
              v-if="error"
              type="danger"
              :message="error"
              @dismissed="clearError"
            />

            <form @submit.prevent="saveDepartment">
              <div class="mb-3">
                <label for="departmentCode" class="form-label">Mã phòng ban <span class="text-danger">*</span></label>
                <input
                  type="text"
                  class="form-control"
                  id="departmentCode"
                  v-model="formData.code"
                  required
                  :disabled="isEdit"
                >
              </div>
              <div class="mb-3">
                <label for="departmentName" class="form-label">Tên phòng ban <span class="text-danger">*</span></label>
                <input
                  type="text"
                  class="form-control"
                  id="departmentName"
                  v-model="formData.name"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="departmentManager" class="form-label">Trưởng phòng</label>
                <select class="form-select" id="departmentManager" v-model="formData.manager_id">
                  <option value="">-- Chọn trưởng phòng --</option>
                  <option v-for="employee in employees" :key="employee.id" :value="employee.id">
                    {{ employee.full_name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label for="departmentDescription" class="form-label">Mô tả</label>
                <textarea
                  class="form-control"
                  id="departmentDescription"
                  rows="3"
                  v-model="formData.description"
                ></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Hủy</button>
            <button
              type="button"
              class="btn btn-primary"
              @click="saveDepartment"
              :disabled="saving"
            >
              <span v-if="saving" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              {{ isEdit ? 'Cập nhật' : 'Thêm mới' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal xem chi tiết phòng ban -->
    <div class="modal fade" id="viewDepartmentModal" tabindex="-1" aria-labelledby="viewDepartmentModalLabel" aria-hidden="true" ref="viewDepartmentModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="viewDepartmentModalLabel">Chi tiết phòng ban</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body" v-if="selectedDepartment">
            <div class="mb-3">
              <div class="text-muted small mb-1">Mã phòng ban</div>
              <div class="fw-bold">{{ selectedDepartment.code }}</div>
            </div>
            <div class="mb-3">
              <div class="text-muted small mb-1">Tên phòng ban</div>
              <div class="fw-bold">{{ selectedDepartment.name }}</div>
            </div>
            <div class="mb-3">
              <div class="text-muted small mb-1">Trưởng phòng</div>
              <div class="fw-bold">{{ selectedDepartment.manager || 'Chưa có' }}</div>
            </div>
            <div class="mb-3">
              <div class="text-muted small mb-1">Số nhân viên</div>
              <div class="fw-bold">{{ selectedDepartment.employee_count || 0 }}</div>
            </div>
            <div class="mb-3">
              <div class="text-muted small mb-1">Mô tả</div>
              <div>{{ selectedDepartment.description || 'Không có mô tả' }}</div>
            </div>
            <div class="mb-3">
              <div class="text-muted small mb-1">Ngày tạo</div>
              <div>{{ formatDate(selectedDepartment.created_at) }}</div>
            </div>
            <div>
              <div class="text-muted small mb-1">Cập nhật lần cuối</div>
              <div>{{ formatDate(selectedDepartment.updated_at) }}</div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Đóng</button>
            <button
              type="button"
              class="btn btn-primary"
              @click="openEditModal(selectedDepartment)"
              data-bs-dismiss="modal"
            >
              <font-awesome-icon icon="edit" class="me-2" />
              Chỉnh sửa
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal xác nhận xóa phòng ban -->
    <confirm-dialog
      v-if="showDeleteConfirm"
      title="Xác nhận xóa phòng ban"
      :message="'Bạn có chắc chắn muốn xóa phòng ban ' + (departmentToDelete ? departmentToDelete.name : '') + '?'"
      @confirm="deleteDepartment"
      @cancel="cancelDelete"
    />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import AlertMessage from '@/components/common/AlertMessage.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import { breadcrumbMixin } from '@/utils/breadcrumb'
import debounce from 'lodash/debounce'
import { Modal } from 'bootstrap'

export default {
  name: 'DepartmentListPage',
  components: {
    LoadingSpinner,
    AlertMessage,
    ConfirmDialog
  },
  mixins: [breadcrumbMixin],
  data() {
    return {
      loading: false,
      saving: false,
      error: null,
      searchQuery: '',
      isEdit: false,
      formData: {
        code: '',
        name: '',
        manager_id: '',
        description: ''
      },
      departmentModal: null,
      viewDepartmentModal: null,
      selectedDepartment: null,
      showDeleteConfirm: false,
      departmentToDelete: null,
      departments: [],
      employees: []
    }
  },
  computed: {
    ...mapGetters({
      departmentsData: 'departments/allDepartments',
      isLoading: 'departments/isLoading',
      employeesData: 'employees/allEmployees'
    }),
    filteredDepartments() {
      // Đảm bảo this.departments là một mảng
      if (!this.departments || !Array.isArray(this.departments)) {
        return []
      }

      // Lọc bỏ các phần tử null hoặc undefined
      const validDepartments = this.departments.filter(department => department != null)

      if (!this.searchQuery) {
        return validDepartments
      }

      const query = this.searchQuery.toLowerCase()
      return validDepartments.filter(department =>
        department.code.toLowerCase().includes(query) ||
        department.name.toLowerCase().includes(query) ||
        (department.manager && department.manager.toLowerCase().includes(query)) ||
        (department.description && department.description.toLowerCase().includes(query))
      )
    },
    validFilteredDepartments() {
      // Đảm bảo this.filteredDepartments là một mảng
      if (!this.filteredDepartments || !Array.isArray(this.filteredDepartments)) {
        return []
      }

      return this.filteredDepartments.filter(department => department != null)
    }
  },
  mounted() {
    this.initModals()
    this.fetchDepartments()
  },
  methods: {
    ...mapActions({
      fetchAllDepartments: 'departments/fetchDepartments',
      createDepartment: 'departments/createDepartment',
      updateDepartment: 'departments/updateDepartment',
      removeDepartment: 'departments/deleteDepartment',
      fetchAllEmployees: 'employees/fetchEmployees',
      setError: 'setError',
      clearError: 'clearError',
      setSuccess: 'setSuccess',
      clearSuccess: 'clearSuccess'
    }),
    initModals() {
      // Khởi tạo các modal Bootstrap
      this.$nextTick(() => {
        this.departmentModal = new Modal(this.$refs.departmentModal)
        this.viewDepartmentModal = new Modal(this.$refs.viewDepartmentModal)
      })
    },
    async fetchDepartments() {
      this.loading = true

      try {
        // Lấy danh sách phòng ban từ API
        await this.fetchAllDepartments()

        // Lấy danh sách nhân viên để hiển thị tên trưởng phòng
        await this.fetchAllEmployees({
          page: 1,
          limit: 100 // Lấy đủ nhân viên để có thể chọn làm trưởng phòng
        })

        // Cập nhật dữ liệu local từ store
        this.departments = this.departmentsData
        this.employees = this.employeesData
      } catch (error) {
        console.error('Error fetching departments:', error)
        this.setError('Không thể tải danh sách phòng ban. Vui lòng thử lại sau.')
      } finally {
        this.loading = false
      }
    },
    refreshData() {
      this.fetchDepartments()
    },
    handleSearch: debounce(function() {
      // Không cần làm gì vì chúng ta đã sử dụng computed property
    }, 300),
    openCreateModal() {
      this.isEdit = false
      this.formData = {
        code: this.generateDepartmentCode(),
        name: '',
        manager_id: '',
        description: ''
      }
      this.error = null
      this.departmentModal.show()
    },
    openEditModal(department) {
      this.isEdit = true
      this.formData = {
        id: department.id,
        code: department.code,
        name: department.name,
        manager_id: department.manager_id,
        description: department.description
      }
      this.error = null

      // Đóng modal xem chi tiết nếu đang mở
      if (this.viewDepartmentModal._isShown) {
        this.viewDepartmentModal.hide()
      }

      this.departmentModal.show()
    },
    openViewModal(department) {
      this.selectedDepartment = department
      this.viewDepartmentModal.show()
    },
    generateDepartmentCode() {
      // Trong thực tế, bạn sẽ gọi API để lấy mã phòng ban mới
      // Ở đây chúng ta giả lập
      const randomChars = Math.random().toString(36).substring(2, 4).toUpperCase()
      return randomChars
    },
    async saveDepartment() {
      this.saving = true
      this.error = null

      try {
        // Chuẩn bị dữ liệu
        const departmentData = { ...this.formData }

        if (this.isEdit) {
          // Cập nhật phòng ban qua API
          await this.updateDepartment({ id: departmentData.id, data: departmentData })
          this.setSuccess('Cập nhật phòng ban thành công.')
        } else {
          // Thêm phòng ban mới qua API
          await this.createDepartment(departmentData)
          this.setSuccess('Thêm phòng ban mới thành công.')
        }

        // Cập nhật lại danh sách phòng ban từ API
        await this.fetchDepartments()

        // Đóng modal
        this.departmentModal.hide()
      } catch (error) {
        console.error('Error saving department:', error)
        this.error = this.isEdit
          ? 'Không thể cập nhật phòng ban. Vui lòng thử lại sau.'
          : 'Không thể thêm phòng ban mới. Vui lòng thử lại sau.'
      } finally {
        this.saving = false
      }
    },
    confirmDelete(department) {
      this.departmentToDelete = department
      this.showDeleteConfirm = true
    },
    async deleteDepartment() {
      if (!this.departmentToDelete) return

      this.loading = true

      try {
        // Gọi API để xóa phòng ban
        await this.removeDepartment(this.departmentToDelete.id)

        // Cập nhật lại danh sách phòng ban từ API
        await this.fetchDepartments()

        // Hiển thị thông báo thành công
        this.setSuccess(`Đã xóa phòng ban ${this.departmentToDelete.name} thành công`)
      } catch (error) {
        console.error('Error deleting department:', error)
        this.setError('Không thể xóa phòng ban. Vui lòng thử lại sau.')
      } finally {
        this.loading = false
        this.showDeleteConfirm = false
        this.departmentToDelete = null
      }
    },
    cancelDelete() {
      this.showDeleteConfirm = false
      this.departmentToDelete = null
    },
    viewEmployees(department) {
      // Trong thực tế, bạn sẽ chuyển hướng đến trang danh sách nhân viên với bộ lọc phòng ban
      this.$router.push({
        path: '/employees',
        query: { department: department.id }
      })
    },
    formatDate(dateString) {
      if (!dateString) return null

      const date = new Date(dateString)
      return date.toLocaleDateString('vi-VN')
    }
  }
}
</script>

<style lang="scss" scoped>
.department-list {
  .card {
    border: none;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  }

  .department-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;

    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }

    .card-header {
      background-color: #f8f9fa;
      border-bottom: 1px solid rgba(0, 0, 0, 0.1);
      padding: 1rem 1.5rem;
    }

    .card-body {
      padding: 1.5rem;
    }

    .card-footer {
      background-color: #f8f9fa;
      border-top: 1px solid rgba(0, 0, 0, 0.1);
      padding: 1rem 1.5rem;
    }

    .description-text {
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      text-overflow: ellipsis;
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

    &:disabled {
      background: #6c757d;
      transform: none;
      box-shadow: none;
    }
  }
}
</style>
