<template>
  <div class="auth-container">
    <!-- left side -->
    <div class="decorative-side">
      <div class="orbit-container">
        <h1 class="orbit-center-text">Auction Site</h1>

        <svg class="orbit-path orbit-path-1" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="16.5" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.2" />
        </svg>
        <div class="orbit orbit-1">
          <!-- gavel icon -->
          <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="orbit-icon">
            <path d="m14.5 12.5-8 8a2.119 2.119 0 1 1-3-3l8-8"/>
            <path d="m16 16 6-6"/>
            <path d="m8 8 6-6"/>
            <path d="m9 7 8 8"/>
            <path d="m21 11-8-8"/>
          </svg>
        </div>
        <div class="orbit orbit-1-2">
          <!-- price tag icon -->
          <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="orbit-icon">
            <path d="M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z"/>
            <circle cx="7.5" cy="7.5" r=".5" fill="currentColor"/>
          </svg>
        </div>

        <svg class="orbit-path orbit-path-2" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="35" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.2" />
        </svg>
        <div class="orbit orbit-2">
          <!-- trophy icon -->
          <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="orbit-icon-large">
            <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/>
            <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/>
            <path d="M4 22h16"/>
            <path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/>
            <path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/>
            <path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>
          </svg>
        </div>

        <svg class="orbit-path orbit-path-3" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="35" fill="none" stroke="rgba(255, 255, 255, 0.1)" stroke-width="0.2" />
        </svg>
        <div class="orbit orbit-3">
          <!-- dollar sign icon -->
          <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="orbit-icon-large">
            <line x1="12" x2="12" y1="2" y2="22"/>
            <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
          </svg>
        </div>
        <div class="orbit orbit-3-2">
          <!-- clock icon -->
          <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="orbit-icon-large">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- right side - form -->
    <div class="form-side">
      <div class="form-container">
        <div class="reveal-box">
          <h2 class="form-title">{{ isSignup ? 'Sign up' : 'Welcome back' }}</h2>
        </div>
        
        <div class="reveal-box reveal-delay-1">
          <p class="form-subtitle">
            {{ isSignup ? 'Enter your information to create an account' : 'Sign in to your account' }}
          </p>
        </div>

        <!-- form -->
        <form @submit.prevent="handleSubmit" class="auth-form">
          <!-- full name field for signup -->
          <div v-if="isSignup" class="form-group">
            <div class="reveal-box reveal-delay-2">
              <label for="fullName" class="form-label">
                Full Name <span class="required">*</span>
              </label>
            </div>
            <div class="reveal-box reveal-delay-2 full-width">
              <div class="input-wrapper">
                <input
                  id="fullName"
                  v-model="formData.fullName"
                  type="text"
                  class="form-input"
                  placeholder="Enter your full name"
                />
              </div>
              <div class="error-container">
                <span v-if="errors.fullName" class="error-message">{{ errors.fullName }}</span>
              </div>
            </div>
          </div>

          <!-- email field -->
          <div class="form-group">
            <div class="reveal-box reveal-delay-2">
              <label for="email" class="form-label">
                Email <span class="required">*</span>
              </label>
            </div>
            <div class="reveal-box reveal-delay-2 full-width">
              <div class="input-wrapper">
                <input
                  id="email"
                  v-model="formData.email"
                  type="email"
                  class="form-input"
                  placeholder="Enter your email address"
                />
              </div>
              <div class="error-container">
                <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
              </div>
            </div>
          </div>

          <!-- password field -->
          <div class="form-group">
            <div class="reveal-box reveal-delay-3">
              <label for="password" class="form-label">
                Password <span class="required">*</span>
              </label>
            </div>
            <div class="reveal-box reveal-delay-3 full-width">
              <div class="input-wrapper password-wrapper">
                <input
                  id="password"
                  v-model="formData.password"
                  :type="showPassword ? 'text' : 'password'"
                  class="form-input"
                  placeholder="Enter your password"
                />
                <button
                  type="button"
                  class="password-toggle"
                  @click="showPassword = !showPassword"
                >
                  <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/>
                    <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/>
                    <path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/>
                    <line x1="2" x2="22" y1="2" y2="22"/>
                  </svg>
                </button>
              </div>
              <div class="error-container">
                <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
              </div>
            </div>
          </div>

          <!-- password confirmation field for signup -->
          <div v-if="isSignup" class="form-group">
            <div class="reveal-box reveal-delay-4">
              <label for="passwordConfirm" class="form-label">
                Confirm Password <span class="required">*</span>
              </label>
            </div>
            <div class="reveal-box reveal-delay-4 full-width">
              <div class="input-wrapper">
                <input
                  id="passwordConfirm"
                  v-model="formData.passwordConfirm"
                  type="password"
                  class="form-input"
                  placeholder="Confirm your password"
                />
              </div>
              <div class="error-container">
                <span v-if="errors.passwordConfirm" class="error-message">{{ errors.passwordConfirm }}</span>
              </div>
            </div>
          </div>

          <!-- API Error Message -->
          <div v-if="errors.api" class="reveal-box full-width">
            <div class="api-error">{{ errors.api }}</div>
          </div>

          <!-- Submit Button -->
          <div class="reveal-box reveal-delay-4 full-width">
            <button type="submit" class="submit-button" :class="{ loading: isLoading }" :disabled="isLoading">
              <span v-if="!isLoading">{{ isSignup ? 'Sign up' : 'Sign in' }} →</span>
              <span v-else>Loading...</span>
            </button>
          </div>

          <!-- Forgot Password / Toggle Mode -->
          <div class="reveal-box reveal-delay-5 full-width">
            <div class="footer-links">
              <button v-if="!isSignup" type="button" class="link-button" @click="handleForgotPassword">
                Forgot password?
              </button>
              <button type="button" class="link-button" @click="toggleMode">
                {{ isSignup ? 'Already have an account? Sign in' : "Don't have an account? Sign up" }}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const isSignup = ref(false)
const showPassword = ref(false)
const isLoading = ref(false)

const formData = reactive({
  fullName: '',
  email: '',
  password: '',
  passwordConfirm: ''
})

const errors = reactive({
  fullName: '',
  email: '',
  password: '',
  passwordConfirm: '',
  api: ''
})

const toggleMode = () => {
  isSignup.value = !isSignup.value
  Object.keys(formData).forEach(key => {
    formData[key as keyof typeof formData] = ''
  })
  Object.keys(errors).forEach(key => {
    errors[key as keyof typeof errors] = ''
  })
}

const validateForm = (): boolean => {
  let isValid = true
  
  Object.keys(errors).forEach(key => {
    errors[key as keyof typeof errors] = ''
  })

  if (isSignup.value && formData.fullName.trim().length < 3) {
    errors.fullName = 'Full name must be at least 3 characters'
    isValid = false
  }

  const emailRegex = /\S+@\S+\.\S+/
  if (!emailRegex.test(formData.email)) {
    errors.email = 'Invalid email address'
    isValid = false
  }

  if (formData.password.length < 6) {
    errors.password = 'Password must be at least 6 characters long'
    isValid = false
  }

  if (isSignup.value && formData.password !== formData.passwordConfirm) {
    errors.passwordConfirm = 'Passwords do not match'
    isValid = false
  }

  return isValid
}

const handleSubmit = async () => {
  if (validateForm()) {
    isLoading.value = true
    errors.api = ''

    try {
      let result
      
      if (isSignup.value) {
        result = await authStore.signup(
          formData.fullName,
          formData.email,
          formData.password,
          formData.passwordConfirm
        )
      } else {
        result = await authStore.login(formData.email, formData.password)
      }

      if (result.success) {
        await router.push('/dashboard')
      } else {
        errors.api = result.error || 'Authentication failed'
      }
    } catch (err) {
      errors.api = 'An unexpected error occurred'
    } finally {
      isLoading.value = false
    }
  }
}

const handleForgotPassword = () => {
  console.log('Forgot password clicked')
}
</script>

<style scoped>
@keyframes orbit {
  0% {
    transform: rotate(0deg) translateX(var(--orbit-radius)) rotate(0deg);
  }
  100% {
    transform: rotate(360deg) translateX(var(--orbit-radius)) rotate(-360deg);
  }
}

@keyframes orbit-reverse {
  0% {
    transform: rotate(0deg) translateX(var(--orbit-radius)) rotate(0deg);
  }
  100% {
    transform: rotate(-360deg) translateX(var(--orbit-radius)) rotate(360deg);
  }
}

.auth-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
  background: #0a0e1a;
}

.decorative-side {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(to bottom, #0a0e1a, #0f1523);
  overflow: hidden;
}

.orbit-container {
  position: relative;
  width: 600px;
  height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.orbit-center-text {
  position: relative;
  z-index: 10;
  font-size: 4rem;
  font-weight: 600;
  line-height: 1;
  text-align: center;
  white-space: pre-wrap;
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.4));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  pointer-events: none;
}

.orbit-path {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
}

.orbit-path-1 {
  width: 200px;
  height: 200px;
}

.orbit-path-2,
.orbit-path-3 {
  width: 420px;
  height: 420px;
}

.orbit {
  position: absolute;
  top: 50%;
  left: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.orbit-1,
.orbit-1-2 {
  --orbit-radius: 100px;
  width: 30px;
  height: 30px;
  animation: orbit 20s linear infinite;
}

.orbit-1 {
  animation-delay: calc(-20s);
  background: linear-gradient(135deg, #a855f7, #7c3aed);
}

.orbit-1-2 {
  animation-delay: calc(-10s);
  background: linear-gradient(135deg, #3b82f6, #2563eb);
}

.orbit-2 {
  --orbit-radius: 210px;
  width: 50px;
  height: 50px;
  animation: orbit 20s linear infinite;
  animation-delay: 0s;
  background: linear-gradient(135deg, #f97316, #ea580c);
}

.orbit-3,
.orbit-3-2 {
  --orbit-radius: 210px;
  width: 50px;
  height: 50px;
  animation: orbit-reverse 20s linear infinite;
}

.orbit-3 {
  animation-delay: calc(-10s);
  background: linear-gradient(135deg, #10b981, #059669);
}

.orbit-3-2 {
  animation-delay: calc(-15s);
  background: linear-gradient(135deg, #ec4899, #db2777);
}

.orbit-icon,
.orbit-icon-large {
  color: #ffffff;
  stroke: #ffffff;
}

.orbit-icon {
  width: 20px;
  height: 20px;
}

.orbit-icon-large {
  width: 30px;
  height: 30px;
}

.form-side {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: #0a0e1a;
}

.form-container {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.reveal-box {
  position: relative;
  width: fit-content;
  overflow: hidden;
  animation: reveal-content 0.5s ease-out 0.25s backwards;
}

.reveal-box.full-width {
  width: 100%;
}

.reveal-delay-1 {
  animation-delay: 0.3s;
}

.reveal-delay-2 {
  animation-delay: 0.35s;
}

.reveal-delay-3 {
  animation-delay: 0.4s;
}

.reveal-delay-4 {
  animation-delay: 0.45s;
}

.reveal-delay-5 {
  animation-delay: 0.5s;
}

@keyframes reveal-content {
  from {
    opacity: 0;
    transform: translateY(75px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.form-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #ffffff;
  line-height: 1.2;
}

.form-subtitle {
  font-size: 0.875rem;
  color: #9ca3af;
  line-height: 1.5;
}

.divider {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
}

.divider-line {
  flex: 1;
  height: 1px;
  background: repeating-linear-gradient(
    to right,
    #374151 0px,
    #374151 4px,
    transparent 4px,
    transparent 8px
  );
}

.divider-text {
  font-size: 0.875rem;
  color: #9ca3af;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 500;
  line-height: 1;
  color: #f3f4f6;
}

.required {
  color: #ef4444;
}

.input-wrapper {
  position: relative;
  width: 100%;
}

.password-wrapper {
  position: relative;
}

.form-input {
  display: flex;
  width: 100%;
  height: 44px;
  padding: 0.75rem 1rem;
  font-size: 0.9375rem;
  color: #f3f4f6;
  background: #1f2937;
  border: 1px solid #374151;
  border-radius: 0.5rem;
  transition: all 0.3s ease;
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

.password-toggle {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  padding: 0.25rem;
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  outline: none;
  transition: color 0.2s;
}

.password-toggle:hover {
  color: #f3f4f6;
}

.error-container {
  height: 1rem;
}

.error-message {
  font-size: 0.75rem;
  color: #ef4444;
}

.api-error {
  padding: 0.75rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid #ef4444;
  border-radius: 0.5rem;
  color: #ef4444;
  font-size: 0.875rem;
  text-align: center;
}

.submit-button {
  position: relative;
  display: block;
  width: 100%;
  height: 44px;
  padding: 0 1.5rem;
  background: #1f2937;
  color: #ffffff;
  border: 1px solid #374151;
  border-radius: 0.5rem;
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  outline: none;
  transition: all 0.2s;
  overflow: hidden;
}

.submit-button:hover {
  background: #374151;
}

.submit-button.loading {
  pointer-events: none;
  background: #374151;
}

.submit-button.loading::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(96, 165, 250, 0.3), transparent);
  animation: loading-shine 1s infinite;
}

@keyframes loading-shine {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

.footer-links {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  align-items: center;
}

.link-button {
  font-size: 0.875rem;
  color: #60a5fa;
  background: none;
  border: none;
  cursor: pointer;
  outline: none;
  transition: color 0.2s;
  padding-top: 15px;
}

.link-button:hover {
  color: #93c5fd;
  text-decoration: underline;
}

@media (max-width: 1024px) {
  .decorative-side {
    display: none;
  }

  .form-side {
    width: 100%;
  }
}
</style>
