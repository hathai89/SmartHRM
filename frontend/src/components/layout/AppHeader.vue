<template>
  <header class="app-header">
    <div class="container-fluid">
      <div class="header-content">
        <!-- Logo -->
        <div class="brand">
          <router-link to="/dashboard" class="brand-link">
            <img src="@/assets/images/logo.png" alt="Logo" class="brand-logo">
          </router-link>
        </div>

        <!-- Menu chính -->
        <nav class="main-nav">
          <button class="mobile-menu-toggle" :class="{ 'active': mobileMenuOpen }" @click="toggleMobileMenu($event)" ref="menuToggleBtn">
            <font-awesome-icon icon="bars" />
          </button>

          <ul class="nav-menu" :class="{ 'show': mobileMenuOpen }">
            <!-- Dashboard -->
            <li class="nav-item">
              <router-link to="/dashboard" class="nav-link">
                <font-awesome-icon icon="home" />
                <span>Dashboard</span>
              </router-link>
            </li>

            <!-- Nhân viên -->
            <li class="nav-item dropdown">
              <a href="#" class="nav-link" @click.prevent="toggleDropdown('employees')">
                <font-awesome-icon icon="users" />
                <span>Nhân viên</span>
                <font-awesome-icon icon="chevron-down" class="dropdown-icon" />
              </a>
              <ul class="dropdown-menu" :class="{ 'show': activeDropdown === 'employees' }">
                <li>
                  <router-link to="/employees" class="dropdown-item">
                    <font-awesome-icon icon="list" />
                    <span>Danh sách nhân viên</span>
                  </router-link>
                </li>
                <li v-if="isAdmin">
                  <router-link to="/employees/create" class="dropdown-item">
                    <font-awesome-icon icon="user-plus" />
                    <span>Thêm nhân viên</span>
                  </router-link>
                </li>
              </ul>
            </li>

            <!-- Phòng ban -->
            <li class="nav-item dropdown">
              <a href="#" class="nav-link" @click.prevent="toggleDropdown('departments')">
                <font-awesome-icon icon="building" />
                <span>Phòng ban</span>
                <font-awesome-icon icon="chevron-down" class="dropdown-icon" />
              </a>
              <ul class="dropdown-menu" :class="{ 'show': activeDropdown === 'departments' }">
                <li>
                  <router-link to="/departments" class="dropdown-item">
                    <font-awesome-icon icon="list" />
                    <span>Danh sách phòng ban</span>
                  </router-link>
                </li>
                <li v-if="isAdmin">
                  <router-link to="/departments/create" class="dropdown-item">
                    <font-awesome-icon icon="plus" />
                    <span>Thêm phòng ban</span>
                  </router-link>
                </li>
              </ul>
            </li>

            <!-- Xí nghiệp -->
            <li class="nav-item dropdown">
              <a href="#" class="nav-link" @click.prevent="toggleDropdown('factories')">
                <font-awesome-icon icon="industry" />
                <span>Xí nghiệp</span>
                <font-awesome-icon icon="chevron-down" class="dropdown-icon" />
              </a>
              <ul class="dropdown-menu" :class="{ 'show': activeDropdown === 'factories' }">
                <li>
                  <router-link to="/factories" class="dropdown-item">
                    <font-awesome-icon icon="list" />
                    <span>Danh sách xí nghiệp</span>
                  </router-link>
                </li>
                <li v-if="isAdmin">
                  <router-link to="/factories/create" class="dropdown-item">
                    <font-awesome-icon icon="plus" />
                    <span>Thêm xí nghiệp</span>
                  </router-link>
                </li>
              </ul>
            </li>

            <!-- Tài liệu -->
            <li class="nav-item dropdown">
              <a href="#" class="nav-link" @click.prevent="toggleDropdown('documents')">
                <font-awesome-icon icon="file-alt" />
                <span>Tài liệu</span>
                <font-awesome-icon icon="chevron-down" class="dropdown-icon" />
              </a>
              <ul class="dropdown-menu" :class="{ 'show': activeDropdown === 'documents' }">
                <li>
                  <router-link to="/documents" class="dropdown-item">
                    <font-awesome-icon icon="list" />
                    <span>Danh sách tài liệu</span>
                  </router-link>
                </li>
                <li v-if="isAdmin">
                  <router-link to="/documents/create" class="dropdown-item">
                    <font-awesome-icon icon="plus" />
                    <span>Thêm tài liệu</span>
                  </router-link>
                </li>
                <li v-if="isAdmin">
                  <router-link to="/document-categories" class="dropdown-item">
                    <font-awesome-icon icon="folder" />
                    <span>Danh mục tài liệu</span>
                  </router-link>
                </li>
              </ul>
            </li>

            <!-- Tuyển dụng -->
            <li class="nav-item dropdown">
              <a href="#" class="nav-link" @click.prevent="toggleDropdown('recruitment')">
                <font-awesome-icon icon="user-tie" />
                <span>Tuyển dụng</span>
                <font-awesome-icon icon="chevron-down" class="dropdown-icon" />
              </a>
              <ul class="dropdown-menu" :class="{ 'show': activeDropdown === 'recruitment' }">
                <li>
                  <router-link to="/job-postings" class="dropdown-item">
                    <font-awesome-icon icon="list" />
                    <span>Tin tuyển dụng</span>
                  </router-link>
                </li>
                <li v-if="isAdmin">
                  <router-link to="/job-postings/create" class="dropdown-item">
                    <font-awesome-icon icon="plus" />
                    <span>Thêm tin tuyển dụng</span>
                  </router-link>
                </li>
                <li>
                  <router-link to="/job-applications" class="dropdown-item">
                    <font-awesome-icon icon="file-signature" />
                    <span>Đơn ứng tuyển</span>
                  </router-link>
                </li>
                <li>
                  <router-link to="/interviews" class="dropdown-item">
                    <font-awesome-icon icon="calendar-check" />
                    <span>Lịch phỏng vấn</span>
                  </router-link>
                </li>
              </ul>
            </li>

            <!-- Tài sản -->
            <li class="nav-item dropdown">
              <a href="#" class="nav-link" @click.prevent="toggleDropdown('assets')">
                <font-awesome-icon icon="laptop" />
                <span>Tài sản</span>
                <font-awesome-icon icon="chevron-down" class="dropdown-icon" />
              </a>
              <ul class="dropdown-menu" :class="{ 'show': activeDropdown === 'assets' }">
                <li>
                  <router-link to="/assets" class="dropdown-item">
                    <font-awesome-icon icon="list" />
                    <span>Danh sách tài sản</span>
                  </router-link>
                </li>
                <li v-if="isAdmin">
                  <router-link to="/assets/create" class="dropdown-item">
                    <font-awesome-icon icon="plus" />
                    <span>Thêm tài sản</span>
                  </router-link>
                </li>
                <li v-if="isAdmin">
                  <router-link to="/asset-categories" class="dropdown-item">
                    <font-awesome-icon icon="tags" />
                    <span>Danh mục tài sản</span>
                  </router-link>
                </li>
              </ul>
            </li>

            <!-- Công ty -->
            <li class="nav-item">
              <router-link to="/company" class="nav-link">
                <font-awesome-icon icon="building" />
                <span>Công ty</span>
              </router-link>
            </li>

            <!-- Quản trị (chỉ cho admin) -->
            <li v-if="isAdmin" class="nav-item dropdown">
              <a href="#" class="nav-link" @click.prevent="toggleDropdown('admin')">
                <font-awesome-icon icon="cog" />
                <span>Quản trị</span>
                <font-awesome-icon icon="chevron-down" class="dropdown-icon" />
              </a>
              <ul class="dropdown-menu" :class="{ 'show': activeDropdown === 'admin' }">
                <li>
                  <router-link to="/settings" class="dropdown-item">
                    <font-awesome-icon icon="cog" />
                    <span>Cài đặt</span>
                  </router-link>
                </li>
                <li>
                  <router-link to="/logs" class="dropdown-item">
                    <font-awesome-icon icon="history" />
                    <span>Nhật ký</span>
                  </router-link>
                </li>
              </ul>
            </li>
          </ul>
        </nav>

        <!-- Phần bên phải -->
        <div class="header-right">
          <!-- Thông báo -->
          <div class="dropdown notification-dropdown">
            <button class="btn btn-icon notification-btn" @click="toggleDropdown('notifications')" ref="notificationBtn">
              <font-awesome-icon icon="bell" />
              <span v-if="unreadCount > 0" class="badge">{{ unreadCount }}</span>
            </button>
            <div class="dropdown-menu dropdown-menu-end" :class="{ 'show': activeDropdown === 'notifications' }">
              <div class="dropdown-header">
                <h6>{{ $t('notifications.title') }}</h6>
              </div>
              <div class="dropdown-body">
                <div v-if="!notifications || notifications.length === 0" class="dropdown-item text-center">
                  {{ $t('notifications.noNotifications') || 'Không có thông báo' }}
                </div>
                <template v-else>
                  <a v-for="notification in notifications.slice(0, 5)" :key="notification.id"
                     class="dropdown-item notification-item"
                     href="#"
                     @click.prevent="viewNotification(notification)">
                    <div class="notification-icon">
                      <font-awesome-icon :icon="getNotificationIcon(notification.notification_type)"
                                        :class="getNotificationIconClass(notification.priority)" />
                    </div>
                    <div class="notification-content">
                      <div class="notification-title">{{ notification.title }}</div>
                      <div class="notification-message">{{ notification.message }}</div>
                      <div class="notification-time">{{ formatDate(notification.created_at) }}</div>
                    </div>
                    <div v-if="!notification.is_read" class="notification-badge">
                      <span class="badge-new">{{ $t('notifications.new') }}</span>
                    </div>
                  </a>
                </template>
              </div>
              <div class="dropdown-footer" v-if="notifications && notifications.length > 0">
                <button class="btn btn-sm btn-link" @click="markAllAsRead">
                  {{ $t('notifications.markAllAsRead') || 'Đánh dấu tất cả đã đọc' }}
                </button>
                <router-link to="/notifications" class="btn btn-sm btn-link">
                  {{ $t('notifications.viewAll') || 'Xem tất cả' }}
                </router-link>
              </div>
            </div>
          </div>

          <!-- Người dùng -->
          <div class="dropdown user-dropdown">
            <button class="btn btn-icon user-btn" @click="toggleDropdown('user')" ref="userBtn">
              <img v-if="currentUser && currentUser.avatar"
                   :src="currentUser.avatar"
                   alt="Avatar"
                   class="user-avatar">
              <font-awesome-icon v-else icon="user-circle" class="user-icon" />
              <span class="username d-none d-lg-inline">
                {{ currentUser ? (currentUser.is_superuser ? 'Admin' : currentUser.username) : '' }}
              </span>
            </button>
            <div class="dropdown-menu dropdown-menu-end" :class="{ 'show': activeDropdown === 'user' }">
              <div class="dropdown-header">
                <h6>{{ currentUser ? currentUser.full_name : '' }}</h6>
              </div>
              <router-link to="/profile" class="dropdown-item">
                <font-awesome-icon icon="user" class="item-icon" />
                <span>Hồ sơ cá nhân</span>
              </router-link>
              <router-link to="/change-password" class="dropdown-item">
                <font-awesome-icon icon="lock" class="item-icon" />
                <span>Đổi mật khẩu</span>
              </router-link>
              <div class="dropdown-divider"></div>
              <a href="#" class="dropdown-item" @click.prevent="logout">
                <font-awesome-icon icon="sign-out-alt" class="item-icon" />
                <span>Đăng xuất</span>
              </a>
            </div>
          </div>
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
  data() {
    return {
      activeDropdown: null,
      mobileMenuOpen: false
    }
  },
  computed: {
    ...mapGetters({
      currentUser: 'auth/currentUser',
      notifications: 'notifications/allNotifications',
      unreadCount: 'notifications/unreadCount',
      companyInfo: 'company/companyInfo',
      isAdmin: 'auth/isAdmin'
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
    toggleMobileMenu(event) {
      this.mobileMenuOpen = !this.mobileMenuOpen;
      // Đóng tất cả dropdown khi toggle mobile menu
      this.activeDropdown = null;
      console.log('Mobile menu toggled:', this.mobileMenuOpen);

      // Ngăn chặn sự kiện click lan ra ngoài
      if (event) {
        event.stopPropagation();
      }
    },
    toggleDropdown(dropdown) {
      if (this.activeDropdown === dropdown) {
        this.activeDropdown = null;
      } else {
        this.activeDropdown = dropdown;
      }
    },
    closeDropdowns() {
      this.activeDropdown = null;
    },
    closeDropdownsOnClickOutside(event) {
      // Kiểm tra xem click có phải là bên ngoài dropdown không
      const isNotificationBtn = this.$refs.notificationBtn && this.$refs.notificationBtn.contains(event.target);
      const isUserBtn = this.$refs.userBtn && this.$refs.userBtn.contains(event.target);
      const isDropdownMenu = event.target.closest('.dropdown-menu');
      const isNavLink = event.target.closest('.nav-link');
      const isMenuToggle = this.$refs.menuToggleBtn && this.$refs.menuToggleBtn.contains(event.target);

      if (!isNotificationBtn && !isUserBtn && !isDropdownMenu && !isNavLink && !isMenuToggle) {
        this.closeDropdowns();
        this.mobileMenuOpen = false;
      }
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

      // Đóng dropdown
      this.closeDropdowns();
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

    // Thêm event listener để đóng dropdown khi click ra ngoài
    document.addEventListener('click', this.closeDropdownsOnClickOutside)
  },
  beforeUnmount() {
    // Xóa event listener khi component bị hủy
    document.removeEventListener('click', this.closeDropdownsOnClickOutside)
  }
}
</script>

<style lang="scss" scoped>
.app-header {
  background: linear-gradient(90deg, #0a3d62 0%, #0a3d62 60%, #ff7f50 100%);
  color: white;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  padding: 0;
  height: 50px;

  @media (max-width: 991px) {
    height: 50px;
    min-height: 50px;
  }

  @media (max-width: 767px) {
    height: 50px;
    min-height: 50px;
  }

  .container-fluid {
    height: 100%;
  }

  .header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 100%;
    padding: 0 0.5rem;
    width: 100%;
    max-width: 100%;
    overflow-x: hidden;

    @media (max-width: 991px) {
      flex-wrap: wrap;
      padding: 10px 0.5rem;
      position: relative;
      justify-content: flex-start;
    }
  }

  // Main navigation
  .main-nav {
    flex: 1;
    display: flex;
    justify-content: flex-start;
    position: relative;
    margin: 0 10px;
    overflow-x: auto;
    -ms-overflow-style: none;  /* IE and Edge */
    scrollbar-width: none;  /* Firefox */

    /* Hide scrollbar for Chrome, Safari and Opera */
    &::-webkit-scrollbar {
      display: none;
    }

    @media (max-width: 991px) {
      position: static;
      min-height: 0;
      margin: 0;
    }

    .mobile-menu-toggle {
      display: flex;
      background-color: transparent;
      border: none;
      color: white;
      font-size: 1.25rem;
      cursor: pointer;
      padding: 0.5rem;
      border-radius: 4px;
      transition: all 0.2s ease;
      width: 40px;
      height: 40px;
      align-items: center;
      justify-content: center;
      z-index: 1010;
      position: absolute;
      right: 10px;
      top: 10px;

      &:hover {
        background-color: rgba(255, 255, 255, 0.1);
      }

      &:focus {
        outline: none;
      }

      &.active, &:active {
        background-color: rgba(255, 255, 255, 0.15);
      }

      @media (min-width: 992px) {
        display: none;
      }
    }

    .nav-menu {
      display: flex;
      margin: 0;
      padding: 0;
      background-color: transparent;

      @media (max-width: 991px) {
        position: fixed;
        top: 50px;
        left: 0;
        right: 0;
        flex-direction: column;
        background: #0a3d62;
        padding: 1rem 0;
        display: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 1020;
        max-height: calc(100vh - 50px);
        overflow-y: auto;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        opacity: 0;
        visibility: hidden;
        transition: opacity 0.3s ease, visibility 0.3s ease;

        &.show {
          display: flex !important;
          opacity: 1;
          visibility: visible;
        }
      }

      .nav-item {
        position: relative;

        .nav-link {
          display: flex;
          align-items: center;
          padding: 0 0.5rem;
          height: 50px;
          color: white;
          font-weight: 500;
          transition: all 0.3s ease;
          white-space: nowrap;
          font-size: 0.9rem;

          @media (max-width: 991px) {
            height: auto;
            padding: 1rem;
            font-size: 1.1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
          }

          &:hover, &.router-link-active {
            color: white;
            background-color: rgba(255, 255, 255, 0.2);
            border-bottom: 3px solid #ff6600;

            @media (max-width: 991px) {
              border-bottom: 1px solid rgba(255, 255, 255, 0.05);
              border-left: 3px solid #ff6600;
            }
          }

          svg {
            margin-right: 0.3rem;
            width: 16px;
            text-align: center;
            font-size: 0.9rem;
          }

          span {
            margin-right: 0.3rem;
          }

          .dropdown-icon {
            margin-left: 0.25rem;
            font-size: 0.75rem;
            transition: transform 0.2s ease;
          }
        }

        &.dropdown {
          .nav-link {
            padding-right: 0.8rem;
          }

          &.active .dropdown-icon {
            transform: rotate(180deg);
          }
        }

        .dropdown-menu {
          position: absolute;
          top: 100%;
          left: 0;
          min-width: 220px;
          background: white;
          border-radius: 4px;
          box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
          display: none;
          z-index: 1000;

          @media (max-width: 991px) {
            position: static;
            box-shadow: none;
            border-radius: 0;
            background: rgba(0, 0, 0, 0.15);
            padding: 0;
            margin: 0;
            width: 100%;
          }

          &.show {
            display: block;
          }

          .dropdown-item {
            display: flex;
            align-items: center;
            padding: 0.75rem 1rem;
            color: #343a40;
            transition: all 0.3s ease;

            @media (max-width: 991px) {
              color: white;
              padding: 0.75rem 1rem 0.75rem 2.5rem;
              font-size: 1rem;
            }

            &:hover {
              background-color: rgba(0, 0, 0, 0.05);
              color: #003366;

              @media (max-width: 991px) {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
              }
            }

            svg {
              margin-right: 0.75rem;
              width: 20px;
              text-align: center;
              color: #6c757d;

              @media (max-width: 991px) {
                color: rgba(255, 255, 255, 0.7);
              }
            }
          }
        }
      }
    }
  }

  // Brand
  .brand {
    display: flex;
    align-items: center;
    flex-shrink: 0;

    @media (max-width: 991px) {
      max-width: 60%;
    }

    .brand-link {
      display: flex;
      align-items: center;
      color: white;
      text-decoration: none;
      font-weight: 600;

      .brand-logo {
        height: 36px;
        margin-right: 0.5rem;
        border-radius: 4px;

        @media (max-width: 576px) {
          height: 30px;
        }
      }

      .brand-text {
        font-size: 1.25rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 200px;

        @media (max-width: 768px) {
          max-width: 150px;
          font-size: 1.1rem;
        }

        @media (max-width: 576px) {
          max-width: 120px;
          font-size: 1rem;
        }
      }
    }
  }

  // Header right
  .header-right {
    display: flex;
    align-items: center;
    margin-left: 0.5rem;
    flex-shrink: 0;

    @media (max-width: 991px) {
      position: absolute;
      right: 60px;
      top: 10px;
    }

    .dropdown {
      position: relative;
      margin-left: 0.75rem;

      .btn-icon {
        background: transparent;
        border: none;
        color: white;
        font-size: 1.25rem;
        padding: 0.5rem;
        border-radius: 4px;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        transition: all 0.2s ease;

        &:hover {
          background-color: rgba(255, 255, 255, 0.1);
        }

        &:focus {
          outline: none;
        }

        .badge {
          position: absolute;
          top: 0;
          right: 0;
          background-color: #ff7f50;
          color: white;
          border-radius: 4px;
          min-width: 18px;
          height: 18px;
          font-size: 0.7rem;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 0 4px;
          border: none;
          transform: translate(25%, -25%);
        }
      }

      .user-btn {
        display: flex;
        align-items: center;
        padding: 0.5rem;
        border-radius: 4px;
        background-color: transparent;
        width: auto;
        height: 40px;

        @media (max-width: 991px) {
          padding: 0.25rem;
          width: 40px;
          border-radius: 4px;
          justify-content: center;
          transition: all 0.2s ease;

          &:hover, &:active {
            background-color: rgba(255, 255, 255, 0.1);
          }
        }

        .user-avatar {
          width: 32px;
          height: 32px;
          border-radius: 50%;
          object-fit: cover;
          border: 2px solid rgba(255, 255, 255, 0.5);
        }

        .user-icon {
          font-size: 1.75rem;
          color: white;
          filter: drop-shadow(0 0 1px rgba(255, 255, 255, 0.5));
        }

        .username {
          margin-left: 0.5rem;
          font-weight: 500;
          font-size: 0.9rem;
        }
      }

      .dropdown-menu {
        position: absolute;
        top: 100%;
        right: 0;
        margin-top: 0.5rem;
        min-width: 240px;
        background: white;
        border-radius: 4px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        overflow: hidden;
        display: none;
        animation: fadeIn 0.2s ease;

        &.show {
          display: block;
        }

        .dropdown-header {
          padding: 1rem;
          background-color: #f8f9fa;
          border-bottom: 1px solid #e9ecef;

          h6 {
            margin: 0;
            font-weight: 600;
            color: #343a40;
          }
        }

        .dropdown-body {
          max-height: 300px;
          overflow-y: auto;
        }

        .dropdown-footer {
          padding: 0.75rem 1rem;
          background-color: #f8f9fa;
          border-top: 1px solid #e9ecef;
          display: flex;
          justify-content: space-between;

          .btn-link {
            color: #003366;
            padding: 0.25rem 0.5rem;
            font-size: 0.875rem;
            text-decoration: none;

            &:hover {
              text-decoration: underline;
            }
          }
        }

        .dropdown-item {
          display: flex;
          align-items: center;
          padding: 0.75rem 1rem;
          color: #343a40;
          text-decoration: none;
          transition: all 0.2s ease;

          &:hover {
            background-color: rgba(0, 0, 0, 0.05);
          }

          .item-icon {
            margin-right: 0.75rem;
            width: 20px;
            color: #6c757d;
          }
        }

        .dropdown-divider {
          height: 1px;
          background-color: #e9ecef;
          margin: 0.5rem 0;
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
            display: flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
            background-color: rgba(0, 0, 0, 0.05);
            border-radius: 50%;
            flex-shrink: 0;

            svg {
              font-size: 1rem;
            }
          }

          .notification-content {
            flex: 1;
            min-width: 0;

            .notification-title {
              font-weight: 600;
              margin-bottom: 0.25rem;
              font-size: 0.875rem;
            }

            .notification-message {
              color: #6c757d;
              font-size: 0.8125rem;
              margin-bottom: 0.25rem;
              white-space: nowrap;
              overflow: hidden;
              text-overflow: ellipsis;
            }

            .notification-time {
              color: #adb5bd;
              font-size: 0.75rem;
            }
          }

          .notification-badge {
            margin-left: 0.5rem;
            flex-shrink: 0;

            .badge-new {
              display: inline-block;
              background-color: #ff7f50;
              color: white;
              font-size: 0.75rem;
              padding: 0.25rem 0.5rem;
              border-radius: 4px;
              box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            }
          }
        }
      }
    }
  }
}

// Animation
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

// CSS Variables
:root {
  --primary: #0a3d62;
  --primary-dark: #0c2461;
  --accent: #ff7f50;
}
</style>
