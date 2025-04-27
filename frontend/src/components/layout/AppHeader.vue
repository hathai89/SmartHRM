<template>
  <header class="app-header">
    <button class="btn btn-link navbar-toggler" @click="toggleSidebar">
      <font-awesome-icon icon="bars" />
    </button>

    <router-link to="/" class="brand">
      <img src="@/assets/images/logo.png" alt="Logo" class="brand-logo me-2" style="height: 40px; border-radius: 4px;">
      <span>{{ companyName }}</span>
    </router-link>

    <div class="header-nav">
      <!-- Thông báo -->
      <div class="nav-item dropdown">
        <a class="nav-link dropdown-toggle notification-badge" href="#" id="notificationsDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
          <font-awesome-icon icon="bell" />
          <span v-if="unreadCount > 0" class="badge bg-danger">{{ unreadCount }}</span>
        </a>
        <div class="dropdown-menu dropdown-menu-end" aria-labelledby="notificationsDropdown">
          <h6 class="dropdown-header">{{ $t('notifications.title') }}</h6>
          <div v-if="notifications.length === 0" class="dropdown-item text-center">
            {{ $t('notifications.noNotifications') }}
          </div>
          <template v-else>
            <a v-for="notification in notifications.slice(0, 5)" :key="notification.id" class="dropdown-item" href="#" @click.prevent="viewNotification(notification)">
              <div class="d-flex align-items-center">
                <div class="flex-shrink-0">
                  <font-awesome-icon :icon="getNotificationIcon(notification.notification_type)" :class="getNotificationIconClass(notification.priority)" />
                </div>
                <div class="flex-grow-1 ms-2">
                  <div class="fw-bold">{{ notification.title }}</div>
                  <div class="small text-truncate">{{ notification.message }}</div>
                  <div class="small text-muted">{{ formatDate(notification.created_at) }}</div>
                </div>
                <div v-if="!notification.is_read" class="flex-shrink-0 ms-2">
                  <span class="badge bg-primary">{{ $t('notifications.new') }}</span>
                </div>
              </div>
            </a>
            <div class="dropdown-divider"></div>
            <div class="d-flex justify-content-between px-3 py-1">
              <button class="btn btn-sm btn-link" @click="markAllAsRead">
                {{ $t('notifications.markAllAsRead') }}
              </button>
              <router-link to="/notifications" class="btn btn-sm btn-link">
                {{ $t('notifications.viewAll') }}
              </router-link>
            </div>
          </template>
        </div>
      </div>

      <!-- Người dùng -->
      <div class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
          <img v-if="currentUser && currentUser.avatar" :src="currentUser.avatar" alt="Avatar" class="rounded-circle" width="32" height="32">
          <font-awesome-icon v-else icon="user" />
          <span class="ms-2 d-none d-md-inline">{{ currentUser ? (currentUser.is_superuser ? 'Admin' : currentUser.username) : '' }}</span>
        </a>
        <div class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
          <h6 class="dropdown-header">{{ currentUser ? currentUser.full_name : '' }}</h6>
          <router-link to="/profile" class="dropdown-item">
            <font-awesome-icon icon="user" class="me-2" />
            Hồ sơ cá nhân
          </router-link>
          <router-link to="/change-password" class="dropdown-item">
            <font-awesome-icon icon="lock" class="me-2" />
            Đổi mật khẩu
          </router-link>
          <div class="dropdown-divider"></div>
          <a href="#" class="dropdown-item" @click.prevent="logout">
            <font-awesome-icon icon="sign-out-alt" class="me-2" />
            Đăng xuất
          </a>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import moment from 'moment'

export default {
  name: 'AppHeader',
  computed: {
    ...mapGetters({
      currentUser: 'auth/currentUser',
      notifications: 'notifications/allNotifications',
      unreadCount: 'notifications/unreadCount',
      companyInfo: 'company/companyInfo'
    }),
    companyName() {
      return this.companyInfo ? this.companyInfo.name : 'SmartHRM';
    }
  },
  methods: {
    ...mapActions({
      logoutAction: 'auth/logout',
      fetchNotifications: 'notifications/fetchNotifications',
      markAsRead: 'notifications/markAsRead',
      markAllAsReadAction: 'notifications/markAllAsRead'
    }),
    toggleSidebar() {
      this.$emit('toggle-sidebar')
    },
    async logout() {
      try {
        await this.logoutAction()
        this.$router.push('/login')
      } catch (error) {
        console.error('Lỗi khi đăng xuất:', error)
      }
    },
    viewNotification(notification) {
      // Đánh dấu thông báo đã đọc
      if (!notification.is_read) {
        this.markAsRead(notification.id)
      }

      // Chuyển hướng đến liên kết của thông báo nếu có
      if (notification.link) {
        this.$router.push(notification.link)
      }
    },
    async markAllAsRead() {
      try {
        await this.markAllAsReadAction()
      } catch (error) {
        console.error('Lỗi khi đánh dấu tất cả đã đọc:', error)
      }
    },
    formatDate(date) {
      return moment(date).fromNow()
    },
    getNotificationIcon(type) {
      switch (type) {
        case 'system':
          return 'cog'
        case 'employee':
          return 'user'
        case 'document':
          return 'file-alt'
        case 'task':
          return 'tasks'
        default:
          return 'bell'
      }
    },
    getNotificationIconClass(priority) {
      switch (priority) {
        case 'low':
          return 'text-info'
        case 'normal':
          return 'text-primary'
        case 'high':
          return 'text-warning'
        case 'urgent':
          return 'text-danger'
        default:
          return 'text-primary'
      }
    }
  },
  created() {
    // Tải thông báo khi component được tạo
    this.fetchNotifications()

    // Tải thông tin công ty
    this.$store.dispatch('company/fetchCompanyInfo')
  }
}
</script>
