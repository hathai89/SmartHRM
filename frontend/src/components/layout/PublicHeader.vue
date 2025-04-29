<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white">
    <div class="container">
      <router-link class="navbar-brand" to="/">
        <img src="@/assets/images/logo.png" alt="SmartHRM" height="40" />
      </router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/careers">Cơ hội việc làm</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/login">Đăng nhập</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'PublicHeader'
}
</script>

<style scoped>
.navbar {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.nav-link {
  font-weight: 500;
  padding: 0.5rem 1rem;
}

.nav-link:hover {
  color: var(--bs-primary);
}
</style>
