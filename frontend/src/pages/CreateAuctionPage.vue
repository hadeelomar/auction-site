<template>
  <div class="page-wrapper">
    <Navbar />
    
    <main class="main-content">
      <div class="page-container">
        <div class="page-header">
          <h1 class="page-title">Create Auction</h1>
          <p class="page-description">List a new item for auction</p>
        </div>

        <form class="auction-form" @submit.prevent="handleSubmit">
          <!-- item details -->
          <div class="form-section">
            <h2 class="section-title">Item Details</h2>
            
            <div class="form-group">
              <label for="title" class="form-label">Title <span class="required">*</span></label>
              <input id="title" v-model="formData.title" type="text" class="form-input" placeholder="Enter item title" />
            </div>

            <div class="form-group">
              <label for="description" class="form-label">Description <span class="required">*</span></label>
              <textarea id="description" v-model="formData.description" class="form-textarea" rows="4" placeholder="Describe your item in detail"></textarea>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="startingPrice" class="form-label">Starting Price <span class="required">*</span></label>
                <div class="input-with-prefix">
                  <span class="input-prefix">£</span>
                  <input id="startingPrice" v-model="formData.startingPrice" type="number" class="form-input with-prefix" placeholder="0.00" />
                </div>
              </div>

              <div class="form-group">
                <label for="endDate" class="form-label">End Date & Time <span class="required">*</span></label>
                <input id="endDate" v-model="formData.endDate" type="datetime-local" class="form-input" />
              </div>
            </div>
          </div>

          <!-- image upload -->
          <div class="form-section">
            <h2 class="section-title">Item Image</h2>
            <div class="image-upload-area">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect width="18" height="18" x="3" y="3" rx="2" ry="2"/>
                <circle cx="9" cy="9" r="2"/>
                <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
              </svg>
              <p class="upload-text">Drag and drop an image here, or click to browse</p>
              <p class="upload-hint">PNG, JPG up to 10MB</p>
            </div>
          </div>

          <!-- form actions -->
          <div class="form-actions">
            <router-link to="/" class="cancel-button">Cancel</router-link>
            <button type="submit" class="submit-button">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="m14.5 12.5-8 8a2.119 2.119 0 1 1-3-3l8-8"/>
                <path d="m16 16 6-6"/>
                <path d="m8 8 6-6"/>
                <path d="m9 7 8 8"/>
                <path d="m21 11-8-8"/>
              </svg>
              Create Auction
            </button>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import Navbar from '../components/Navbar.vue'

const formData = reactive({
  title: '',
  description: '',
  startingPrice: '',
  endDate: ''
})

const handleSubmit = () => {
  console.log('Form submitted:', formData)
}
</script>

<style scoped>
.page-wrapper {
  min-height: 100vh;
  background: #f9fafb;
}

.main-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.page-container {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.page-header {
  margin-bottom: 2rem;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 0.5rem;
}

.page-description {
  color: #6b7280;
}

.auction-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-section {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 1.5rem;
}

.section-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
  margin-bottom: 1.25rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}

.form-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.required {
  color: #ef4444;
}

.form-input, .form-textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 0.9375rem;
  color: #111827;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  outline: none;
  transition: all 0.2s;
}

.form-input:focus, .form-textarea:focus {
  border-color: #ea580c;
  box-shadow: 0 0 0 3px rgba(234, 88, 12, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.input-with-prefix {
  position: relative;
  display: flex;
  align-items: center;
}

.input-prefix {
  position: absolute;
  left: 1rem;
  color: #6b7280;
  font-weight: 500;
}

.form-input.with-prefix {
  padding-left: 2rem;
}

.image-upload-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  border: 2px dashed #d1d5db;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  color: #9ca3af;
}

.image-upload-area:hover {
  border-color: #ea580c;
  background: #fff7ed;
}

.upload-text {
  margin-top: 1rem;
  font-weight: 500;
  color: #374151;
}

.upload-hint {
  margin-top: 0.25rem;
  font-size: 0.8125rem;
  color: #9ca3af;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.cancel-button {
  padding: 0.75rem 1.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s;
}

.cancel-button:hover {
  background: #f3f4f6;
}

.submit-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #ffffff;
  background: linear-gradient(135deg, #ea580c, #f97316);
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.submit-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(234, 88, 12, 0.3);
}
</style>
