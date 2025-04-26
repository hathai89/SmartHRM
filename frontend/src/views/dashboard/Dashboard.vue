<template>
  <div class="dashboard">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="h3">Bảng điều khiển</h1>
      <div class="d-flex">
        <button class="btn btn-outline-secondary me-2" @click="refreshData">
          <font-awesome-icon icon="sync" :class="{ 'fa-spin': loading }" />
          Làm mới
        </button>
      </div>
    </div>

      <div v-if="loading">
        <loading-spinner />
      </div>

      <template v-else>
        <!-- Welcome message -->
        <div class="card mb-4 card-gradient">
          <div class="card-header">
            <h5 class="mb-0">Chào mừng đến với hệ thống quản lý nhân sự</h5>
          </div>
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="me-4">
                <img v-if="companyInfo && companyInfo.logo_url" :src="companyInfo.logo_url" alt="Logo công ty" style="max-height: 80px; max-width: 100%;">
                <i v-else class="fas fa-building fa-4x text-primary"></i>
              </div>
              <div>
                <h4 class="mb-2">{{ companyInfo ? companyInfo.name : 'CÔNG TY CỔ PHẦN DỆT MAY 29/3' }}</h4>
                <p class="mb-1"><i class="fas fa-map-marker-alt me-2"></i>{{ companyInfo ? companyInfo.address : 'Đang tải...' }}</p>
                <p class="mb-1"><i class="fas fa-phone me-2"></i>{{ companyInfo ? companyInfo.phone : 'Đang tải...' }}</p>
                <p class="mb-0"><i class="fas fa-envelope me-2"></i>{{ companyInfo ? companyInfo.email : 'Đang tải...' }}</p>
              </div>
            </div>
            <div class="mt-3">
              <p class="card-text">{{ new Date().toLocaleDateString('vi-VN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }) }}</p>
            </div>
          </div>
        </div>

        <!-- Stats cards -->
        <div class="row">
          <div class="col-md-3 col-sm-6 mb-4">
            <div class="card dashboard-card bg-gradient-primary text-white">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="card-title">Tổng số nhân viên</h6>
                    <h2 class="mb-0">{{ stats.totalEmployees }}</h2>
                  </div>
                  <div>
                    <font-awesome-icon icon="users" size="2x" />
                  </div>
                </div>
              </div>
              <div class="card-footer">
                <router-link to="/employees" class="text-white">
                  Xem chi tiết <font-awesome-icon icon="arrow-right" />
                </router-link>
              </div>
            </div>
          </div>

          <div class="col-md-3 col-sm-6 mb-4">
            <div class="card dashboard-card bg-gradient-horizontal text-white">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="card-title">Phòng ban</h6>
                    <h2 class="mb-0">{{ stats.totalDepartments }}</h2>
                  </div>
                  <div>
                    <font-awesome-icon icon="building" size="2x" />
                  </div>
                </div>
              </div>
              <div class="card-footer">
                <router-link to="/departments" class="text-white">
                  Xem chi tiết <font-awesome-icon icon="arrow-right" />
                </router-link>
              </div>
            </div>
          </div>

          <div class="col-md-3 col-sm-6 mb-4">
            <div class="card dashboard-card card-accent text-white">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="card-title">Xí nghiệp</h6>
                    <h2 class="mb-0">{{ stats.totalFactories }}</h2>
                  </div>
                  <div>
                    <font-awesome-icon icon="industry" size="2x" />
                  </div>
                </div>
              </div>
              <div class="card-footer">
                <router-link to="/factories" class="text-white">
                  Xem chi tiết <font-awesome-icon icon="arrow-right" />
                </router-link>
              </div>
            </div>
          </div>

          <div class="col-md-3 col-sm-6 mb-4">
            <div class="card dashboard-card bg-gradient-primary text-white">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="card-title">Tài liệu</h6>
                    <h2 class="mb-0">{{ stats.totalDocuments }}</h2>
                  </div>
                  <div>
                    <font-awesome-icon icon="file-alt" size="2x" />
                  </div>
                </div>
              </div>
              <div class="card-footer">
                <router-link to="/documents" class="text-white">
                  Xem chi tiết <font-awesome-icon icon="arrow-right" />
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent activities and notifications -->
        <div class="row">
          <div class="col-lg-8 mb-4">
            <div class="card card-gradient">
              <div class="card-header">
                <h5 class="card-title mb-0">Hoạt động gần đây</h5>
              </div>
              <div class="card-body">
                <div v-if="activities.length === 0" class="text-center py-3">
                  <p class="text-muted">Không có hoạt động nào gần đây</p>
                </div>
                <ul v-else class="list-group list-group-flush">
                  <li v-for="(activity, index) in activities" :key="index" class="list-group-item">
                    <div class="d-flex align-items-center">
                      <div class="flex-shrink-0">
                        <font-awesome-icon :icon="getActivityIcon(activity.type)" class="me-3" />
                      </div>
                      <div class="flex-grow-1 ms-3">
                        <div>{{ activity.description }}</div>
                        <small class="text-muted">{{ formatDate(activity.timestamp) }}</small>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <div class="col-lg-4 mb-4">
            <div class="card card-accent">
              <div class="card-header">
                <h5 class="card-title mb-0">Thông báo</h5>
              </div>
              <div class="card-body">
                <div v-if="notifications.length === 0" class="text-center py-3">
                  <p class="text-muted">Không có thông báo nào</p>
                </div>
                <ul v-else class="list-group list-group-flush">
                  <li v-for="notification in notifications.slice(0, 5)" :key="notification.id" class="list-group-item">
                    <div class="d-flex align-items-center">
                      <div class="flex-shrink-0">
                        <font-awesome-icon :icon="getNotificationIcon(notification.notification_type)" :class="getNotificationIconClass(notification.priority)" class="me-3" />
                      </div>
                      <div class="flex-grow-1 ms-3">
                        <div class="fw-bold">{{ notification.title }}</div>
                        <div>{{ notification.message }}</div>
                        <small class="text-muted">{{ formatDate(notification.created_at) }}</small>
                      </div>
                      <div v-if="!notification.is_read" class="flex-shrink-0 ms-3">
                        <span class="badge bg-primary">Mới</span>
                      </div>
                    </div>
                  </li>
                </ul>
                <div class="text-center mt-3">
                  <router-link to="/notifications" class="btn btn-sm btn-outline-primary">
                    Xem tất cả thông báo
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import moment from 'moment'
import { breadcrumbMixin } from '@/utils/breadcrumb'

export default {
  name: 'DashboardPage',
  components: {
    LoadingSpinner
  },
  mixins: [breadcrumbMixin],
  data() {
    return {
      loading: false,
      stats: {
        totalEmployees: 0,
        totalDepartments: 0,
        totalFactories: 0,
        totalDocuments: 0
      },
      activities: [],
      // Dữ liệu mẫu cho activities
      sampleActivities: [
        { type: 'employee', description: 'Nhân viên Nguyễn Văn A đã được thêm mới', timestamp: new Date(Date.now() - 3600000) },
        { type: 'document', description: 'Tài liệu "Quy trình tuyển dụng" đã được cập nhật', timestamp: new Date(Date.now() - 7200000) },
        { type: 'department', description: 'Phòng Nhân sự đã được cập nhật thông tin', timestamp: new Date(Date.now() - 86400000) },
        { type: 'login', description: 'Bạn đã đăng nhập vào hệ thống', timestamp: new Date() }
      ]
    }
  },
  computed: {
    ...mapGetters({
      currentUser: 'auth/currentUser',
      notifications: 'notifications/allNotifications',
      companyInfo: 'company/companyInfo'
    })
  },
  created() {
    this.fetchDashboardData()
    this.fetchCompanyInfo()
  },
  methods: {
    async fetchDashboardData() {
      this.loading = true

      try {
        // Trong thực tế, bạn sẽ gọi API để lấy dữ liệu
        // Ở đây chúng ta sử dụng dữ liệu mẫu
        await new Promise(resolve => setTimeout(resolve, 1000))

        this.stats = {
          totalEmployees: 125,
          totalDepartments: 12,
          totalFactories: 5,
          totalDocuments: 48
        }

        this.activities = this.sampleActivities
      } catch (error) {
        console.error('Error fetching dashboard data:', error)
      } finally {
        this.loading = false
      }
    },
    refreshData() {
      this.fetchDashboardData()
      this.fetchCompanyInfo()
    },
    async fetchCompanyInfo() {
      try {
        await this.$store.dispatch('company/fetchCompanyInfo')
      } catch (error) {
        console.error('Error fetching company info:', error)
      }
    },
    formatDate(date) {
      return moment(date).fromNow()
    },
    getActivityIcon(type) {
      switch (type) {
        case 'employee':
          return 'user'
        case 'document':
          return 'file-alt'
        case 'department':
          return 'building'
        case 'factory':
          return 'industry'
        case 'login':
          return 'sign-in-alt'
        default:
          return 'history'
      }
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
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  .card-gradient {
    border: none;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);

    .card-header {
      background: linear-gradient(90deg, var(--primary-color, #003366) 0%, var(--primary-light, #0066cc) 100%);
      color: white;
      border: none;
      padding: 1rem 1.5rem;
    }
  }

  .card-accent {
    border: none;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);

    .card-header {
      background: linear-gradient(90deg, var(--accent-color, #ff6600) 0%, var(--accent-light, #ff9933) 100%);
      color: white;
      border: none;
      padding: 1rem 1.5rem;
    }
  }

  .dashboard-card {
    height: 100%;
    border: none;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;

    &:hover {
      transform: translateY(-5px);
    }

    .card-body {
      padding: 1.5rem;
    }

    .card-footer {
      background: rgba(0, 0, 0, 0.1);
      border-top: none;
      padding: 0.75rem 1.5rem;

      a {
        display: flex;
        justify-content: space-between;
        align-items: center;
        text-decoration: none;

        &:hover {
          text-decoration: underline;
        }
      }
    }
  }

  .bg-gradient-primary {
    background: linear-gradient(135deg, var(--primary-color, #003366) 0%, var(--primary-light, #0066cc) 100%);
  }

  .bg-gradient-horizontal {
    background: linear-gradient(90deg, var(--primary-color, #003366) 0%, var(--accent-color, #ff6600) 100%);
  }
}
</style>
