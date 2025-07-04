import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// Lưu store vào window để có thể truy cập từ bất kỳ đâu
window.store = store

// Import Bootstrap và BootstrapVue
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'
import { BootstrapVue3 } from 'bootstrap-vue-3'

// Import FontAwesome
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
  faUser, faLock, faSignOutAlt, faCog, faBell, faHome,
  faUsers, faBuilding, faFileAlt, faBriefcase, faChartBar,
  faPlus, faEdit, faTrash, faSearch, faEye, faEyeSlash, faCheck, faTimes,
  faChevronDown, faChevronUp, faChevronLeft, faChevronRight,
  faExclamationTriangle, faInfoCircle, faQuestionCircle,
  faArrowLeft, faArrowRight, faSignInAlt, faIndustry, faTasks,
  faHistory, faCalendarAlt, faPhone, faEnvelope, faMapMarkerAlt,
  faFolder, faSync, faList, faTable, faFilter, faSort, faSortUp, faSortDown,
  faDownload, faUpload, faPrint, faClipboard, faCalendar, faBook, faBookmark,
  // Thêm các biểu tượng còn thiếu
  faBars, faUserPlus, faEllipsisV, faTrashAlt, faKey, faCamera, faIdCard,
  faFile, faCheckCircle, faCheckDouble, faBellSlash, faAngleDoubleLeft,
  faAngleLeft, faAngleRight, faAngleDoubleRight, faDatabase, faUsersCog,
  faPaperPlane, faUndo, faEllipsisH, faTachometerAlt, faUserCircle,
  // Thêm biểu tượng cho menu mới
  faUserTie, faFileSignature, faCalendarCheck, faLaptop, faTags,
  // Thêm các biểu tượng còn thiếu
  faTree, faNetworkWired, faProjectDiagram, faSitemap, faThList, faColumns,
  // Thêm biểu tượng cho cấu trúc cây phòng ban và xí nghiệp
  faLayerGroup, faExpand, faCompress, faCogs,
  // Thêm biểu tượng cho trang tuyển dụng
  faInfinity, faExclamationCircle, faTimesCircle, faShareAlt, faClock
} from '@fortawesome/free-solid-svg-icons'

// Import i18n
import i18n from './i18n'

// Thêm các icon vào thư viện
library.add(
  faUser, faLock, faSignOutAlt, faCog, faBell, faHome,
  faUsers, faBuilding, faFileAlt, faBriefcase, faChartBar,
  faPlus, faEdit, faTrash, faSearch, faEye, faEyeSlash, faCheck, faTimes,
  faChevronDown, faChevronUp, faChevronLeft, faChevronRight,
  faExclamationTriangle, faInfoCircle, faQuestionCircle,
  faArrowLeft, faArrowRight, faSignInAlt, faIndustry, faTasks,
  faHistory, faCalendarAlt, faPhone, faEnvelope, faMapMarkerAlt,
  faFolder, faSync, faList, faTable, faFilter, faSort, faSortUp, faSortDown,
  faDownload, faUpload, faPrint, faClipboard, faCalendar, faBook, faBookmark,
  // Thêm các biểu tượng còn thiếu
  faBars, faUserPlus, faEllipsisV, faTrashAlt, faKey, faCamera, faIdCard,
  faFile, faCheckCircle, faCheckDouble, faBellSlash, faAngleDoubleLeft,
  faAngleLeft, faAngleRight, faAngleDoubleRight, faDatabase, faUsersCog,
  faPaperPlane, faUndo, faEllipsisH, faTachometerAlt, faUserCircle,
  // Thêm biểu tượng cho menu mới
  faUserTie, faFileSignature, faCalendarCheck, faLaptop, faTags,
  // Thêm các biểu tượng còn thiếu
  faTree, faNetworkWired, faProjectDiagram, faSitemap, faThList, faColumns,
  // Thêm biểu tượng cho cấu trúc cây phòng ban
  faLayerGroup, faExpand, faCompress, faCogs,
  // Thêm biểu tượng cho trang tuyển dụng
  faInfinity, faExclamationCircle, faTimesCircle, faShareAlt, faClock
)

// i18n đã được cấu hình trong file i18n.js

// Tạo ứng dụng Vue
const app = createApp(App)

// Sử dụng các plugin
app.use(store)
app.use(router)
app.use(BootstrapVue3)
app.use(i18n)

// Đăng ký component toàn cục
app.component('font-awesome-icon', FontAwesomeIcon)

// Mount ứng dụng
app.mount('#app')
