import api from './api.service';

/**
 * Service để tương tác với API Profile
 */
class ProfileService {
  /**
   * Lấy thông tin hồ sơ cá nhân
   * @returns {Promise} - Promise chứa thông tin hồ sơ
   */
  getProfile() {
    return api.get('/auth/profile/');
  }

  /**
   * Cập nhật thông tin hồ sơ cá nhân
   * @param {Object} profileData - Dữ liệu hồ sơ cần cập nhật
   * @returns {Promise} - Promise chứa thông tin hồ sơ đã cập nhật
   */
  updateProfile(profileData) {
    return api.patch('/auth/profile/', profileData);
  }

  /**
   * Upload ảnh đại diện
   * @param {File} file - File ảnh đại diện
   * @returns {Promise} - Promise chứa URL ảnh đại diện mới
   */
  uploadAvatar(file) {
    const formData = new FormData();
    formData.append('avatar', file);

    return api.post('/auth/profile/avatar/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  }
}

export default new ProfileService();
