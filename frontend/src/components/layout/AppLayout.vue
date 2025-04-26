<template>
  <div>
    <app-header @toggle-sidebar="toggleSidebar" />

    <div class="app-container">
      <app-sidebar :is-open="sidebarOpen" />

      <main class="main-content">
        <div class="container-fluid">
          <slot></slot>
        </div>
      </main>
    </div>

    <app-footer />

    <!-- Toast container for notifications -->
    <div class="toast-container position-fixed bottom-0 end-0 p-3" id="toastContainer"></div>
  </div>
</template>

<script>
import AppHeader from './AppHeader.vue'
import AppSidebar from './AppSidebar.vue'
import AppFooter from './AppFooter.vue'

export default {
  name: 'AppLayout',
  components: {
    AppHeader,
    AppSidebar,
    AppFooter
  },
  data() {
    return {
      sidebarOpen: true
    }
  },
  methods: {
    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen
    },
    checkScreenSize() {
      // Tự động đóng sidebar trên màn hình nhỏ
      this.sidebarOpen = window.innerWidth >= 768
    }
  },
  created() {
    // Kiểm tra kích thước màn hình khi component được tạo
    this.checkScreenSize()

    // Thêm event listener để kiểm tra khi thay đổi kích thước màn hình
    window.addEventListener('resize', this.checkScreenSize)
  },
  beforeUnmount() {
    // Xóa event listener khi component bị hủy
    window.removeEventListener('resize', this.checkScreenSize)
  }
}
</script>
