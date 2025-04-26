<template>
  <div class="not-found-page">
    <div class="container text-center">
      <div class="error-code">404</div>
      <h1 class="error-title">{{ $t('errors.notFound') }}</h1>
      <p class="error-message">{{ $t('errors.notFoundMessage') }}</p>
      <div class="mt-4">
        <button class="btn btn-outline-secondary me-2" @click="goBack">
          <font-awesome-icon icon="arrow-left" class="me-2" />
          {{ $t('errors.goBack') }}
        </button>
        <router-link to="/" class="btn btn-primary">
          <font-awesome-icon icon="home" class="me-2" />
          {{ $t('errors.goHome') }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound',
  methods: {
    goBack() {
      this.$router.go(-1)
    }
  }
}
</script>

<style scoped>
.not-found-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f8f9fa;
}

.error-code {
  font-size: 8rem;
  font-weight: 700;
  color: #007bff;
  line-height: 1;
}

.error-title {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.error-message {
  font-size: 1.2rem;
  color: #6c757d;
  max-width: 500px;
  margin: 0 auto;
}
</style>
