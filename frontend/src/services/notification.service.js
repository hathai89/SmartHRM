import api from './api.service'

class NotificationService {
  getNotifications() {
    return api.get('/notifications/')
  }

  markAsRead(id) {
    return api.post(`/notifications/${id}/read/`)
  }

  markAllAsRead() {
    return api.post('/notifications/read-all/')
  }

  deleteNotification(id) {
    return api.delete(`/notifications/${id}/`)
  }
}

export default new NotificationService()
