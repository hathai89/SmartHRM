<template>
  <footer class="footer bg-white py-4 mt-auto">
    <div class="container">
      <div class="row">
        <div class="col-md-6">
          <p class="mb-0">&copy; {{ currentYear }} SmartHRM. Tất cả quyền được bảo lưu.</p>
        </div>
        <div class="col-md-6 text-md-end">
          <ul class="list-inline mb-0">
            <li class="list-inline-item">
              <a href="#" class="text-muted">Điều khoản sử dụng</a>
            </li>
            <li class="list-inline-item">
              <a href="#" class="text-muted">Chính sách bảo mật</a>
            </li>
            <li class="list-inline-item">
              <a href="#" class="text-muted">Liên hệ</a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'PublicFooter',
  computed: {
    currentYear() {
      return new Date().getFullYear();
    }
  }
}
</script>

<style scoped>
.footer {
  border-top: 1px solid #eee;
}

.list-inline-item:not(:last-child) {
  margin-right: 1rem;
}

a {
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
