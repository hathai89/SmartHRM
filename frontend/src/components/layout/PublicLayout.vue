<template>
  <div class="public-container d-flex flex-column min-vh-100">
    <public-header />
    <main class="flex-grow-1">
      <slot></slot>
    </main>
    <public-footer />
  </div>
</template>

<script>
import PublicHeader from './PublicHeader.vue';
import PublicFooter from './PublicFooter.vue';

export default {
  name: 'PublicLayout',
  components: {
    PublicHeader,
    PublicFooter
  }
}
</script>

<style scoped>
.public-container {
  background-color: #f8f9fa;
}
</style>
