<template>
  <div class="company-info">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="h2">Thông tin công ty</h1>
    </div>

    <div v-if="loading" class="text-center py-5">
      <loading-spinner />
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <template v-else>
      <div class="card card-gradient mb-4">
        <div class="card-header">
          <h5 class="mb-0">Thông tin cơ bản</h5>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-3 text-center mb-4 mb-md-0">
              <img
                v-if="company.logo"
                :src="company.logo"
                :alt="company.name"
                class="img-fluid mb-3"
                style="max-height: 150px;"
              >
              <div
                v-else
                class="bg-light d-flex align-items-center justify-content-center"
                style="height: 150px; width: 100%;"
              >
                <i class="fas fa-building fa-4x text-muted"></i>
              </div>
            </div>
            <div class="col-md-9">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <h6 class="text-muted">Tên công ty</h6>
                  <p class="mb-0 fs-5 fw-bold">{{ company.name }}</p>
                </div>
                <div class="col-md-6 mb-3">
                  <h6 class="text-muted">Tên viết tắt</h6>
                  <p class="mb-0">{{ company.short_name || '--' }}</p>
                </div>
                <div class="col-md-6 mb-3">
                  <h6 class="text-muted">Mã số thuế</h6>
                  <p class="mb-0">{{ company.tax_code }}</p>
                </div>
                <div class="col-md-6 mb-3">
                  <h6 class="text-muted">Ngày thành lập</h6>
                  <p class="mb-0">{{ formatDate(company.foundation_date) || '--' }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-md-6">
          <div class="card mb-4">
            <div class="card-header bg-primary text-white">
              <h5 class="mb-0">Thông tin liên hệ</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <h6 class="text-muted">Địa chỉ</h6>
                <p class="mb-0">{{ company.address }}</p>
              </div>
              <div class="mb-3">
                <h6 class="text-muted">Số điện thoại</h6>
                <p class="mb-0">{{ company.phone }}</p>
              </div>
              <div class="mb-3">
                <h6 class="text-muted">Email</h6>
                <p class="mb-0">{{ company.email }}</p>
              </div>
              <div class="mb-3">
                <h6 class="text-muted">Fax</h6>
                <p class="mb-0">{{ company.fax || '--' }}</p>
              </div>
              <div class="mb-0">
                <h6 class="text-muted">Website</h6>
                <p class="mb-0" v-if="company.website">
                  <a :href="company.website" target="_blank">{{ company.website }}</a>
                </p>
                <p class="mb-0" v-else>--</p>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6">
          <div class="card mb-4">
            <div class="card-header bg-primary text-white">
              <h5 class="mb-0">Người đại diện</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <h6 class="text-muted">Họ tên</h6>
                <p class="mb-0">{{ company.representative }}</p>
              </div>
              <div class="mb-0">
                <h6 class="text-muted">Chức vụ</h6>
                <p class="mb-0">{{ company.position }}</p>
              </div>
            </div>
          </div>

          <div class="card mb-4">
            <div class="card-header bg-primary text-white">
              <h5 class="mb-0">Phòng nhân sự / Tuyển dụng</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <h6 class="text-muted">Tên phòng</h6>
                <p class="mb-0">{{ company.hr_department }}</p>
              </div>
              <div class="mb-3">
                <h6 class="text-muted">Số điện thoại</h6>
                <p class="mb-0">{{ company.hr_phone || '--' }}</p>
              </div>
              <div class="mb-0">
                <h6 class="text-muted">Email tuyển dụng</h6>
                <p class="mb-0">{{ company.career_email || '--' }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card mb-4" v-if="company.description">
        <div class="card-header bg-primary text-white">
          <h5 class="mb-0">Mô tả công ty</h5>
        </div>
        <div class="card-body">
          <p class="mb-0" v-html="formatDescription(company.description)"></p>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import LoadingSpinner from '@/components/common/LoadingSpinner.vue';
import { COMPANY_ENDPOINTS } from '@/api/api';
import api from '@/services/api.service';
import { breadcrumbMixin } from '@/utils/breadcrumb';

export default {
  name: 'CompanyInfo',
  components: {
    LoadingSpinner
  },
  mixins: [breadcrumbMixin],
  setup() {
    const company = ref({});
    const loading = ref(true);
    const error = ref(null);

    const fetchCompanyInfo = async () => {
      try {
        loading.value = true;
        const response = await api.get(COMPANY_ENDPOINTS.INFO);
        company.value = response.data;
      } catch (err) {
        console.error('Error fetching company info:', err);
        error.value = 'Không thể tải thông tin công ty. Vui lòng thử lại sau.';
      } finally {
        loading.value = false;
      }
    };

    const formatDate = (dateString) => {
      if (!dateString) return null;
      const date = new Date(dateString);
      return date.toLocaleDateString('vi-VN');
    };

    const formatDescription = (text) => {
      if (!text) return '';
      return text.replace(/\n/g, '<br>');
    };

    onMounted(() => {
      fetchCompanyInfo();
    });

    return {
      company,
      loading,
      error,
      formatDate,
      formatDescription
    };
  }
};
</script>

<style lang="scss" scoped>
.company-info {
  .card-gradient {
    border: none;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);

    .card-header {
      background: linear-gradient(90deg, var(--primary-color, #003366) 0%, var(--accent-color, #ff6600) 100%);
      color: white;
      border: none;
      padding: 1rem 1.5rem;
    }
  }
}
</style>
