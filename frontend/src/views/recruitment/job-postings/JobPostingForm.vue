<template>
  <div class="container-fluid">
    <div class="card">
      <div class="card-header">
        <h5 class="card-title mb-0">{{ isEditing ? 'Chỉnh sửa tin tuyển dụng' : 'Tạo tin tuyển dụng' }}</h5>
      </div>
      <div class="card-body">
        <form @submit.prevent="saveJobPosting">
          <div class="row mb-4">
            <div class="col-md-8">
              <!-- Thông tin cơ bản -->
              <div class="card mb-4">
                <div class="card-header">
                  <h6 class="card-title mb-0">Thông tin cơ bản</h6>
                </div>
                <div class="card-body">
                  <div class="mb-3">
                    <label for="title" class="form-label">Tiêu đề tin tuyển dụng <span class="text-danger">*</span></label>
                    <input
                      id="title"
                      v-model="formData.title"
                      type="text"
                      class="form-control"
                      :class="{ 'is-invalid': errors.title }"
                      required
                    />
                    <div v-if="errors.title" class="invalid-feedback">
                      {{ errors.title }}
                    </div>
                  </div>

                  <div class="mb-3">
                    <label for="job_code" class="form-label">Mã tin tuyển dụng</label>
                    <input
                      id="job_code"
                      v-model="formData.job_code"
                      type="text"
                      class="form-control"
                      :class="{ 'is-invalid': errors.job_code }"
                      placeholder="Để trống để tạo mã tự động"
                    />
                    <div v-if="errors.job_code" class="invalid-feedback">
                      {{ errors.job_code }}
                    </div>
                    <div class="form-text">Mã tin tuyển dụng sẽ được tạo tự động nếu để trống</div>
                  </div>

                  <div class="mb-3">
                    <label for="workplace_type" class="form-label">Nơi làm việc <span class="text-danger">*</span></label>
                    <select
                      id="workplace_type"
                      v-model="formData.workplace_type"
                      class="form-select"
                      :class="{ 'is-invalid': errors.workplace_type }"
                      required
                    >
                      <option value="">-- Chọn nơi làm việc --</option>
                      <option value="department">Phòng ban</option>
                      <option value="factory">Xí nghiệp</option>
                    </select>
                    <div v-if="errors.workplace_type" class="invalid-feedback">
                      {{ errors.workplace_type }}
                    </div>
                  </div>

                  <div v-if="formData.workplace_type === 'department'" class="mb-3">
                    <label for="department" class="form-label">Phòng ban <span class="text-danger">*</span></label>
                    <select
                      id="department"
                      v-model="formData.department"
                      class="form-select"
                      :class="{ 'is-invalid': errors.department }"
                      required
                      @change="onDepartmentChange"
                    >
                      <option value="">-- Chọn phòng ban --</option>
                      <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                        {{ dept.name }}
                      </option>
                    </select>
                    <div v-if="errors.department" class="invalid-feedback">
                      {{ errors.department }}
                    </div>
                  </div>

                  <div v-if="formData.workplace_type === 'factory'" class="mb-3">
                    <label for="factory" class="form-label">Xí nghiệp <span class="text-danger">*</span></label>
                    <select
                      id="factory"
                      v-model="formData.factory"
                      class="form-select"
                      :class="{ 'is-invalid': errors.factory }"
                      required
                      @change="onFactoryChange"
                    >
                      <option value="">-- Chọn xí nghiệp --</option>
                      <option v-for="factory in factories" :key="factory.id" :value="factory.id">
                        {{ factory.name }}
                      </option>
                    </select>
                    <div v-if="errors.factory" class="invalid-feedback">
                      {{ errors.factory }}
                    </div>
                  </div>

                  <!-- Bộ phận cho Phòng ban -->
                  <div v-if="formData.workplace_type === 'department' && formData.department" class="mb-3">
                    <label for="division" class="form-label">Bộ phận</label>
                    <select
                      id="division"
                      v-model="formData.division"
                      class="form-select"
                      :class="{ 'is-invalid': errors.division }"
                      @change="onDivisionChange"
                    >
                      <option value="">-- Chọn bộ phận --</option>
                      <option v-for="division in divisions" :key="division.id" :value="division.id">
                        {{ division.name }}
                      </option>
                    </select>
                    <div v-if="errors.division" class="invalid-feedback">
                      {{ errors.division }}
                    </div>
                    <div v-if="divisions.length === 0" class="form-text text-info">
                      Không có bộ phận nào trong phòng ban này. Bạn có thể thêm bộ phận trong phần Quản lý phòng ban.
                    </div>
                  </div>

                  <!-- Bộ phận cho Xí nghiệp -->
                  <div v-if="formData.workplace_type === 'factory' && formData.factory" class="mb-3">
                    <label for="factory_division" class="form-label">Bộ phận</label>
                    <select
                      id="factory_division"
                      v-model="formData.division"
                      class="form-select"
                      :class="{ 'is-invalid': errors.division }"
                      @change="onDivisionChange"
                    >
                      <option value="">-- Chọn bộ phận --</option>
                      <option v-for="division in divisions" :key="division.id" :value="division.id">
                        {{ division.name }}
                      </option>
                    </select>
                    <div v-if="errors.division" class="invalid-feedback">
                      {{ errors.division }}
                    </div>
                    <div v-if="divisions.length === 0" class="form-text text-info">
                      Không có bộ phận nào trong xí nghiệp này. Bạn có thể thêm bộ phận trong phần Quản lý xí nghiệp.
                    </div>
                  </div>

                  <!-- Nhóm cho Phòng ban -->
                  <div v-if="formData.workplace_type === 'department' && formData.division" class="mb-3">
                    <label for="team" class="form-label">Nhóm</label>
                    <select
                      id="team"
                      v-model="formData.team"
                      class="form-select"
                      :class="{ 'is-invalid': errors.team }"
                    >
                      <option value="">-- Chọn nhóm --</option>
                      <option v-for="team in teams" :key="team.id" :value="team.id">
                        {{ team.name }}
                      </option>
                    </select>
                    <div v-if="errors.team" class="invalid-feedback">
                      {{ errors.team }}
                    </div>
                    <div v-if="teams.length === 0" class="form-text text-info">
                      Không có nhóm nào trong bộ phận này. Bạn có thể thêm nhóm trong phần Quản lý phòng ban.
                    </div>
                  </div>

                  <!-- Nhóm cho Xí nghiệp -->
                  <div v-if="formData.workplace_type === 'factory' && formData.division" class="mb-3">
                    <label for="factory_team" class="form-label">Nhóm</label>
                    <select
                      id="factory_team"
                      v-model="formData.team"
                      class="form-select"
                      :class="{ 'is-invalid': errors.team }"
                    >
                      <option value="">-- Chọn nhóm --</option>
                      <option v-for="team in teams" :key="team.id" :value="team.id">
                        {{ team.name }}
                      </option>
                    </select>
                    <div v-if="errors.team" class="invalid-feedback">
                      {{ errors.team }}
                    </div>
                    <div v-if="teams.length === 0" class="form-text text-info">
                      Không có nhóm nào trong bộ phận này. Bạn có thể thêm nhóm trong phần Quản lý xí nghiệp.
                    </div>
                  </div>

                  <div class="mb-3">
                    <label for="positions" class="form-label">Số lượng cần tuyển <span class="text-danger">*</span></label>
                    <input
                      id="positions"
                      v-model.number="formData.positions"
                      type="number"
                      min="1"
                      class="form-control"
                      :class="{ 'is-invalid': errors.positions }"
                      required
                    />
                    <div v-if="errors.positions" class="invalid-feedback">
                      {{ errors.positions }}
                    </div>
                  </div>

                  <div class="mb-3">
                    <label for="employment_type" class="form-label">Hình thức làm việc <span class="text-danger">*</span></label>
                    <select
                      id="employment_type"
                      v-model="formData.employment_type"
                      class="form-select"
                      :class="{ 'is-invalid': errors.employment_type }"
                      required
                    >
                      <option value="">-- Chọn hình thức làm việc --</option>
                      <option value="full_time">Toàn thời gian</option>
                      <option value="part_time">Bán thời gian</option>
                      <option value="contract">Hợp đồng</option>
                      <option value="temporary">Tạm thời</option>
                      <option value="internship">Thực tập</option>
                    </select>
                    <div v-if="errors.employment_type" class="invalid-feedback">
                      {{ errors.employment_type }}
                    </div>
                  </div>

                  <div class="mb-3">
                    <label for="location" class="form-label">Địa điểm làm việc <span class="text-danger">*</span></label>
                    <input
                      id="location"
                      v-model="formData.location"
                      type="text"
                      class="form-control"
                      :class="{ 'is-invalid': errors.location }"
                      required
                    />
                    <div v-if="errors.location" class="invalid-feedback">
                      {{ errors.location }}
                    </div>
                  </div>


                </div>
              </div>

              <!-- Mô tả công việc -->
              <div class="card mb-4">
                <div class="card-header">
                  <h6 class="card-title mb-0">Mô tả công việc</h6>
                </div>
                <div class="card-body">
                  <div class="mb-3">
                    <label for="description" class="form-label">Mô tả công việc <span class="text-danger">*</span></label>
                    <textarea
                      id="description"
                      v-model="formData.description"
                      class="form-control"
                      :class="{ 'is-invalid': errors.description }"
                      rows="6"
                      required
                    ></textarea>
                    <div v-if="errors.description" class="invalid-feedback">
                      {{ errors.description }}
                    </div>
                  </div>

                  <div class="mb-3">
                    <label for="requirements" class="form-label">Yêu cầu ứng viên <span class="text-danger">*</span></label>
                    <textarea
                      id="requirements"
                      v-model="formData.requirements"
                      class="form-control"
                      :class="{ 'is-invalid': errors.requirements }"
                      rows="6"
                      required
                    ></textarea>
                    <div v-if="errors.requirements" class="invalid-feedback">
                      {{ errors.requirements }}
                    </div>
                  </div>

                  <div class="mb-3">
                    <label for="benefits" class="form-label">Quyền lợi <span class="text-danger">*</span></label>
                    <textarea
                      id="benefits"
                      v-model="formData.benefits"
                      class="form-control"
                      :class="{ 'is-invalid': errors.benefits }"
                      rows="6"
                      required
                    ></textarea>
                    <div v-if="errors.benefits" class="invalid-feedback">
                      {{ errors.benefits }}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="col-md-4">
              <!-- Yêu cầu kinh nghiệm và học vấn -->
              <div class="card mb-4">
                <div class="card-header">
                  <h6 class="card-title mb-0">Yêu cầu kinh nghiệm và học vấn</h6>
                </div>
                <div class="card-body">
                  <div class="mb-3">
                    <label for="experience_level" class="form-label">Kinh nghiệm <span class="text-danger">*</span></label>
                    <select
                      id="experience_level"
                      v-model="formData.experience_level"
                      class="form-select"
                      :class="{ 'is-invalid': errors.experience_level }"
                      required
                    >
                      <option value="">-- Chọn kinh nghiệm --</option>
                      <option value="entry">Mới tốt nghiệp</option>
                      <option value="junior">Sơ cấp (1-2 năm)</option>
                      <option value="mid">Trung cấp (3-5 năm)</option>
                      <option value="senior">Cao cấp (5+ năm)</option>
                      <option value="lead">Nhóm trưởng/Quản lý</option>
                      <option value="executive">Điều hành cấp cao</option>
                    </select>
                    <div v-if="errors.experience_level" class="invalid-feedback">
                      {{ errors.experience_level }}
                    </div>
                  </div>

                  <div class="mb-3">
                    <label for="education_required" class="form-label">Học vấn <span class="text-danger">*</span></label>
                    <select
                      id="education_required"
                      v-model="formData.education_required"
                      class="form-select"
                      :class="{ 'is-invalid': errors.education_required }"
                      required
                    >
                      <option value="">-- Chọn học vấn --</option>
                      <option value="none">Không yêu cầu bằng cấp</option>
                      <option value="high_school">Tốt nghiệp THPT</option>
                      <option value="vocational">Trung cấp nghề</option>
                      <option value="college">Cao đẳng</option>
                      <option value="bachelor">Đại học</option>
                      <option value="master">Thạc sĩ</option>
                      <option value="phd">Tiến sĩ</option>
                    </select>
                    <div v-if="errors.education_required" class="invalid-feedback">
                      {{ errors.education_required }}
                    </div>
                  </div>
                </div>
              </div>

              <!-- Mức lương -->
              <div class="card mb-4">
                <div class="card-header">
                  <h6 class="card-title mb-0">Mức lương</h6>
                </div>
                <div class="card-body">
                  <div class="mb-3">
                    <div class="form-check mb-2">
                      <input
                        id="is_salary_visible"
                        v-model="formData.is_salary_visible"
                        type="checkbox"
                        class="form-check-input"
                        @change="onSalaryVisibleChange"
                      />
                      <label for="is_salary_visible" class="form-check-label">Hiển thị mức lương</label>
                    </div>

                    <div class="form-check mb-2">
                      <input
                        id="is_salary_negotiable"
                        v-model="formData.is_salary_negotiable"
                        type="checkbox"
                        class="form-check-input"
                        @change="onSalaryNegotiableChange"
                      />
                      <label for="is_salary_negotiable" class="form-check-label">Thỏa thuận</label>
                    </div>
                  </div>

                  <div class="mb-3" v-if="formData.is_salary_visible && !formData.is_salary_negotiable">
                    <label for="min_salary" class="form-label">Mức lương tối thiểu</label>
                    <input
                      id="min_salary"
                      v-model.number="formData.min_salary"
                      type="number"
                      min="0"
                      class="form-control"
                      :class="{ 'is-invalid': errors.min_salary }"
                    />
                    <div v-if="errors.min_salary" class="invalid-feedback">
                      {{ errors.min_salary }}
                    </div>
                  </div>

                  <div class="mb-3" v-if="formData.is_salary_visible && !formData.is_salary_negotiable">
                    <label for="max_salary" class="form-label">Mức lương tối đa</label>
                    <input
                      id="max_salary"
                      v-model.number="formData.max_salary"
                      type="number"
                      min="0"
                      class="form-control"
                      :class="{ 'is-invalid': errors.max_salary }"
                    />
                    <div v-if="errors.max_salary" class="invalid-feedback">
                      {{ errors.max_salary }}
                    </div>
                  </div>

                  <div v-if="formData.is_salary_negotiable" class="alert alert-info">
                    <small>Khi chọn "Thỏa thuận", mức lương sẽ được hiển thị là "Thỏa thuận" thay vì giá trị cụ thể.</small>
                  </div>
                </div>
              </div>

              <!-- Thời gian -->
              <div class="card mb-4">
                <div class="card-header">
                  <h6 class="card-title mb-0">Thời gian</h6>
                </div>
                <div class="card-body">
                  <div class="mb-3">
                    <label for="publish_date" class="form-label">Ngày đăng <span class="text-danger">*</span></label>
                    <input
                      id="publish_date"
                      v-model="formData.publish_date"
                      type="date"
                      class="form-control"
                      :class="{ 'is-invalid': errors.publish_date }"
                      required
                    />
                    <div v-if="errors.publish_date" class="invalid-feedback">
                      {{ errors.publish_date }}
                    </div>
                  </div>

                  <div class="mb-3">
                    <label for="closing_date" class="form-label">Hạn nộp hồ sơ <span class="text-danger">*</span></label>
                    <div class="form-check mb-2">
                      <input
                        id="is_open_until_filled"
                        v-model="formData.is_open_until_filled"
                        type="checkbox"
                        class="form-check-input"
                        @change="onOpenUntilFilledChange"
                      />
                      <label for="is_open_until_filled" class="form-check-label">Tuyển dụng đến khi đủ</label>
                    </div>
                    <input
                      id="closing_date"
                      v-model="formData.closing_date"
                      type="date"
                      class="form-control"
                      :class="{ 'is-invalid': errors.closing_date }"
                      :disabled="formData.is_open_until_filled"
                      :required="!formData.is_open_until_filled"
                    />
                    <div v-if="errors.closing_date" class="invalid-feedback">
                      {{ errors.closing_date }}
                    </div>
                    <div v-if="formData.is_open_until_filled" class="form-text text-info">
                      Tin tuyển dụng sẽ mở cho đến khi đủ số lượng ứng viên cần tuyển.
                    </div>
                  </div>
                </div>
              </div>

              <!-- Trạng thái -->
              <div class="card mb-4">
                <div class="card-header">
                  <h6 class="card-title mb-0">Trạng thái</h6>
                </div>
                <div class="card-body">
                  <div class="mb-3">
                    <label for="status" class="form-label">Trạng thái <span class="text-danger">*</span></label>
                    <select
                      id="status"
                      v-model="formData.status"
                      class="form-select"
                      :class="{ 'is-invalid': errors.status }"
                      required
                    >
                      <option value="draft">Nháp</option>
                      <option value="pending">Chờ duyệt</option>
                      <option value="published">Đăng ngay</option>
                      <option value="closed">Đã đóng</option>
                      <option value="cancelled">Đã hủy</option>
                    </select>
                    <div v-if="errors.status" class="invalid-feedback">
                      {{ errors.status }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="d-flex justify-content-end">
            <router-link to="/recruitment/job-postings" class="btn btn-outline-secondary me-2">
              Hủy
            </router-link>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
              {{ isEditing ? 'Cập nhật' : 'Tạo tin tuyển dụng' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'JobPostingForm',
  data() {
    return {
      formData: {
        title: '',
        job_code: '',
        workplace_type: '',
        department: '',
        factory: '',
        division: '',
        team: '',
        positions: 1,
        employment_type: '',
        location: '',
        description: '',
        requirements: '',
        benefits: '',
        experience_level: '',
        education_required: '',
        is_salary_visible: true,
        is_salary_negotiable: false,
        min_salary: null,
        max_salary: null,
        publish_date: this.formatDateForInput(new Date()),
        closing_date: this.formatDateForInput(new Date(Date.now() + 30 * 24 * 60 * 60 * 1000)), // 30 days from now
        is_open_until_filled: false,
        status: 'draft'
      },
      errors: {},
      departments: [],
      factories: [],
      divisions: [],
      teams: [],
      savedClosingDate: null
    }
  },
  computed: {
    ...mapGetters('recruitment', ['jobPosting', 'loading', 'error']),
    ...mapGetters('departments', ['allDepartments']),
    ...mapGetters('factories', ['allFactories']),

    isEditing() {
      return !!this.$route.params.id
    },

    jobId() {
      return this.$route.params.id
    }
  },
  created() {
    this.fetchDepartments()
    this.fetchFactories()

    if (this.isEditing) {
      this.fetchJobPosting()
    }
  },
  methods: {
    async fetchDepartments() {
      await this.$store.dispatch('departments/fetchDepartments')
      this.departments = this.allDepartments.filter(dept => dept.dept_type === 'department')
      console.log('All Departments:', this.allDepartments)
    },

    async fetchFactories() {
      await this.$store.dispatch('factories/fetchFactories')
      this.factories = this.allFactories.filter(factory => factory.factory_type === 'factory')
    },

    async fetchJobPosting() {
      try {
        await this.$store.dispatch('recruitment/fetchJobPosting', this.jobId)

        if (this.jobPosting) {
          // Populate form data from job posting
          this.formData = {
            title: this.jobPosting.title,
            job_code: this.jobPosting.job_code,
            workplace_type: this.jobPosting.department ? 'department' : 'factory',
            department: this.jobPosting.department?.id || '',
            factory: this.jobPosting.factory?.id || '',
            division: this.jobPosting.division?.id || '',
            team: this.jobPosting.team?.id || '',
            positions: this.jobPosting.positions,
            employment_type: this.jobPosting.employment_type,
            location: this.jobPosting.location,
            description: this.jobPosting.description,
            requirements: this.jobPosting.requirements,
            benefits: this.jobPosting.benefits,
            experience_level: this.jobPosting.experience_level,
            education_required: this.jobPosting.education_required,
            is_salary_visible: this.jobPosting.is_salary_visible,
            is_salary_negotiable: this.jobPosting.is_salary_negotiable || false,
            min_salary: this.jobPosting.min_salary,
            max_salary: this.jobPosting.max_salary,
            publish_date: this.formatDateForInput(this.jobPosting.publish_date),
            closing_date: this.formatDateForInput(this.jobPosting.closing_date),
            is_open_until_filled: this.jobPosting.is_open_until_filled || false,
            status: this.jobPosting.status
          }

          // Load divisions and teams if department is selected
          if (this.formData.department) {
            await this.onDepartmentChange()

            // If division is selected, load teams
            if (this.formData.division) {
              await this.onDivisionChange()
            }
          }
        }
      } catch (error) {
        console.error('Error fetching job posting:', error)
      }
    },

    formatDateForInput(dateString) {
      if (!dateString) return ''

      const date = new Date(dateString)
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')

      return `${year}-${month}-${day}`
    },

    validateForm() {
      this.errors = {}

      if (!this.formData.title) {
        this.errors.title = 'Vui lòng nhập tiêu đề tin tuyển dụng'
      }

      // Kiểm tra job_code nếu được nhập (không bắt buộc)
      if (this.formData.job_code && this.formData.job_code.trim() === '') {
        // Nếu người dùng chỉ nhập khoảng trắng, đặt lại thành chuỗi rỗng
        this.formData.job_code = ''
      }

      if (!this.formData.workplace_type) {
        this.errors.workplace_type = 'Vui lòng chọn nơi làm việc'
      } else if (this.formData.workplace_type === 'department' && !this.formData.department) {
        this.errors.department = 'Vui lòng chọn phòng ban'
      } else if (this.formData.workplace_type === 'factory' && !this.formData.factory) {
        this.errors.factory = 'Vui lòng chọn xí nghiệp'
      }

      // Bộ phận và nhóm không bắt buộc, không cần kiểm tra

      if (!this.formData.positions || this.formData.positions < 1) {
        this.errors.positions = 'Vui lòng nhập số lượng cần tuyển hợp lệ'
      }

      if (!this.formData.employment_type) {
        this.errors.employment_type = 'Vui lòng chọn hình thức làm việc'
      }

      if (!this.formData.location) {
        this.errors.location = 'Vui lòng nhập địa điểm làm việc'
      }

      if (!this.formData.description) {
        this.errors.description = 'Vui lòng nhập mô tả công việc'
      }

      if (!this.formData.requirements) {
        this.errors.requirements = 'Vui lòng nhập yêu cầu ứng viên'
      }

      if (!this.formData.benefits) {
        this.errors.benefits = 'Vui lòng nhập quyền lợi'
      }

      if (!this.formData.experience_level) {
        this.errors.experience_level = 'Vui lòng chọn kinh nghiệm'
      }

      if (!this.formData.education_required) {
        this.errors.education_required = 'Vui lòng chọn học vấn'
      }

      if (this.formData.is_salary_visible && !this.formData.is_salary_negotiable) {
        if (this.formData.min_salary && this.formData.max_salary && parseInt(this.formData.min_salary) > parseInt(this.formData.max_salary)) {
          this.errors.max_salary = 'Mức lương tối đa phải lớn hơn mức lương tối thiểu'
        }
      }

      if (!this.formData.publish_date) {
        this.errors.publish_date = 'Vui lòng chọn ngày đăng'
      }

      if (!this.formData.is_open_until_filled) {
        if (!this.formData.closing_date) {
          this.errors.closing_date = 'Vui lòng chọn hạn nộp hồ sơ hoặc chọn "Tuyển dụng đến khi đủ"'
        } else if (new Date(this.formData.closing_date) <= new Date(this.formData.publish_date)) {
          this.errors.closing_date = 'Hạn nộp hồ sơ phải sau ngày đăng'
        }
      }

      if (!this.formData.status) {
        this.errors.status = 'Vui lòng chọn trạng thái'
      }

      return Object.keys(this.errors).length === 0
    },

    onSalaryVisibleChange() {
      // Nếu không hiển thị mức lương, thì không thể thỏa thuận
      if (!this.formData.is_salary_visible) {
        this.formData.is_salary_negotiable = false
      }
    },

    onSalaryNegotiableChange() {
      // Nếu thỏa thuận, thì phải hiển thị mức lương
      if (this.formData.is_salary_negotiable) {
        this.formData.is_salary_visible = true
        // Xóa giá trị mức lương khi chọn thỏa thuận
        this.formData.min_salary = null
        this.formData.max_salary = null
      }
    },

    onOpenUntilFilledChange() {
      // Nếu tuyển dụng đến khi đủ, không cần hạn nộp hồ sơ
      if (this.formData.is_open_until_filled) {
        // Lưu lại giá trị cũ để khôi phục khi bỏ chọn
        this.savedClosingDate = this.formData.closing_date
        // Đặt giá trị mặc định xa trong tương lai (1 năm)
        const oneYearLater = new Date()
        oneYearLater.setFullYear(oneYearLater.getFullYear() + 1)
        this.formData.closing_date = this.formatDateForInput(oneYearLater)
      } else if (this.savedClosingDate) {
        // Khôi phục giá trị cũ khi bỏ chọn
        this.formData.closing_date = this.savedClosingDate
      }
    },

    async onDepartmentChange() {
      // Reset division and team when department changes
      this.formData.division = ''
      this.formData.team = ''
      this.divisions = []
      this.teams = []

      if (this.formData.department) {
        // Fetch divisions for the selected department
        this.divisions = this.allDepartments.filter(
          dept => dept.dept_type === 'division' && dept.parent === parseInt(this.formData.department)
        )
        console.log('Divisions:', this.divisions)
      }
    },

    async onFactoryChange() {
      // Reset division and team when factory changes
      this.formData.division = ''
      this.formData.team = ''
      this.divisions = []
      this.teams = []

      if (this.formData.factory) {
        // Fetch divisions for the selected factory
        // Lấy các bộ phận thuộc xí nghiệp này
        try {
          // Lấy danh sách xí nghiệp và bộ phận
          await this.$store.dispatch('factories/fetchFactories')

          // Lọc các bộ phận thuộc xí nghiệp đã chọn
          const allFactories = this.$store.getters['factories/allFactories']
          console.log('All Factories:', allFactories)

          // Lọc các bộ phận (factory_type = 'division') có parent là xí nghiệp đã chọn
          this.divisions = allFactories.filter(
            item => item.factory_type === 'division' &&
                   item.parent &&
                   item.parent === parseInt(this.formData.factory)
          )
          console.log('Factory Divisions:', this.divisions)
        } catch (error) {
          console.error('Error fetching factory divisions:', error)
          this.divisions = []
        }
      }
    },

    async onDivisionChange() {
      // Reset team when division changes
      this.formData.team = ''
      this.teams = []

      if (this.formData.division) {
        try {
          if (this.formData.workplace_type === 'department') {
            // Nếu là phòng ban, lấy nhóm từ Department
            this.teams = this.allDepartments.filter(
              dept => dept.dept_type === 'team' && dept.parent === parseInt(this.formData.division)
            )
          } else if (this.formData.workplace_type === 'factory') {
            // Nếu là xí nghiệp, lấy nhóm từ Factory
            const allFactories = this.$store.getters['factories/allFactories']
            this.teams = allFactories.filter(
              item => item.factory_type === 'team' &&
                     item.parent &&
                     item.parent === parseInt(this.formData.division)
            )
          }
          console.log('Teams:', this.teams)
        } catch (error) {
          console.error('Error fetching teams:', error)
          this.teams = []
        }
      }
    },

    async saveJobPosting() {
      if (!this.validateForm()) {
        return
      }

      try {
        // Chuyển đổi các giá trị số từ chuỗi sang số
        const positions = parseInt(this.formData.positions, 10) || 1
        const minSalary = this.formData.min_salary ? parseInt(this.formData.min_salary, 10) : null
        const maxSalary = this.formData.max_salary ? parseInt(this.formData.max_salary, 10) : null

        // Đảm bảo các trường ID là số nguyên
        const departmentId = this.formData.department ? parseInt(this.formData.department, 10) : null
        const factoryId = this.formData.factory ? parseInt(this.formData.factory, 10) : null
        const divisionId = this.formData.division ? parseInt(this.formData.division, 10) : null
        const teamId = this.formData.team ? parseInt(this.formData.team, 10) : null

        const data = {
          title: this.formData.title.trim(),
          // Chỉ gửi job_code nếu người dùng đã nhập, nếu không thì không gửi trường này để backend tạo tự động
          ...(this.formData.job_code ? { job_code: this.formData.job_code.trim() } : {}),
          description: this.formData.description.trim(),
          requirements: this.formData.requirements.trim(),
          benefits: this.formData.benefits.trim(),
          positions: positions,
          min_salary: this.formData.is_salary_negotiable ? null : minSalary,
          max_salary: this.formData.is_salary_negotiable ? null : maxSalary,
          is_salary_visible: this.formData.is_salary_visible,
          is_salary_negotiable: this.formData.is_salary_negotiable,
          workplace_type: this.formData.workplace_type,
          location: this.formData.location.trim(),
          publish_date: this.formData.publish_date,
          closing_date: this.formData.closing_date,
          is_open_until_filled: this.formData.is_open_until_filled,
          status: this.formData.status,
          employment_type: this.formData.employment_type,
          experience_level: this.formData.experience_level,
          education_required: this.formData.education_required
        }

        // Xử lý nơi làm việc dựa trên workplace_type
        if (this.formData.workplace_type === 'department') {
          data.department = departmentId
          data.factory = null

          // Thêm thông tin về bộ phận và nhóm
          data.division = divisionId
          data.team = teamId
        } else if (this.formData.workplace_type === 'factory') {
          data.factory = factoryId
          data.department = null

          // Thêm thông tin về bộ phận và nhóm thuộc xí nghiệp
          data.division = divisionId
          data.team = teamId
        }

        // Log dữ liệu trước khi gửi để debug
        console.log('Sending data to API:', data)

        if (this.isEditing) {
          await this.$store.dispatch('recruitment/updateJobPosting', {
            id: this.jobId,
            data
          })
          this.$store.dispatch('app/setSuccess', 'Cập nhật tin tuyển dụng thành công')
        } else {
          await this.$store.dispatch('recruitment/createJobPosting', data)
          this.$store.dispatch('app/setSuccess', 'Tạo tin tuyển dụng thành công')
        }

        this.$router.push('/recruitment/job-postings')
      } catch (error) {
        console.error('Error saving job posting:', error)

        // Xử lý lỗi chi tiết từ server
        if (error.response && error.response.data) {
          const errorData = error.response.data

          // Nếu server trả về lỗi dạng object với các trường cụ thể
          if (typeof errorData === 'object' && errorData !== null) {
            // Cập nhật errors state với lỗi từ server
            this.errors = { ...this.errors, ...errorData }

            // Tạo thông báo lỗi chi tiết
            let errorMessage = this.isEditing ? 'Cập nhật tin tuyển dụng thất bại: ' : 'Tạo tin tuyển dụng thất bại: '

            // Thêm chi tiết lỗi vào thông báo
            const errorDetails = Object.entries(errorData)
              .map(([field, messages]) => {
                if (Array.isArray(messages)) {
                  return `${field}: ${messages.join(', ')}`
                } else if (typeof messages === 'string') {
                  return `${field}: ${messages}`
                }
                return null
              })
              .filter(Boolean)
              .join('; ')

            this.$store.dispatch('app/setError', errorMessage + errorDetails)
          } else {
            // Nếu server trả về lỗi dạng string
            this.$store.dispatch('app/setError', this.isEditing ? 'Cập nhật tin tuyển dụng thất bại: ' : 'Tạo tin tuyển dụng thất bại: ' + errorData)
          }
        } else {
          // Lỗi không có response data
          this.$store.dispatch('app/setError', this.isEditing ? 'Cập nhật tin tuyển dụng thất bại' : 'Tạo tin tuyển dụng thất bại')
        }

        // Cuộn lên đầu trang để hiển thị lỗi
        window.scrollTo(0, 0)
      }
    }
  }
}
</script>

<style scoped>
.form-label {
  font-weight: 500;
}

.card-header {
  background-color: #f8f9fa;
}

.card-title {
  font-weight: 600;
}
</style>
