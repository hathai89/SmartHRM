<template>
  <transition name="fade">
    <div v-if="show" class="error-notification">
      <div class="alert alert-danger alert-dismissible fade show" role="alert">
        <strong>{{ title }}:</strong> {{ message }}
        <button type="button" class="btn-close" @click="onClose" aria-label="Close"></button>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'ErrorNotification',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: 'Lỗi'
    },
    message: {
      type: String,
      default: 'Đã xảy ra lỗi không xác định.'
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
.error-notification {
  position: fixed;
  top: 70px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  width: 80%;
  max-width: 600px;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    transform: translate(-50%, -20px);
    opacity: 0;
  }
  to {
    transform: translate(-50%, 0);
    opacity: 1;
  }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
