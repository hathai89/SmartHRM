<template>
  <div class="department-tree">
    <div class="card">
      <div class="card-header">
        <h5 class="card-title mb-0">Cấu trúc phòng ban</h5>
      </div>
      <div class="card-body">
        <div v-if="loading" class="text-center py-3">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Đang tải...</span>
          </div>
        </div>
        <div v-else-if="error" class="alert alert-danger">
          {{ error }}
        </div>
        <div v-else-if="!treeData || treeData.length === 0" class="alert alert-info">
          Không có dữ liệu phòng ban
        </div>
        <div v-else>
          <!-- Thanh công cụ -->
          <div class="mb-3 d-flex justify-content-between">
            <div class="btn-group">
              <button class="btn btn-sm btn-outline-secondary" @click="expandAll">
                <font-awesome-icon icon="expand" class="me-1" /> Mở rộng tất cả
              </button>
              <button class="btn btn-sm btn-outline-secondary" @click="collapseAll">
                <font-awesome-icon icon="compress" class="me-1" /> Thu gọn tất cả
              </button>
            </div>
            <div class="input-group" style="width: 250px">
              <span class="input-group-text">
                <font-awesome-icon icon="search" />
              </span>
              <input
                type="text"
                class="form-control form-control-sm"
                v-model="searchQuery"
                placeholder="Tìm kiếm phòng ban..."
              >
            </div>
          </div>

          <!-- Cây phòng ban -->
          <div class="tree-container">
            <ul class="tree-root">
              <department-tree-node
                v-for="department in filteredTreeData"
                :key="department.id"
                :department="department"
                :search-query="searchQuery"
                @node-click="handleNodeClick"
                @edit-node="handleEditNode"
                @add-child="handleAddChild"
                @delete-node="handleDeleteNode"
              />
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal thêm/chỉnh sửa phòng ban -->
    <div class="modal fade" id="departmentModal" tabindex="-1" aria-labelledby="departmentModalLabel" aria-hidden="true" ref="departmentModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="departmentModalLabel">
              {{ isEdit ? 'Chỉnh sửa phòng ban' : 'Thêm phòng ban mới' }}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <alert-message
              v-if="formError"
              type="danger"
              :message="formError"
              @dismissed="formError = null"
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
                <label for="departmentType" class="form-label">Loại <span class="text-danger">*</span></label>
                <select class="form-select" id="departmentType" v-model="formData.dept_type" required>
                  <option value="department">Phòng ban</option>
                  <option value="division">Bộ phận</option>
                  <option value="team">Nhóm</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="departmentParent" class="form-label">Đơn vị cha</label>
                <select class="form-select" id="departmentParent" v-model="formData.parent">
                  <option :value="null">-- Không có --</option>
                  <option 
                    v-for="dept in availableParents" 
                    :key="dept.id" 
                    :value="dept.id"
                  >
                    {{ dept.name }} ({{ dept.code }})
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

    <!-- Modal xác nhận xóa -->
    <confirm-dialog
      v-if="showDeleteConfirm"
      title="Xác nhận xóa phòng ban"
      :message="'Bạn có chắc chắn muốn xóa phòng ban ' + (departmentToDelete ? departmentToDelete.name : '') + '?'"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
    />
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import { Modal } from 'bootstrap'
import AlertMessage from '@/components/common/AlertMessage.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import DepartmentTreeNode from './DepartmentTreeNode.vue'

export default {
  name: 'DepartmentTree',
  components: {
    AlertMessage,
    ConfirmDialog,
    DepartmentTreeNode
  },
  props: {
    initialExpanded: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      treeData: [],
      loading: false,
      error: null,
      searchQuery: '',
      expandedNodes: new Set(),
      departmentModal: null,
      isEdit: false,
      formData: {
        id: null,
        code: '',
        name: '',
        dept_type: 'department',
        parent: null,
        description: ''
      },
      formError: null,
      saving: false,
      showDeleteConfirm: false,
      departmentToDelete: null,
      selectedParentId: null
    }
  },
  computed: {
    filteredTreeData() {
      if (!this.searchQuery) {
        return this.treeData
      }

      // Hàm đệ quy để lọc cây
      const filterTree = (nodes) => {
        if (!nodes) return []

        return nodes.filter(node => {
          // Kiểm tra nếu node hiện tại khớp với từ khóa tìm kiếm
          const nodeMatches = 
            node.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
            node.code.toLowerCase().includes(this.searchQuery.toLowerCase())

          // Lọc các node con
          const filteredChildren = filterTree(node.children)
          
          // Nếu có node con khớp, giữ lại node cha
          if (filteredChildren.length > 0) {
            node.children = filteredChildren
            return true
          }

          // Nếu không có node con khớp, chỉ giữ lại node cha nếu nó khớp
          return nodeMatches
        })
      }

      return filterTree(JSON.parse(JSON.stringify(this.treeData)))
    },
    availableParents() {
      // Lọc danh sách các phòng ban có thể là parent dựa trên loại phòng ban đang chọn
      const flattenDepartments = (departments, result = []) => {
        departments.forEach(dept => {
          result.push(dept)
          if (dept.children && dept.children.length > 0) {
            flattenDepartments(dept.children, result)
          }
        })
        return result
      }

      const allDepartments = flattenDepartments(this.treeData)
      
      // Lọc theo ràng buộc
      if (this.formData.dept_type === 'division') {
        // Bộ phận chỉ có thể thuộc phòng ban
        return allDepartments.filter(dept => dept.dept_type === 'department')
      } else if (this.formData.dept_type === 'team') {
        // Nhóm chỉ có thể thuộc bộ phận
        return allDepartments.filter(dept => dept.dept_type === 'division')
      }
      
      // Phòng ban không có parent
      return []
    }
  },
  mounted() {
    this.initModal()
    this.fetchDepartmentTree()
  },
  methods: {
    ...mapActions({
      fetchDepartmentTreeData: 'departments/fetchDepartmentTree',
      createDepartment: 'departments/createDepartment',
      updateDepartment: 'departments/updateDepartment',
      deleteDepartment: 'departments/deleteDepartment'
    }),
    initModal() {
      this.$nextTick(() => {
        this.departmentModal = new Modal(this.$refs.departmentModal)
      })
    },
    async fetchDepartmentTree() {
      this.loading = true
      this.error = null

      try {
        const response = await this.fetchDepartmentTreeData()
        this.treeData = response

        // Mở rộng tất cả các node nếu initialExpanded = true
        if (this.initialExpanded) {
          this.expandAll()
        }
      } catch (error) {
        console.error('Error fetching department tree:', error)
        this.error = 'Không thể tải cấu trúc phòng ban. Vui lòng thử lại sau.'
      } finally {
        this.loading = false
      }
    },
    expandAll() {
      const expandNodes = (nodes) => {
        if (!nodes) return
        
        nodes.forEach(node => {
          this.expandedNodes.add(node.id)
          if (node.children && node.children.length > 0) {
            expandNodes(node.children)
          }
        })
      }
      
      expandNodes(this.treeData)
    },
    collapseAll() {
      this.expandedNodes.clear()
    },
    handleNodeClick(department) {
      // Toggle expanded state
      if (this.expandedNodes.has(department.id)) {
        this.expandedNodes.delete(department.id)
      } else {
        this.expandedNodes.add(department.id)
      }
    },
    handleEditNode(department) {
      this.isEdit = true
      this.formData = {
        id: department.id,
        code: department.code,
        name: department.name,
        dept_type: department.dept_type,
        parent: department.parent,
        description: department.description || ''
      }
      this.formError = null
      this.departmentModal.show()
    },
    handleAddChild(parentDepartment) {
      this.isEdit = false
      this.selectedParentId = parentDepartment ? parentDepartment.id : null
      
      // Xác định loại phòng ban con dựa trên loại phòng ban cha
      let childType = 'department'
      if (parentDepartment) {
        if (parentDepartment.dept_type === 'department') {
          childType = 'division'
        } else if (parentDepartment.dept_type === 'division') {
          childType = 'team'
        }
      }
      
      this.formData = {
        id: null,
        code: this.generateDepartmentCode(),
        name: '',
        dept_type: childType,
        parent: parentDepartment ? parentDepartment.id : null,
        description: ''
      }
      
      this.formError = null
      this.departmentModal.show()
    },
    handleDeleteNode(department) {
      this.departmentToDelete = department
      this.showDeleteConfirm = true
    },
    generateDepartmentCode() {
      // Tạo mã phòng ban ngẫu nhiên
      const randomChars = Math.random().toString(36).substring(2, 4).toUpperCase()
      const timestamp = Date.now().toString().slice(-4)
      return `PB${randomChars}${timestamp}`
    },
    async saveDepartment() {
      this.saving = true
      this.formError = null

      try {
        const departmentData = { ...this.formData }
        
        if (this.isEdit) {
          await this.updateDepartment({ id: departmentData.id, data: departmentData })
        } else {
          await this.createDepartment(departmentData)
        }
        
        // Cập nhật lại cây phòng ban
        await this.fetchDepartmentTree()
        
        // Đóng modal
        this.departmentModal.hide()
        
        // Hiển thị thông báo thành công
        this.$emit('department-saved', {
          success: true,
          message: this.isEdit ? 'Cập nhật phòng ban thành công' : 'Thêm phòng ban mới thành công'
        })
      } catch (error) {
        console.error('Error saving department:', error)
        this.formError = this.isEdit
          ? 'Không thể cập nhật phòng ban. Vui lòng thử lại sau.'
          : 'Không thể thêm phòng ban mới. Vui lòng thử lại sau.'
      } finally {
        this.saving = false
      }
    },
    async confirmDelete() {
      if (!this.departmentToDelete) return
      
      this.loading = true
      
      try {
        await this.deleteDepartment(this.departmentToDelete.id)
        
        // Cập nhật lại cây phòng ban
        await this.fetchDepartmentTree()
        
        // Hiển thị thông báo thành công
        this.$emit('department-saved', {
          success: true,
          message: `Đã xóa phòng ban ${this.departmentToDelete.name} thành công`
        })
      } catch (error) {
        console.error('Error deleting department:', error)
        this.$emit('department-saved', {
          success: false,
          message: 'Không thể xóa phòng ban. Vui lòng thử lại sau.'
        })
      } finally {
        this.loading = false
        this.showDeleteConfirm = false
        this.departmentToDelete = null
      }
    },
    cancelDelete() {
      this.showDeleteConfirm = false
      this.departmentToDelete = null
    }
  }
}
</script>

<style lang="scss" scoped>
.department-tree {
  .tree-container {
    max-height: 600px;
    overflow-y: auto;
  }
  
  .tree-root {
    list-style: none;
    padding-left: 0;
  }
}
</style>
