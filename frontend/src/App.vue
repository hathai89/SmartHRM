<template>
  <div id="app">
    <!-- Loading Screen -->
    <div v-if="!isReady" class="loading-container">
      <div class="spinner-border text-light" role="status">
        <span class="visually-hidden">Đang tải...</span>
      </div>
      <p class="mt-3 text-light">Đang tải ứng dụng...</p>
    </div>

    <!-- Thông báo lỗi -->
    <error-notification
      :show="hasError"
      :message="error"
      @close="clearError"
    />

    <!-- Thông báo offline -->
    <offline-notification
      :show="showOfflineNotification"
      @close="hideOfflineNotification"
    />

    <!-- Main Application -->
    <div v-if="isReady">
      <app-layout v-if="isAuthenticated && routeRequiresAuth">
        <breadcrumb :items="breadcrumbs" />
        <router-view />
      </app-layout>
      <public-layout v-else-if="!routeRequiresAuth">
        <router-view />
      </public-layout>
      <div v-else class="auth-layout">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import BreadcrumbNav from '@/components/common/Breadcrumb.vue';
import { getBreadcrumbs } from '@/utils/breadcrumb';
import AppLayout from '@/components/layout/AppLayout.vue';
import PublicLayout from '@/components/layout/PublicLayout.vue';
import ErrorNotification from '@/components/common/ErrorNotification.vue';
import OfflineNotification from '@/components/common/OfflineNotification.vue';

export default {
  name: 'App',
  components: {
    Breadcrumb: BreadcrumbNav,
    AppLayout,
    PublicLayout,
    ErrorNotification,
    OfflineNotification
  },
  data() {
    return {
      isReady: false
    }
  },
  computed: {
    isAuthenticated() {
      return this.$store.getters['auth/isAuthenticated'];
    },
    routeRequiresAuth() {
      // Kiểm tra xem route hiện tại có yêu cầu xác thực không
      // Nếu có bất kỳ route nào trong matched có requiresAuth === false, thì đây là route public
      const isPublicRoute = this.$route.matched.some(record => record.meta.requiresAuth === false);
      return !isPublicRoute;
    },
    currentYear() {
      return new Date().getFullYear();
    },
    breadcrumbs() {
      return getBreadcrumbs(this.$route.name, this.$route.params);
    },
    companyName() {
      const companyInfo = this.$store.getters['company/companyInfo'];
      return companyInfo ? companyInfo.name : 'SmartHRM';
    },
    hasError() {
      return this.$store.getters.hasError;
    },
    error() {
      return this.$store.getters.error;
    },
    showOfflineNotification() {
      return this.$store.getters['app/showOfflineNotification'];
    },
    isOffline() {
      return this.$store.getters['app/isOffline'];
    }
  },
  created() {
    // Kiểm tra xem người dùng đã đăng nhập chưa
    this.checkAuth();

    // Lấy thông tin công ty
    this.fetchCompanyInfo();

    // Kiểm tra kết nối đến backend
    this.checkBackendConnection();

    // Thiết lập kiểm tra kết nối định kỳ
    this.setupConnectionCheck();
  },
  methods: {
    async checkAuth() {
      try {
        // Kiểm tra token trong localStorage
        const token = localStorage.getItem('token');

        if (token) {
          // Nếu có token, kiểm tra tính hợp lệ
          await this.$store.dispatch('auth/checkAuth');
        }
      } catch (error) {
        console.error('Lỗi khi kiểm tra xác thực:', error);
        // Xóa token nếu không hợp lệ
        localStorage.removeItem('token');
      } finally {
        // Đánh dấu ứng dụng đã sẵn sàng
        this.isReady = true;
      }
    },

    async fetchCompanyInfo() {
      try {
        await this.$store.dispatch('company/fetchCompanyInfo');
      } catch (error) {
        console.error('Lỗi khi lấy thông tin công ty:', error);
      }
    },

    clearError() {
      this.$store.dispatch('clearError');
    },

    hideOfflineNotification() {
      this.$store.dispatch('app/hideOfflineNotification');
    },

    async checkBackendConnection() {
      await this.$store.dispatch('app/checkBackendConnection');
    },

    setupConnectionCheck() {
      // Kiểm tra kết nối mỗi 30 giây
      setInterval(() => {
        this.checkBackendConnection();
      }, 30000);
    }
  }
}
</script>

<style lang="scss">
// Import các file SCSS
@import '@/assets/scss/variables.scss';
@import '@/assets/scss/main.scss';

// Reset và base styles
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

// Thiết lập border-radius 50% cho các phần tử tròn
.rounded-circle,
.avatar,
.user-avatar img,
.profile-avatar img,
.btn-icon,
.btn-circle,
.avatar-img {
  border-radius: 50% !important;
}

// Thiết lập border-radius 4px cho badge
.badge,
.dropdown-toggle[data-bs-toggle="dropdown"] .badge {
  border-radius: 4px !important;
}

// Flat design badges
.stat-badge {
  display: inline-flex;
  align-items: center;
  font-size: 0.9rem;
  padding: 6px 12px;
  border-radius: 4px;
  font-weight: 500;
  color: white;
  box-shadow: none;
  border: none;
}

.stat-badge-primary {
  background-color: $primary;
  color: white;
}

.stat-badge-info {
  background-color: $info;
  color: white;
}

.stat-badge-secondary {
  background-color: $secondary;
  color: white;
}

// Flat buttons
.btn-flat {
  border-radius: 4px;
  box-shadow: none;
  border: none;
  padding: 8px 16px;
  font-weight: 500;
  transition: background-color 0.2s, transform 0.1s;

  &:hover {
    transform: translateY(-1px);
  }

  &:active {
    transform: translateY(1px);
  }
}

.btn-flat-primary {
  background-color: $primary;
  color: white;

  &:hover {
    background-color: darken($primary, 5%);
    color: white;
  }
}

.btn-flat-secondary {
  background-color: #f0f0f0;
  color: $dark;

  &:hover {
    background-color: darken(#f0f0f0, 5%);
    color: $dark;
  }
}

body {
  font-family: $font-family-sans-serif;
  font-size: $font-size-base;
  line-height: 1.5;
  color: $dark;
  background-color: #f5f5f5;
}

a {
  color: inherit;
  text-decoration: none;
}

ul {
  list-style: none;
}

// Loading container
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  font-size: 1.2rem;
  background: linear-gradient(135deg, $gradient-start 0%, $gradient-middle 50%, $gradient-end 100%);
}

// App container
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

// Loading container styles
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  font-size: 1.2rem;
  background: linear-gradient(135deg, $gradient-start 0%, $gradient-middle 50%, $gradient-end 100%);
}

// CSS cho thông báo lỗi đã được chuyển sang component ErrorNotification

// Gradient backgrounds
.bg-gradient-primary {
  background: linear-gradient(135deg, $gradient-start 0%, $gradient-middle 50%, $gradient-end 100%);
}

.bg-gradient-horizontal {
  background: linear-gradient(90deg, $gradient-start 0%, $gradient-end 100%);
}

// Card styles with gradient
.card-gradient {
  border: none;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);

  .card-header {
    background: linear-gradient(90deg, $primary 0%, $primary-light 100%);
    color: white;
    border: none;
    padding: 1rem 1.5rem;
  }

  &.card-accent {
    .card-header {
      background: linear-gradient(90deg, $accent 0%, $accent-light 100%);
    }
  }
}

// Buttons with gradient
.btn-gradient {
  background: linear-gradient(90deg, $primary 0%, $primary-light 100%);
  border: none;
  color: white;

  &:hover {
    background: linear-gradient(90deg, $primary-dark 0%, $primary 100%);
    color: white;
  }

  &.btn-accent {
    background: linear-gradient(90deg, $accent 0%, $accent-light 100%);

    &:hover {
      background: linear-gradient(90deg, darken($accent, 10%) 0%, $accent 100%);
    }
  }
}

// Animation for dropdowns
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-menu.show {
  animation: fadeIn 0.3s ease;
}

// Public layout styles
.public-layout {
  min-height: 100vh;
  background-color: #f8f9fa;

  .navbar {
    background-color: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }
}

// Auth layout styles
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, $gradient-start 0%, $gradient-middle 50%, $gradient-end 100%);
}
</style>
