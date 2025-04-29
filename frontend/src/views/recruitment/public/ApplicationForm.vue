<template>
  <div class="container py-5">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Đang tải...</span>
      </div>
    </div>
    <div v-else-if="!jobPosting" class="text-center py-5">
      <div class="alert alert-danger">
        <h4 class="alert-heading">Không tìm thấy vị trí</h4>
        <p>Vị trí này không tồn tại hoặc đã hết hạn.</p>
        <hr />
        <router-link to="/careers" class="btn btn-primary">
          Xem các vị trí khác
        </router-link>
      </div>
    </div>
    <div v-else-if="isExpired" class="text-center py-5">
      <div class="alert alert-warning">
        <h4 class="alert-heading">Đã hết hạn ứng tuyển</h4>
        <p>Vị trí này đã hết hạn ứng tuyển.</p>
        <hr />
        <router-link to="/careers" class="btn btn-primary">
          Xem các vị trí khác
        </router-link>
      </div>
    </div>
    <div v-else-if="submitted" class="text-center py-5">
      <div class="alert alert-success">
        <h4 class="alert-heading">Nộp đơn thành công!</h4>
        <p>Cảm ơn bạn đã ứng tuyển vị trí {{ jobPosting.title }}.</p>
        <p>Chúng tôi sẽ xem xét hồ sơ của bạn và liên hệ trong thời gian sớm nhất.</p>
        <hr />
        <div class="d-flex justify-content-center">
          <router-link to="/careers" class="btn btn-primary me-2">
            Xem các vị trí khác
          </router-link>
          <router-link :to="`/careers/${jobId}`" class="btn btn-outline-primary">
            Quay lại thông tin vị trí
          </router-link>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="row mb-4">
        <div class="col-md-12">
          <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
              <li class="breadcrumb-item"><router-link to="/">Trang chủ</router-link></li>
              <li class="breadcrumb-item"><router-link to="/careers">Cơ hội việc làm</router-link></li>
              <li class="breadcrumb-item">
                <router-link :to="`/careers/${jobId}`">{{ jobPosting.title }}</router-link>
              </li>
              <li class="breadcrumb-item active" aria-current="page">Ứng tuyển</li>
            </ol>
          </nav>
          <h1 class="mb-2">Ứng tuyển vị trí: {{ jobPosting.title }}</h1>
          <h5 class="text-muted mb-4">{{ jobPosting.department_name || jobPosting.factory_name }}</h5>
        </div>
      </div>

      <div class="row">
        <div class="col-md-8">
          <div class="card">
            <div class="card-header">
              <h5 class="card-title mb-0">Thông tin ứng tuyển</h5>
            </div>
            <div class="card-body">
              <form @submit.prevent="submitApplication">
                <div class="form-section mb-4">
                  <h5 class="form-section-title border-bottom pb-2">Thông tin cá nhân</h5>
                  <div class="row">
                    <div class="col-md-6 col-lg-4 mb-3">
                      <label for="last_name" class="form-label">Họ và tên đệm <span class="text-danger">*</span></label>
                      <input
                        id="last_name"
                        v-model="formData.last_name"
                        type="text"
                        class="form-control"
                        :class="{ 'is-invalid': errors.last_name }"
                        required
                      />
                      <div v-if="errors.last_name" class="invalid-feedback">
                        {{ errors.last_name }}
                      </div>
                      <small class="form-text text-muted">Ví dụ: Nguyễn Văn (Ghi họ và tên đệm)</small>
                    </div>

                    <div class="col-md-6 col-lg-4 mb-3">
                      <label for="first_name" class="form-label">Tên <span class="text-danger">*</span></label>
                      <input
                        id="first_name"
                        v-model="formData.first_name"
                        type="text"
                        class="form-control"
                        :class="{ 'is-invalid': errors.first_name }"
                        required
                      />
                      <div v-if="errors.first_name" class="invalid-feedback">
                        {{ errors.first_name }}
                      </div>
                      <small class="form-text text-muted">Ví dụ: Anh (Chỉ ghi tên, không ghi tên đệm)</small>
                    </div>

                    <div class="col-md-6 col-lg-4 mb-3">
                      <label for="gender" class="form-label">Giới tính <span class="text-danger">*</span></label>
                      <select
                        id="gender"
                        v-model="formData.gender"
                        class="form-select"
                        :class="{ 'is-invalid': errors.gender }"
                        :disabled="loadingOptions"
                        required
                      >
                        <option value="">-- Chọn --</option>
                        <option v-for="option in genderOptions || []" :key="option?.id" :value="option?.id">
                          {{ option?.name }}
                        </option>
                      </select>
                      <div v-if="loadingOptions" class="form-text text-muted">
                        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                        Đang tải dữ liệu...
                      </div>
                      <div v-if="errors.gender" class="invalid-feedback">
                        {{ errors.gender }}
                      </div>
                    </div>

                    <div class="col-md-6 col-lg-4 mb-3">
                      <label for="date_of_birth" class="form-label">Ngày sinh <span class="text-danger">*</span></label>
                      <input
                        id="date_of_birth"
                        v-model="formData.date_of_birth"
                        type="date"
                        class="form-control"
                        :class="{ 'is-invalid': errors.date_of_birth }"
                        required
                      />
                      <div v-if="errors.date_of_birth" class="invalid-feedback">
                        {{ errors.date_of_birth }}
                      </div>
                    </div>

                    <div class="col-md-6 col-lg-4 mb-3">
                      <label for="email" class="form-label">Email <span class="text-danger">*</span></label>
                      <input
                        id="email"
                        v-model="formData.email"
                        type="email"
                        class="form-control"
                        :class="{ 'is-invalid': errors.email }"
                        required
                      />
                      <div v-if="errors.email" class="invalid-feedback">
                        {{ errors.email }}
                      </div>
                    </div>

                    <div class="col-md-6 col-lg-4 mb-3">
                      <label for="phone" class="form-label">Số điện thoại <span class="text-danger">*</span></label>
                      <input
                        id="phone"
                        v-model="formData.phone"
                        type="tel"
                        class="form-control"
                        :class="{ 'is-invalid': errors.phone }"
                        required
                      />
                      <div v-if="errors.phone" class="invalid-feedback">
                        {{ errors.phone }}
                      </div>
                    </div>

                    <div class="col-md-6 col-lg-4 mb-3">
                      <label for="marital_status" class="form-label">Tình trạng hôn nhân</label>
                      <select
                        id="marital_status"
                        v-model="formData.marital_status"
                        class="form-select"
                        :class="{ 'is-invalid': errors.marital_status }"
                        :disabled="loadingOptions"
                      >
                        <option value="">-- Chọn --</option>
                        <option v-for="option in maritalStatusOptions || []" :key="option?.id" :value="option?.id">
                          {{ option?.name }}
                        </option>
                      </select>
                      <div v-if="loadingOptions" class="form-text text-muted">
                        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                        Đang tải dữ liệu...
                      </div>
                      <div v-if="errors.marital_status" class="invalid-feedback">
                        {{ errors.marital_status }}
                      </div>
                    </div>

                    <div class="col-md-6 col-lg-4 mb-3">
                      <label for="nationality" class="form-label">Quốc tịch</label>
                      <input
                        id="nationality"
                        v-model="formData.nationality"
                        type="text"
                        class="form-control"
                        :class="{ 'is-invalid': errors.nationality }"
                      />
                      <div v-if="errors.nationality" class="invalid-feedback">
                        {{ errors.nationality }}
                      </div>
                    </div>

                    <div class="col-md-6 col-lg-4 mb-3">
                      <label for="birth_place" class="form-label">Nơi sinh</label>
                      <input
                        id="birth_place"
                        v-model="formData.birth_place"
                        type="text"
                        class="form-control"
                        :class="{ 'is-invalid': errors.birth_place }"
                      />
                      <div v-if="errors.birth_place" class="invalid-feedback">
                        {{ errors.birth_place }}
                      </div>
                    </div>

                    <div class="col-md-6 col-lg-4 mb-3">
                      <label for="ethnicity" class="form-label">Dân tộc</label>
                      <input
                        id="ethnicity"
                        v-model="formData.ethnicity"
                        type="text"
                        class="form-control"
                        :class="{ 'is-invalid': errors.ethnicity }"
                      />
                      <div v-if="errors.ethnicity" class="invalid-feedback">
                        {{ errors.ethnicity }}
                      </div>
                    </div>

                    <div class="col-md-6 col-lg-4 mb-3">
                      <label for="religion" class="form-label">Tôn giáo</label>
                      <input
                        id="religion"
                        v-model="formData.religion"
                        type="text"
                        class="form-control"
                        :class="{ 'is-invalid': errors.religion }"
                      />
                      <div v-if="errors.religion" class="invalid-feedback">
                        {{ errors.religion }}
                      </div>
                    </div>

                    <div class="col-md-6 col-lg-4 mb-3">
                      <div class="form-check form-switch mt-4">
                        <input
                          id="is_party_member"
                          v-model="formData.is_party_member"
                          type="checkbox"
                          class="form-check-input"
                        />
                        <label class="form-check-label" for="is_party_member">
                          Là Đảng viên
                        </label>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Thông tin CCCD/CMND -->
                <div class="form-section mb-4">
                  <h5 class="form-section-title border-bottom pb-2">Thông tin CCCD/CMND</h5>
                  <div class="row">
                    <div class="col-md-6 col-lg-4 mb-3">
                      <label for="id_card_number" class="form-label">Số CCCD/CMND <span class="text-danger">*</span></label>
                      <input
                        id="id_card_number"
                        v-model="formData.id_card_number"
                        type="text"
                        class="form-control"
                        :class="{ 'is-invalid': errors.id_card_number }"
                        required
                      />
                      <div v-if="errors.id_card_number" class="invalid-feedback">
                        {{ errors.id_card_number }}
                      </div>
                    </div>

                    <div class="col-md-6 col-lg-4 mb-3">
                      <label for="id_card_issue_date" class="form-label">Ngày cấp <span class="text-danger">*</span></label>
                      <input
                        id="id_card_issue_date"
                        v-model="formData.id_card_issue_date"
                        type="date"
                        class="form-control"
                        :class="{ 'is-invalid': errors.id_card_issue_date }"
                        required
                      />
                      <div v-if="errors.id_card_issue_date" class="invalid-feedback">
                        {{ errors.id_card_issue_date }}
                      </div>
                    </div>

                    <div class="col-md-6 col-lg-4 mb-3">
                      <label for="id_card_issue_place" class="form-label">Nơi cấp <span class="text-danger">*</span></label>
                      <input
                        id="id_card_issue_place"
                        v-model="formData.id_card_issue_place"
                        type="text"
                        class="form-control"
                        :class="{ 'is-invalid': errors.id_card_issue_place }"
                        required
                      />
                      <div v-if="errors.id_card_issue_place" class="invalid-feedback">
                        {{ errors.id_card_issue_place }}
                      </div>
                    </div>

                    <div class="col-md-6 mb-3">
                      <label for="id_card_front_image" class="form-label">Ảnh mặt trước CCCD/CMND <span class="text-danger">*</span></label>
                      <input
                        id="id_card_front_image"
                        type="file"
                        class="form-control"
                        :class="{ 'is-invalid': errors.id_card_front_image }"
                        @change="e => handleFileUpload(e, 'id_card_front_image')"
                        required
                      />
                      <div v-if="errors.id_card_front_image" class="invalid-feedback">
                        {{ errors.id_card_front_image }}
                      </div>
                      <small class="form-text text-muted">Ảnh CCCD/CMND mặt trước. Định dạng JPG, PNG. Tối đa 2MB.</small>
                    </div>

                    <div class="col-md-6 mb-3">
                      <label for="id_card_back_image" class="form-label">Ảnh mặt sau CCCD/CMND <span class="text-danger">*</span></label>
                      <input
                        id="id_card_back_image"
                        type="file"
                        class="form-control"
                        :class="{ 'is-invalid': errors.id_card_back_image }"
                        @change="e => handleFileUpload(e, 'id_card_back_image')"
                        required
                      />
                      <div v-if="errors.id_card_back_image" class="invalid-feedback">
                        {{ errors.id_card_back_image }}
                      </div>
                      <small class="form-text text-muted">Ảnh CCCD/CMND mặt sau. Định dạng JPG, PNG. Tối đa 2MB.</small>
                    </div>
                  </div>
                </div>

                <!-- Thông tin liên hệ và địa chỉ -->
                <div class="form-section mb-4">
                  <h5 class="form-section-title border-bottom pb-2">Thông tin liên hệ và địa chỉ</h5>
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="permanent_address" class="form-label">Địa chỉ thường trú <span class="text-danger">*</span></label>
                      <input
                        id="permanent_address"
                        v-model="formData.permanent_address"
                        type="text"
                        class="form-control"
                        :class="{ 'is-invalid': errors.permanent_address }"
                        required
                      />
                      <div v-if="errors.permanent_address" class="invalid-feedback">
                        {{ errors.permanent_address }}
                      </div>
                    </div>

                    <div class="col-md-6 mb-3">
                      <label for="address" class="form-label">Địa chỉ liên hệ <span class="text-danger">*</span></label>
                      <input
                        id="address"
                        v-model="formData.address"
                        type="text"
                        class="form-control"
                        :class="{ 'is-invalid': errors.address }"
                        :readonly="formData.same_as_permanent"
                        required
                      />
                      <div v-if="errors.address" class="invalid-feedback">
                        {{ errors.address }}
                      </div>

                      <div class="form-check mt-2">
                        <input
                          id="same_as_permanent"
                          v-model="formData.same_as_permanent"
                          type="checkbox"
                          class="form-check-input"
                          @change="handleSameAddressChange"
                        />
                        <label class="form-check-label" for="same_as_permanent">
                          Giống địa chỉ thường trú
                        </label>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Thông tin liên hệ khẩn cấp -->
                <div class="form-section mb-4">
                  <h5 class="form-section-title border-bottom pb-2">Thông tin liên hệ khẩn cấp</h5>
                  <div class="row">
                    <div class="col-md-6 col-lg-4 mb-3">
                      <label for="emergency_contact_name" class="form-label">Tên người liên hệ <span class="text-danger">*</span></label>
                      <input
                        id="emergency_contact_name"
                        v-model="formData.emergency_contact_name"
                        type="text"
                        class="form-control"
                        :class="{ 'is-invalid': errors.emergency_contact_name }"
                        required
                      />
                      <div v-if="errors.emergency_contact_name" class="invalid-feedback">
                        {{ errors.emergency_contact_name }}
                      </div>
                    </div>

                    <div class="col-md-6 col-lg-4 mb-3">
                      <label for="emergency_contact_relationship" class="form-label">Mối quan hệ <span class="text-danger">*</span></label>
                      <input
                        id="emergency_contact_relationship"
                        v-model="formData.emergency_contact_relationship"
                        type="text"
                        class="form-control"
                        :class="{ 'is-invalid': errors.emergency_contact_relationship }"
                        required
                      />
                      <div v-if="errors.emergency_contact_relationship" class="invalid-feedback">
                        {{ errors.emergency_contact_relationship }}
                      </div>
                    </div>

                    <div class="col-md-6 col-lg-4 mb-3">
                      <label for="emergency_contact_phone" class="form-label">Số điện thoại <span class="text-danger">*</span></label>
                      <input
                        id="emergency_contact_phone"
                        v-model="formData.emergency_contact_phone"
                        type="tel"
                        class="form-control"
                        :class="{ 'is-invalid': errors.emergency_contact_phone }"
                        required
                      />
                      <div v-if="errors.emergency_contact_phone" class="invalid-feedback">
                        {{ errors.emergency_contact_phone }}
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Thông tin gia đình -->
                <div class="form-section mb-4">
                  <h5 class="form-section-title border-bottom pb-2">Thông tin gia đình</h5>
                  <div class="row">
                    <div class="col-md-6 col-lg-3 mb-3">
                      <label for="father_name" class="form-label">Tên cha</label>
                      <input
                        id="father_name"
                        v-model="formData.father_name"
                        type="text"
                        class="form-control"
                        :class="{ 'is-invalid': errors.father_name }"
                      />
                      <div v-if="errors.father_name" class="invalid-feedback">
                        {{ errors.father_name }}
                      </div>
                    </div>

                    <div class="col-md-6 col-lg-3 mb-3">
                      <label for="father_phone" class="form-label">Số điện thoại cha</label>
                      <input
                        id="father_phone"
                        v-model="formData.father_phone"
                        type="tel"
                        class="form-control"
                        :class="{ 'is-invalid': errors.father_phone }"
                      />
                      <div v-if="errors.father_phone" class="invalid-feedback">
                        {{ errors.father_phone }}
                      </div>
                    </div>

                    <div class="col-md-6 col-lg-3 mb-3">
                      <label for="mother_name" class="form-label">Tên mẹ</label>
                      <input
                        id="mother_name"
                        v-model="formData.mother_name"
                        type="text"
                        class="form-control"
                        :class="{ 'is-invalid': errors.mother_name }"
                      />
                      <div v-if="errors.mother_name" class="invalid-feedback">
                        {{ errors.mother_name }}
                      </div>
                    </div>

                    <div class="col-md-6 col-lg-3 mb-3">
                      <label for="mother_phone" class="form-label">Số điện thoại mẹ</label>
                      <input
                        id="mother_phone"
                        v-model="formData.mother_phone"
                        type="tel"
                        class="form-control"
                        :class="{ 'is-invalid': errors.mother_phone }"
                      />
                      <div v-if="errors.mother_phone" class="invalid-feedback">
                        {{ errors.mother_phone }}
                      </div>
                    </div>

                    <div class="col-12 mb-3">
                      <div class="form-check form-switch mb-3">
                        <input
                          id="is_family_policy"
                          v-model="formData.is_family_policy"
                          type="checkbox"
                          class="form-check-input"
                          @change="handleFamilyPolicyChange"
                        />
                        <label class="form-check-label" for="is_family_policy">
                          Thuộc diện chính sách
                        </label>
                      </div>

                      <div v-if="formData.is_family_policy" class="row ms-2">
                        <div class="col-md-6 mb-3">
                          <label for="family_policy_type" class="form-label">Loại chính sách</label>
                          <select
                            id="family_policy_type"
                            v-model="formData.family_policy_type"
                            class="form-select"
                            :class="{ 'is-invalid': errors.family_policy_type }"
                            :disabled="loadingOptions"
                          >
                            <option value="">-- Chọn loại chính sách --</option>
                            <option v-for="option in familyPolicyTypeOptions || []" :key="option?.id" :value="option?.id">
                              {{ option?.name }}
                            </option>
                          </select>
                          <div v-if="loadingOptions" class="form-text text-muted">
                            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                            Đang tải dữ liệu...
                          </div>
                          <div v-if="errors.family_policy_type" class="invalid-feedback">
                            {{ errors.family_policy_type }}
                          </div>
                        </div>

                        <div class="col-md-6 mb-3">
                          <label for="family_policy_detail" class="form-label">Chi tiết chính sách</label>
                          <input
                            id="family_policy_detail"
                            v-model="formData.family_policy_detail"
                            type="text"
                            class="form-control"
                            :class="{ 'is-invalid': errors.family_policy_detail }"
                          />
                          <div v-if="errors.family_policy_detail" class="invalid-feedback">
                            {{ errors.family_policy_detail }}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Thông tin nghĩa vụ quân sự -->
                <div class="form-section mb-4">
                  <h5 class="form-section-title border-bottom pb-2">Thông tin nghĩa vụ quân sự</h5>
                  <div class="row">
                    <div class="col-12 mb-3">
                      <div class="form-check form-switch mb-3">
                        <input
                          id="military_service"
                          v-model="formData.military_service"
                          type="checkbox"
                          class="form-check-input"
                          @change="handleMilitaryServiceChange"
                        />
                        <label class="form-check-label" for="military_service">
                          Đã hoàn thành nghĩa vụ quân sự
                        </label>
                      </div>

                      <div v-if="formData.military_service" class="row ms-2">
                        <div class="col-md-6 col-lg-4 mb-3">
                          <label for="military_service_date" class="form-label">Ngày bắt đầu</label>
                          <input
                            id="military_service_date"
                            v-model="formData.military_service_date"
                            type="date"
                            class="form-control"
                            :class="{ 'is-invalid': errors.military_service_date }"
                          />
                          <div v-if="errors.military_service_date" class="invalid-feedback">
                            {{ errors.military_service_date }}
                          </div>
                        </div>

                        <div class="col-md-6 col-lg-4 mb-3">
                          <label for="military_service_end_date" class="form-label">Ngày kết thúc</label>
                          <input
                            id="military_service_end_date"
                            v-model="formData.military_service_end_date"
                            type="date"
                            class="form-control"
                            :class="{ 'is-invalid': errors.military_service_end_date }"
                          />
                          <div v-if="errors.military_service_end_date" class="invalid-feedback">
                            {{ errors.military_service_end_date }}
                          </div>
                        </div>

                        <div class="col-md-6 col-lg-4 mb-3">
                          <label for="military_service_role" class="form-label">Chức vụ</label>
                          <input
                            id="military_service_role"
                            v-model="formData.military_service_role"
                            type="text"
                            class="form-control"
                            :class="{ 'is-invalid': errors.military_service_role }"
                          />
                          <div v-if="errors.military_service_role" class="invalid-feedback">
                            {{ errors.military_service_role }}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>



                <!-- Hồ sơ và thông tin nghề nghiệp -->
                <div class="form-section mb-4">
                  <h5 class="form-section-title border-bottom pb-2">Hồ sơ và thông tin nghề nghiệp</h5>
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="resume" class="form-label">CV của bạn</label>
                      <input
                        id="resume"
                        type="file"
                        class="form-control"
                        :class="{ 'is-invalid': errors.resume }"
                        @change="e => handleFileUpload(e, 'resume')"
                      />
                      <div v-if="errors.resume" class="invalid-feedback">
                        {{ errors.resume }}
                      </div>
                      <small class="form-text text-muted">Hỗ trợ định dạng PDF, DOC, DOCX. Kích thước tối đa 5MB.</small>
                    </div>

                    <div class="col-md-6 mb-3">
                      <label for="avatar" class="form-label">Ảnh đại diện</label>
                      <input
                        id="avatar"
                        type="file"
                        class="form-control"
                        :class="{ 'is-invalid': errors.avatar }"
                        @change="e => handleFileUpload(e, 'avatar')"
                      />
                      <div v-if="errors.avatar" class="invalid-feedback">
                        {{ errors.avatar }}
                      </div>
                      <small class="form-text text-muted">Hỗ trợ định dạng JPG, PNG, GIF. Kích thước tối đa 2MB.</small>
                    </div>

                    <div class="col-md-12 mb-3">
                      <label for="education_level" class="form-label">Trình độ học vấn</label>
                      <select
                        id="education_level"
                        v-model="formData.education_level"
                        class="form-select"
                        :class="{ 'is-invalid': errors.education_level }"
                        :disabled="loadingOptions"
                      >
                        <option value="">-- Chọn trình độ học vấn --</option>
                        <option v-for="option in educationLevelOptions || []" :key="option?.id" :value="option?.id">
                          {{ option?.name }}
                        </option>
                      </select>
                      <div v-if="loadingOptions" class="form-text text-muted">
                        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                        Đang tải dữ liệu...
                      </div>
                      <div v-if="errors.education_level" class="invalid-feedback">
                        {{ errors.education_level }}
                      </div>
                    </div>

                    <div class="col-md-12 mb-3">
                      <label for="education_detail" class="form-label">Chi tiết học vấn</label>
                      <textarea
                        id="education_detail"
                        v-model="formData.education_detail"
                        class="form-control"
                        :class="{ 'is-invalid': errors.education_detail }"
                        rows="3"
                      ></textarea>
                      <div v-if="errors.education_detail" class="invalid-feedback">
                        {{ errors.education_detail }}
                      </div>
                    </div>

                    <div class="col-md-12 mb-3">
                      <label for="experience" class="form-label">Kinh nghiệm làm việc</label>
                      <textarea
                        id="experience"
                        v-model="formData.experience"
                        class="form-control"
                        :class="{ 'is-invalid': errors.experience }"
                        rows="3"
                      ></textarea>
                      <div v-if="errors.experience" class="invalid-feedback">
                        {{ errors.experience }}
                      </div>
                    </div>

                    <div class="col-md-12 mb-3">
                      <label for="skills" class="form-label">Kỹ năng</label>
                      <textarea
                        id="skills"
                        v-model="formData.skills"
                        class="form-control"
                        :class="{ 'is-invalid': errors.skills }"
                        rows="3"
                      ></textarea>
                      <div v-if="errors.skills" class="invalid-feedback">
                        {{ errors.skills }}
                      </div>
                    </div>

                    <div class="col-md-12 mb-3">
                      <label for="cover_letter" class="form-label">Thư giới thiệu</label>
                      <textarea
                        id="cover_letter"
                        v-model="formData.cover_letter"
                        class="form-control"
                        :class="{ 'is-invalid': errors.cover_letter }"
                        rows="5"
                      ></textarea>
                      <div v-if="errors.cover_letter" class="invalid-feedback">
                        {{ errors.cover_letter }}
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Thông tin bổ sung -->
                <div class="form-section mb-4">
                  <h5 class="form-section-title border-bottom pb-2">Thông tin bổ sung</h5>
                  <div class="row">
                    <div class="col-md-6 col-lg-3 mb-3">
                      <label for="portfolio_url" class="form-label">Liên kết portfolio</label>
                      <input
                        id="portfolio_url"
                        v-model="formData.portfolio_url"
                        type="url"
                        class="form-control"
                        :class="{ 'is-invalid': errors.portfolio_url }"
                      />
                      <div v-if="errors.portfolio_url" class="invalid-feedback">
                        {{ errors.portfolio_url }}
                      </div>
                    </div>

                    <div class="col-md-6 col-lg-3 mb-3">
                      <label for="linkedin_profile" class="form-label">LinkedIn</label>
                      <input
                        id="linkedin_profile"
                        v-model="formData.linkedin_profile"
                        type="url"
                        class="form-control"
                        :class="{ 'is-invalid': errors.linkedin_profile }"
                      />
                      <div v-if="errors.linkedin_profile" class="invalid-feedback">
                        {{ errors.linkedin_profile }}
                      </div>
                    </div>

                    <div class="col-md-6 col-lg-3 mb-3">
                      <label for="expected_salary" class="form-label">Mức lương mong muốn</label>
                      <input
                        id="expected_salary"
                        v-model.number="formData.expected_salary"
                        type="number"
                        min="0"
                        step="1000000"
                        class="form-control"
                        :class="{ 'is-invalid': errors.expected_salary }"
                      />
                      <div v-if="errors.expected_salary" class="invalid-feedback">
                        {{ errors.expected_salary }}
                      </div>
                    </div>

                    <div class="col-md-6 col-lg-3 mb-3">
                      <label for="salary_currency" class="form-label">Đơn vị tiền tệ</label>
                      <select
                        id="salary_currency"
                        v-model="formData.salary_currency"
                        class="form-select"
                        :class="{ 'is-invalid': errors.salary_currency }"
                      >
                        <option value="VND">VND</option>
                        <option value="USD">USD</option>
                        <option value="EUR">EUR</option>
                      </select>
                      <div v-if="errors.salary_currency" class="invalid-feedback">
                        {{ errors.salary_currency }}
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Điều khoản -->
                <div class="form-section mb-4">
                  <div class="form-check mb-4">
                    <input
                      id="agree_terms"
                      v-model="formData.agree_terms"
                      type="checkbox"
                      class="form-check-input"
                      :class="{ 'is-invalid': errors.agree_terms }"
                      required
                    />
                    <label for="agree_terms" class="form-check-label">
                      Tôi đồng ý với <a href="#" @click.prevent="showTerms">điều khoản và điều kiện</a> <span class="text-danger">*</span>
                    </label>
                    <div v-if="errors.agree_terms" class="invalid-feedback">
                      {{ errors.agree_terms }}
                    </div>
                  </div>
                </div>

                <div class="text-end mt-4">
                  <router-link :to="`/careers/${jobId}`" class="btn btn-secondary me-2">
                    <font-awesome-icon icon="times" class="me-1" /> Hủy
                  </router-link>
                  <button type="submit" class="btn btn-primary" :disabled="submitting">
                    <span v-if="submitting" class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
                    <font-awesome-icon v-else icon="paper-plane" class="me-1" /> {{ submitting ? 'Đang gửi...' : 'Gửi đơn ứng tuyển' }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card mb-4">
            <div class="card-header">
              <h5 class="card-title mb-0">Thông tin vị trí</h5>
            </div>
            <div class="card-body">
              <h6>{{ jobPosting.title }}</h6>
              <p class="text-muted">{{ jobPosting.department_name || jobPosting.factory_name }}</p>

              <div class="mb-3">
                <span class="badge bg-primary me-2">{{ jobPosting.employment_type_display }}</span>
                <span class="badge bg-secondary">{{ jobPosting.location }}</span>
              </div>

              <div class="alert" :class="{'alert-warning': daysRemaining > 0, 'alert-info': jobPosting.is_open_until_filled}">
                <div class="d-flex align-items-center">
                  <font-awesome-icon :icon="jobPosting.is_open_until_filled ? 'calendar-check' : 'clock'" class="me-2" />
                  <div>
                    <strong>Hạn nộp hồ sơ:</strong> {{ jobPosting.is_open_until_filled ? 'Tuyển dụng đến khi đủ' : formatDate(jobPosting.closing_date) }}
                    <div v-if="daysRemaining > 0 && !jobPosting.is_open_until_filled" class="small">
                      Còn {{ daysRemaining }} ngày để ứng tuyển
                    </div>
                    <div v-else-if="jobPosting.is_open_until_filled" class="small">
                      Vẫn còn nhận hồ sơ ứng tuyển
                    </div>
                  </div>
                </div>
              </div>

              <div class="d-grid gap-2 mt-3">
                <router-link :to="`/careers/${jobId}`" class="btn btn-outline-primary">
                  <font-awesome-icon icon="arrow-left" class="me-1" />
                  Quay lại thông tin vị trí
                </router-link>
              </div>
            </div>
          </div>

          <div class="card mb-4">
            <div class="card-header">
              <h5 class="card-title mb-0">Mẹo ứng tuyển</h5>
            </div>
            <div class="card-body">
              <ul class="list-group list-group-flush">
                <li class="list-group-item">
                  <font-awesome-icon icon="check" class="text-success me-2" />
                  Điền đầy đủ thông tin trong đơn ứng tuyển
                </li>
                <li class="list-group-item">
                  <font-awesome-icon icon="check" class="text-success me-2" />
                  Cập nhật CV mới nhất của bạn
                </li>
                <li class="list-group-item">
                  <font-awesome-icon icon="check" class="text-success me-2" />
                  Viết thư giới thiệu phù hợp với vị trí ứng tuyển
                </li>
                <li class="list-group-item">
                  <font-awesome-icon icon="check" class="text-success me-2" />
                  Nêu rõ kỹ năng và kinh nghiệm liên quan
                </li>
                <li class="list-group-item">
                  <font-awesome-icon icon="check" class="text-success me-2" />
                  Kiểm tra lại thông tin trước khi gửi
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'ApplicationForm',
  data() {
    return {
      formData: {
        // Thông tin cơ bản
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        date_of_birth: '',
        gender: null,
        marital_status: null,
        nationality: 'Việt Nam',
        birth_place: '',
        ethnicity: '',
        religion: '',
        is_party_member: false,

        // Thông tin CCCD/CMND
        id_card_number: '',
        id_card_issue_date: '',
        id_card_issue_place: '',
        id_card_front_image: null,
        id_card_back_image: null,

        // Thông tin địa chỉ
        permanent_address: '',
        address: '',
        same_as_permanent: false,

        // Thông tin liên hệ khẩn cấp
        emergency_contact_name: '',
        emergency_contact_relationship: '',
        emergency_contact_phone: '',

        // Thông tin gia đình
        father_name: '',
        father_phone: '',
        mother_name: '',
        mother_phone: '',
        is_family_policy: false,
        family_policy_type: null,
        family_policy_detail: '',

        // Thông tin nghĩa vụ quân sự
        military_service: false,
        military_service_date: '',
        military_service_end_date: '',
        military_service_role: '',

        // Thông tin chuyên môn
        education_level: null,
        education_detail: '',
        experience: '',
        skills: '',
        cover_letter: '',
        resume: null,
        avatar: null,

        // Thông tin bổ sung
        portfolio_url: '',
        linkedin_profile: '',
        expected_salary: null,
        salary_currency: 'VND',

        // Điều khoản
        agree_terms: false,

        // Trường ẩn
        job_posting: null
      },
      maritalStatusOptions: [],
      familyPolicyTypeOptions: [],
      genderOptions: [],
      educationLevelOptions: [],
      errors: {},
      submitting: false,
      submitted: false,
      loadingOptions: false
    }
  },
  computed: {
    ...mapGetters('recruitment', ['jobPosting', 'loading', 'error']),

    jobId() {
      return this.$route.params.id
    },

    isExpired() {
      if (!this.jobPosting) return true

      // Nếu tuyển dụng đến khi đủ, không bao giờ hết hạn
      if (this.jobPosting.is_open_until_filled) return false

      // Nếu không có ngày hết hạn, coi như đã hết hạn
      if (!this.jobPosting.closing_date) return true

      const today = new Date()
      const closingDate = new Date(this.jobPosting.closing_date)

      return today > closingDate
    },

    daysRemaining() {
      if (!this.jobPosting) return 0

      // Nếu tuyển dụng đến khi đủ, trả về 1 để hiển thị là còn nhận hồ sơ
      if (this.jobPosting.is_open_until_filled) return 1

      // Nếu không có ngày hết hạn, trả về 0
      if (!this.jobPosting.closing_date) return 0

      const today = new Date()
      const closingDate = new Date(this.jobPosting.closing_date)
      const diffTime = closingDate - today
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

      return diffDays > 0 ? diffDays : 0
    }
  },
  created() {
    this.fetchJobPosting()
    this.fetchOptions()
  },
  methods: {
    async fetchJobPosting() {
      try {
        await this.$store.dispatch('recruitment/fetchPublicJobPosting', this.jobId)
      } catch (error) {
        console.error('Error fetching job posting:', error)
      }
    },

    async fetchOptions() {
      // Khởi tạo mảng rỗng để tránh lỗi null
      this.maritalStatusOptions = []
      this.familyPolicyTypeOptions = []
      this.genderOptions = []
      this.educationLevelOptions = []

      this.loadingOptions = true
      try {
        // Lấy danh sách tình trạng hôn nhân
        const maritalStatusResponse = await this.$store.dispatch('recruitment/fetchMaritalStatus')
        console.log('Marital status response:', maritalStatusResponse)

        if (maritalStatusResponse && maritalStatusResponse.results && Array.isArray(maritalStatusResponse.results)) {
          this.maritalStatusOptions = maritalStatusResponse.results
        }

        // Lấy danh sách loại chính sách gia đình
        const familyPolicyTypesResponse = await this.$store.dispatch('recruitment/fetchFamilyPolicyTypes')
        console.log('Family policy types response:', familyPolicyTypesResponse)

        if (familyPolicyTypesResponse && familyPolicyTypesResponse.results && Array.isArray(familyPolicyTypesResponse.results)) {
          this.familyPolicyTypeOptions = familyPolicyTypesResponse.results
        }

        // Lấy danh sách giới tính
        const gendersResponse = await this.$store.dispatch('recruitment/fetchGenders')
        console.log('Genders response:', gendersResponse)

        if (gendersResponse && gendersResponse.results && Array.isArray(gendersResponse.results)) {
          this.genderOptions = gendersResponse.results
        }

        // Lấy danh sách trình độ học vấn
        const educationLevelsResponse = await this.$store.dispatch('recruitment/fetchEducationLevels')
        console.log('Education levels response:', educationLevelsResponse)

        if (educationLevelsResponse && educationLevelsResponse.results && Array.isArray(educationLevelsResponse.results)) {
          this.educationLevelOptions = educationLevelsResponse.results
        }
      } catch (error) {
        console.error('Error fetching options:', error)
      } finally {
        this.loadingOptions = false
      }
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('vi-VN')
    },

    handleFileUpload(event, fieldName) {
      const file = event.target.files[0]
      if (!file) return

      // Xác định loại file và kích thước tối đa dựa trên trường
      let allowedTypes = []
      let maxSize = 0
      let errorMessage = ''

      if (fieldName === 'resume') {
        allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        maxSize = 5 * 1024 * 1024 // 5MB
        errorMessage = 'Chỉ chấp nhận file PDF, DOC, DOCX. Kích thước tối đa 5MB.'
      } else if (fieldName === 'avatar') {
        allowedTypes = ['image/jpeg', 'image/png', 'image/gif']
        maxSize = 2 * 1024 * 1024 // 2MB
        errorMessage = 'Chỉ chấp nhận file JPG, PNG, GIF. Kích thước tối đa 2MB.'
      } else if (fieldName === 'id_card_front_image' || fieldName === 'id_card_back_image') {
        allowedTypes = ['image/jpeg', 'image/png']
        maxSize = 2 * 1024 * 1024 // 2MB
        errorMessage = 'Chỉ chấp nhận file JPG, PNG. Kích thước tối đa 2MB.'
      }

      // Kiểm tra loại file
      if (!allowedTypes.includes(file.type)) {
        this.errors[fieldName] = errorMessage
        return
      }

      // Kiểm tra kích thước file
      if (file.size > maxSize) {
        this.errors[fieldName] = `Kích thước file không được vượt quá ${maxSize / (1024 * 1024)}MB`
        return
      }

      // Lưu file và xóa lỗi
      this.formData[fieldName] = file
      this.errors[fieldName] = null
    },

    handleSameAddressChange() {
      if (this.formData.same_as_permanent) {
        this.formData.address = this.formData.permanent_address
      }
    },

    handleFamilyPolicyChange() {
      if (!this.formData.is_family_policy) {
        this.formData.family_policy_type = null
        // Không xóa giá trị family_policy_detail để người dùng không phải nhập lại
      }
    },

    handleMilitaryServiceChange() {
      if (!this.formData.military_service) {
        this.formData.military_service_date = ''
        this.formData.military_service_end_date = ''
        this.formData.military_service_role = ''
      }
    },

    validateForm() {
      this.errors = {}

      // Thông tin cơ bản
      if (!this.formData.first_name) {
        this.errors.first_name = 'Vui lòng nhập tên'
      }

      if (!this.formData.last_name) {
        this.errors.last_name = 'Vui lòng nhập họ và tên đệm'
      }

      if (!this.formData.email) {
        this.errors.email = 'Vui lòng nhập email'
      } else if (!this.validateEmail(this.formData.email)) {
        this.errors.email = 'Email không hợp lệ'
      }

      if (!this.formData.phone) {
        this.errors.phone = 'Vui lòng nhập số điện thoại'
      } else if (!this.validatePhone(this.formData.phone)) {
        this.errors.phone = 'Số điện thoại không hợp lệ'
      }

      if (!this.formData.date_of_birth) {
        this.errors.date_of_birth = 'Vui lòng nhập ngày sinh'
      } else if (!this.validateDate(this.formData.date_of_birth)) {
        this.errors.date_of_birth = 'Ngày sinh không hợp lệ'
      }

      // Thông tin CCCD/CMND
      if (!this.formData.id_card_number) {
        this.errors.id_card_number = 'Vui lòng nhập số CCCD/CMND'
      }

      if (!this.formData.id_card_issue_date) {
        this.errors.id_card_issue_date = 'Vui lòng nhập ngày cấp'
      } else if (!this.validateDate(this.formData.id_card_issue_date)) {
        this.errors.id_card_issue_date = 'Ngày cấp không hợp lệ'
      }

      if (!this.formData.id_card_issue_place) {
        this.errors.id_card_issue_place = 'Vui lòng nhập nơi cấp'
      }

      if (!this.formData.id_card_front_image) {
        this.errors.id_card_front_image = 'Vui lòng tải lên ảnh mặt trước CCCD/CMND'
      }

      if (!this.formData.id_card_back_image) {
        this.errors.id_card_back_image = 'Vui lòng tải lên ảnh mặt sau CCCD/CMND'
      }

      // Thông tin địa chỉ
      if (!this.formData.permanent_address) {
        this.errors.permanent_address = 'Vui lòng nhập địa chỉ thường trú'
      }

      if (!this.formData.address) {
        this.errors.address = 'Vui lòng nhập địa chỉ liên hệ'
      }

      // Thông tin liên hệ khẩn cấp
      if (!this.formData.emergency_contact_name) {
        this.errors.emergency_contact_name = 'Vui lòng nhập tên người liên hệ khẩn cấp'
      }

      if (!this.formData.emergency_contact_relationship) {
        this.errors.emergency_contact_relationship = 'Vui lòng nhập mối quan hệ'
      }

      if (!this.formData.emergency_contact_phone) {
        this.errors.emergency_contact_phone = 'Vui lòng nhập số điện thoại liên hệ khẩn cấp'
      } else if (!this.validatePhone(this.formData.emergency_contact_phone)) {
        this.errors.emergency_contact_phone = 'Số điện thoại không hợp lệ'
      }

      // Thông tin gia đình
      if (this.formData.is_family_policy) {
        if (!this.formData.family_policy_type) {
          this.errors.family_policy_type = 'Vui lòng chọn loại chính sách'
        }
        // Chi tiết chính sách không bắt buộc
      }

      // Thông tin nghĩa vụ quân sự
      if (this.formData.military_service) {
        if (!this.formData.military_service_date) {
          this.errors.military_service_date = 'Vui lòng nhập ngày bắt đầu'
        } else if (!this.validateDate(this.formData.military_service_date)) {
          this.errors.military_service_date = 'Ngày bắt đầu không hợp lệ'
        }

        if (!this.formData.military_service_end_date) {
          this.errors.military_service_end_date = 'Vui lòng nhập ngày kết thúc'
        } else if (!this.validateDate(this.formData.military_service_end_date)) {
          this.errors.military_service_end_date = 'Ngày kết thúc không hợp lệ'
        }
      }

      // Thông tin chuyên môn không bắt buộc

      // Điều khoản
      if (!this.formData.agree_terms) {
        this.errors.agree_terms = 'Vui lòng đồng ý với điều khoản và điều kiện'
      }

      return Object.keys(this.errors).length === 0
    },

    validateEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      return re.test(email)
    },

    validatePhone(phone) {
      const re = /^[0-9+\-\s()]{8,15}$/
      return re.test(phone)
    },

    validateDate(date) {
      const d = new Date(date)
      return !isNaN(d.getTime())
    },

    async submitApplication() {
      if (!this.validateForm()) {
        // Cuộn đến lỗi đầu tiên
        this.$nextTick(() => {
          const firstError = document.querySelector('.is-invalid')
          if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' })
          }
        })
        return
      }

      this.submitting = true

      try {
        // Chuẩn bị dữ liệu để gửi đến API
        const formData = new FormData()

        // Thêm tất cả các trường vào FormData
        for (const key in this.formData) {
          // Xử lý các trường file đặc biệt
          if (key === 'resume' || key === 'avatar' || key === 'id_card_front_image' || key === 'id_card_back_image') {
            if (this.formData[key]) {
              formData.append(key, this.formData[key])
            }
          }
          // Xử lý các trường boolean
          else if (typeof this.formData[key] === 'boolean') {
            formData.append(key, this.formData[key] ? 'true' : 'false')
          }
          // Xử lý các trường object (ForeignKey)
          else if (key === 'marital_status' || key === 'family_policy_type' || key === 'gender' || key === 'education_level') {
            if (this.formData[key] !== null && this.formData[key] !== undefined) {
              formData.append(key, this.formData[key])
            }
          }
          // Xử lý các trường khác
          else if (this.formData[key] !== null && this.formData[key] !== undefined) {
            formData.append(key, this.formData[key])
          }
        }

        // Thêm job_posting ID
        formData.append('job_posting', this.jobId)

        // Đổi tên trường agree_terms để phù hợp với API
        formData.append('agree_terms', this.formData.agree_terms ? 'true' : 'false')

        // Tạo full_name từ first_name và last_name nếu cả hai đều có
        if (this.formData.first_name && this.formData.last_name) {
          formData.append('full_name', `${this.formData.last_name} ${this.formData.first_name}`)
        }

        // Gửi đơn ứng tuyển thông qua store
        await this.$store.dispatch('recruitment/submitApplication', formData)

        this.submitted = true
        this.submitting = false

        // Cuộn lên đầu trang để hiển thị thông báo thành công
        window.scrollTo({ top: 0, behavior: 'smooth' })
      } catch (error) {
        console.error('Error submitting application:', error)

        // Hiển thị thông báo lỗi cụ thể nếu có
        if (error.response && error.response.data) {
          const errorData = error.response.data

          // Xử lý lỗi validation từ server
          if (errorData.errors) {
            this.errors = { ...this.errors, ...errorData.errors }

            // Cuộn đến lỗi đầu tiên
            this.$nextTick(() => {
              const firstError = document.querySelector('.is-invalid')
              if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' })
              }
            })
          } else if (errorData.detail) {
            this.$store.dispatch('app/setError', errorData.detail)
          } else {
            this.$store.dispatch('app/setError', 'Có lỗi xảy ra khi gửi đơn ứng tuyển. Vui lòng thử lại sau.')
          }
        } else {
          this.$store.dispatch('app/setError', 'Có lỗi xảy ra khi gửi đơn ứng tuyển. Vui lòng thử lại sau.')
        }

        this.submitting = false
      }
    },

    showTerms() {
      // In a real app, this would show a modal with terms and conditions
      alert('Điều khoản và điều kiện:\n\n1. Thông tin cá nhân của bạn sẽ được bảo mật và chỉ sử dụng cho mục đích tuyển dụng.\n2. Bạn xác nhận rằng tất cả thông tin cung cấp là chính xác và trung thực.\n3. Chúng tôi có thể liên hệ với bạn qua email hoặc điện thoại về đơn ứng tuyển này.')
    }
  }
}
</script>

<style scoped>
.form-label {
  font-weight: 500;
}

.badge {
  font-size: 0.8rem;
  padding: 0.4em 0.6em;
}

.form-section {
  margin-bottom: 2rem;
}

.form-section-title {
  color: #495057;
  font-weight: 600;
  margin-bottom: 1rem;
}

.required-field::after,
.form-label span.text-danger {
  content: "*";
  color: #dc3545;
  margin-left: 0.25rem;
}

.form-check-input:checked {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.form-switch .form-check-input {
  width: 2.5em;
  margin-left: -2.8em;
}

.form-switch .form-check-input:focus {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -4 8 8'%3e%3ccircle r='3' fill='rgba%280, 0, 0, 0.25%29'/%3e%3c/svg%3e");
}

.form-switch .form-check-input:checked {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -4 8 8'%3e%3ccircle r='3' fill='%23fff'/%3e%3c/svg%3e");
}
</style>
