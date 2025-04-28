<template>
  <li class="tree-node" :class="{ 'has-children': hasChildren }">
    <div class="node-content" :class="{ 'highlight': isHighlighted }">
      <div class="node-header" @click="$emit('node-click', department)">
        <div class="node-toggle" v-if="hasChildren">
          <font-awesome-icon :icon="isExpanded ? 'chevron-down' : 'chevron-right'" />
        </div>
        <div class="node-icon">
          <font-awesome-icon :icon="nodeIcon" :class="nodeIconClass" />
        </div>
        <div class="node-title">
          <span class="node-name">{{ department.name }}</span>
          <span class="node-code">({{ department.code }})</span>
          <span class="node-stats">
            <template v-if="department.dept_type === 'department'">
              <span class="stat-item" title="Nhân viên"><font-awesome-icon icon="user" /> {{ employeeCount }}</span>
              <span class="stat-item" title="Bộ phận"><font-awesome-icon icon="layer-group" /> {{ divisionCount }}</span>
              <span class="stat-item" title="Nhóm"><font-awesome-icon icon="users" /> {{ teamCount }}</span>
            </template>
            <template v-else-if="department.dept_type === 'division'">
              <span class="stat-item" title="Nhân viên"><font-awesome-icon icon="user" /> {{ employeeCount }}</span>
              <span class="stat-item" title="Nhóm"><font-awesome-icon icon="users" /> {{ teamCount }}</span>
            </template>
            <template v-else>
              <span class="stat-item" title="Nhân viên"><font-awesome-icon icon="user" /> {{ employeeCount }}</span>
            </template>
          </span>
        </div>
      </div>
      <div class="node-actions">
        <button class="btn btn-sm btn-outline-primary" @click="$emit('add-child', department)" title="Thêm đơn vị con">
          <font-awesome-icon icon="plus" />
        </button>
        <button class="btn btn-sm btn-outline-secondary" @click="$emit('edit-node', department)" title="Chỉnh sửa">
          <font-awesome-icon icon="edit" />
        </button>
        <button class="btn btn-sm btn-outline-danger" @click="$emit('delete-node', department)" title="Xóa">
          <font-awesome-icon icon="trash-alt" />
        </button>
      </div>
    </div>
    <div v-if="isExpanded">
      <!-- Tabs cho nhân viên và ứng viên (chỉ hiển thị ở cấp phòng ban) -->
      <div class="department-detail-tabs">
        <template v-if="department.dept_type === 'department'">
          <ul class="nav nav-tabs nav-tabs-sm">
            <li class="nav-item">
              <a class="nav-link" :class="{ active: activeTab === 'employees' }" href="#" @click.prevent="activeTab = 'employees'">
                <font-awesome-icon icon="users" class="me-1" />
                Nhân viên
                <span v-if="department.employees && department.employees.length > 0" class="badge bg-secondary ms-1">{{ department.employees.length }}</span>
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" :class="{ active: activeTab === 'candidates' }" href="#" @click.prevent="activeTab = 'candidates'">
                <font-awesome-icon icon="user-tie" class="me-1" />
                Ứng viên
              </a>
            </li>
          </ul>

          <!-- Tab nội dung -->
          <div class="tab-content mt-2">
            <!-- Tab nhân viên -->
            <div v-if="activeTab === 'employees'" class="employee-list">
              <table class="table table-sm table-hover">
                <thead>
                  <tr>
                    <th>Mã NV</th>
                    <th>Họ tên</th>
                    <th>Chức vụ</th>
                    <th>Trạng thái</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="!department.employees || department.employees.length === 0">
                    <td colspan="4" class="text-center text-muted">Chưa có nhân viên</td>
                  </tr>
                  <tr v-else v-for="employee in department.employees" :key="employee.id">
                    <td>{{ employee.code }}</td>
                    <td>{{ employee.full_name }}</td>
                    <td>{{ employee.job_title_name }}</td>
                    <td><span class="badge" :class="getStatusClass(employee.status)">{{ getStatusText(employee.status) }}</span></td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Tab ứng viên -->
            <div v-else-if="activeTab === 'candidates'" class="candidate-list">
              <div class="text-center py-3">
                <font-awesome-icon icon="user-tie" class="fa-2x mb-2 text-muted" />
                <p class="text-muted mb-0">Chưa có ứng viên nào</p>
              </div>
            </div>
          </div>
        </template>

        <!-- Hiển thị danh sách nhân viên trực tiếp cho bộ phận và nhóm -->
        <template v-else>
          <div class="employee-list">
            <h6 class="employee-list-title">
              Danh sách nhân viên
              <span v-if="department.employees && department.employees.length > 0">({{ department.employees.length }})</span>
            </h6>
            <table class="table table-sm table-hover">
              <thead>
                <tr>
                  <th>Mã NV</th>
                  <th>Họ tên</th>
                  <th>Chức vụ</th>
                  <th>Trạng thái</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="!department.employees || department.employees.length === 0">
                  <td colspan="4" class="text-center text-muted">Chưa có nhân viên</td>
                </tr>
                <tr v-else v-for="employee in department.employees" :key="employee.id">
                  <td>{{ employee.code }}</td>
                  <td>{{ employee.full_name }}</td>
                  <td>{{ employee.job_title_name }}</td>
                  <td><span class="badge" :class="getStatusClass(employee.status)">{{ getStatusText(employee.status) }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </template>
      </div>

      <!-- Danh sách phòng ban con -->
      <ul v-if="hasChildren" class="tree-children">
        <department-tree-node
          v-for="child in department.children"
          :key="child.id"
          :department="child"
          :search-query="searchQuery"
          :expanded-nodes="expandedNodes"
          @node-click="$emit('node-click', $event)"
          @edit-node="$emit('edit-node', $event)"
          @add-child="$emit('add-child', $event)"
          @delete-node="$emit('delete-node', $event)"
        />
      </ul>
    </div>
  </li>
</template>

<script>
export default {
  name: 'DepartmentTreeNode',
  props: {
    department: {
      type: Object,
      required: true
    },
    searchQuery: {
      type: String,
      default: ''
    },
    expandedNodes: {
      type: Set,
      default: () => new Set()
    }
  },
  data() {
    return {
      activeTab: 'employees' // Tab mặc định là nhân viên
    }
  },
  methods: {
    getStatusClass(status) {
      switch (status) {
        case 'active':
          return 'bg-success'
        case 'inactive':
          return 'bg-secondary'
        case 'on_leave':
          return 'bg-warning'
        case 'terminated':
          return 'bg-danger'
        default:
          return 'bg-secondary'
      }
    },
    getStatusText(status) {
      switch (status) {
        case 'active':
          return 'Đang làm việc'
        case 'inactive':
          return 'Tạm nghỉ'
        case 'on_leave':
          return 'Nghỉ phép'
        case 'terminated':
          return 'Đã nghỉ việc'
        default:
          return 'Không xác định'
      }
    }
  },
  computed: {
    hasChildren() {
      return this.department.children && this.department.children.length > 0
    },
    isExpanded() {
      return this.expandedNodes.has(this.department.id)
    },
    isHighlighted() {
      if (!this.searchQuery) return false

      return (
        this.department.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        this.department.code.toLowerCase().includes(this.searchQuery.toLowerCase())
      )
    },
    employeeCount() {
      return this.department.employees ? this.department.employees.length : 0
    },
    divisionCount() {
      if (!this.department.children) return 0
      return this.department.children.filter(child => child.dept_type === 'division').length
    },
    teamCount() {
      if (!this.department.children) return 0

      // Đối với phòng ban, tính tổng số nhóm (bao gồm cả nhóm trong các bộ phận)
      if (this.department.dept_type === 'department') {
        let count = 0
        // Đếm nhóm trực tiếp thuộc phòng ban
        count += this.department.children.filter(child => child.dept_type === 'team').length

        // Đếm nhóm trong các bộ phận
        const divisions = this.department.children.filter(child => child.dept_type === 'division')
        for (const division of divisions) {
          if (division.children) {
            count += division.children.filter(child => child.dept_type === 'team').length
          }
        }
        return count
      }

      // Đối với bộ phận, chỉ tính số nhóm trực tiếp
      return this.department.children.filter(child => child.dept_type === 'team').length
    },
    nodeIcon() {
      switch (this.department.dept_type) {
        case 'department':
          return 'building'
        case 'division':
          return 'layer-group'
        case 'team':
          return 'users'
        default:
          return 'folder'
      }
    },
    nodeIconClass() {
      switch (this.department.dept_type) {
        case 'department':
          return 'text-primary'
        case 'division':
          return 'text-info'
        case 'team':
          return 'text-success'
        default:
          return 'text-secondary'
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.tree-node {
  position: relative;
  padding: 0.25rem 0;

  &.has-children {
    &::before {
      content: '';
      position: absolute;
      top: 1.5rem;
      left: 0.5rem;
      width: 2px;
      height: calc(100% - 1.5rem);
      background-color: #e9ecef;
    }
  }

  .node-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5rem;
    border-radius: 0.25rem;
    border: 1px solid #e9ecef;
    background-color: white;
    margin-bottom: 0.5rem;
    transition: all 0.2s;

    &:hover {
      background-color: #f8f9fa;
      border-color: #dee2e6;
    }

    &.highlight {
      background-color: #fff3cd;
      border-color: #ffecb5;
    }
  }

  .node-header {
    display: flex;
    align-items: center;
    cursor: pointer;
    flex: 1;
  }

  .node-toggle {
    width: 1.5rem;
    text-align: center;
    color: #6c757d;
  }

  .node-icon {
    width: 1.5rem;
    text-align: center;
    margin-right: 0.5rem;
  }

  .node-title {
    font-weight: 500;
    display: flex;
    align-items: center;
    flex-wrap: wrap;

    .node-code {
      font-weight: normal;
      color: #6c757d;
      font-size: 0.875rem;
      margin-left: 0.25rem;
    }

    .node-stats {
      margin-left: 0.75rem;
      font-size: 0.75rem;
      color: #6c757d;
      display: flex;
      align-items: center;

      .stat-item {
        display: inline-flex;
        align-items: center;
        margin-right: 0.5rem;
        background-color: #f8f9fa;
        padding: 0.125rem 0.375rem;
        border-radius: 0.25rem;
        border: 1px solid #e9ecef;

        svg {
          margin-right: 0.25rem;
          font-size: 0.7rem;
        }
      }
    }
  }

  .node-actions {
    display: flex;
    gap: 0.25rem;
    opacity: 0.5;
    transition: opacity 0.2s;

    .btn {
      padding: 0.125rem 0.25rem;
      font-size: 0.75rem;
    }
  }

  .node-content:hover .node-actions {
    opacity: 1;
  }

  .department-detail-tabs {
    margin: 0.5rem 0 1rem 1.5rem;
    border-left: 2px solid #e9ecef;
    padding-left: 1rem;

    .nav-tabs-sm {
      border-bottom: 1px solid #dee2e6;

      .nav-item {
        margin-bottom: -1px;
      }

      .nav-link {
        padding: 0.25rem 0.75rem;
        font-size: 0.85rem;
        border: 1px solid transparent;
        border-top-left-radius: 0.25rem;
        border-top-right-radius: 0.25rem;

        &:hover {
          border-color: #e9ecef #e9ecef #dee2e6;
        }

        &.active {
          color: #495057;
          background-color: #fff;
          border-color: #dee2e6 #dee2e6 #fff;
        }

        .badge {
          font-size: 0.7rem;
          padding: 0.15rem 0.4rem;
        }
      }
    }

    .employee-list, .candidate-list {
      padding: 0.5rem 0;

      table {
        font-size: 0.85rem;

        th {
          font-weight: 500;
          color: #495057;
        }

        .badge {
          font-size: 0.75rem;
          padding: 0.25rem 0.5rem;
          border-radius: 0.25rem;
        }
      }
    }
  }

  .tree-children {
    list-style: none;
    padding-left: 1.5rem;
    position: relative;

    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0.5rem;
      width: 1rem;
      height: 1px;
      background-color: #e9ecef;
    }
  }
}
</style>
