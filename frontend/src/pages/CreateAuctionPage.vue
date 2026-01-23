<template>
  <div class="page-wrapper">
    <Navbar />
    
    <main class="main-content">
      <div class="page-container">
        <div class="page-header">
          <h1 class="page-title">{{ isEditMode ? t('createAuction.editAuction') : t('createAuction.createAuction') }}</h1>
          <p class="page-description">{{ isEditMode ? t('createAuction.updateDescription') : t('createAuction.createDescription') }}</p>
        </div>

        <form class="auction-form" @submit.prevent="handleSubmit" v-if="!loading">
          <!-- item details -->
          <div class="form-section">
            <h2 class="section-title">{{ t('createAuction.itemDetails') }}</h2>
            
            <div class="form-group">
              <label for="title" class="form-label">{{ t('createAuction.title') }} <span class="required">*</span></label>
              <input 
                id="title" 
                v-model="formData.title" 
                type="text" 
                class="form-input" 
                :class="{ error: errors.title }"
                :placeholder="t('createAuction.titlePlaceholder')" 
              />
              <span v-if="errors.title" class="error-message">{{ errors.title }}</span>
            </div>

            <div class="form-group">
              <label for="description" class="form-label">{{ t('createAuction.description') }} <span class="required">*</span></label>
              <textarea 
                id="description" 
                v-model="formData.description" 
                class="form-textarea"
                :class="{ error: errors.description }"
                rows="4" 
                :placeholder="t('createAuction.descriptionPlaceholder')"
              ></textarea>
              <span v-if="errors.description" class="error-message">{{ errors.description }}</span>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="startingPrice" class="form-label">{{ t('createAuction.startingPrice') }} <span class="required">*</span></label>
                <div class="input-with-prefix">
                  <span class="input-prefix">{{ i18nStore.currentCurrencySymbol }}</span>
                  <input 
                    id="startingPrice" 
                    v-model="formData.startingPrice" 
                    type="number" 
                    class="form-input with-prefix"
                    :class="{ error: errors.startingPrice }"
                    placeholder="0.00" 
                  />
                </div>
                <span v-if="errors.startingPrice" class="error-message">{{ errors.startingPrice }}</span>
              </div>

              <div class="form-group">
                <label for="endDate" class="form-label">{{ t('createAuction.endDate') }} <span class="required">*</span></label>
                <input 
                  id="endDate" 
                  v-model="formData.endDate" 
                  type="datetime-local" 
                  class="form-input"
                  :class="{ error: errors.endDate }"
                />
                <span v-if="errors.endDate" class="error-message">{{ errors.endDate }}</span>
              </div>

              <div class="form-group">
                <label for="category" class="form-label">{{ t('createAuction.category') }}</label>
                <select 
                  id="category" 
                  v-model="formData.category" 
                  class="form-input"
                >
                  <option value="electronics">{{ t('categories.electronics') }}</option>
                  <option value="fashion">{{ t('categories.fashion') }}</option>
                  <option value="home">{{ t('categories.home') }}</option>
                  <option value="sports">{{ t('categories.sports') }}</option>
                  <option value="art">{{ t('categories.art') }}</option>
                  <option value="vehicles">{{ t('categories.vehicles') }}</option>
                </select>
              </div>
            </div>
          </div>

          <!-- image upload -->
          <div class="form-section">
            <h2 class="section-title">{{ t('createAuction.itemImage') }}</h2>
            <div class="image-upload-area" @click="fileInput?.click()">
              <input 
                ref="fileInput"
                type="file" 
                accept="image/*" 
                @change="handleFileSelect"
                style="display: none"
              />
              
              <div v-if="imagePreview" class="image-preview">
                <img :src="imagePreview" alt="Preview" />
                <button type="button" class="remove-image" @click.stop="removeImage">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </button>
              </div>
              
              <div v-else class="upload-placeholder">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect width="18" height="18" x="3" y="3" rx="2" ry="2"/>
                  <circle cx="9" cy="9" r="2"/>
                  <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
                </svg>
                <p class="upload-text">{{ t('createAuction.dragDropText') }}</p>
                <p class="upload-hint">{{ t('createAuction.uploadHint') }}</p>
              </div>
            </div>
            <span v-if="errors.image" class="error-message">{{ errors.image }}</span>
          </div>

          <!-- form actions -->
          <div class="form-actions">
            <router-link to="/" class="cancel-button">{{ t('common.cancel') }}</router-link>
            <button type="submit" class="submit-button" :disabled="isSubmitting">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="m14.5 12.5-8 8a2.119 2.119 0 0 1-3-3l8-8"/>
                <path d="m16 16 6-6"/>
                <path d="m8 8 6-6"/>
                <path d="m9 7 8 8"/>
                <path d="m21 11-8-8"/>
              </svg>
              {{ isSubmitting ? (isEditMode ? t('createAuction.updating') : t('createAuction.creating')) : (isEditMode ? t('createAuction.submitUpdate') : t('createAuction.submitCreate')) }}
            </button>
          </div>
          
          <!-- General error message -->
          <div v-if="errors.general" class="general-error">
            {{ errors.general }}
          </div>
        </form>
        
        <!-- Loading state -->
        <div v-if="loading" class="loading-state">
          <p>{{ t('createAuction.loading') }}</p>
        </div>
      </div>
    </main>
    
    <!-- Footer -->
    <footer class="footer">
      <div class="footer-content">
        <p>2026 Bido. {{ t('footer.allRightsReserved') }}</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import Navbar from '../components/Navbar.vue'
import { useI18nStore } from '../stores/i18n'

const { t } = useI18n()
const i18nStore = useI18nStore()
const router = useRouter()
const route = useRoute()

// Check if we're in edit mode
const isEditMode = computed(() => route.name === 'edit-auction')
const auctionId = computed(() => route.params.id as string)

const formData = reactive({
  title: '',
  description: '',
  startingPrice: '',
  endDate: '',
  category: 'electronics'
})

const errors = ref<Record<string, string>>({})
const isSubmitting = ref(false)
const selectedFile = ref<File | null>(null)
const imagePreview = ref<string>('')
const fileInput = ref<HTMLInputElement | null>(null)
const loading = ref(false)

const validateForm = (): boolean => {
  const newErrors: Record<string, string> = {}
  
  if (!formData.title.trim()) {
    newErrors.title = t('createAuction.titleRequired')
  } else if (formData.title.length < 3) {
    newErrors.title = t('createAuction.titleMinLength')
  }
  
  if (!formData.description.trim()) {
    newErrors.description = t('createAuction.descriptionRequired')
  } else if (formData.description.length < 10) {
    newErrors.description = t('createAuction.descriptionMinLength')
  }
  
  if (!formData.startingPrice) {
    newErrors.startingPrice = t('createAuction.startingPriceRequired')
  } else if (parseFloat(formData.startingPrice) <= 0) {
    newErrors.startingPrice = t('createAuction.startingPricePositive')
  }
  
  if (!formData.endDate) {
    newErrors.endDate = t('createAuction.endDateRequired')
  } else {
    const endDate = new Date(formData.endDate)
    const now = new Date()
    if (endDate <= now) {
      newErrors.endDate = t('createAuction.endDateFuture')
    }
  }
  
  errors.value = newErrors
  return Object.keys(newErrors).length === 0
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (file) {
    // Validate file type
    if (!file.type.startsWith('image/')) {
      errors.value.image = t('createAuction.selectImageFile')
      return
    }
    
    // Validate file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
      errors.value.image = t('createAuction.imageSizeError')
      return
    }
    
    selectedFile.value = file
    errors.value.image = ''
    
    // Create preview
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target?.result as string
    }
    reader.readAsDataURL(file)
  }
}

const removeImage = () => {
  selectedFile.value = null
  imagePreview.value = ''
  errors.value.image = ''
  // Clear the file input
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }
  
  isSubmitting.value = true
  
  try {
    let response: Response
    let data: any
    
    if (isEditMode.value) {
      // Edit mode - send JSON data
      const jsonData = {
        title: formData.title,
        description: formData.description,
        starting_price: formData.startingPrice,
        end_date: new Date(formData.endDate).toISOString(),
        category: formData.category
      }
      
      response = await fetch(`/api/auctions/${auctionId.value}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(jsonData),
        credentials: 'same-origin'
      })
      
      data = await response.json()
    } else {
      // Create mode - send FormData (for file upload)
      const submitData = new FormData()
      submitData.append('title', formData.title)
      submitData.append('description', formData.description)
      submitData.append('starting_price', formData.startingPrice)
      submitData.append('end_date', new Date(formData.endDate).toISOString())
      submitData.append('category', formData.category)
      
      if (selectedFile.value) {
        submitData.append('image', selectedFile.value)
      }
      
      response = await fetch('http://localhost:8001/api/auctions/create/', {
        method: 'POST',
        body: submitData,
        credentials: 'same-origin'
      })
      
      data = await response.json()
    }
    
    if (!response.ok) {
      if (response.status === 401) {
        errors.value.general = `You must be logged in to ${isEditMode.value ? 'edit' : 'create'} an auction. Please <a href="http://localhost:8001/login/" class="error-link">sign in</a> first.`
      } else if (data.error) {
        errors.value.general = data.error
      } else {
        errors.value.general = `Failed to ${isEditMode.value ? 'update' : 'create'} auction`
      }
      return
    }
    
    // Success - redirect based on mode
    if (isEditMode.value) {
      router.push('/auctions')
    } else {
      router.push(`/auction/${data.auction.id}`)
    }
    
  } catch (err) {
    errors.value.general = 'Network error. Please try again.'
    console.error(`${isEditMode.value ? 'Update' : 'Create'} auction error:`, err)
  } finally {
    isSubmitting.value = false
  }
}

// Load existing auction data if in edit mode
const loadAuctionData = async () => {
  if (!isEditMode.value) return
  
  try {
    loading.value = true
    const response = await fetch(`/api/auctions/${auctionId.value}/`)
    if (!response.ok) {
      throw new Error('Failed to fetch auction details')
    }
    
    const data = await response.json()
    const auction = data.item
    
    // Populate form with existing data
    formData.title = auction.title
    formData.description = auction.description
    formData.startingPrice = auction.starting_price.toString()
    formData.endDate = new Date(auction.ends_at).toISOString().slice(0, 16)
    formData.category = auction.category || 'electronics'
    imagePreview.value = auction.image || ''
    
  } catch (err) {
    errors.value.general = 'Failed to load auction data'
    console.error('Error loading auction:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadAuctionData()
})
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

.submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

/* Error styles */
.error-message {
  display: block;
  color: #dc2626;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.form-input.error,
.form-textarea.error {
  border-color: #dc2626;
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.general-error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
  text-align: center;
}

/* Error link styles */
.error-link {
  color: #ea580c;
  text-decoration: underline;
  font-weight: 500;
}

.error-link:hover {
  color: #c2410c;
}

/* Image preview styles */
.image-preview {
  position: relative;
  width: 100%;
  height: 200px;
  border-radius: 8px;
  overflow: hidden;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-image {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s;
}

.remove-image:hover {
  background: rgba(0, 0, 0, 0.9);
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
}

.footer {
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  padding: 2rem 0;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  text-align: center;
}

.footer-content p {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}
</style>
