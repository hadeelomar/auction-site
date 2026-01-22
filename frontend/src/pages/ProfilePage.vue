<template>
  <div class="page-wrapper">
    <Navbar />
    
    <main class="main-content">
      <div class="profile-container">
        <!-- profile header -->
        <div class="profile-header reveal-box" :class="{ 'revealed': isRevealed }">
          <h1 class="profile-title">Profile Settings</h1>
          <p class="profile-subtitle">Manage your account information</p>
        </div>

        <form @submit.prevent="handleSubmit" class="profile-form" novalidate>
          <!-- avatar upload -->
          <div class="form-section reveal-box" :class="{ 'revealed': isRevealed }" style="animation-delay: 0.1s">
            <h2 class="section-title">Profile Picture</h2>
            <div class="avatar-upload-container">
              <div
                :class="['avatar-preview', { 'dragging': isDragging }]"
                @click="openFileDialog"
                @dragenter="handleDragEnter"
                @dragleave="handleDragLeave"
                @dragover="handleDragOver"
                @drop="handleDrop"
              >
                <input
                  ref="fileInput"
                  type="file"
                  accept="image/*"
                  @change="handleFileChange"
                  class="file-input"
                />
                <img v-if="previewUrl" :src="previewUrl" alt="Profile" class="avatar-image" />
                <div v-else class="avatar-placeholder">
                  <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                </div>
                <button
                  v-if="previewUrl"
                  type="button"
                  class="remove-button"
                  @click.stop="removeImage"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                </button>
              </div>
              <div class="avatar-info">
                <p class="avatar-label">{{ previewUrl ? 'Avatar uploaded' : 'Upload avatar' }}</p>
                <p class="avatar-hint">PNG, JPG up to 5MB</p>
              </div>
              <span v-if="errors.image" class="error-message">{{ errors.image }}</span>
            </div>
          </div>

          <!-- personal info -->
          <div class="form-section reveal-box" :class="{ 'revealed': isRevealed }" style="animation-delay: 0.2s">
            <h2 class="section-title">Personal Information</h2>
            
            <div class="form-grid">
              <div class="form-group">
                <label for="firstName" class="form-label">First Name <span class="required">*</span></label>
                <input id="firstName" v-model="formData.firstName" type="text" class="form-input" placeholder="Enter first name" />
                <span v-if="errors.firstName" class="error-message">{{ errors.firstName }}</span>
              </div>

              <div class="form-group">
                <label for="lastName" class="form-label">Last Name <span class="required">*</span></label>
                <input id="lastName" v-model="formData.lastName" type="text" class="form-input" placeholder="Enter last name" />
                <span v-if="errors.lastName" class="error-message">{{ errors.lastName }}</span>
              </div>

              <div class="form-group">
                <label for="email" class="form-label">Email <span class="required">*</span></label>
                <input id="email" v-model="formData.email" type="email" class="form-input" placeholder="Enter your email" />
                <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
              </div>

              <div class="form-group">
                <label for="dateOfBirth" class="form-label">Date of Birth</label>
                <input id="dateOfBirth" v-model="formData.dateOfBirth" type="date" class="form-input" />
                <span v-if="errors.dateOfBirth" class="error-message">{{ errors.dateOfBirth }}</span>
              </div>
            </div>
          </div>

          <!-- password change -->
          <div class="form-section reveal-box" :class="{ 'revealed': isRevealed }" style="animation-delay: 0.3s">
            <h2 class="section-title">Change Password</h2>
            <p class="section-description">Leave blank if you don't want to change your password</p>
            
            <div class="form-grid">
              <div class="form-group">
                <label for="currentPassword" class="form-label">Current Password</label>
                <input id="currentPassword" v-model="formData.currentPassword" type="password" class="form-input" placeholder="Enter current password" />
                <span v-if="errors.currentPassword" class="error-message">{{ errors.currentPassword }}</span>
              </div>

              <div class="form-group">
                <label for="newPassword" class="form-label">New Password</label>
                <input id="newPassword" v-model="formData.newPassword" type="password" class="form-input" placeholder="Enter new password" />
                <span v-if="errors.newPassword" class="error-message">{{ errors.newPassword }}</span>
              </div>
            </div>
          </div>

          <!-- form actions -->
          <div class="form-actions reveal-box" :class="{ 'revealed': isRevealed }" style="animation-delay: 0.4s">
            <button type="button" class="cancel-button" @click="loadUserData">Reset</button>
            <button type="submit" class="save-button" :disabled="isLoading">
              <span v-if="!isLoading">Save Changes</span>
              <span v-else>Saving...</span>
            </button>
          </div>
        </form>
      </div>
    </main>
  </div>

  <!-- toast -->
  <Transition name="toast">
    <div v-if="toast.show" :class="['toast', `toast-${toast.type}`]">
      <svg v-if="toast.type === 'success'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="20 6 9 17 4 12"/>
      </svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
      <span>{{ toast.message }}</span>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import Navbar from '../components/Navbar.vue'

const authStore = useAuthStore()

const fileInput = ref<HTMLInputElement | null>(null)

const isDragging = ref(false)
const isLoading = ref(false)
const selectedFile = ref<File | null>(null)
const previewUrl = ref<string>('')
const croppedBlob = ref<Blob | null>(null)
const isRevealed = ref(false)

const formData = reactive({
  firstName: '',
  lastName: '',
  email: '',
  dateOfBirth: '',
  currentPassword: '',
  newPassword: ''
})

const errors = reactive({
  firstName: '',
  lastName: '',
  email: '',
  dateOfBirth: '',
  image: '',
  currentPassword: '',
  newPassword: ''
})

const toast = reactive({
  show: false,
  message: '',
  type: 'success' as 'success' | 'error'
})

const openFileDialog = () => fileInput.value?.click()

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) processFile(target.files[0])
}

const handleDragEnter = (e: DragEvent) => { e.preventDefault(); e.stopPropagation(); isDragging.value = true }
const handleDragLeave = (e: DragEvent) => { e.preventDefault(); e.stopPropagation(); isDragging.value = false }
const handleDragOver = (e: DragEvent) => { e.preventDefault(); e.stopPropagation() }

const handleDrop = (e: DragEvent) => {
  e.preventDefault(); e.stopPropagation(); isDragging.value = false
  if (e.dataTransfer?.files && e.dataTransfer.files[0]) processFile(e.dataTransfer.files[0])
}

const processFile = (file: File) => {
  errors.image = ''
  if (!file.type.startsWith('image/')) { errors.image = 'Please select an image file'; return }
  if (file.size > 5 * 1024 * 1024) { errors.image = 'File size must be less than 5MB'; return }
  selectedFile.value = file
  autoCropImage(file)
}

const autoCropImage = (file: File) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    const img = new Image()
    img.onload = () => {
      const canvas = document.createElement('canvas')
      const ctx = canvas.getContext('2d')
      if (!ctx) return
      
      const size = Math.min(img.width, img.height)
      const x = (img.width - size) / 2
      const y = (img.height - size) / 2
      
      canvas.width = 200
      canvas.height = 200
      ctx.drawImage(img, x, y, size, size, 0, 0, 200, 200)
      
      canvas.toBlob((blob) => {
        if (blob) {
          croppedBlob.value = blob
          previewUrl.value = URL.createObjectURL(blob)
        }
      }, 'image/jpeg', 0.9)
    }
    img.src = e.target?.result as string
  }
  reader.readAsDataURL(file)
}

const removeImage = () => { 
  previewUrl.value = ''
  selectedFile.value = null
  croppedBlob.value = null
  if (fileInput.value) fileInput.value.value = '' 
}

const validateForm = (): boolean => {
  let isValid = true
  errors.firstName = ''; errors.lastName = ''; errors.email = ''; errors.dateOfBirth = ''; errors.currentPassword = ''; errors.newPassword = ''
  if (!formData.firstName.trim()) { errors.firstName = 'First name is required'; isValid = false }
  if (!formData.lastName.trim()) { errors.lastName = 'Last name is required'; isValid = false }
  if (!/\S+@\S+\.\S+/.test(formData.email)) { errors.email = 'Invalid email address'; isValid = false }
  if (formData.dateOfBirth && new Date(formData.dateOfBirth) > new Date()) { errors.dateOfBirth = 'Date cannot be in the future'; isValid = false }
  if ((formData.currentPassword || formData.newPassword) && (!formData.currentPassword || !formData.newPassword)) {
    if (!formData.currentPassword) errors.currentPassword = 'Current password required'
    if (!formData.newPassword) errors.newPassword = 'New password required'
    isValid = false
  }
  if (formData.newPassword && formData.newPassword.length < 6) { errors.newPassword = 'Password must be at least 6 characters'; isValid = false }
  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) return
  isLoading.value = true
  try {
    await fetchCsrfToken()
    const csrfToken = getCookie('csrftoken')
    const formDataToSend = new FormData()
    formDataToSend.append('first_name', formData.firstName)
    formDataToSend.append('last_name', formData.lastName)
    formDataToSend.append('email', formData.email)
    formDataToSend.append('date_of_birth', formData.dateOfBirth || '')
    if (formData.currentPassword) formDataToSend.append('current_password', formData.currentPassword)
    if (formData.newPassword) formDataToSend.append('new_password', formData.newPassword)
    if (croppedBlob.value) formDataToSend.append('profile_image', croppedBlob.value, 'profile.jpg')

    const response = await fetch('http://localhost:8000/api/profile/update/', {
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken || '' },
      credentials: 'include',
      body: formDataToSend
    })

    if (response.ok) {
      await authStore.checkAuth()
      showToast('Profile updated successfully', 'success')
      formData.currentPassword = ''; formData.newPassword = ''
    } else {
      const error = await response.json()
      showToast(error.error || 'Failed to update profile', 'error')
    }
  } catch (err) {
    showToast('An error occurred while updating profile', 'error')
  } finally {
    isLoading.value = false
  }
}

const loadUserData = async () => {
  await authStore.checkAuth()
  if (authStore.user) {
    formData.firstName = authStore.user.first_name || ''
    formData.lastName = authStore.user.last_name || ''
    formData.email = authStore.user.email || ''
    formData.dateOfBirth = authStore.user.date_of_birth || ''
    if (authStore.user.profile_image) previewUrl.value = authStore.user.profile_image
  }
}

function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop()?.split(';').shift() || null
  return null
}

async function fetchCsrfToken() {
  try { await fetch('http://localhost:8000/api/auth/csrf/', { credentials: 'include' }) } catch (err) { console.error('Failed to fetch CSRF token:', err) }
}

function showToast(message: string, type: 'success' | 'error' = 'success') {
  toast.message = message; toast.type = type; toast.show = true
  setTimeout(() => { toast.show = false }, 3000)
}

onMounted(async () => {
  await loadUserData()
  setTimeout(() => { isRevealed.value = true }, 50)
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

.profile-container {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.profile-header {
  margin-bottom: 2rem;
}

.profile-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 0.5rem;
}

.profile-subtitle {
  color: #6b7280;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
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
  margin-bottom: 1rem;
}

.section-description {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 1rem;
}

.avatar-upload-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.avatar-preview {
  position: relative;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 2px dashed #d1d5db;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  overflow: hidden;
}

.avatar-preview:hover, .avatar-preview.dragging {
  border-color: #ea580c;
  background: #fff7ed;
}

.file-input {
  display: none;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  color: #9ca3af;
}

.remove-button {
  position: absolute;
  top: 0;
  right: 0;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #ef4444;
  border: none;
  color: #ffffff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.avatar-label {
  font-weight: 500;
  color: #374151;
}

.avatar-hint {
  font-size: 0.8125rem;
  color: #9ca3af;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

@media (max-width: 640px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.required {
  color: #ef4444;
}

.form-input {
  width: 100%;
  height: 44px;
  padding: 0 1rem;
  font-size: 0.9375rem;
  color: #111827;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  outline: none;
  transition: all 0.2s;
}

.form-input:focus {
  border-color: #ea580c;
  box-shadow: 0 0 0 3px rgba(234, 88, 12, 0.1);
}

.error-message {
  font-size: 0.75rem;
  color: #dc2626;
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
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-button:hover {
  background: #f3f4f6;
}

.save-button {
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

.save-button:hover {
  box-shadow: 0 4px 12px rgba(234, 88, 12, 0.3);
}

.save-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.reveal-box {
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.reveal-box.revealed {
  opacity: 1;
  transform: translateY(0);
}

.toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  font-size: 0.9375rem;
  font-weight: 500;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  z-index: 1000;
}

.toast-success {
  background: #d1fae5;
  color: #065f46;
}

.toast-error {
  background: #fee2e2;
  color: #991b1b;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(1rem);
}
</style>
