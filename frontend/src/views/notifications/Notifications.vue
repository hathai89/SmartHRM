<template>
  <div class="notifications-page">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="h3">Thông báo</h1>
      <div class="d-flex">
        <button class="btn btn-outline-secondary me-2" @click="refreshNotifications">
          <font-awesome-icon icon="sync" :class="{ 'fa-spin': loading }" />
          Làm mới
        </button>
        <button class="btn btn-primary" @click="markAllAsRead" :disabled="unreadCount === 0">
          <font-awesome-icon icon="check-double" class="me-2" />
          Đánh dấu tất cả đã đọc
        </button>
      </div>
    </div>

    <div class="card mb-4">
      <div class="card-body">
        <div class="row mb-3">
          <div class="col-md-6 mb-2">
            <div class="input-group">
              <span class="input-group-text">
                <font-awesome-icon icon="search" />
              </span>
              <input
                type="text"
                class="form-control"
                v-model="searchQuery"
                placeholder="Tìm kiếm thông báo..."
                @input="handleSearch"
              >
            </div>
          </div>
          <div class="col-md-3 mb-2">
            <select class="form-select" v-model="typeFilter" @change="handleFilterChange">
              <option value="">Tất cả loại</option>
              <option value="system">Hệ thống</option>
              <option value="employee">Nhân viên</option>
              <option value="document">Tài liệu</option>
              <option value="task">Công việc</option>
            </select>
          </div>
          <div class="col-md-3 mb-2">
            <select class="form-select" v-model="readFilter" @change="handleFilterChange">
              <option value="">Tất cả trạng thái</option>
              <option value="unread">Chưa đọc</option>
              <option value="read">Đã đọc</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading">
      <loading-spinner />
    </div>

    <template v-else>
      <div class="notification-list">
        <div v-if="filteredNotifications.length === 0" class="text-center py-5">
          <font-awesome-icon icon="bell-slash" size="3x" class="text-muted mb-3" />
          <p class="lead">Không có thông báo nào</p>
        </div>

        <div v-else>
          <div
            v-for="notification in filteredNotifications"
            :key="notification.id"
            class="notification-item"
            :class="{ 'unread': !notification.is_read }"
            @click="viewNotification(notification)"
          >
            <div class="notification-icon">
              <font-awesome-icon
                :icon="getNotificationIcon(notification.notification_type)"
                :class="getNotificationIconClass(notification.priority)"
              />
            </div>
            <div class="notification-content">
              <div class="notification-header">
                <h5 class="notification-title">{{ notification.title }}</h5>
                <div class="notification-meta">
                  <span class="notification-time">{{ formatDate(notification.created_at) }}</span>
                  <span
                    v-if="!notification.is_read"
                    class="notification-badge"
                  >
                    Mới
                  </span>
                </div>
              </div>
              <div class="notification-message">{{ notification.message }}</div>
              <div class="notification-footer">
                <span class="notification-type">
                  {{ getNotificationTypeText(notification.notification_type) }}
                </span>
                <span class="notification-priority">
                  {{ getNotificationPriorityText(notification.priority) }}
                </span>
              </div>
            </div>
            <div class="notification-actions">
              <button
                class="btn btn-sm btn-outline-primary"
                @click.stop="markAsRead(notification)"
                v-if="!notification.is_read"
              >
                <font-awesome-icon icon="check" />
              </button>
              <button
                class="btn btn-sm btn-outline-danger"
                @click.stop="deleteNotification(notification)"
              >
                <font-awesome-icon icon="trash-alt" />
              </button>
            </div>
          </div>

          <div class="d-flex justify-content-center mt-4">
            <app-pagination
              :total-items="totalItems"
              :per-page="perPage"
              :current-page="currentPage"
              @page-changed="handlePageChange"
            />
          </div>
        </div>
      </div>
    </template>

    <!-- Modal xác nhận xóa thông báo -->
    <confirm-dialog
      v-if="showDeleteConfirm"
      title="Xác nhận xóa thông báo"
      :message="'Bạn có chắc chắn muốn xóa thông báo này?'"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
    />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import AppPagination from '@/components/common/AppPagination.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import { breadcrumbMixin } from '@/utils/breadcrumb'
import debounce from 'lodash/debounce'
import moment from 'moment'

export default {
  name: 'NotificationsPage',
  components: {
    LoadingSpinner,
    AppPagination,
    ConfirmDialog
  },
  mixins: [breadcrumbMixin],
  data() {
    return {
      loading: false,
      searchQuery: '',
      typeFilter: '',
      readFilter: '',
      currentPage: 1,
      perPage: 10,
      showDeleteConfirm: false,
      notificationToDelete: null,
      // Dữ liệu mẫu
      notifications: [
        {
          id: 1,
          title: 'Cập nhật hệ thống',
          message: 'Hệ thống sẽ được nâng cấp vào ngày 15/06/2023. Vui lòng lưu lại công việc của bạn trước thời gian này.',
          notification_type: 'system',
          priority: 'high',
          is_read: false,
          created_at: '2023-06-10T08:00:00Z',
          link: '/dashboard'
        },
        {
          id: 2,
          title: 'Nhân viên mới',
          message: 'Nguyễn Văn A đã được thêm vào hệ thống. Vui lòng kiểm tra thông tin và phân quyền.',
          notification_type: 'employee',
          priority: 'normal',
          is_read: true,
          created_at: '2023-06-09T10:30:00Z',
          link: '/employees/1'
        },
        {
          id: 3,
          title: 'Tài liệu mới',
          message: 'Tài liệu "Quy trình sản xuất 2023" đã được tải lên. Vui lòng xem xét và phê duyệt.',
          notification_type: 'document',
          priority: 'normal',
          is_read: false,
          created_at: '2023-06-08T14:15:00Z',
          link: '/documents'
        },
        {
          id: 4,
          title: 'Công việc quá hạn',
          message: 'Công việc "Báo cáo tháng 5" đã quá hạn. Vui lòng hoàn thành sớm.',
          notification_type: 'task',
          priority: 'urgent',
          is_read: false,
          created_at: '2023-06-07T09:45:00Z',
          link: '/tasks'
        },
        {
          id: 5,
          title: 'Lịch họp',
          message: 'Cuộc họp giao ban sẽ diễn ra vào lúc 9:00 ngày 12/06/2023 tại phòng họp A.',
          notification_type: 'system',
          priority: 'normal',
          is_read: true,
          created_at: '2023-06-06T16:20:00Z',
          link: '/calendar'
        },
        {
          id: 6,
          title: 'Yêu cầu phê duyệt',
          message: 'Trần Thị B đã gửi yêu cầu phê duyệt nghỉ phép từ ngày 20/06/2023 đến 22/06/2023.',
          notification_type: 'employee',
          priority: 'normal',
          is_read: true,
          created_at: '2023-06-05T11:10:00Z',
          link: '/approvals'
        },
        {
          id: 7,
          title: 'Cảnh báo bảo mật',
          message: 'Phát hiện đăng nhập bất thường vào tài khoản của bạn. Vui lòng kiểm tra và đổi mật khẩu nếu cần thiết.',
          notification_type: 'system',
          priority: 'urgent',
          is_read: false,
          created_at: '2023-06-04T22:30:00Z',
          link: '/profile'
        },
        {
          id: 8,
          title: 'Nhắc nhở',
          message: 'Vui lòng cập nhật thông tin cá nhân của bạn trước ngày 30/06/2023.',
          notification_type: 'system',
          priority: 'low',
          is_read: true,
          created_at: '2023-06-03T08:45:00Z',
          link: '/profile'
        },
        {
          id: 9,
          title: 'Tài liệu cần xem xét',
          message: 'Tài liệu "Kế hoạch kinh doanh Q3/2023" đang chờ bạn xem xét và góp ý.',
          notification_type: 'document',
          priority: 'high',
          is_read: false,
          created_at: '2023-06-02T15:20:00Z',
          link: '/documents'
        },
        {
          id: 10,
          title: 'Công việc mới',
          message: 'Bạn đã được giao công việc "Báo cáo tháng 6". Hạn hoàn thành: 05/07/2023.',
          notification_type: 'task',
          priority: 'normal',
          is_read: true,
          created_at: '2023-06-01T10:00:00Z',
          link: '/tasks'
        }
      ]
    }
  },
  computed: {
    ...mapGetters({
      // allNotifications: 'notifications/allNotifications',
      // isLoading: 'notifications/isLoading',
      // unreadCount: 'notifications/unreadCount'
    }),
    filteredNotifications() {
      let result = [...this.notifications]

      // Lọc theo loại thông báo
      if (this.typeFilter) {
        result = result.filter(notification => notification.notification_type === this.typeFilter)
      }

      // Lọc theo trạng thái đọc
      if (this.readFilter === 'read') {
        result = result.filter(notification => notification.is_read)
      } else if (this.readFilter === 'unread') {
        result = result.filter(notification => !notification.is_read)
      }

      // Lọc theo từ khóa tìm kiếm
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        result = result.filter(notification =>
          notification.title.toLowerCase().includes(query) ||
          notification.message.toLowerCase().includes(query)
        )
      }

      // Sắp xếp theo thời gian tạo (mới nhất lên đầu)
      result.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))

      return result
    },
    paginatedNotifications() {
      const startIndex = (this.currentPage - 1) * this.perPage
      const endIndex = startIndex + this.perPage
      return this.filteredNotifications.slice(startIndex, endIndex)
    },
    totalItems() {
      return this.filteredNotifications.length
    },
    unreadCount() {
      return this.notifications.filter(notification => !notification.is_read).length
    }
  },
  mounted() {
    this.fetchNotifications()
  },
  methods: {
    ...mapActions({
      // fetchAllNotifications: 'notifications/fetchNotifications',
      // markAsReadAction: 'notifications/markAsRead',
      // markAllAsReadAction: 'notifications/markAllAsRead',
      // deleteNotificationAction: 'notifications/deleteNotification',
      setSuccess: 'setSuccess',
      setError: 'setError'
    }),
    async fetchNotifications() {
      this.loading = true

      try {
        // Trong thực tế, bạn sẽ gọi API để lấy dữ liệu
        // await this.fetchAllNotifications()

        // Giả lập API call
        await new Promise(resolve => setTimeout(resolve, 1000))
      } catch (error) {
        console.error('Error fetching notifications:', error)
        this.setError('Không thể tải thông báo. Vui lòng thử lại sau.')
      } finally {
        this.loading = false
      }
    },
    refreshNotifications() {
      this.fetchNotifications()
    },
    handleSearch: debounce(function() {
      this.currentPage = 1
    }, 300),
    handleFilterChange() {
      this.currentPage = 1
    },
    handlePageChange(page) {
      this.currentPage = page
    },
    viewNotification(notification) {
      // Đánh dấu thông báo đã đọc
      if (!notification.is_read) {
        this.markAsRead(notification)
      }

      // Chuyển hướng đến liên kết của thông báo nếu có
      if (notification.link) {
        this.$router.push(notification.link)
      }
    },
    async markAsRead(notification) {
      if (notification.is_read) return

      try {
        // Trong thực tế, bạn sẽ gọi API để đánh dấu đã đọc
        // await this.markAsReadAction(notification.id)

        // Giả lập API call
        await new Promise(resolve => setTimeout(resolve, 500))

        // Cập nhật trạng thái trong danh sách
        const index = this.notifications.findIndex(n => n.id === notification.id)
        if (index !== -1) {
          this.notifications[index].is_read = true
        }
      } catch (error) {
        console.error('Error marking notification as read:', error)
        this.setError('Không thể đánh dấu thông báo đã đọc. Vui lòng thử lại sau.')
      }
    },
    async markAllAsRead() {
      try {
        // Trong thực tế, bạn sẽ gọi API để đánh dấu tất cả đã đọc
        // await this.markAllAsReadAction()

        // Giả lập API call
        await new Promise(resolve => setTimeout(resolve, 1000))

        // Cập nhật trạng thái trong danh sách
        this.notifications.forEach(notification => {
          notification.is_read = true
        })

        this.setSuccess('Đã đánh dấu tất cả thông báo là đã đọc.')
      } catch (error) {
        console.error('Error marking all notifications as read:', error)
        this.setError('Không thể đánh dấu tất cả thông báo đã đọc. Vui lòng thử lại sau.')
      }
    },
    deleteNotification(notification) {
      this.notificationToDelete = notification
      this.showDeleteConfirm = true
    },
    async confirmDelete() {
      if (!this.notificationToDelete) return

      try {
        // Trong thực tế, bạn sẽ gọi API để xóa thông báo
        // await this.deleteNotificationAction(this.notificationToDelete.id)

        // Giả lập API call
        await new Promise(resolve => setTimeout(resolve, 500))

        // Xóa thông báo khỏi danh sách
        this.notifications = this.notifications.filter(n => n.id !== this.notificationToDelete.id)

        this.setSuccess('Đã xóa thông báo thành công.')
      } catch (error) {
        console.error('Error deleting notification:', error)
        this.setError('Không thể xóa thông báo. Vui lòng thử lại sau.')
      } finally {
        this.showDeleteConfirm = false
        this.notificationToDelete = null
      }
    },
    cancelDelete() {
      this.showDeleteConfirm = false
      this.notificationToDelete = null
    },
    formatDate(dateString) {
      return moment(dateString).fromNow()
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
    },
    getNotificationTypeText(type) {
      switch (type) {
        case 'system':
          return 'Hệ thống'
        case 'employee':
          return 'Nhân viên'
        case 'document':
          return 'Tài liệu'
        case 'task':
          return 'Công việc'
        default:
          return 'Khác'
      }
    },
    getNotificationPriorityText(priority) {
      switch (priority) {
        case 'low':
          return 'Thấp'
        case 'normal':
          return 'Bình thường'
        case 'high':
          return 'Cao'
        case 'urgent':
          return 'Khẩn cấp'
        default:
          return 'Bình thường'
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.notifications-page {
  .notification-list {
    .notification-item {
      display: flex;
      align-items: flex-start;
      padding: 1.5rem;
      margin-bottom: 1rem;
      background-color: #fff;
      border-radius: 10px;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
      transition: all 0.3s ease;
      cursor: pointer;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
      }

      &.unread {
        border-left: 4px solid var(--primary-color, #003366);
        background-color: rgba(0, 51, 102, 0.02);
      }

      .notification-icon {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #f8f9fa;
        border-radius: 50%;
        margin-right: 1rem;
        font-size: 1.2rem;
      }

      .notification-content {
        flex: 1;

        .notification-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 0.5rem;

          .notification-title {
            font-size: 1.1rem;
            font-weight: 600;
            margin: 0;
          }

          .notification-meta {
            display: flex;
            align-items: center;

            .notification-time {
              font-size: 0.85rem;
              color: #6c757d;
              margin-right: 0.75rem;
            }

            .notification-badge {
              background-color: var(--primary-color, #003366);
              color: white;
              font-size: 0.75rem;
              padding: 0.25rem 0.5rem;
              border-radius: 20px;
            }
          }
        }

        .notification-message {
          margin-bottom: 0.75rem;
          color: #495057;
        }

        .notification-footer {
          display: flex;
          gap: 1rem;

          .notification-type,
          .notification-priority {
            font-size: 0.85rem;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            background-color: #f8f9fa;
            color: #6c757d;
          }
        }
      }

      .notification-actions {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        margin-left: 1rem;
      }
    }
  }

  .btn-primary {
    background: linear-gradient(90deg, var(--primary-color, #003366) 0%, var(--accent-color, #ff6600) 100%);
    border: none;
    padding: 0.5rem 1.5rem;
    font-weight: 500;
    transition: all 0.3s ease;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }

    &:disabled {
      background: #6c757d;
      transform: none;
      box-shadow: none;
    }
  }
}
</style>
