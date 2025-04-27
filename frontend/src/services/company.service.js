import api from './api.service';
import { COMPANY_ENDPOINTS } from '@/api/api';

/**
 * Service để tương tác với API Company
 */
class CompanyService {
  /**
   * Lấy thông tin công ty
   * @returns {Promise} - Promise chứa thông tin công ty
   */
  getCompanyInfo() {
    return api.get(COMPANY_ENDPOINTS.INFO);
  }
}

export default new CompanyService();
