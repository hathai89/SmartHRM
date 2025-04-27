import api from './api.service'
import { NOTIFICATION_ENDPOINTS } from '@/api/api'

class NotificationService {
  getNotifications() {
    return api.get(NOTIFICATION_ENDPOINTS.LIST)
  }

  markAsRead(id) {
    return api.post(NOTIFICATION_ENDPOINTS.MARK_READ(id))
  }

  markAllAsRead() {
    return api.post(NOTIFICATION_ENDPOINTS.MARK_ALL_READ)
  }

  deleteNotification(id) {
    return api.delete(`/notifications/${id}/`)
  }
}

export default new NotificationService()
