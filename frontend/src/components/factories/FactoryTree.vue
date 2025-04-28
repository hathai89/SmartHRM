<template>
  <div class="factory-tree">
    <div class="card">
      <div class="card-header">
        <div class="d-flex justify-content-between align-items-center">
          <h5 class="card-title mb-0">Cấu trúc xí nghiệp</h5>
          <div v-if="!loading && treeData.length > 0" class="d-flex align-items-center">
            <div class="stat-badge stat-badge-primary me-2">
              <font-awesome-icon icon="industry" class="me-1" />
              {{ factoryStats.factories }} xí nghiệp
            </div>
            <div class="stat-badge stat-badge-info me-2">
              <font-awesome-icon icon="layer-group" class="me-1" />
              {{ factoryStats.divisions }} bộ phận
            </div>
            <div class="stat-badge stat-badge-secondary">
              <font-awesome-icon icon="users" class="me-1" />
              {{ factoryStats.teams }} nhóm
            </div>
          </div>
        </div>
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
          Không có dữ liệu xí nghiệp
        </div>
        <div v-else>
          <!-- Thanh công cụ -->
          <div class="mb-3 d-flex justify-content-between">
            <div class="d-flex">
              <button class="btn-flat btn-flat-secondary me-2" style="padding: 4px 10px; font-size: 0.875rem;" @click="expandAll">
                <font-awesome-icon icon="expand" class="me-1" /> Mở rộng tất cả
              </button>
              <button class="btn-flat btn-flat-secondary" style="padding: 4px 10px; font-size: 0.875rem;" @click="collapseAll">
                <font-awesome-icon icon="compress" class="me-1" /> Thu gọn tất cả
              </button>
            </div>
            <div class="input-group" style="width: 250px">
              <span class="input-group-text" style="border-radius: 4px 0 0 4px; border: none; background-color: #f0f0f0;">
                <font-awesome-icon icon="search" />
              </span>
              <input
                type="text"
                class="form-control form-control-sm"
                v-model="searchQuery"
                placeholder="Tìm kiếm xí nghiệp..."
                style="border-radius: 0 4px 4px 0; border: none; background-color: #f0f0f0;"
              >
            </div>
          </div>

          <!-- Cây xí nghiệp -->
          <div class="tree-container">
            <ul class="tree-root">
              <factory-tree-node
                v-for="factory in filteredTreeData"
                :key="factory.id"
                :factory="factory"
                :search-query="searchQuery"
                :expanded-nodes="expandedNodes"
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

    <!-- Modal thêm/chỉnh sửa xí nghiệp -->
    <div class="modal fade" id="factoryModal" tabindex="-1" aria-labelledby="factoryModalLabel" aria-hidden="true" ref="factoryModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="factoryModalLabel">
              {{ isEdit ? 'Chỉnh sửa xí nghiệp' : 'Thêm xí nghiệp mới' }}
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
                <label for="factoryType" class="form-label">Loại <span class="text-danger">*</span></label>
                <select class="form-select" id="factoryType" v-model="formData.factory_type" required>
                  <option value="factory">Xí nghiệp</option>
                  <option value="division">Bộ phận</option>
                  <option value="team">Nhóm</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="factoryParent" class="form-label">Đơn vị cha</label>
                <select class="form-select" id="factoryParent" v-model="formData.parent">
                  <option :value="null">-- Không có --</option>
                  <option
                    v-for="factory in availableParents"
                    :key="factory.id"
                    :value="factory.id"
                  >
                    {{ factory.name }} ({{ factory.code }})
                  </option>
                </select>
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
              <div class="mb-3">
                <label for="factoryCapacity" class="form-label">Công suất</label>
                <input
                  type="text"
                  class="form-control"
                  id="factoryCapacity"
                  v-model="formData.capacity"
                >
              </div>
              <div class="mb-3">
                <label for="factoryEstablishedDate" class="form-label">Ngày thành lập</label>
                <input
                  type="date"
                  class="form-control"
                  id="factoryEstablishedDate"
                  v-model="formData.established_date"
                >
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

    <!-- Modal xác nhận xóa -->
    <confirm-dialog
      v-if="showDeleteConfirm"
      title="Xác nhận xóa xí nghiệp"
      :message="'Bạn có chắc chắn muốn xóa xí nghiệp ' + (factoryToDelete ? factoryToDelete.name : '') + '?'"
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
import FactoryTreeNode from './FactoryTreeNode.vue'

export default {
  name: 'FactoryTree',
  components: {
    AlertMessage,
    ConfirmDialog,
    FactoryTreeNode
  },
  props: {
    initialExpanded: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      treeData: [],
      loading: false,
      error: null,
      searchQuery: '',
      expandedNodes: new Set(),
      factoryModal: null,
      isEdit: false,
      formData: {
        id: null,
        code: '',
        name: '',
        factory_type: 'factory',
        parent: null,
        description: '',
        capacity: '',
        established_date: null
      },
      formError: null,
      saving: false,
      showDeleteConfirm: false,
      factoryToDelete: null,
      selectedParentId: null
    }
  },
  computed: {
    factoryStats() {
      // Hàm đệ quy để đếm số lượng xí nghiệp, bộ phận, nhóm
      const countFactoryTypes = (nodes) => {
        if (!nodes || !Array.isArray(nodes)) return { factories: 0, divisions: 0, teams: 0 }

        let stats = { factories: 0, divisions: 0, teams: 0 }

        nodes.forEach(node => {
          if (node.factory_type === 'factory') {
            stats.factories++
          } else if (node.factory_type === 'division') {
            stats.divisions++
          } else if (node.factory_type === 'team') {
            stats.teams++
          }

          // Đệ quy đếm các node con
          if (node.children && node.children.length > 0) {
            const childStats = countFactoryTypes(node.children)
            stats.factories += childStats.factories
            stats.divisions += childStats.divisions
            stats.teams += childStats.teams
          }
        })

        return stats
      }

      return countFactoryTypes(this.treeData)
    },
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
      // Lọc danh sách các xí nghiệp có thể là parent dựa trên loại xí nghiệp đang chọn
      const flattenFactories = (factories, result = []) => {
        factories.forEach(factory => {
          result.push(factory)
          if (factory.children && factory.children.length > 0) {
            flattenFactories(factory.children, result)
          }
        })
        return result
      }

      const allFactories = flattenFactories(this.treeData)

      // Lọc theo ràng buộc
      if (this.formData.factory_type === 'division') {
        // Bộ phận chỉ có thể thuộc xí nghiệp
        return allFactories.filter(factory => factory.factory_type === 'factory')
      } else if (this.formData.factory_type === 'team') {
        // Nhóm chỉ có thể thuộc bộ phận
        return allFactories.filter(factory => factory.factory_type === 'division')
      }

      // Xí nghiệp không có parent
      return []
    }
  },
  mounted() {
    this.initModal()
    this.fetchFactoryTree()
  },
  methods: {
    ...mapActions({
      fetchFactoryTreeData: 'factories/fetchFactoryTree',
      createFactory: 'factories/createFactory',
      updateFactory: 'factories/updateFactory',
      deleteFactory: 'factories/deleteFactory'
    }),
    initModal() {
      this.$nextTick(() => {
        if (this.$refs.factoryModal) {
          this.factoryModal = new Modal(this.$refs.factoryModal)
        }
      })
    },
    async fetchFactoryTree() {
      this.loading = true
      this.error = null

      try {
        const response = await this.fetchFactoryTreeData()
        this.treeData = response

        console.log('Fetched factory tree:', this.treeData)

        // Mở rộng tất cả các node nếu initialExpanded = true
        if (this.initialExpanded) {
          this.expandAll()
        }
      } catch (error) {
        console.error('Error fetching factory tree:', error)
        this.error = 'Không thể tải cấu trúc xí nghiệp. Vui lòng thử lại sau.'
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
    handleNodeClick(factory) {
      // Toggle expanded state
      if (this.expandedNodes.has(factory.id)) {
        this.expandedNodes.delete(factory.id)
      } else {
        this.expandedNodes.add(factory.id)
      }
    },
    handleEditNode(factory) {
      this.isEdit = true
      this.formData = {
        id: factory.id,
        code: factory.code,
        name: factory.name,
        factory_type: factory.factory_type,
        parent: factory.parent,
        description: factory.description || '',
        capacity: factory.capacity || '',
        established_date: factory.established_date || null
      }
      this.formError = null
      this.factoryModal.show()
    },
    handleAddChild(parentFactory) {
      this.isEdit = false
      this.selectedParentId = parentFactory ? parentFactory.id : null

      // Xác định loại xí nghiệp con dựa trên loại xí nghiệp cha
      let childType = 'factory'
      if (parentFactory) {
        if (parentFactory.factory_type === 'factory') {
          childType = 'division'
        } else if (parentFactory.factory_type === 'division') {
          childType = 'team'
        }
      }

      this.formData = {
        id: null,
        code: this.generateFactoryCode(),
        name: '',
        factory_type: childType,
        parent: parentFactory ? parentFactory.id : null,
        description: '',
        capacity: '',
        established_date: null
      }

      this.formError = null
      this.factoryModal.show()
    },
    handleDeleteNode(factory) {
      this.factoryToDelete = factory
      this.showDeleteConfirm = true
    },
    generateFactoryCode() {
      // Tạo mã xí nghiệp ngẫu nhiên
      const randomChars = Math.random().toString(36).substring(2, 4).toUpperCase()
      const timestamp = Date.now().toString().slice(-4)
      return `XN${randomChars}${timestamp}`
    },
    async saveFactory() {
      this.saving = true
      this.formError = null

      try {
        const factoryData = { ...this.formData }

        if (this.isEdit) {
          await this.updateFactory({ id: factoryData.id, data: factoryData })
        } else {
          await this.createFactory(factoryData)
        }

        // Cập nhật lại cây xí nghiệp
        await this.fetchFactoryTree()

        // Đóng modal
        this.factoryModal.hide()

        // Hiển thị thông báo thành công
        this.$emit('factory-saved', {
          success: true,
          message: this.isEdit ? 'Cập nhật xí nghiệp thành công' : 'Thêm xí nghiệp mới thành công'
        })
      } catch (error) {
        console.error('Error saving factory:', error)
        this.formError = this.isEdit
          ? 'Không thể cập nhật xí nghiệp. Vui lòng thử lại sau.'
          : 'Không thể thêm xí nghiệp mới. Vui lòng thử lại sau.'
      } finally {
        this.saving = false
      }
    },
    async confirmDelete() {
      if (!this.factoryToDelete) return

      this.loading = true

      try {
        await this.deleteFactory(this.factoryToDelete.id)

        // Cập nhật lại cây xí nghiệp
        await this.fetchFactoryTree()

        // Hiển thị thông báo thành công
        this.$emit('factory-saved', {
          success: true,
          message: `Đã xóa xí nghiệp ${this.factoryToDelete.name} thành công`
        })
      } catch (error) {
        console.error('Error deleting factory:', error)
        this.$emit('factory-saved', {
          success: false,
          message: 'Không thể xóa xí nghiệp. Vui lòng thử lại sau.'
        })
      } finally {
        this.loading = false
        this.showDeleteConfirm = false
        this.factoryToDelete = null
      }
    },
    cancelDelete() {
      this.showDeleteConfirm = false
      this.factoryToDelete = null
    }
  }
}
</script>

<style lang="scss" scoped>
.factory-tree {
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
