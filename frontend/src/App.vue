<template>
  <div id="app">
    <!-- Loading Screen -->
    <div v-if="!isReady" class="loading-container">
      <div class="spinner-border text-light" role="status">
        <span class="visually-hidden">Đang tải...</span>
      </div>
      <p class="mt-3 text-light">Đang tải ứng dụng...</p>
    </div>

    <!-- Main Application -->
    <div v-else class="app-container">
      <!-- Header with Navigation -->
      <header class="app-header" v-if="isAuthenticated">
        <div class="container-fluid">
          <div class="header-content">
            <!-- Logo and Brand -->
            <div class="brand">
              <router-link to="/dashboard" class="brand-link">
                <img src="@/assets/images/logo.png" alt="SmartHRM Logo" class="brand-logo">
              </router-link>
            </div>

            <!-- Main Navigation -->
            <nav class="main-nav">
              <button class="mobile-menu-toggle" @click="toggleMobileMenu">
                <i class="fas fa-bars"></i>
              </button>

              <ul class="nav-menu" :class="{ 'show': mobileMenuOpen }">
                <!-- Thông tin người dùng (chỉ hiển thị trên mobile) -->
                <li class="nav-item user-info-mobile d-lg-none" v-if="isAuthenticated">
                  <div class="user-info-container">
                    <div class="user-avatar">
                      <img v-if="$store.getters['auth/currentUser'] && $store.getters['auth/currentUser'].avatar"
                           :src="$store.getters['auth/currentUser'].avatar"
                           alt="Avatar"
                           class="rounded-circle">
                      <i v-else class="fas fa-user-circle"></i>
                    </div>
                    <div class="user-details">
                      <div class="user-name">{{ username }}</div>
                      <div class="user-role" v-if="$store.getters['auth/currentUser']">
                        {{ $store.getters['auth/currentUser'].is_superuser ? 'Quản trị viên' : 'Người dùng' }}
                      </div>
                    </div>
                  </div>
                </li>

                <li class="nav-item">
                  <router-link to="/dashboard" class="nav-link">
                    <i class="fas fa-tachometer-alt"></i> Bảng điều khiển
                  </router-link>
                </li>

                <li class="nav-item dropdown">
                  <a href="#" class="nav-link dropdown-toggle" @click.prevent="toggleDropdown('employees')">
                    <i class="fas fa-users"></i> Nhân viên
                    <i class="fas fa-chevron-down"></i>
                  </a>
                  <ul class="dropdown-menu" :class="{ 'show': activeDropdown === 'employees' }">
                    <li>
                      <router-link to="/employees" class="dropdown-item">
                        <i class="fas fa-list"></i> Danh sách nhân viên
                      </router-link>
                    </li>
                    <li>
                      <router-link to="/employees/add" class="dropdown-item">
                        <i class="fas fa-plus"></i> Thêm nhân viên
                      </router-link>
                    </li>
                    <li>
                      <router-link to="/positions" class="dropdown-item">
                        <i class="fas fa-id-card"></i> Chức danh
                      </router-link>
                    </li>
                  </ul>
                </li>

                <li class="nav-item dropdown">
                  <a href="#" class="nav-link dropdown-toggle" @click.prevent="toggleDropdown('departments')">
                    <i class="fas fa-building"></i> Phòng ban
                    <i class="fas fa-chevron-down"></i>
                  </a>
                  <ul class="dropdown-menu" :class="{ 'show': activeDropdown === 'departments' }">
                    <li>
                      <router-link to="/departments" class="dropdown-item">
                        <i class="fas fa-list"></i> Danh sách phòng ban
                      </router-link>
                    </li>
                    <li>
                      <router-link to="/departments/add" class="dropdown-item">
                        <i class="fas fa-plus"></i> Thêm phòng ban
                      </router-link>
                    </li>
                  </ul>
                </li>

                <li class="nav-item dropdown">
                  <a href="#" class="nav-link dropdown-toggle" @click.prevent="toggleDropdown('factories')">
                    <i class="fas fa-industry"></i> Xí nghiệp
                    <i class="fas fa-chevron-down"></i>
                  </a>
                  <ul class="dropdown-menu" :class="{ 'show': activeDropdown === 'factories' }">
                    <li>
                      <router-link to="/factories" class="dropdown-item">
                        <i class="fas fa-list"></i> Danh sách xí nghiệp
                      </router-link>
                    </li>
                    <li>
                      <router-link to="/factories/add" class="dropdown-item">
                        <i class="fas fa-plus"></i> Thêm xí nghiệp
                      </router-link>
                    </li>
                  </ul>
                </li>

                <li class="nav-item dropdown">
                  <a href="#" class="nav-link dropdown-toggle" @click.prevent="toggleDropdown('more')">
                    <i class="fas fa-ellipsis-h"></i> Khác
                    <i class="fas fa-chevron-down"></i>
                  </a>
                  <ul class="dropdown-menu" :class="{ 'show': activeDropdown === 'more' }">
                    <li>
                      <router-link to="/recruitment" class="dropdown-item">
                        <i class="fas fa-user-plus"></i> Tuyển dụng
                      </router-link>
                    </li>
                    <li>
                      <router-link to="/assets" class="dropdown-item">
                        <i class="fas fa-laptop"></i> Tài sản
                      </router-link>
                    </li>
                    <li>
                      <router-link to="/documents" class="dropdown-item">
                        <i class="fas fa-file-alt"></i> Tài liệu
                      </router-link>
                    </li>
                    <li>
                      <router-link to="/company" class="dropdown-item">
                        <i class="fas fa-building"></i> Công ty
                      </router-link>
                    </li>
                  </ul>
                </li>
              </ul>
            </nav>

            <!-- User Menu and Notifications -->
            <div class="user-menu">
              <!-- Nút thông báo với nhãn -->
              <div class="notifications dropdown">
                <a href="#" class="dropdown-toggle notification-btn" @click.prevent="toggleDropdown('notifications')" title="Thông báo">
                  <div class="icon-container">
                    <i class="fas fa-bell"></i>
                    <span class="badge" v-if="unreadNotifications > 0">{{ unreadNotifications }}</span>
                  </div>
                  <span class="btn-label d-none d-md-inline">Thông báo</span>
                </a>
                <div class="dropdown-menu notifications-menu" :class="{ 'show': activeDropdown === 'notifications' }">
                  <div class="dropdown-header">
                    <h6>Thông báo</h6>
                  </div>
                  <div class="dropdown-body">
                    <div v-if="notifications.length === 0" class="no-notifications">
                      <p>Không có thông báo mới</p>
                    </div>
                    <div v-else class="notification-list">
                      <div v-for="notification in notifications" :key="notification.id" class="notification-item">
                        <div class="notification-icon">
                          <i class="fas fa-info-circle"></i>
                        </div>
                        <div class="notification-content">
                          <p class="notification-text">{{ notification.message }}</p>
                          <p class="notification-time">{{ notification.time }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="dropdown-footer" v-if="notifications.length > 0">
                    <router-link to="/notifications">Xem tất cả</router-link>
                  </div>
                </div>
              </div>

              <!-- Nút người dùng với nhãn -->
              <div class="user dropdown">
                <a href="#" class="dropdown-toggle user-btn" @click.prevent="toggleDropdown('user')" title="Tài khoản">
                  <div class="icon-container">
                    <i class="fas fa-user-circle"></i>
                  </div>
                  <span class="username">{{ username }}</span>
                </a>
                <div class="dropdown-menu user-menu" :class="{ 'show': activeDropdown === 'user' }">
                  <router-link to="/profile" class="dropdown-item">
                    <i class="fas fa-user"></i> Hồ sơ
                  </router-link>
                  <router-link to="/settings" class="dropdown-item">
                    <i class="fas fa-cog"></i> Cài đặt
                  </router-link>
                  <div class="dropdown-divider"></div>
                  <a href="#" class="dropdown-item" @click.prevent="logout">
                    <i class="fas fa-sign-out-alt"></i> Đăng xuất
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      <!-- Main Content -->
      <main class="app-main">
        <div class="container-fluid">
          <breadcrumb v-if="isAuthenticated" :items="breadcrumbs" />
          <router-view />
        </div>
      </main>

      <!-- Footer -->
      <footer class="app-footer" v-if="isAuthenticated">
        <div class="container-fluid">
          <div class="footer-content">
            <p class="copyright">© {{ currentYear }} {{ companyName }}. Bản quyền thuộc về công ty.</p>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script>
import BreadcrumbNav from '@/components/common/Breadcrumb.vue';
import { getBreadcrumbs } from '@/utils/breadcrumb';

export default {
  name: 'App',
  components: {
    Breadcrumb: BreadcrumbNav
  },
  data() {
    return {
      isReady: false,
      mobileMenuOpen: false,
      activeDropdown: null,
      notifications: [],
      unreadNotifications: 0,
      username: ''
    }
  },
  computed: {
    isAuthenticated() {
      return this.$store.getters['auth/isAuthenticated'];
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
    }
  },
  created() {
    // Kiểm tra xem người dùng đã đăng nhập chưa
    this.checkAuth();

    // Đóng dropdown khi click ra ngoài
    document.addEventListener('click', this.closeDropdownsOnClickOutside);

    // Lấy thông tin công ty
    this.fetchCompanyInfo();
  },
  beforeUnmount() {
    document.removeEventListener('click', this.closeDropdownsOnClickOutside);
  },
  methods: {
    async checkAuth() {
      try {
        // Kiểm tra token trong localStorage
        const token = localStorage.getItem('token');

        if (token) {
          // Nếu có token, kiểm tra tính hợp lệ
          await this.$store.dispatch('auth/checkAuth');

          // Nếu đăng nhập thành công, lấy thông báo
          if (this.isAuthenticated) {
            this.fetchNotifications();
            this.fetchUserInfo();
          }
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

    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen;
      // Đóng tất cả dropdown khi toggle mobile menu
      this.activeDropdown = null;
    },

    toggleDropdown(dropdown) {
      if (this.activeDropdown === dropdown) {
        this.activeDropdown = null;
      } else {
        this.activeDropdown = dropdown;
      }
    },

    closeDropdownsOnClickOutside(event) {
      const isDropdownToggle = event.target.closest('.dropdown-toggle');
      const isDropdownMenu = event.target.closest('.dropdown-menu');

      if (!isDropdownToggle && !isDropdownMenu) {
        this.activeDropdown = null;
      }
    },

    async fetchNotifications() {
      try {
        // Trong thực tế, bạn sẽ gọi API thực sự để lấy thông báo
        // const response = await this.$api.get('/notifications');

        // Tạm thời để trống, sẽ được cập nhật khi API thông báo được triển khai
        this.notifications = [];
        this.unreadNotifications = 0;
      } catch (error) {
        console.error('Lỗi khi lấy thông báo:', error);
      }
    },

    async fetchUserInfo() {
      try {
        // Lấy thông tin người dùng từ store
        const user = this.$store.getters['auth/currentUser'];
        if (user) {
          this.username = user.is_superuser ? 'Admin' : user.username;
        }
      } catch (error) {
        console.error('Lỗi khi lấy thông tin người dùng:', error);
      }
    },

    async logout() {
      try {
        await this.$store.dispatch('auth/logout');
        this.$router.push('/login');
      } catch (error) {
        console.error('Lỗi khi đăng xuất:', error);
      }
    },

    async fetchCompanyInfo() {
      try {
        await this.$store.dispatch('company/fetchCompanyInfo');
      } catch (error) {
        console.error('Lỗi khi lấy thông tin công ty:', error);
      }
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
.badge,
.dropdown-toggle[data-bs-toggle="dropdown"] .badge,
.btn-icon,
.btn-circle,
.avatar-img {
  border-radius: 50% !important;
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

// Header
.app-header {
  background: linear-gradient(90deg, $primary 0%, $primary-dark 100%);
  color: white;
  padding: 0;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

  .header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: $header-height;
    padding: 0 1rem;

    @media (max-width: $breakpoint-md) {
      padding: 0 0.5rem;
    }
  }

  .brand {
    .brand-link {
      display: flex;
      align-items: center;
      font-size: 1.5rem;
      font-weight: $font-weight-bold;
      color: white;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100%;

      @media (max-width: $breakpoint-md) {
        font-size: 1.2rem;
        max-width: 200px;
      }

      @media (max-width: $breakpoint-sm) {
        max-width: 150px;
      }

      .brand-logo {
        height: 40px;
        margin-right: 0.5rem;
        border-radius: 4px;
        flex-shrink: 0;

        @media (max-width: $breakpoint-sm) {
          height: 32px;
        }
      }

      span {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      i {
        margin-right: 0.5rem;
        flex-shrink: 0;
      }
    }
  }

  .main-nav {
    flex: 1;
    display: flex;
    justify-content: center;

    .mobile-menu-toggle {
      display: none;
      background-color: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: white;
      font-size: 1.5rem;
      cursor: pointer;
      padding: 0.5rem;
      z-index: 1001;
      border-radius: 4px;
      transition: all 0.2s ease;
      width: 40px;
      height: 40px;
      position: relative;

      &::after {
        content: 'Menu';
        position: absolute;
        bottom: -20px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 0.7rem;
        color: rgba(255, 255, 255, 0.7);
        white-space: nowrap;
        opacity: 0;
        transition: opacity 0.2s ease;
      }

      &:hover {
        background-color: rgba(255, 255, 255, 0.2);

        &::after {
          opacity: 1;
        }
      }

      &:active {
        background-color: rgba(255, 255, 255, 0.3);
      }

      @media (max-width: $breakpoint-lg) {
        display: flex;
        position: absolute;
        right: 1rem;
        align-items: center;
        justify-content: center;
      }
    }

    .nav-menu {
      display: flex;
      margin: 0;
      padding: 0;

      @media (max-width: $breakpoint-lg) {
        position: fixed;
        top: $header-height;
        left: 0;
        right: 0;
        flex-direction: column;
        background: $primary;
        padding: 1rem 0;
        display: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        max-height: calc(100vh - #{$header-height});
        overflow-y: auto;

        &.show {
          display: flex;
        }
      }

      .user-info-mobile {
        padding: 1.5rem 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1rem;
        background-color: rgba(0, 0, 0, 0.1);

        .user-info-container {
          display: flex;
          align-items: center;

          .user-avatar {
            margin-right: 1rem;

            img, i {
              width: 50px;
              height: 50px;
              border-radius: 50%;
              object-fit: cover;
              border: 2px solid rgba(255, 255, 255, 0.5);
            }

            i {
              font-size: 50px;
              color: white;
            }
          }

          .user-details {
            .user-name {
              font-weight: bold;
              color: white;
              font-size: 1.1rem;
              margin-bottom: 0.3rem;
            }

            .user-role {
              font-size: 0.85rem;
              color: rgba(255, 255, 255, 0.8);
              background-color: rgba(255, 255, 255, 0.1);
              padding: 0.2rem 0.5rem;
              border-radius: 3px;
              display: inline-block;
            }
          }
        }
      }

      .nav-item {
        position: relative;

        .nav-link {
          display: flex;
          align-items: center;
          padding: 0 1rem;
          height: $header-height;
          color: rgba(255, 255, 255, 0.9);
          transition: all 0.3s ease;

          @media (max-width: $breakpoint-lg) {
            height: auto;
            padding: 1rem;
            font-size: 1.1rem;
            border-left: 3px solid transparent;
          }

          &:hover, &.router-link-active {
            color: white;
            background-color: rgba(255, 255, 255, 0.1);

            @media (max-width: $breakpoint-lg) {
              border-left-color: $accent;
            }
          }

          i {
            margin-right: 0.75rem;
            width: 20px;
            text-align: center;
            font-size: 1.1rem;

            @media (max-width: $breakpoint-lg) {
              font-size: 1.2rem;
            }
          }

          .fa-chevron-down {
            margin-left: auto;
            font-size: 0.75rem;

            @media (max-width: $breakpoint-lg) {
              margin-right: 0;
            }
          }
        }

        .dropdown-menu {
          position: absolute;
          top: 100%;
          left: 0;
          min-width: 200px;
          background: white;
          border-radius: 4px;
          box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
          display: none;
          z-index: 1000;

          @media (max-width: $breakpoint-lg) {
            position: static;
            box-shadow: none;
            border-radius: 0;
            background: rgba(0, 0, 0, 0.15);
            padding: 0.5rem 0;
            margin: 0;
            border-left: 3px solid rgba(255, 255, 255, 0.1);
          }

          &.show {
            display: block;
          }

          .dropdown-item {
            display: flex;
            align-items: center;
            padding: 0.75rem 1rem;
            color: $dark;
            transition: all 0.3s ease;

            @media (max-width: $breakpoint-lg) {
              color: rgba(255, 255, 255, 0.9);
              padding: 0.75rem 1rem 0.75rem 2.5rem;
              font-size: 1rem;
              border-left: 3px solid transparent;
            }

            &:hover, &.router-link-active {
              background-color: rgba(0, 0, 0, 0.05);
              color: $primary;

              @media (max-width: $breakpoint-lg) {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border-left-color: $accent;
              }
            }

            i {
              margin-right: 0.75rem;
              width: 20px;
              text-align: center;

              @media (max-width: $breakpoint-lg) {
                font-size: 1.1rem;
              }
            }
          }
        }
      }
    }
  }

  .user-menu {
    display: flex;
    align-items: center;

    .dropdown {
      position: relative;
      margin-left: 1.5rem;
      z-index: 1001;

      @media (max-width: $breakpoint-sm) {
        margin-left: 1rem;
      }

      .dropdown-toggle {
        display: flex;
        align-items: center;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        transition: all 0.2s ease;
        position: relative;

        &:hover {
          background-color: rgba(255, 255, 255, 0.1);
        }

        &.notification-btn {
          background-color: rgba(255, 255, 255, 0.1);
          border: 1px solid rgba(255, 255, 255, 0.2);

          .icon-container {
            position: relative;
            margin-right: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 24px;
            height: 24px;
          }

          .btn-label {
            font-weight: 500;
            font-size: 0.9rem;
          }

          @media (max-width: $breakpoint-md) {
            padding: 0.5rem;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            justify-content: center;
          }
        }

        &.user-btn {
          background-color: rgba(0, 0, 0, 0.1);
          border: 1px solid rgba(255, 255, 255, 0.2);

          .icon-container {
            position: relative;
            margin-right: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 24px;
            height: 24px;
          }

          @media (max-width: $breakpoint-md) {
            background-color: transparent;
            border: none;
            padding: 0.5rem;
          }
        }

        i {
          font-size: 1.5rem;

          @media (max-width: $breakpoint-sm) {
            font-size: 1.3rem;
          }
        }

        .badge {
          position: absolute;
          top: -5px;
          right: -5px;
          background-color: $accent;
          color: white;
          border-radius: 50%;
          width: 20px;
          height: 20px;
          font-size: 0.75rem;
          display: flex;
          align-items: center;
          justify-content: center;
          border: 2px solid $primary;
          z-index: 2;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);

          @media (max-width: $breakpoint-sm) {
            width: 18px;
            height: 18px;
            font-size: 0.65rem;
            top: -3px;
            right: -3px;
          }
        }

        .username {
          margin-left: 0.5rem;
          display: none;
          font-weight: 500;

          @media (min-width: $breakpoint-md) {
            display: inline;
          }
        }
      }

      .dropdown-menu {
        position: absolute;
        top: 100%;
        right: 0;
        min-width: 200px;
        background: white;
        border-radius: 4px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        display: none;
        z-index: 1000;

        &.show {
          display: block;
        }

        &.notifications-menu {
          width: 300px;

          .dropdown-header {
            padding: 0.75rem 1rem;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);

            h6 {
              margin: 0;
              font-weight: $font-weight-bold;
            }
          }

          .dropdown-body {
            max-height: 300px;
            overflow-y: auto;

            .no-notifications {
              padding: 1rem;
              text-align: center;
              color: $secondary;
            }

            .notification-item {
              display: flex;
              padding: 0.75rem 1rem;
              border-bottom: 1px solid rgba(0, 0, 0, 0.05);

              &:hover {
                background-color: rgba(0, 0, 0, 0.02);
              }

              .notification-icon {
                margin-right: 0.75rem;
                color: $primary;
              }

              .notification-content {
                flex: 1;

                .notification-text {
                  margin: 0;
                  font-size: 0.875rem;
                }

                .notification-time {
                  margin: 0;
                  font-size: 0.75rem;
                  color: $secondary;
                }
              }
            }
          }

          .dropdown-footer {
            padding: 0.75rem 1rem;
            text-align: center;
            border-top: 1px solid rgba(0, 0, 0, 0.1);

            a {
              color: $primary;
              font-weight: $font-weight-bold;

              &:hover {
                text-decoration: underline;
              }
            }
          }
        }

        &.user-menu {
          .dropdown-item {
            display: flex;
            align-items: center;
            padding: 0.75rem 1rem;
            color: $dark;
            transition: all 0.3s ease;

            &:hover {
              background-color: rgba(0, 0, 0, 0.05);
              color: $primary;
            }

            i {
              margin-right: 0.5rem;
              width: 20px;
              text-align: center;
            }
          }

          .dropdown-divider {
            height: 1px;
            background-color: rgba(0, 0, 0, 0.1);
            margin: 0.5rem 0;
          }
        }
      }
    }
  }
}

// Main content
.app-main {
  flex: 1;
  padding: 2rem 0;
  background-color: #f5f5f5;
}

// Footer
.app-footer {
  background: $primary;
  color: rgba(255, 255, 255, 0.8);
  padding: 1rem 0;

  .footer-content {
    display: flex;
    justify-content: center;
    align-items: center;

    .copyright {
      margin: 0;
      text-align: center;
    }
  }
}

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
</style>
