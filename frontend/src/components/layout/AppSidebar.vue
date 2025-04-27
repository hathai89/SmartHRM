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

<style lang="scss" scoped>
.sidebar {
  position: fixed;
  top: 60px; /* Chiều cao của header */
  left: 0;
  bottom: 0;
  width: 250px;
  background: linear-gradient(to bottom, #f8f9fa, #ffffff);
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  z-index: 900;
  transition: all 0.3s ease;
  overflow-y: auto;
  transform: translateX(-100%);

  @media (min-width: 768px) {
    transform: translateX(0);
  }

  &.show {
    transform: translateX(0);
  }

  .sidebar-header {
    padding: 1rem;
    background-color: rgba(0, 0, 0, 0.05);
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);

    h5 {
      font-weight: 600;
      color: var(--primary);
      margin: 0;
    }
  }

  .sidebar-menu {
    padding: 1rem 0;

    .menu-header {
      padding: 0.5rem 1rem;
      font-size: 0.8rem;
      font-weight: 600;
      text-transform: uppercase;
      color: #6c757d;
      margin-top: 1rem;
    }

    li {
      a {
        display: flex;
        align-items: center;
        padding: 0.75rem 1rem;
        color: #343a40;
        transition: all 0.2s ease;

        &:hover, &.active {
          background-color: rgba(0, 51, 102, 0.05);
          color: var(--primary);
          border-left: 3px solid var(--primary);
        }

        svg {
          width: 20px;
          margin-right: 0.75rem;
          color: #6c757d;
        }

        &.active svg {
          color: var(--primary);
        }
      }
    }
  }
}

// CSS Variables
:root {
  --primary: #003366;
  --primary-dark: #001f3f;
  --accent: #ff6600;
}

// No need for this anymore as we handle it in AppLayout.vue
</style>
