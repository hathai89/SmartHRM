<template>
  <aside class="sidebar" :class="{ 'show': isOpen }">
    <div class="sidebar-header">
      <h5 class="mb-0">{{ $t('common.appName') }}</h5>
    </div>
    
    <ul class="sidebar-menu">
      <!-- Dashboard -->
      <li>
        <router-link to="/dashboard" :class="{ 'active': isActive('/dashboard') }">
          <font-awesome-icon icon="home" />
          {{ $t('dashboard.title') }}
        </router-link>
      </li>
      
      <!-- Nhân viên -->
      <li class="menu-header">{{ $t('employees.title') }}</li>
      <li>
        <router-link to="/employees" :class="{ 'active': isActive('/employees') }">
          <font-awesome-icon icon="users" />
          {{ $t('employees.list') }}
        </router-link>
      </li>
      <li v-if="isAdmin">
        <router-link to="/employees/create" :class="{ 'active': isActive('/employees/create') }">
          <font-awesome-icon icon="user-plus" />
          {{ $t('employees.create') }}
        </router-link>
      </li>
      
      <!-- Phòng ban -->
      <li class="menu-header">{{ $t('departments.title') }}</li>
      <li>
        <router-link to="/departments" :class="{ 'active': isActive('/departments') }">
          <font-awesome-icon icon="building" />
          {{ $t('departments.list') }}
        </router-link>
      </li>
      <li v-if="isAdmin">
        <router-link to="/departments/create" :class="{ 'active': isActive('/departments/create') }">
          <font-awesome-icon icon="plus" />
          {{ $t('departments.create') }}
        </router-link>
      </li>
      
      <!-- Xí nghiệp -->
      <li class="menu-header">{{ $t('factories.title') }}</li>
      <li>
        <router-link to="/factories" :class="{ 'active': isActive('/factories') }">
          <font-awesome-icon icon="industry" />
          {{ $t('factories.list') }}
        </router-link>
      </li>
      <li v-if="isAdmin">
        <router-link to="/factories/create" :class="{ 'active': isActive('/factories/create') }">
          <font-awesome-icon icon="plus" />
          {{ $t('factories.create') }}
        </router-link>
      </li>
      
      <!-- Tài liệu -->
      <li class="menu-header">{{ $t('documents.title') }}</li>
      <li>
        <router-link to="/documents" :class="{ 'active': isActive('/documents') }">
          <font-awesome-icon icon="file-alt" />
          {{ $t('documents.list') }}
        </router-link>
      </li>
      <li v-if="isAdmin">
        <router-link to="/documents/create" :class="{ 'active': isActive('/documents/create') }">
          <font-awesome-icon icon="plus" />
          {{ $t('documents.create') }}
        </router-link>
      </li>
      <li v-if="isAdmin">
        <router-link to="/document-categories" :class="{ 'active': isActive('/document-categories') }">
          <font-awesome-icon icon="folder" />
          {{ $t('documents.categories.title') }}
        </router-link>
      </li>
      
      <!-- Quản trị hệ thống (chỉ cho admin) -->
      <li v-if="isAdmin" class="menu-header">{{ $t('admin.title') }}</li>
      <li v-if="isAdmin">
        <router-link to="/settings" :class="{ 'active': isActive('/settings') }">
          <font-awesome-icon icon="cog" />
          {{ $t('admin.settings') }}
        </router-link>
      </li>
      <li v-if="isAdmin">
        <router-link to="/logs" :class="{ 'active': isActive('/logs') }">
          <font-awesome-icon icon="history" />
          {{ $t('admin.logs') }}
        </router-link>
      </li>
    </ul>
  </aside>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'AppSidebar',
  props: {
    isOpen: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    ...mapGetters({
      isAdmin: 'auth/isAdmin'
    })
  },
  methods: {
    isActive(path) {
      return this.$route.path.startsWith(path)
    }
  }
}
</script>
