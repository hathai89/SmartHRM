<template>
  <nav aria-label="Page navigation" v-if="totalPages > 1">
    <ul class="pagination">
      <!-- Nút Previous -->
      <li class="page-item" :class="{ disabled: currentPage === 1 }">
        <a class="page-link" href="#" aria-label="Previous" @click.prevent="changePage(currentPage - 1)">
          <span aria-hidden="true">&laquo;</span>
        </a>
      </li>

      <!-- Nút trang đầu tiên -->
      <li class="page-item" :class="{ active: currentPage === 1 }">
        <a class="page-link" href="#" @click.prevent="changePage(1)">1</a>
      </li>

      <!-- Dấu ... bên trái -->
      <li v-if="showLeftEllipsis" class="page-item disabled">
        <span class="page-link">...</span>
      </li>

      <!-- Các nút trang ở giữa -->
      <li
        v-for="page in middlePages"
        :key="page"
        class="page-item"
        :class="{ active: currentPage === page }"
      >
        <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
      </li>

      <!-- Dấu ... bên phải -->
      <li v-if="showRightEllipsis" class="page-item disabled">
        <span class="page-link">...</span>
      </li>

      <!-- Nút trang cuối cùng -->
      <li v-if="totalPages > 1" class="page-item" :class="{ active: currentPage === totalPages }">
        <a class="page-link" href="#" @click.prevent="changePage(totalPages)">{{ totalPages }}</a>
      </li>

      <!-- Nút Next -->
      <li class="page-item" :class="{ disabled: currentPage === totalPages }">
        <a class="page-link" href="#" aria-label="Next" @click.prevent="changePage(currentPage + 1)">
          <span aria-hidden="true">&raquo;</span>
        </a>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'AppPagination',
  props: {
    totalItems: {
      type: Number,
      required: true
    },
    perPage: {
      type: Number,
      default: 10
    },
    currentPage: {
      type: Number,
      default: 1
    },
    maxVisiblePages: {
      type: Number,
      default: 5
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.totalItems / this.perPage)
    },
    middlePages() {
      if (this.totalPages <= 1) return []

      let startPage = Math.max(2, this.currentPage - Math.floor(this.maxVisiblePages / 2))
      let endPage = Math.min(this.totalPages - 1, startPage + this.maxVisiblePages - 3)

      if (endPage - startPage < this.maxVisiblePages - 3) {
        startPage = Math.max(2, endPage - (this.maxVisiblePages - 3) + 1)
      }

      const pages = []
      for (let i = startPage; i <= endPage; i++) {
        pages.push(i)
      }

      return pages
    },
    showLeftEllipsis() {
      return this.totalPages > 2 && this.middlePages.length > 0 && this.middlePages[0] > 2
    },
    showRightEllipsis() {
      return this.totalPages > 2 && this.middlePages.length > 0 && this.middlePages[this.middlePages.length - 1] < this.totalPages - 1
    }
  },
  methods: {
    changePage(page) {
      if (page < 1 || page > this.totalPages || page === this.currentPage) return
      this.$emit('page-changed', page)
    }
  }
}
</script>

<style lang="scss" scoped>
.pagination {
  .page-item {
    .page-link {
      color: var(--primary-color, #003366);
      border-color: #dee2e6;

      &:hover {
        background-color: #e9ecef;
        border-color: #dee2e6;
        color: var(--accent-color, #ff6600);
      }
    }

    &.active .page-link {
      background: linear-gradient(90deg, var(--primary-color, #003366) 0%, var(--accent-color, #ff6600) 100%);
      border-color: var(--primary-color, #003366);
      color: white;
    }

    &.disabled .page-link {
      color: #6c757d;
      pointer-events: none;
      background-color: #fff;
      border-color: #dee2e6;
    }
  }
}
</style>
