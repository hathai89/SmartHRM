<template>
  <li class="tree-node" :class="{ 'has-children': hasChildren }">
    <div class="node-content" :class="{ 'highlight': isHighlighted }">
      <div class="node-header" @click="$emit('node-click', factory)">
        <div class="node-toggle" v-if="hasChildren">
          <font-awesome-icon :icon="isExpanded ? 'chevron-down' : 'chevron-right'" />
        </div>
        <div class="node-icon">
          <font-awesome-icon :icon="nodeIcon" :class="nodeIconClass" />
        </div>
        <div class="node-title">
          <span class="node-name">{{ factory.name }}</span>
          <span class="node-code">({{ factory.code }})</span>
        </div>
      </div>
      <div class="node-actions">
        <button class="btn btn-sm btn-outline-primary" @click="$emit('add-child', factory)" title="Thêm đơn vị con">
          <font-awesome-icon icon="plus" />
        </button>
        <button class="btn btn-sm btn-outline-secondary" @click="$emit('edit-node', factory)" title="Chỉnh sửa">
          <font-awesome-icon icon="edit" />
        </button>
        <button class="btn btn-sm btn-outline-danger" @click="$emit('delete-node', factory)" title="Xóa">
          <font-awesome-icon icon="trash-alt" />
        </button>
      </div>
    </div>
    <ul v-if="hasChildren && isExpanded" class="tree-children">
      <factory-tree-node
        v-for="child in factory.children"
        :key="child.id"
        :factory="child"
        :search-query="searchQuery"
        :expanded-nodes="expandedNodes"
        @node-click="$emit('node-click', $event)"
        @edit-node="$emit('edit-node', $event)"
        @add-child="$emit('add-child', $event)"
        @delete-node="$emit('delete-node', $event)"
      />
    </ul>
  </li>
</template>

<script>
export default {
  name: 'FactoryTreeNode',
  props: {
    factory: {
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
  computed: {
    hasChildren() {
      return this.factory.children && this.factory.children.length > 0
    },
    isExpanded() {
      return this.expandedNodes.has(this.factory.id)
    },
    isHighlighted() {
      if (!this.searchQuery) return false
      
      return (
        this.factory.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        this.factory.code.toLowerCase().includes(this.searchQuery.toLowerCase())
      )
    },
    nodeIcon() {
      switch (this.factory.factory_type) {
        case 'factory':
          return 'industry'
        case 'division':
          return 'layer-group'
        case 'team':
          return 'users'
        default:
          return 'folder'
      }
    },
    nodeIconClass() {
      switch (this.factory.factory_type) {
        case 'factory':
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
    
    .node-code {
      font-weight: normal;
      color: #6c757d;
      font-size: 0.875rem;
      margin-left: 0.25rem;
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
