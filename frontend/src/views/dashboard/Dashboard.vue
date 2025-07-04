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
            <div class="card dashboard-card bg-gradient-primary text-white">
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
            <div class="card dashboard-card bg-gradient-primary text-white">
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
            <div class="card card-gradient">
              <div class="card-header">
                <h5 class="card-title mb-0">Thông báo</h5>
              </div>
              <div class="card-body">
                <div v-if="!notifications || notifications.length === 0" class="text-center py-3">
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
                        <span class="badge bg-primary" style="border-radius: 4px;">Mới</span>
                      </div>
                    </div>
                  </li>
                </ul>
                <div v-if="notifications && notifications.length > 0" class="text-center mt-3">
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
import apiClient from '@/services/api.service'

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
      activities: []
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
        // Gọi API để lấy dữ liệu thống kê
        const [employeesResponse, departmentsResponse, factoriesResponse, documentsResponse, activitiesResponse] = await Promise.all([
          apiClient.get('/employees/'),
          apiClient.get('/departments/'),
          apiClient.get('/factories/'),
          apiClient.get('/documents/'),
          apiClient.get('/dashboard/activities/')
        ]);

        // Cập nhật thống kê với xử lý an toàn
        // Đếm số nhân viên
        const totalEmployees = employeesResponse.data?.count || (employeesResponse.data?.results || []).length || 0;

        // Đếm số phòng ban (chỉ đếm các phòng ban cấp cao nhất, không đếm bộ phận và nhóm)
        const departments = departmentsResponse.data?.results || [];
        const totalDepartments = departments.filter(dept => dept.dept_type === 'department').length;

        // Đếm số xí nghiệp (chỉ đếm các xí nghiệp cấp cao nhất, không đếm bộ phận và nhóm)
        const factories = factoriesResponse.data?.results || [];
        const totalFactories = factories.filter(factory => factory.factory_type === 'factory').length;

        // Đếm số tài liệu
        const totalDocuments = documentsResponse.data?.count || (documentsResponse.data?.results || []).length || 0;

        this.stats = {
          totalEmployees,
          totalDepartments,
          totalFactories,
          totalDocuments
        }

        // Cập nhật hoạt động gần đây với xử lý an toàn
        if (activitiesResponse.data?.results) {
          this.activities = activitiesResponse.data.results;
        } else {
          // Không có dữ liệu hoạt động hoặc dữ liệu không hợp lệ
          this.activities = [];
        }
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        // Xử lý lỗi và hiển thị thông báo cho người dùng
        this.$store.dispatch('setError', 'Không thể tải dữ liệu bảng điều khiển. Vui lòng thử lại sau.');
      } finally {
        this.loading = false;
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
}
</style>
