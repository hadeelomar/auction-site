<template>
  <div class="auth-container">
    <!-- left side - form -->
    <div class="form-side">
      <div class="form-container">
        <!-- logo -->
        <router-link to="/" class="logo">
          <div class="logo-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="m14.5 12.5-8 8a2.119 2.119 0 1 1-3-3l8-8"/>
              <path d="m16 16 6-6"/>
              <path d="m8 8 6-6"/>
              <path d="m9 7 8 8"/>
              <path d="m21 11-8-8"/>
            </svg>
          </div>
          <span class="logo-text">Bido</span>
        </router-link>

        <!-- header -->
        <div class="reveal-box">
          <p class="welcome-text">{{ isSignup ? 'Join us today!' : 'Welcome back' }}</p>
        </div>
        <div class="reveal-box reveal-delay-1">
          <h1 class="form-title">{{ isSignup ? 'Sign up' : 'Sign in' }}</h1>
        </div>

        <!-- form -->
        <form @submit.prevent="handleSubmit" class="auth-form">
          <!-- Full Name Field for Signup -->
          <div v-if="isSignup" class="form-group reveal-box reveal-delay-2">
            <label for="fullName" class="form-label">Full Name</label>
            <input
              id="fullName"
              v-model="formData.fullName"
              type="text"
              class="form-input"
              placeholder="Enter your full name"
            />
            <span v-if="errors.fullName" class="error-message">{{ errors.fullName }}</span>
          </div>

          <!-- email field -->
          <div class="form-group reveal-box reveal-delay-2">
            <label for="email" class="form-label">Email</label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              class="form-input"
              placeholder="example@email.com"
            />
            <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
          </div>

          <!-- dob field for signup -->
          <div v-if="isSignup" class="form-group reveal-box reveal-delay-2">
            <label for="dateOfBirth" class="form-label">Date of Birth</label>
            <input
              id="dateOfBirth"
              v-model="formData.dateOfBirth"
              type="date"
              class="form-input"
            />
            <span v-if="errors.dateOfBirth" class="error-message">{{ errors.dateOfBirth }}</span>
          </div>

          <!-- password field -->
          <div class="form-group reveal-box reveal-delay-3">
            <div class="label-row">
              <label for="password" class="form-label">Password</label>
              <button v-if="!isSignup" type="button" class="forgot-link" @click="handleForgotPassword">
                Forgot Password ?
              </button>
            </div>
            <div class="password-wrapper">
              <input
                id="password"
                v-model="formData.password"
                :type="showPassword ? 'text' : 'password'"
                class="form-input"
                placeholder="Enter your password"
              />
              <button type="button" class="password-toggle" @click="showPassword = !showPassword">
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
            <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
          </div>

          <!-- password confirmation for signup -->
          <div v-if="isSignup" class="form-group reveal-box reveal-delay-4">
            <label for="passwordConfirm" class="form-label">Confirm Password</label>
            <input
              id="passwordConfirm"
              v-model="formData.passwordConfirm"
              type="password"
              class="form-input"
              placeholder="Confirm your password"
            />
            <span v-if="errors.passwordConfirm" class="error-message">{{ errors.passwordConfirm }}</span>
          </div>

          <div v-if="errors.api" class="api-error reveal-box">{{ errors.api }}</div>
          <div class="reveal-box reveal-delay-4">
            <button type="submit" class="submit-button" :class="{ loading: isLoading }" :disabled="isLoading">
              <span v-if="!isLoading">{{ isSignup ? 'SIGN UP' : 'SIGN IN' }}</span>
              <span v-else>Loading...</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M5 12h14"/>
                <path d="m12 5 7 7-7 7"/>
              </svg>
            </button>
          </div>

          <!-- toggle - login/signup -->
          <div class="reveal-box reveal-delay-5">
            <p class="toggle-text">
              {{ isSignup ? 'Already have an account ?' : "I don't have an account ?" }}
              <button type="button" class="toggle-link" @click="toggleMode">
                {{ isSignup ? 'Sign in' : 'Sign up' }}
              </button>
            </p>
          </div>
        </form>
      </div>
    </div>

    <!-- right side -->
    <div class="decorative-side">
      <img 
        src="../../public/image.png" 
        alt="Shopping illustration" 
        class="decorative-image"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const isSignup = ref(route.path === '/signup')
const showPassword = ref(false)
const isLoading = ref(false)

const formData = reactive({
  fullName: '',
  email: '',
  dateOfBirth: '',
  password: '',
  passwordConfirm: ''
})

const errors = reactive({
  fullName: '',
  email: '',
  dateOfBirth: '',
  password: '',
  passwordConfirm: '',
  api: ''
})

const toggleMode = () => {
  isSignup.value = !isSignup.value
  router.replace(isSignup.value ? '/signup' : '/login')
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

  if (isSignup.value && formData.dateOfBirth) {
    const dob = new Date(formData.dateOfBirth)
    if (dob > new Date()) {
      errors.dateOfBirth = 'Date of birth cannot be in the future'
      isValid = false
    }
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
          formData.passwordConfirm,
          formData.dateOfBirth
        )
      } else {
        result = await authStore.login(formData.email, formData.password)
      }

      if (result.success) {
        await router.push('/')
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
.auth-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
  background: #ffffff;
}

.form-side {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.form-container {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  margin-bottom: 1rem;
}

.logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #ea580c, #f97316);
  border-radius: 10px;
  color: #ffffff;
}

.logo-text {
  font-size: 1.25rem;
  font-weight: 700;
  color: #ea580c;
}

.reveal-box {
  animation: reveal-content 0.5s ease-out backwards;
}

.reveal-delay-1 { animation-delay: 0.1s; }
.reveal-delay-2 { animation-delay: 0.15s; }
.reveal-delay-3 { animation-delay: 0.2s; }
.reveal-delay-4 { animation-delay: 0.25s; }
.reveal-delay-5 { animation-delay: 0.3s; }

@keyframes reveal-content {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.welcome-text {
  font-size: 0.9375rem;
  color: #6b7280;
}

.form-title {
  font-size: 2.25rem;
  font-weight: 700;
  color: #111827;
  margin-top: 0.25rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 0.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.forgot-link {
  font-size: 0.8125rem;
  color: #ea580c;
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.2s;
}

.forgot-link:hover {
  color: #c2410c;
}

.password-wrapper {
  position: relative;
}

.form-input {
  width: 100%;
  height: 48px;
  padding: 0 1rem;
  font-size: 0.9375rem;
  color: #111827;
  background: #ffffff;
  border: none;
  border-bottom: 2px solid #fecaca;
  outline: none;
  transition: all 0.2s;
}

.form-input::placeholder {
  color: #9ca3af;
}

.form-input:focus {
  border-bottom-color: #ea580c;
}

.password-toggle {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  padding: 0.25rem;
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
}

.password-toggle:hover {
  color: #6b7280;
}

.error-message {
  font-size: 0.75rem;
  color: #dc2626;
}

.api-error {
  padding: 0.75rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  color: #dc2626;
  font-size: 0.875rem;
  text-align: center;
}

.submit-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: fit-content;
  height: 48px;
  padding: 0 2rem;
  font-size: 0.875rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  color: #ffffff;
  background: linear-gradient(135deg, #ea580c, #f97316);
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 0.5rem;
}

.submit-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(234, 88, 12, 0.35);
}

.submit-button.loading {
  pointer-events: none;
  opacity: 0.8;
}

.toggle-text {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.5rem;
}

.toggle-link {
  color: #ea580c;
  font-weight: 600;
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.2s;
}

.toggle-link:hover {
  color: #c2410c;
}

.decorative-side {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fef3e2 0%, #fde8d0 50%, #fcd9b8 100%);
  padding: 2rem;
}

.decorative-image {
  max-width: 90%;
  max-height: 80vh;
  object-fit: contain;
}

@media (max-width: 1024px) {
  .decorative-side {
    display: none;
  }
}
</style>
