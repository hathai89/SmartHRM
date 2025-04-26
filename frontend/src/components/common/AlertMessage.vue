<template>
  <div v-if="show" class="alert" :class="alertClass" role="alert">
    <div class="d-flex align-items-center">
      <font-awesome-icon v-if="icon" :icon="icon" class="me-2" />
      <div v-if="title" class="fw-bold me-2">{{ title }}</div>
      <div>{{ message }}</div>
    </div>
    <button v-if="dismissible" type="button" class="btn-close" @click="dismiss" aria-label="Close"></button>
  </div>
</template>

<script>
export default {
  name: 'AlertMessage',
  props: {
    type: {
      type: String,
      default: 'info',
      validator: value => ['success', 'info', 'warning', 'danger'].includes(value)
    },
    message: {
      type: String,
      required: true
    },
    title: {
      type: String,
      default: ''
    },
    dismissible: {
      type: Boolean,
      default: true
    },
    timeout: {
      type: Number,
      default: 0 // 0 means no auto-dismiss
    },
    showIcon: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      show: true,
      timer: null
    }
  },
  computed: {
    alertClass() {
      return {
        [`alert-${this.type}`]: true,
        'alert-dismissible fade show': this.dismissible
      }
    },
    icon() {
      if (!this.showIcon) return null
      
      switch (this.type) {
        case 'success':
          return 'check-circle'
        case 'info':
          return 'info-circle'
        case 'warning':
          return 'exclamation-triangle'
        case 'danger':
          return 'exclamation-circle'
        default:
          return 'info-circle'
      }
    }
  },
  mounted() {
    if (this.timeout > 0) {
      this.timer = setTimeout(() => {
        this.dismiss()
      }, this.timeout)
    }
  },
  beforeUnmount() {
    if (this.timer) {
      clearTimeout(this.timer)
    }
  },
  methods: {
    dismiss() {
      this.show = false
      this.$emit('dismissed')
    }
  }
}
</script>
