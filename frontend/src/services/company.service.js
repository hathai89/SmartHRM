import axios from './axios';
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
    return axios.get(COMPANY_ENDPOINTS.INFO);
  }
}

export default new CompanyService();
