<template>
  <div class="dashboard-wrapper">
    <Sidebar :open="sidebarOpen" @toggle="sidebarOpen = !sidebarOpen" />
    <div class="dashboard-content">
      <DashboardHeader 
        page-title="Profile Settings"
        :isDark="isDark" 
        @toggle-theme="isDark = !isDark"
      />
      <main class="main-content">
        <div class="profile-container">
          <!-- Profile header with animations -->
          <div class="profile-header reveal-box" :class="{ 'revealed': isRevealed }">
            <h1 class="profile-title">Profile Settings</h1>
            <p class="profile-subtitle">Manage your account information</p>
          </div>

          <form @submit.prevent="handleSubmit" class="profile-form">
            <!-- Avatar Upload Section -->
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

            <!-- Personal Information -->
            <div class="form-section reveal-box" :class="{ 'revealed': isRevealed }" style="animation-delay: 0.2s">
              <h2 class="section-title">Personal Information</h2>
              
              <div class="form-grid">
                <!-- Added first name and last name fields -->
                <div class="form-group">
                  <label for="firstName" class="form-label">
                    First Name <span class="required">*</span>
                  </label>
                  <input
                    id="firstName"
                    v-model="formData.firstName"
                    type="text"
                    class="form-input"
                    placeholder="Enter first name"
                  />
                  <span v-if="errors.firstName" class="error-message">{{ errors.firstName }}</span>
                </div>

                <div class="form-group">
                  <label for="lastName" class="form-label">
                    Last Name <span class="required">*</span>
                  </label>
                  <input
                    id="lastName"
                    v-model="formData.lastName"
                    type="text"
                    class="form-input"
                    placeholder="Enter last name"
                  />
                  <span v-if="errors.lastName" class="error-message">{{ errors.lastName }}</span>
                </div>

                <div class="form-group">
                  <label for="email" class="form-label">
                    Email <span class="required">*</span>
                  </label>
                  <input
                    id="email"
                    v-model="formData.email"
                    type="email"
                    class="form-input"
                    placeholder="Enter your email"
                  />
                  <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
                </div>

                <div class="form-group">
                  <label for="dateOfBirth" class="form-label">Date of Birth</label>
                  <input
                    id="dateOfBirth"
                    v-model="formData.dateOfBirth"
                    type="date"
                    class="form-input"
                  />
                  <span v-if="errors.dateOfBirth" class="error-message">{{ errors.dateOfBirth }}</span>
                </div>
              </div>
            </div>

            <!-- Added password change section -->
            <div class="form-section reveal-box" :class="{ 'revealed': isRevealed }" style="animation-delay: 0.3s">
              <h2 class="section-title">Change Password</h2>
              <p class="section-description">Leave blank if you don't want to change your password</p>
              
              <div class="form-grid">
                <div class="form-group">
                  <label for="currentPassword" class="form-label">Current Password</label>
                  <input
                    id="currentPassword"
                    v-model="formData.currentPassword"
                    type="password"
                    class="form-input"
                    placeholder="Enter current password"
                    autocomplete="current-password"
                  />
                  <span v-if="errors.currentPassword" class="error-message">{{ errors.currentPassword }}</span>
                </div>

                <div class="form-group">
                  <label for="newPassword" class="form-label">New Password</label>
                  <input
                    id="newPassword"
                    v-model="formData.newPassword"
                    type="password"
                    class="form-input"
                    placeholder="Enter new password"
                    autocomplete="new-password"
                  />
                  <span v-if="errors.newPassword" class="error-message">{{ errors.newPassword }}</span>
                </div>
              </div>
            </div>

            <!-- Form Actions -->
            <div class="form-actions reveal-box" :class="{ 'revealed': isRevealed }" style="animation-delay: 0.4s">
              <button type="button" class="cancel-button" @click="loadUserData">
                Reset
              </button>
              <button type="submit" class="save-button" :disabled="isLoading">
                <span v-if="!isLoading">Save Changes</span>
                <span v-else>Saving...</span>
              </button>
            </div>
          </form>

          <!-- Cropper Modal -->
          <div v-if="showCropper" class="modal-overlay" @click="closeCropper">
            <div class="modal-content" @click.stop>
              <div class="modal-header">
                <h3 class="modal-title">Crop Image</h3>
                <button type="button" class="modal-close" @click="closeCropper">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                </button>
              </div>
              <div class="cropper-container">
                <canvas ref="cropperCanvas" class="cropper-canvas"></canvas>
                <div class="crop-overlay">
                  <div
                    ref="cropBox"
                    class="crop-box"
                    :style="cropBoxStyle"
                    @mousedown="startDrag"
                  >
                    <div class="crop-grid">
                      <div class="grid-line"></div>
                      <div class="grid-line"></div>
                      <div class="grid-line grid-horizontal"></div>
                      <div class="grid-line grid-horizontal"></div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="modal-actions">
                <button type="button" class="modal-button-secondary" @click="closeCropper">
                  Cancel
                </button>
                <button type="button" class="modal-button-primary" @click="applyCrop">
                  Apply Crop
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>

  <!-- Toast Notification -->
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
import { ref, reactive, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import Sidebar from '../components/Sidebar.vue'
import DashboardHeader from '../components/DashboardHeader.vue'

const authStore = useAuthStore()
const sidebarOpen = ref(true)
const isDark = ref(true)

const fileInput = ref<HTMLInputElement | null>(null)
const cropperCanvas = ref<HTMLCanvasElement | null>(null)
const cropBox = ref<HTMLDivElement | null>(null)

const isDragging = ref(false)
const showCropper = ref(false)
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

// Cropper state
const cropState = reactive({
  image: null as HTMLImageElement | null,
  x: 50,
  y: 50,
  size: 200,
  dragging: false,
  startX: 0,
  startY: 0
})

const cropBoxStyle = computed(() => ({
  left: `${cropState.x}px`,
  top: `${cropState.y}px`,
  width: `${cropState.size}px`,
  height: `${cropState.size}px`
}))

const openFileDialog = () => {
  fileInput.value?.click()
}

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    processFile(target.files[0])
  }
}

const handleDragEnter = (e: DragEvent) => {
  e.preventDefault()
  e.stopPropagation()
  isDragging.value = true
}

const handleDragLeave = (e: DragEvent) => {
  e.preventDefault()
  e.stopPropagation()
  isDragging.value = false
}

const handleDragOver = (e: DragEvent) => {
  e.preventDefault()
  e.stopPropagation()
}

const handleDrop = (e: DragEvent) => {
  e.preventDefault()
  e.stopPropagation()
  isDragging.value = false

  if (e.dataTransfer?.files && e.dataTransfer.files[0]) {
    processFile(e.dataTransfer.files[0])
  }
}

const processFile = (file: File) => {
  errors.image = ''

  // Validate file type
  if (!file.type.startsWith('image/')) {
    errors.image = 'Please select an image file'
    return
  }

  // Validate file size (5MB)
  if (file.size > 5 * 1024 * 1024) {
    errors.image = 'File size must be less than 5MB'
    return
  }

  selectedFile.value = file
  loadImageForCropping(file)
}

const loadImageForCropping = (file: File) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    const img = new Image()
    img.onload = () => {
      cropState.image = img
      showCropper.value = true
      drawCropper()
    }
    img.src = e.target?.result as string
  }
  reader.readAsDataURL(file)
}

const drawCropper = () => {
  if (!cropperCanvas.value || !cropState.image) return

  const canvas = cropperCanvas.value
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  const maxWidth = 600
  const maxHeight = 400
  const scale = Math.min(maxWidth / cropState.image.width, maxHeight / cropState.image.height, 1)

  canvas.width = cropState.image.width * scale
  canvas.height = cropState.image.height * scale

  ctx.drawImage(cropState.image, 0, 0, canvas.width, canvas.height)

  // Initialize crop box in center
  cropState.size = Math.min(canvas.width, canvas.height) * 0.5
  cropState.x = (canvas.width - cropState.size) / 2
  cropState.y = (canvas.height - cropState.size) / 2
}

const startDrag = (e: MouseEvent) => {
  cropState.dragging = true
  cropState.startX = e.clientX - cropState.x
  cropState.startY = e.clientY - cropState.y

  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
}

const onDrag = (e: MouseEvent) => {
  if (!cropState.dragging || !cropperCanvas.value) return

  const canvas = cropperCanvas.value
  const newX = e.clientX - cropState.startX
  const newY = e.clientY - cropState.startY

  cropState.x = Math.max(0, Math.min(newX, canvas.width - cropState.size))
  cropState.y = Math.max(0, Math.min(newY, canvas.height - cropState.size))
}

const stopDrag = () => {
  cropState.dragging = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
}

const applyCrop = () => {
  if (!cropperCanvas.value || !cropState.image) return

  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  canvas.width = 200
  canvas.height = 200

  const scale = cropState.image.width / cropperCanvas.value.width

  ctx.drawImage(
    cropState.image,
    cropState.x * scale,
    cropState.y * scale,
    cropState.size * scale,
    cropState.size * scale,
    0,
    0,
    200,
    200
  )

  canvas.toBlob((blob) => {
    if (blob) {
      croppedBlob.value = blob
      previewUrl.value = URL.createObjectURL(blob)
      closeCropper()
    }
  }, 'image/jpeg', 0.9)
}

const closeCropper = () => {
  showCropper.value = false
  cropState.image = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const removeImage = () => {
  previewUrl.value = ''
  selectedFile.value = null
  croppedBlob.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const validateForm = (): boolean => {
  let isValid = true

  errors.firstName = ''
  errors.lastName = ''
  errors.email = ''
  errors.dateOfBirth = ''
  errors.currentPassword = ''
  errors.newPassword = ''

  if (!formData.firstName.trim()) {
    errors.firstName = 'First name is required'
    isValid = false
  }

  if (!formData.lastName.trim()) {
    errors.lastName = 'Last name is required'
    isValid = false
  }

  const emailRegex = /\S+@\S+\.\S+/
  if (!emailRegex.test(formData.email)) {
    errors.email = 'Invalid email address'
    isValid = false
  }

  if (formData.dateOfBirth) {
    const date = new Date(formData.dateOfBirth)
    if (date > new Date()) {
      errors.dateOfBirth = 'Date cannot be in the future'
      isValid = false
    }
  }

  if ((formData.currentPassword || formData.newPassword) && (!formData.currentPassword || !formData.newPassword)) {
    if (!formData.currentPassword) {
      errors.currentPassword = 'Current password required to change password'
    }
    if (!formData.newPassword) {
      errors.newPassword = 'New password required'
    }
    isValid = false
  }

  if (formData.newPassword && formData.newPassword.length < 6) {
    errors.newPassword = 'Password must be at least 6 characters'
    isValid = false
  }

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
    if (formData.dateOfBirth) {
      formDataToSend.append('date_of_birth', formData.dateOfBirth)
    }
    if (formData.currentPassword) {
      formDataToSend.append('current_password', formData.currentPassword)
    }
    if (formData.newPassword) {
      formDataToSend.append('new_password', formData.newPassword)
    }
    if (croppedBlob.value) {
      formDataToSend.append('profile_image', croppedBlob.value, 'profile.jpg')
    }

    const response = await fetch('http://localhost:8000/api/profile/update/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken || ''
      },
      credentials: 'include',
      body: formDataToSend
    })

    if (response.ok) {
      await authStore.checkAuth()
      showToast('Profile updated successfully', 'success')
      formData.currentPassword = ''
      formData.newPassword = ''
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
    if (authStore.user.profile_image) {
      previewUrl.value = authStore.user.profile_image
    }
  }
}

function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop()?.split(';').shift() || null
  return null
}

async function fetchCsrfToken() {
  try {
    await fetch('http://localhost:8000/api/auth/csrf/', {
      credentials: 'include'
    })
  } catch (err) {
    console.error('Failed to fetch CSRF token:', err)
  }
}

function showToast(message: string, type: 'success' | 'error' = 'success') {
  toast.message = message
  toast.type = type
  toast.show = true
  
  setTimeout(() => {
    toast.show = false
  }, 3000)
}

onMounted(async () => {
  await loadUserData()
  setTimeout(() => {
    isRevealed.value = true
  }, 50)
})
</script>

<style scoped>
/* Remove duplicate dashboard-wrapper styles, they're inherited */
.dashboard-wrapper {
  display: flex;
  min-height: 100vh;
  width: 100%;
  background: #0a0e1a;
}

.dashboard-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: auto;
}

.main-content {
  flex: 1;
  padding: 2rem;
}

.profile-container {
  max-width: 800px;
  margin: 0 auto;
}

.profile-header {
  margin-bottom: 2rem;
}

.profile-title {
  font-size: 2rem;
  font-weight: 700;
  color: #f3f4f6;
  margin-bottom: 0.5rem;
}

.profile-subtitle {
  font-size: 1rem;
  color: #9ca3af;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-section {
  background: #1f2937;
  border: 1px solid #374151;
  border-radius: 0.75rem;
  padding: 1.5rem;
}

.section-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #f3f4f6;
  margin-bottom: 1.5rem;
}

.avatar-upload-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.avatar-preview {
  position: relative;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 2px dashed #374151;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
}

.avatar-preview:hover {
  border-color: #60a5fa;
  box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.15);
}

.avatar-preview.dragging {
  border-color: #60a5fa;
  background: rgba(96, 165, 250, 0.1);
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
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #374151;
  color: #9ca3af;
}

.remove-button {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #1f2937;
  border: 1px solid #374151;
  border-radius: 50%;
  color: #f3f4f6;
  cursor: pointer;
  transition: all 0.2s;
}

.remove-button:hover {
  background: #ef4444;
  border-color: #ef4444;
}

.avatar-info {
  text-align: center;
}

.avatar-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #f3f4f6;
  margin-bottom: 0.25rem;
}

.avatar-hint {
  font-size: 0.75rem;
  color: #6b7280;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #f3f4f6;
}

.required {
  color: #ef4444;
}

.form-input {
  width: 100%;
  height: 44px;
  padding: 0.75rem 1rem;
  font-size: 0.9375rem;
  color: #f3f4f6;
  background: #0f1523;
  border: 1px solid #374151;
  border-radius: 0.5rem;
  transition: all 0.3s;
  outline: none;
}

.form-input::placeholder {
  color: #6b7280;
}

.form-input:hover {
  border-color: #60a5fa;
  box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.15);
}

.form-input:focus {
  border-color: #60a5fa;
  box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.25);
}

.error-message {
  font-size: 0.75rem;
  color: #ef4444;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.cancel-button,
.save-button {
  height: 44px;
  padding: 0 1.5rem;
  font-size: 0.9375rem;
  font-weight: 500;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
  outline: none;
}

.cancel-button {
  background: transparent;
  border: 1px solid #374151;
  color: #f3f4f6;
}

.cancel-button:hover {
  background: rgba(255, 255, 255, 0.05);
}

.save-button {
  background: #3b82f6;
  border: none;
  color: white;
}

.save-button:hover {
  background: #2563eb;
}

.save-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: #1f2937;
  border: 1px solid #374151;
  border-radius: 0.75rem;
  width: 90%;
  max-width: 700px;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid #374151;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #f3f4f6;
}

.modal-close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: transparent;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  border-radius: 0.375rem;
  transition: all 0.2s;
}

.modal-close:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #f3f4f6;
}

.cropper-container {
  position: relative;
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #0f1523;
  min-height: 400px;
}

.cropper-canvas {
  max-width: 100%;
  max-height: 400px;
  display: block;
}

.crop-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.crop-box {
  position: absolute;
  border: 2px solid #60a5fa;
  box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.5);
  cursor: move;
  pointer-events: all;
}

.crop-grid {
  position: absolute;
  inset: 0;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(3, 1fr);
}

.grid-line {
  border-right: 1px solid rgba(255, 255, 255, 0.3);
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.grid-line:nth-child(3),
.grid-line:nth-child(6),
.grid-line:nth-child(9) {
  border-right: none;
}

.grid-line.grid-horizontal:nth-child(7),
.grid-line.grid-horizontal:nth-child(8),
.grid-line.grid-horizontal:nth-child(9) {
  border-bottom: none;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #374151;
}

.modal-button-secondary,
.modal-button-primary {
  height: 40px;
  padding: 0 1.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
  outline: none;
}

.modal-button-secondary {
  background: transparent;
  border: 1px solid #374151;
  color: #f3f4f6;
}

.modal-button-secondary:hover {
  background: rgba(255, 255, 255, 0.05);
}

.modal-button-primary {
  background: #3b82f6;
  border: none;
  color: white;
}

.modal-button-primary:hover {
  background: #2563eb;
}

/* Toast Styles */
.toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  background: #1f2937;
  border: 1px solid #374151;
  border-radius: 0.5rem;
  color: #f3f4f6;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
  z-index: 1001;
}

.toast-success {
  border-left: 3px solid #10b981;
}

.toast-error {
  border-left: 3px solid #ef4444;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.toast-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

/* Added reveal animation styles like login page */
.reveal-box {
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.reveal-box.revealed {
  opacity: 1;
  transform: translateY(0);
}

.section-description {
  font-size: 0.875rem;
  color: #9ca3af;
  margin-bottom: 1.5rem;
}
</style>
