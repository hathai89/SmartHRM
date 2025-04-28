<template>
  <div class="factory-list">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="h3">Danh sách xí nghiệp</h1>
      <div class="d-flex">
        <button class="btn btn-outline-secondary me-2" @click="refreshData">
          <font-awesome-icon icon="sync" :class="{ 'fa-spin': loading }" />
          Làm mới
        </button>
        <button class="btn btn-primary" @click="openCreateModal">
          <font-awesome-icon icon="plus" class="me-2" />
          Thêm xí nghiệp
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
                placeholder="Tìm kiếm xí nghiệp..."
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
        <div class="col-lg-4 mb-4" v-for="(factory, index) in validFilteredFactories" :key="factory.id || index">
          <div class="card h-100 factory-card">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0">{{ factory.name }}</h5>
              <div class="dropdown">
                <button class="btn btn-sm btn-outline-secondary" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
                  <font-awesome-icon icon="ellipsis-v" />
                </button>
                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton">
                  <li>
                    <a class="dropdown-item" href="#" @click.prevent="openEditModal(factory)">
                      <font-awesome-icon icon="edit" class="me-2" />
                      Chỉnh sửa
                    </a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="#" @click.prevent="openViewModal(factory)">
                      <font-awesome-icon icon="eye" class="me-2" />
                      Xem chi tiết
                    </a>
                  </li>
                  <li><hr class="dropdown-divider"></li>
                  <li>
                    <a class="dropdown-item text-danger" href="#" @click.prevent="confirmDelete(factory)">
                      <font-awesome-icon icon="trash-alt" class="me-2" />
                      Xóa
                    </a>
                  </li>
                </ul>
              </div>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <div class="text-muted small mb-1">Mã xí nghiệp</div>
                <div>{{ factory.code }}</div>
              </div>
              <div class="mb-3">
                <div class="text-muted small mb-1">Quản đốc</div>
                <div>{{ factory.manager || 'Chưa có' }}</div>
              </div>
              <div class="mb-3">
                <div class="text-muted small mb-1">Địa chỉ</div>
                <div class="address-text">{{ factory.address || 'Chưa cập nhật' }}</div>
              </div>
              <div class="mb-3">
                <div class="text-muted small mb-1">Số nhân viên</div>
                <div>{{ factory.employee_count || 0 }}</div>
              </div>
              <div>
                <div class="text-muted small mb-1">Mô tả</div>
                <div class="description-text">{{ factory.description || 'Không có mô tả' }}</div>
              </div>
            </div>
            <div class="card-footer">
              <button class="btn btn-sm btn-outline-primary w-100" @click="viewEmployees(factory)">
                <font-awesome-icon icon="users" class="me-2" />
                Xem danh sách nhân viên
              </button>
            </div>
          </div>
        </div>

        <div class="col-12" v-if="filteredFactories.length === 0">
          <div class="alert alert-info text-center">
            Không tìm thấy xí nghiệp nào
          </div>
        </div>
      </div>
    </template>

    <!-- Modal thêm/chỉnh sửa xí nghiệp -->
    <div class="modal fade" id="factoryModal" tabindex="-1" aria-labelledby="factoryModalLabel" aria-hidden="true" ref="factoryModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="factoryModalLabel">{{ isEdit ? 'Chỉnh sửa xí nghiệp' : 'Thêm xí nghiệp mới' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <alert-message
              v-if="error"
              type="danger"
              :message="error"
              @dismissed="clearError"
            />

            <form @submit.prevent="saveFactory">
              <div class="mb-3">
                <label for="factoryCode" class="form-label">Mã xí nghiệp <span class="text-danger">*</span></label>
                <input
                  type="text"
                  class="form-control"
                  id="factoryCode"
                  v-model="formData.code"
                  required
                  :disabled="isEdit"
                >
              </div>
              <div class="mb-3">
                <label for="factoryName" class="form-label">Tên xí nghiệp <span class="text-danger">*</span></label>
                <input
                  type="text"
                  class="form-control"
                  id="factoryName"
                  v-model="formData.name"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="factoryManager" class="form-label">Quản đốc</label>
                <select class="form-select" id="factoryManager" v-model="formData.manager_id">
                  <option value="">-- Chọn quản đốc --</option>
                  <option v-for="employee in employees" :key="employee.id" :value="employee.id">
                    {{ employee.full_name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label for="factoryAddress" class="form-label">Địa chỉ</label>
                <textarea
                  class="form-control"
                  id="factoryAddress"
                  rows="2"
                  v-model="formData.address"
                ></textarea>
              </div>
              <div class="mb-3">
                <label for="factoryDescription" class="form-label">Mô tả</label>
                <textarea
                  class="form-control"
                  id="factoryDescription"
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
              @click="saveFactory"
              :disabled="saving"
            >
              <span v-if="saving" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              {{ isEdit ? 'Cập nhật' : 'Thêm mới' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal xem chi tiết xí nghiệp -->
    <div class="modal fade" id="viewFactoryModal" tabindex="-1" aria-labelledby="viewFactoryModalLabel" aria-hidden="true" ref="viewFactoryModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="viewFactoryModalLabel">Chi tiết xí nghiệp</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body" v-if="selectedFactory">
            <div class="mb-3">
              <div class="text-muted small mb-1">Mã xí nghiệp</div>
              <div class="fw-bold">{{ selectedFactory.code }}</div>
            </div>
            <div class="mb-3">
              <div class="text-muted small mb-1">Tên xí nghiệp</div>
              <div class="fw-bold">{{ selectedFactory.name }}</div>
            </div>
            <div class="mb-3">
              <div class="text-muted small mb-1">Quản đốc</div>
              <div class="fw-bold">{{ selectedFactory.manager || 'Chưa có' }}</div>
            </div>
            <div class="mb-3">
              <div class="text-muted small mb-1">Địa chỉ</div>
              <div>{{ selectedFactory.address || 'Chưa cập nhật' }}</div>
            </div>
            <div class="mb-3">
              <div class="text-muted small mb-1">Số nhân viên</div>
              <div class="fw-bold">{{ selectedFactory.employee_count || 0 }}</div>
            </div>
            <div class="mb-3">
              <div class="text-muted small mb-1">Mô tả</div>
              <div>{{ selectedFactory.description || 'Không có mô tả' }}</div>
            </div>
            <div class="mb-3">
              <div class="text-muted small mb-1">Ngày tạo</div>
              <div>{{ formatDate(selectedFactory.created_at) }}</div>
            </div>
            <div>
              <div class="text-muted small mb-1">Cập nhật lần cuối</div>
              <div>{{ formatDate(selectedFactory.updated_at) }}</div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Đóng</button>
            <button
              type="button"
              class="btn btn-primary"
              @click="openEditModal(selectedFactory)"
              data-bs-dismiss="modal"
            >
              <font-awesome-icon icon="edit" class="me-2" />
              Chỉnh sửa
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal xác nhận xóa xí nghiệp -->
    <confirm-dialog
      v-if="showDeleteConfirm"
      title="Xác nhận xóa xí nghiệp"
      :message="'Bạn có chắc chắn muốn xóa xí nghiệp ' + (factoryToDelete ? factoryToDelete.name : '') + '?'"
      @confirm="deleteFactory"
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
  name: 'FactoryListPage',
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
        address: '',
        description: ''
      },
      factoryModal: null,
      viewFactoryModal: null,
      selectedFactory: null,
      showDeleteConfirm: false,
      factoryToDelete: null,
      factories: [],
      employees: []
    }
  },
  computed: {
    ...mapGetters({
      factoriesData: 'factories/allFactories',
      isLoading: 'factories/isLoading',
      employeesData: 'employees/allEmployees'
    }),
    filteredFactories() {
      // Đảm bảo this.factories là một mảng
      if (!this.factories || !Array.isArray(this.factories)) {
        return []
      }

      // Lọc bỏ các phần tử null hoặc undefined
      const validFactories = this.factories.filter(factory => factory != null)

      if (!this.searchQuery) {
        return validFactories
      }

      const query = this.searchQuery.toLowerCase()
      return validFactories.filter(factory =>
        factory.code.toLowerCase().includes(query) ||
        factory.name.toLowerCase().includes(query) ||
        (factory.manager && factory.manager.toLowerCase().includes(query)) ||
        (factory.address && factory.address.toLowerCase().includes(query)) ||
        (factory.description && factory.description.toLowerCase().includes(query))
      )
    },
    validFilteredFactories() {
      // Đảm bảo this.filteredFactories là một mảng
      if (!this.filteredFactories || !Array.isArray(this.filteredFactories)) {
        return []
      }

      return this.filteredFactories.filter(factory => factory != null)
    }
  },
  mounted() {
    this.initModals()
    this.fetchFactories()
  },
  methods: {
    ...mapActions({
      fetchAllFactories: 'factories/fetchFactories',
      createFactory: 'factories/createFactory',
      updateFactory: 'factories/updateFactory',
      removeFactory: 'factories/deleteFactory',
      fetchAllEmployees: 'employees/fetchEmployees',
      setError: 'setError',
      clearError: 'clearError',
      setSuccess: 'setSuccess',
      clearSuccess: 'clearSuccess'
    }),
    initModals() {
      // Khởi tạo các modal Bootstrap
      this.$nextTick(() => {
        this.factoryModal = new Modal(this.$refs.factoryModal)
        this.viewFactoryModal = new Modal(this.$refs.viewFactoryModal)
      })
    },
    async fetchFactories() {
      this.loading = true

      try {
        // Lấy danh sách xí nghiệp từ API
        await this.fetchAllFactories()

        // Lấy danh sách nhân viên để hiển thị tên quản đốc
        await this.fetchAllEmployees({
          page: 1,
          limit: 100 // Lấy đủ nhân viên để có thể chọn làm quản đốc
        })

        // Cập nhật dữ liệu local từ store
        this.factories = this.factoriesData
        this.employees = this.employeesData
      } catch (error) {
        console.error('Error fetching factories:', error)
        this.setError('Không thể tải danh sách xí nghiệp. Vui lòng thử lại sau.')
      } finally {
        this.loading = false
      }
    },
    refreshData() {
      this.fetchFactories()
    },
    handleSearch: debounce(function() {
      // Không cần làm gì vì chúng ta đã sử dụng computed property
    }, 300),
    openCreateModal() {
      this.isEdit = false
      this.formData = {
        code: this.generateFactoryCode(),
        name: '',
        manager_id: '',
        address: '',
        description: ''
      }
      this.error = null
      this.factoryModal.show()
    },
    openEditModal(factory) {
      this.isEdit = true
      this.formData = {
        id: factory.id,
        code: factory.code,
        name: factory.name,
        manager_id: factory.manager_id,
        address: factory.address,
        description: factory.description
      }
      this.error = null

      // Đóng modal xem chi tiết nếu đang mở
      if (this.viewFactoryModal && this.viewFactoryModal._isShown) {
        this.viewFactoryModal.hide()
      }

      this.factoryModal.show()
    },
    openViewModal(factory) {
      this.selectedFactory = factory
      this.viewFactoryModal.show()
    },
    generateFactoryCode() {
      // Trong thực tế, bạn sẽ gọi API để lấy mã xí nghiệp mới
      // Ở đây chúng ta giả lập
      const randomNum = Math.floor(Math.random() * 100).toString().padStart(2, '0')
      return `XN${randomNum}`
    },
    async saveFactory() {
      this.saving = true
      this.error = null

      try {
        // Chuẩn bị dữ liệu
        const factoryData = { ...this.formData }

        if (this.isEdit) {
          // Cập nhật xí nghiệp qua API
          await this.updateFactory({ id: factoryData.id, data: factoryData })
          this.setSuccess('Cập nhật xí nghiệp thành công.')
        } else {
          // Thêm xí nghiệp mới qua API
          await this.createFactory(factoryData)
          this.setSuccess('Thêm xí nghiệp mới thành công.')
        }

        // Cập nhật lại danh sách xí nghiệp từ API
        await this.fetchFactories()

        // Đóng modal
        this.factoryModal.hide()
      } catch (error) {
        console.error('Error saving factory:', error)
        this.error = this.isEdit
          ? 'Không thể cập nhật xí nghiệp. Vui lòng thử lại sau.'
          : 'Không thể thêm xí nghiệp mới. Vui lòng thử lại sau.'
      } finally {
        this.saving = false
      }
    },
    confirmDelete(factory) {
      this.factoryToDelete = factory
      this.showDeleteConfirm = true
    },
    async deleteFactory() {
      if (!this.factoryToDelete) return

      this.loading = true

      try {
        // Gọi API để xóa xí nghiệp
        await this.removeFactory(this.factoryToDelete.id)

        // Cập nhật lại danh sách xí nghiệp từ API
        await this.fetchFactories()

        // Hiển thị thông báo thành công
        this.setSuccess(`Đã xóa xí nghiệp ${this.factoryToDelete.name} thành công`)
      } catch (error) {
        console.error('Error deleting factory:', error)
        this.setError('Không thể xóa xí nghiệp. Vui lòng thử lại sau.')
      } finally {
        this.loading = false
        this.showDeleteConfirm = false
        this.factoryToDelete = null
      }
    },
    cancelDelete() {
      this.showDeleteConfirm = false
      this.factoryToDelete = null
    },
    viewEmployees(factory) {
      // Trong thực tế, bạn sẽ chuyển hướng đến trang danh sách nhân viên với bộ lọc xí nghiệp
      this.$router.push({
        path: '/employees',
        query: { factory: factory.id }
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
.factory-list {
  .card {
    border: none;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  }

  .factory-card {
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

    .description-text, .address-text {
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
