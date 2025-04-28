<template>
  <div class="document-list">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="h3">Quản lý tài liệu</h1>
      <div class="d-flex">
        <button class="btn btn-outline-secondary me-2" @click="refreshData">
          <font-awesome-icon icon="sync" :class="{ 'fa-spin': loading }" />
          Làm mới
        </button>
        <button class="btn btn-primary" @click="openUploadModal">
          <font-awesome-icon icon="upload" class="me-2" />
          Tải lên tài liệu
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
                placeholder="Tìm kiếm tài liệu..."
                @input="handleSearch"
              >
            </div>
          </div>
          <div class="col-md-3 mb-2">
            <select class="form-select" v-model="categoryFilter" @change="handleFilterChange">
              <option value="">Tất cả danh mục</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
          </div>
          <div class="col-md-3 mb-2">
            <select class="form-select" v-model="sortOption" @change="handleSortChange">
              <option value="newest">Mới nhất</option>
              <option value="oldest">Cũ nhất</option>
              <option value="name_asc">Tên (A-Z)</option>
              <option value="name_desc">Tên (Z-A)</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading">
      <loading-spinner />
    </div>

    <template v-else>
      <div class="row">
        <div class="col-lg-4 mb-4" v-for="(document, index) in validFilteredDocuments" :key="document.id || index">
          <div class="card h-100 document-card">
            <div class="card-header d-flex justify-content-between align-items-center">
              <div class="document-icon">
                <font-awesome-icon :icon="getDocumentIcon(document.file_type)" size="lg" />
              </div>
              <div class="dropdown">
                <button class="btn btn-sm btn-outline-secondary" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
                  <font-awesome-icon icon="ellipsis-v" />
                </button>
                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton">
                  <li>
                    <a class="dropdown-item" href="#" @click.prevent="downloadDocument(document)">
                      <font-awesome-icon icon="download" class="me-2" />
                      Tải xuống
                    </a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="#" @click.prevent="openViewModal(document)">
                      <font-awesome-icon icon="eye" class="me-2" />
                      Xem chi tiết
                    </a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="#" @click.prevent="openEditModal(document)">
                      <font-awesome-icon icon="edit" class="me-2" />
                      Chỉnh sửa
                    </a>
                  </li>
                  <li><hr class="dropdown-divider"></li>
                  <li>
                    <a class="dropdown-item text-danger" href="#" @click.prevent="confirmDelete(document)">
                      <font-awesome-icon icon="trash-alt" class="me-2" />
                      Xóa
                    </a>
                  </li>
                </ul>
              </div>
            </div>
            <div class="card-body">
              <h5 class="card-title text-truncate">{{ document.name }}</h5>
              <div class="mb-2">
                <span class="badge bg-primary">{{ getCategoryName(document.category_id) }}</span>
                <span class="badge bg-secondary ms-1">{{ document.file_type }}</span>
              </div>
              <div class="mb-2 small text-muted">
                <font-awesome-icon icon="user" class="me-1" />
                {{ document.uploaded_by }}
              </div>
              <div class="mb-2 small text-muted">
                <font-awesome-icon icon="calendar-alt" class="me-1" />
                {{ formatDate(document.upload_date) }}
              </div>
              <div class="mb-2 small text-muted">
                <font-awesome-icon icon="file" class="me-1" />
                {{ formatFileSize(document.file_size) }}
              </div>
              <p class="card-text description-text">{{ document.description || 'Không có mô tả' }}</p>
            </div>
            <div class="card-footer">
              <div class="d-grid gap-2">
                <button class="btn btn-sm btn-outline-primary" @click="downloadDocument(document)">
                  <font-awesome-icon icon="download" class="me-2" />
                  Tải xuống
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="col-12" v-if="filteredDocuments.length === 0">
          <div class="alert alert-info text-center">
            Không tìm thấy tài liệu nào
          </div>
        </div>
      </div>
    </template>

    <!-- Modal tải lên tài liệu -->
    <div class="modal fade" id="uploadModal" tabindex="-1" aria-labelledby="uploadModalLabel" aria-hidden="true" ref="uploadModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="uploadModalLabel">Tải lên tài liệu mới</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <alert-message
              v-if="error"
              type="danger"
              :message="error"
              @dismissed="clearError"
            />

            <form @submit.prevent="uploadDocument">
              <div class="mb-3">
                <label for="documentName" class="form-label">Tên tài liệu <span class="text-danger">*</span></label>
                <input
                  type="text"
                  class="form-control"
                  id="documentName"
                  v-model="formData.name"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="documentCategory" class="form-label">Danh mục <span class="text-danger">*</span></label>
                <select class="form-select" id="documentCategory" v-model="formData.category_id" required>
                  <option value="">-- Chọn danh mục --</option>
                  <option v-for="category in categories" :key="category.id" :value="category.id">
                    {{ category.name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label for="documentDescription" class="form-label">Mô tả</label>
                <textarea
                  class="form-control"
                  id="documentDescription"
                  rows="3"
                  v-model="formData.description"
                ></textarea>
              </div>
              <div class="mb-3">
                <label for="documentFile" class="form-label">Tệp <span class="text-danger">*</span></label>
                <div class="input-group">
                  <input
                    type="file"
                    class="form-control"
                    id="documentFile"
                    ref="fileInput"
                    @change="handleFileChange"
                    required
                  >
                </div>
                <div class="form-text" v-if="selectedFile">
                  Kích thước: {{ formatFileSize(selectedFile.size) }}
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Hủy</button>
            <button
              type="button"
              class="btn btn-primary"
              @click="uploadDocument"
              :disabled="uploading"
            >
              <span v-if="uploading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Tải lên
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal chỉnh sửa tài liệu -->
    <div class="modal fade" id="editModal" tabindex="-1" aria-labelledby="editModalLabel" aria-hidden="true" ref="editModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editModalLabel">Chỉnh sửa tài liệu</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <alert-message
              v-if="error"
              type="danger"
              :message="error"
              @dismissed="clearError"
            />

            <form @submit.prevent="updateDocument">
              <div class="mb-3">
                <label for="editDocumentName" class="form-label">Tên tài liệu <span class="text-danger">*</span></label>
                <input
                  type="text"
                  class="form-control"
                  id="editDocumentName"
                  v-model="formData.name"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="editDocumentCategory" class="form-label">Danh mục <span class="text-danger">*</span></label>
                <select class="form-select" id="editDocumentCategory" v-model="formData.category_id" required>
                  <option value="">-- Chọn danh mục --</option>
                  <option v-for="category in categories" :key="category.id" :value="category.id">
                    {{ category.name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label for="editDocumentDescription" class="form-label">Mô tả</label>
                <textarea
                  class="form-control"
                  id="editDocumentDescription"
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
              @click="updateDocument"
              :disabled="saving"
            >
              <span v-if="saving" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Cập nhật
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal xem chi tiết tài liệu -->
    <div class="modal fade" id="viewDocumentModal" tabindex="-1" aria-labelledby="viewDocumentModalLabel" aria-hidden="true" ref="viewDocumentModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="viewDocumentModalLabel">Chi tiết tài liệu</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body" v-if="selectedDocument">
            <div class="text-center mb-4">
              <div class="document-icon-lg mb-3">
                <font-awesome-icon :icon="getDocumentIcon(selectedDocument.file_type)" size="3x" />
              </div>
              <h5>{{ selectedDocument.name }}</h5>
              <div>
                <span class="badge bg-primary">{{ getCategoryName(selectedDocument.category_id) }}</span>
                <span class="badge bg-secondary ms-1">{{ selectedDocument.file_type }}</span>
              </div>
            </div>

            <div class="mb-3">
              <div class="text-muted small mb-1">Mô tả</div>
              <div>{{ selectedDocument.description || 'Không có mô tả' }}</div>
            </div>
            <div class="mb-3">
              <div class="text-muted small mb-1">Kích thước</div>
              <div>{{ formatFileSize(selectedDocument.file_size) }}</div>
            </div>
            <div class="mb-3">
              <div class="text-muted small mb-1">Người tải lên</div>
              <div>{{ selectedDocument.uploaded_by }}</div>
            </div>
            <div class="mb-3">
              <div class="text-muted small mb-1">Ngày tải lên</div>
              <div>{{ formatDate(selectedDocument.upload_date) }}</div>
            </div>
            <div class="mb-3">
              <div class="text-muted small mb-1">Cập nhật lần cuối</div>
              <div>{{ formatDate(selectedDocument.last_modified) }}</div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Đóng</button>
            <button
              type="button"
              class="btn btn-outline-primary me-2"
              @click="downloadDocument(selectedDocument)"
            >
              <font-awesome-icon icon="download" class="me-2" />
              Tải xuống
            </button>
            <button
              type="button"
              class="btn btn-primary"
              @click="openEditModal(selectedDocument)"
              data-bs-dismiss="modal"
            >
              <font-awesome-icon icon="edit" class="me-2" />
              Chỉnh sửa
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal xác nhận xóa tài liệu -->
    <confirm-dialog
      v-if="showDeleteConfirm"
      title="Xác nhận xóa tài liệu"
      :message="'Bạn có chắc chắn muốn xóa tài liệu ' + (documentToDelete ? documentToDelete.name : '') + '?'"
      @confirm="deleteDocument"
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
  name: 'DocumentListPage',
  components: {
    LoadingSpinner,
    AlertMessage,
    ConfirmDialog
  },
  mixins: [breadcrumbMixin],
  data() {
    return {
      loading: false,
      uploading: false,
      saving: false,
      error: null,
      searchQuery: '',
      categoryFilter: '',
      sortOption: 'newest',
      formData: {
        name: '',
        category_id: '',
        description: ''
      },
      selectedFile: null,
      uploadModal: null,
      editModal: null,
      viewDocumentModal: null,
      selectedDocument: null,
      showDeleteConfirm: false,
      documentToDelete: null,
      documents: [],
      categories: []
    }
  },
  computed: {
    ...mapGetters({
      documentsData: 'documents/allDocuments',
      categoriesData: 'documents/allCategories',
      isLoading: 'documents/isLoading'
    }),
    filteredDocuments() {
      // Đảm bảo this.documents là một mảng
      if (!this.documents || !Array.isArray(this.documents)) {
        return []
      }

      // Lọc bỏ các phần tử null hoặc undefined
      let result = this.documents.filter(doc => doc != null)

      // Lọc theo danh mục
      if (this.categoryFilter) {
        result = result.filter(doc => doc.category_id === parseInt(this.categoryFilter))
      }

      // Lọc theo từ khóa tìm kiếm
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        result = result.filter(doc =>
          doc.name.toLowerCase().includes(query) ||
          (doc.description && doc.description.toLowerCase().includes(query)) ||
          (doc.file_type && doc.file_type.toLowerCase().includes(query)) ||
          (doc.uploaded_by && doc.uploaded_by.toLowerCase().includes(query))
        )
      }

      // Sắp xếp
      switch (this.sortOption) {
        case 'newest':
          result.sort((a, b) => new Date(b.upload_date) - new Date(a.upload_date))
          break
        case 'oldest':
          result.sort((a, b) => new Date(a.upload_date) - new Date(b.upload_date))
          break
        case 'name_asc':
          result.sort((a, b) => a.name.localeCompare(b.name))
          break
        case 'name_desc':
          result.sort((a, b) => b.name.localeCompare(a.name))
          break
      }

      return result
    },
    validFilteredDocuments() {
      // Đảm bảo this.filteredDocuments là một mảng
      if (!this.filteredDocuments || !Array.isArray(this.filteredDocuments)) {
        return []
      }

      return this.filteredDocuments.filter(doc => doc != null)
    }
  },
  mounted() {
    this.initModals()
    this.fetchDocuments()
  },
  methods: {
    ...mapActions({
      fetchAllDocuments: 'documents/fetchDocuments',
      fetchAllCategories: 'documents/fetchCategories',
      uploadNewDocument: 'documents/uploadDocument',
      updateDocumentInfo: 'documents/updateDocument',
      removeDocument: 'documents/deleteDocument',
      setError: 'setError',
      clearError: 'clearError',
      setSuccess: 'setSuccess',
      clearSuccess: 'clearSuccess'
    }),
    initModals() {
      // Khởi tạo các modal Bootstrap
      this.$nextTick(() => {
        this.uploadModal = new Modal(this.$refs.uploadModal)
        this.editModal = new Modal(this.$refs.editModal)
        this.viewDocumentModal = new Modal(this.$refs.viewDocumentModal)
      })
    },
    async fetchDocuments() {
      this.loading = true

      try {
        // Lấy danh sách tài liệu từ API
        await this.fetchAllDocuments()

        // Lấy danh sách danh mục tài liệu từ API
        await this.fetchAllCategories()

        // Cập nhật dữ liệu local từ store
        this.documents = this.documentsData
        this.categories = this.categoriesData
      } catch (error) {
        console.error('Error fetching documents:', error)
        this.setError('Không thể tải danh sách tài liệu. Vui lòng thử lại sau.')
      } finally {
        this.loading = false
      }
    },
    refreshData() {
      this.fetchDocuments()
    },
    handleSearch: debounce(function() {
      // Không cần làm gì vì chúng ta đã sử dụng computed property
    }, 300),
    handleFilterChange() {
      // Không cần làm gì vì chúng ta đã sử dụng computed property
    },
    handleSortChange() {
      // Không cần làm gì vì chúng ta đã sử dụng computed property
    },
    openUploadModal() {
      this.formData = {
        name: '',
        category_id: '',
        description: ''
      }
      this.selectedFile = null
      this.error = null

      // Reset file input
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = ''
      }

      this.uploadModal.show()
    },
    openEditModal(document) {
      this.formData = {
        id: document.id,
        name: document.name,
        category_id: document.category_id,
        description: document.description
      }
      this.error = null

      // Đóng modal xem chi tiết nếu đang mở
      if (this.viewDocumentModal && this.viewDocumentModal._isShown) {
        this.viewDocumentModal.hide()
      }

      this.editModal.show()
    },
    openViewModal(document) {
      this.selectedDocument = document
      this.viewDocumentModal.show()
    },
    handleFileChange(event) {
      const file = event.target.files[0]
      if (!file) return

      // Kiểm tra kích thước file (tối đa 10MB)
      if (file.size > 10 * 1024 * 1024) {
        this.error = 'Kích thước file quá lớn. Vui lòng chọn file nhỏ hơn 10MB.'
        this.$refs.fileInput.value = ''
        this.selectedFile = null
        return
      }

      this.selectedFile = file

      // Tự động điền tên tài liệu nếu chưa có
      if (!this.formData.name) {
        // Lấy tên file không bao gồm phần mở rộng
        const fileName = file.name.split('.').slice(0, -1).join('.')
        this.formData.name = fileName
      }
    },
    async uploadDocument() {
      if (!this.selectedFile) {
        this.error = 'Vui lòng chọn file để tải lên.'
        return
      }

      this.uploading = true
      this.error = null

      try {
        // Chuẩn bị dữ liệu
        const formData = new FormData()
        formData.append('file', this.selectedFile)
        formData.append('name', this.formData.name)
        formData.append('category_id', this.formData.category_id)
        formData.append('description', this.formData.description || '')

        // Gọi API để tải lên tài liệu
        await this.uploadNewDocument(formData)

        // Cập nhật lại danh sách tài liệu từ API
        await this.fetchDocuments()

        // Hiển thị thông báo thành công
        this.setSuccess('Tải lên tài liệu thành công.')

        // Đóng modal
        this.uploadModal.hide()
      } catch (error) {
        console.error('Error uploading document:', error)
        this.error = 'Không thể tải lên tài liệu. Vui lòng thử lại sau.'
      } finally {
        this.uploading = false
      }
    },
    async updateDocument() {
      this.saving = true
      this.error = null

      try {
        // Chuẩn bị dữ liệu
        const documentData = { ...this.formData }

        // Gọi API để cập nhật tài liệu
        await this.updateDocumentInfo({ id: documentData.id, data: documentData })

        // Cập nhật lại danh sách tài liệu từ API
        await this.fetchDocuments()

        // Hiển thị thông báo thành công
        this.setSuccess('Cập nhật tài liệu thành công.')

        // Đóng modal
        this.editModal.hide()
      } catch (error) {
        console.error('Error updating document:', error)
        this.error = 'Không thể cập nhật tài liệu. Vui lòng thử lại sau.'
      } finally {
        this.saving = false
      }
    },
    confirmDelete(document) {
      this.documentToDelete = document
      this.showDeleteConfirm = true
    },
    async deleteDocument() {
      if (!this.documentToDelete) return

      this.loading = true

      try {
        // Gọi API để xóa tài liệu
        await this.removeDocument(this.documentToDelete.id)

        // Cập nhật lại danh sách tài liệu từ API
        await this.fetchDocuments()

        // Hiển thị thông báo thành công
        this.setSuccess(`Đã xóa tài liệu ${this.documentToDelete.name} thành công`)
      } catch (error) {
        console.error('Error deleting document:', error)
        this.setError('Không thể xóa tài liệu. Vui lòng thử lại sau.')
      } finally {
        this.loading = false
        this.showDeleteConfirm = false
        this.documentToDelete = null
      }
    },
    cancelDelete() {
      this.showDeleteConfirm = false
      this.documentToDelete = null
    },
    downloadDocument(document) {
      // Trong thực tế, bạn sẽ tải xuống tài liệu từ server
      // Ở đây chúng ta giả lập bằng cách hiển thị thông báo
      this.setSuccess(`Đang tải xuống tài liệu: ${document.name}`)

      // Giả lập tải xuống
      setTimeout(() => {
        console.log('Downloading document:', document.file_url)
      }, 1000)
    },
    getCategoryName(categoryId) {
      const category = this.categories.find(c => c.id === categoryId)
      return category ? category.name : 'Không xác định'
    },
    getDocumentIcon(fileType) {
      switch (fileType.toLowerCase()) {
        case 'pdf':
          return ['far', 'file-pdf']
        case 'docx':
        case 'doc':
          return ['far', 'file-word']
        case 'xlsx':
        case 'xls':
          return ['far', 'file-excel']
        case 'pptx':
        case 'ppt':
          return ['far', 'file-powerpoint']
        case 'jpg':
        case 'jpeg':
        case 'png':
        case 'gif':
          return ['far', 'file-image']
        case 'zip':
        case 'rar':
          return ['far', 'file-archive']
        default:
          return ['far', 'file']
      }
    },
    formatDate(dateString) {
      if (!dateString) return null

      const date = new Date(dateString)
      return date.toLocaleDateString('vi-VN')
    },
    formatFileSize(bytes) {
      if (!bytes) return '0 Bytes'

      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))

      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
  }
}
</script>

<style lang="scss" scoped>
.document-list {
  .card {
    border: none;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  }

  .document-card {
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
      font-size: 0.9rem;
      color: #6c757d;
    }

    .document-icon {
      width: 40px;
      height: 40px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 8px;
      background-color: rgba(0, 0, 0, 0.05);
      color: var(--primary-color, #003366);
    }
  }

  .document-icon-lg {
    width: 80px;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 16px;
    background-color: rgba(0, 0, 0, 0.05);
    color: var(--primary-color, #003366);
    margin: 0 auto;
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
