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
                <span>Hachiba</span>
              </router-link>
            </div>

            <!-- Main Navigation -->
            <nav class="main-nav">
              <button class="mobile-menu-toggle" @click="toggleMobileMenu">
                <i class="fas fa-bars"></i>
              </button>

              <ul class="nav-menu" :class="{ 'show': mobileMenuOpen }">
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
              <div class="notifications dropdown">
                <a href="#" class="dropdown-toggle" @click.prevent="toggleDropdown('notifications')">
                  <i class="fas fa-bell"></i>
                  <span class="badge" v-if="unreadNotifications > 0">{{ unreadNotifications }}</span>
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

              <div class="user dropdown">
                <a href="#" class="dropdown-toggle" @click.prevent="toggleDropdown('user')">
                  <i class="fas fa-user-circle"></i>
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
            <p class="copyright">© {{ currentYear }} CÔNG TY CỔ PHẦN DỆT MAY 29/3. Bản quyền thuộc về công ty.</p>
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
      username: 'Admin'
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
    }
  },
  created() {
    // Kiểm tra xem người dùng đã đăng nhập chưa
    this.checkAuth();

    // Đóng dropdown khi click ra ngoài
    document.addEventListener('click', this.closeDropdownsOnClickOutside);
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
        // Giả lập API call
        // Trong thực tế, bạn sẽ gọi API thực sự
        // const response = await this.$api.get('/notifications');

        // Dữ liệu mẫu
        setTimeout(() => {
          this.notifications = [
            { id: 1, message: 'Có 3 nhân viên mới cần phê duyệt', time: '10 phút trước', read: false },
            { id: 2, message: 'Báo cáo tháng đã được cập nhật', time: '1 giờ trước', read: false },
            { id: 3, message: 'Lịch họp tuần đã được cập nhật', time: '2 giờ trước', read: true }
          ];

          this.unreadNotifications = this.notifications.filter(n => !n.read).length;
        }, 1000);
      } catch (error) {
        console.error('Lỗi khi lấy thông báo:', error);
      }
    },

    async fetchUserInfo() {
      try {
        // Giả lập API call
        // Trong thực tế, bạn sẽ gọi API thực sự
        // const response = await this.$api.get('/user/profile');

        // Dữ liệu mẫu
        setTimeout(() => {
          this.username = 'Nguyễn Văn A';
        }, 1000);
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

body {
  font-family: $font-family-sans-serif;
  font-size: $font-size-base;
  line-height: 1.5;
  color: $dark;
  background-color: #f5f5f5;
}

a {
  text-decoration: none;
  color: inherit;
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
  }

  .brand {
    .brand-link {
      display: flex;
      align-items: center;
      font-size: 1.5rem;
      font-weight: $font-weight-bold;
      color: white;

      .brand-logo {
        height: 40px;
        margin-right: 0.5rem;
        border-radius: 4px;
      }

      i {
        margin-right: 0.5rem;
      }
    }
  }

  .main-nav {
    flex: 1;
    display: flex;
    justify-content: center;

    .mobile-menu-toggle {
      display: none;
      background: none;
      border: none;
      color: white;
      font-size: 1.5rem;
      cursor: pointer;

      @media (max-width: $breakpoint-lg) {
        display: block;
        position: absolute;
        right: 1rem;
      }
    }

    .nav-menu {
      display: flex;
      margin: 0;
      padding: 0;

      @media (max-width: $breakpoint-lg) {
        position: absolute;
        top: $header-height;
        left: 0;
        right: 0;
        flex-direction: column;
        background: $primary;
        padding: 1rem 0;
        display: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);

        &.show {
          display: flex;
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
            padding: 0.75rem 1rem;
          }

          &:hover, &.router-link-active {
            color: white;
            background-color: rgba(255, 255, 255, 0.1);
          }

          i {
            margin-right: 0.5rem;
          }

          .fa-chevron-down {
            margin-left: 0.5rem;
            font-size: 0.75rem;
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
            background: rgba(0, 0, 0, 0.1);
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
            }

            &:hover, &.router-link-active {
              background-color: rgba(0, 0, 0, 0.05);
              color: $primary;

              @media (max-width: $breakpoint-lg) {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
              }
            }

            i {
              margin-right: 0.5rem;
              width: 20px;
              text-align: center;
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
      margin-left: 1rem;

      .dropdown-toggle {
        display: flex;
        align-items: center;
        color: white;

        i {
          font-size: 1.25rem;
        }

        .badge {
          position: absolute;
          top: -5px;
          right: -5px;
          background-color: $accent;
          color: white;
          border-radius: 50%;
          width: 18px;
          height: 18px;
          font-size: 0.75rem;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .username {
          margin-left: 0.5rem;
          display: none;

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
