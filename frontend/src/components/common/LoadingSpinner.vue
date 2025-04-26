<template>
  <div class="loading-spinner" :class="{ 'overlay': overlay }">
    <div class="spinner-border" :class="spinnerClass" role="status">
      <span class="visually-hidden">{{ $t('common.loading') }}</span>
    </div>
    <p v-if="text" class="mt-2">{{ text }}</p>
  </div>
</template>

<script>
export default {
  name: 'LoadingSpinner',
  props: {
    overlay: {
      type: Boolean,
      default: false
    },
    size: {
      type: String,
      default: 'md',
      validator: value => ['sm', 'md', 'lg'].includes(value)
    },
    variant: {
      type: String,
      default: 'primary',
      validator: value => ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark'].includes(value)
    },
    text: {
      type: String,
      default: ''
    }
  },
  computed: {
    spinnerClass() {
      return {
        [`spinner-border-${this.size === 'md' ? '' : this.size}`]: this.size !== 'md',
        [`text-${this.variant}`]: true
      }
    }
  }
}
</script>

<style scoped>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.loading-spinner.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.7);
  z-index: 9999;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

.spinner-border-lg {
  width: 3rem;
  height: 3rem;
}
</style>
