/**
 * API endpoints configuration
 */

// Determine the API base URL
let apiBaseUrl = process.env.VUE_APP_API_URL || '/api';

// Detect if we're running in Django's template environment
if (typeof window !== 'undefined' && window.DJANGO_SETTINGS) {
  // Use the API URL provided by Django
  apiBaseUrl = window.DJANGO_SETTINGS.API_URL;
}

// Export the API base URL
export const API_BASE_URL = apiBaseUrl;

// Auth endpoints
export const AUTH_ENDPOINTS = {
  LOGIN: '/auth/login/',
  LOGOUT: '/auth/logout/',
  REFRESH_TOKEN: '/auth/token/refresh/',
  VERIFY_TOKEN: '/auth/token/verify/',
  CHANGE_PASSWORD: '/auth/password/change/',
  RESET_PASSWORD: '/auth/password/reset/',
  RESET_PASSWORD_CONFIRM: '/auth/password/reset/confirm/',
  USER_INFO: '/auth/user/',
};

// Employee endpoints
export const EMPLOYEE_ENDPOINTS = {
  LIST: '/employees/',
  DETAIL: (id) => `/employees/${id}/`,
  CREATE: '/employees/',
  UPDATE: (id) => `/employees/${id}/`,
  DELETE: (id) => `/employees/${id}/`,
  SEARCH: '/employees/search/',
  EXPORT: '/employees/export/',
  IMPORT: '/employees/import/',
};

// Department endpoints
export const DEPARTMENT_ENDPOINTS = {
  LIST: '/departments/',
  DETAIL: (id) => `/departments/${id}/`,
  CREATE: '/departments/',
  UPDATE: (id) => `/departments/${id}/`,
  DELETE: (id) => `/departments/${id}/`,
};

// Factory endpoints
export const FACTORY_ENDPOINTS = {
  LIST: '/factories/',
  DETAIL: (id) => `/factories/${id}/`,
  CREATE: '/factories/',
  UPDATE: (id) => `/factories/${id}/`,
  DELETE: (id) => `/factories/${id}/`,
};

// Document endpoints
export const DOCUMENT_ENDPOINTS = {
  LIST: '/documents/',
  DETAIL: (id) => `/documents/${id}/`,
  CREATE: '/documents/',
  UPDATE: (id) => `/documents/${id}/`,
  DELETE: (id) => `/documents/${id}/`,
  DOWNLOAD: (id) => `/documents/${id}/download/`,
};

// Company endpoints
export const COMPANY_ENDPOINTS = {
  INFO: '/company/info/',
};

// Dashboard endpoints
export const DASHBOARD_ENDPOINTS = {
  STATS: '/dashboard/stats/',
  RECENT_ACTIVITIES: '/dashboard/activities/',
  CHARTS: '/dashboard/charts/',
};

// Notification endpoints
export const NOTIFICATION_ENDPOINTS = {
  LIST: '/notifications/',
  MARK_READ: (id) => `/notifications/${id}/read/`,
  MARK_ALL_READ: '/notifications/read-all/',
};
