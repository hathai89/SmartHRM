// Configuración global de la aplicación
export const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api'
export const ITEMS_PER_PAGE = 10
export const DATE_FORMAT = 'dd/MM/yyyy'
export const DATE_TIME_FORMAT = 'HH:mm - dd/MM/yyyy'

// Configuración de autenticación
export const TOKEN_KEY = 'token'
export const USER_KEY = 'user'

// Configuración de notificaciones
export const NOTIFICATION_TIMEOUT = 5000 // 5 segundos

// Configuración de carga de archivos
export const MAX_FILE_SIZE = 5 * 1024 * 1024 // 5MB
export const ALLOWED_FILE_TYPES = [
  'image/jpeg',
  'image/png',
  'image/gif',
  'application/pdf',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'application/vnd.ms-excel',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
]
