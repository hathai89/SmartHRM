<template>
  <div class="modal fade" tabindex="-1" aria-hidden="true" ref="modal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header" :class="headerClass">
          <h5 class="modal-title">{{ title }}</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div v-if="icon" class="text-center mb-3">
            <font-awesome-icon :icon="icon" :class="iconClass" size="3x" />
          </div>
          <p>{{ message }}</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
            {{ cancelText }}
          </button>
          <button type="button" :class="confirmButtonClass" @click="confirm">
            {{ confirmText }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap'

export default {
  name: 'ConfirmDialog',
  props: {
    title: {
      type: String,
      default: 'Xác nhận'
    },
    message: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: 'primary',
      validator: value => ['primary', 'success', 'danger', 'warning', 'info'].includes(value)
    },
    confirmText: {
      type: String,
      default: 'Xác nhận'
    },
    cancelText: {
      type: String,
      default: 'Hủy'
    },
    icon: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      modal: null
    }
  },
  computed: {
    headerClass() {
      return {
        'bg-primary text-white': this.type === 'primary',
        'bg-success text-white': this.type === 'success',
        'bg-danger text-white': this.type === 'danger',
        'bg-warning': this.type === 'warning',
        'bg-info text-white': this.type === 'info'
      }
    },
    confirmButtonClass() {
      return {
        'btn': true,
        'btn-primary': this.type === 'primary',
        'btn-success': this.type === 'success',
        'btn-danger': this.type === 'danger',
        'btn-warning': this.type === 'warning',
        'btn-info': this.type === 'info'
      }
    },
    iconClass() {
      return {
        'text-primary': this.type === 'primary',
        'text-success': this.type === 'success',
        'text-danger': this.type === 'danger',
        'text-warning': this.type === 'warning',
        'text-info': this.type === 'info'
      }
    }
  },
  mounted() {
    this.modal = new Modal(this.$refs.modal)
  },
  methods: {
    show() {
      this.modal.show()
    },
    hide() {
      this.modal.hide()
    },
    confirm() {
      this.$emit('confirm')
      this.hide()
    }
  }
}
</script>
