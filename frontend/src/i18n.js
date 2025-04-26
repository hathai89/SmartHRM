import { createI18n } from 'vue-i18n'
import vi from './locales/vi'

const messages = {
  vi
}

export default createI18n({
  legacy: false,
  locale: 'vi',
  fallbackLocale: 'vi',
  messages
})
