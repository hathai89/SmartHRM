<template>
  <nav aria-label="breadcrumb" class="mb-4" v-if="items && items.length > 0">
    <ol class="breadcrumb">
      <li class="breadcrumb-item">
        <router-link :to="{ name: 'dashboard' }">
          <i class="fas fa-home"></i>
        </router-link>
      </li>
      <li
        v-for="(item, index) in items"
        :key="index"
        class="breadcrumb-item"
        :class="{ 'active': index === items.length - 1 }"
      >
        <router-link
          v-if="item.route && index !== items.length - 1"
          :to="item.route"
        >
          {{ item.title }}
        </router-link>
        <span v-else>{{ item.title }}</span>
      </li>
    </ol>
  </nav>
</template>

<script>
export default {
  name: 'BreadcrumbNav',
  props: {
    items: {
      type: Array,
      default: () => []
    }
  }
}
</script>

<style lang="scss" scoped>
.breadcrumb {
  background-color: transparent;
  padding: 0.5rem 0;
  margin-bottom: 1.5rem;
  border-radius: 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.breadcrumb-item + .breadcrumb-item::before {
  content: "›";
  color: var(--secondary-color, #00264d);
}

.breadcrumb-item a {
  color: var(--primary-color, #003366);
  text-decoration: none;
}

.breadcrumb-item a:hover {
  color: var(--accent-color, #ff6600);
  text-decoration: underline;
}

.breadcrumb-item.active {
  color: var(--secondary-color, #00264d);
  font-weight: 500;
}
</style>
