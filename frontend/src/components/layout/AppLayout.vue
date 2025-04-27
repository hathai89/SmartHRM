<template>
  <div class="app-layout">
    <app-header />

    <main class="main-content">
      <div class="container-fluid">
        <slot></slot>
      </div>
    </main>

    <app-footer />

    <!-- Toast container for notifications -->
    <div class="toast-container position-fixed bottom-0 end-0 p-3" id="toastContainer"></div>
  </div>
</template>

<script>
import AppHeader from './AppHeader.vue'
import AppFooter from './AppFooter.vue'

export default {
  name: 'AppLayout',
  components: {
    AppHeader,
    AppFooter
  }
}
</script>

<style lang="scss" scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  position: relative;
}

.main-content {
  flex: 1;
  padding: 2rem 1rem;
  background-color: #f5f5f5;
  margin-top: 60px; /* Chiều cao của header */
}
</style>
