<template>
  <div v-if="show" class="offline-notification">
    <div class="alert alert-warning alert-dismissible fade show" role="alert">
      <strong>Chế độ Offline:</strong> Ứng dụng đang hoạt động ở chế độ offline. Một số tính năng có thể không khả dụng.
      <button type="button" class="btn-close" @click="onClose" aria-label="Close"></button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OfflineNotification',
  props: {
    show: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    onClose() {
      this.$emit('close');
    }
  }
}
</script>

<style lang="scss" scoped>
.offline-notification {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  width: 80%;
  max-width: 600px;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    transform: translate(-50%, 20px);
    opacity: 0;
  }
  to {
    transform: translate(-50%, 0);
    opacity: 1;
  }
}
</style>
