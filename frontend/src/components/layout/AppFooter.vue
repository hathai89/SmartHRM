<template>
  <footer class="app-footer">
    <div class="container-fluid">
      <div class="footer-content">
        <p class="copyright">© {{ currentYear }} CÔNG TY CỔ PHẦN DỆT MAY 29/3. Bản quyền thuộc về công ty.</p>
        <p class="version">Phiên bản: 1.0.0</p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter',
  computed: {
    currentYear() {
      return new Date().getFullYear()
    }
  }
}
</script>

<style lang="scss" scoped>
.app-footer {
  background: var(--primary, #003366);
  color: rgba(255, 255, 255, 0.8);
  padding: 1rem 0;
  margin-top: auto;
  z-index: 900;
  width: 100%;

  .footer-content {
    display: flex;
    justify-content: space-between;
    align-items: center;

    @media (max-width: 768px) {
      flex-direction: column;
      text-align: center;

      .version {
        margin-top: 0.5rem;
      }
    }

    .copyright, .version {
      margin: 0;
    }
  }
}
</style>
