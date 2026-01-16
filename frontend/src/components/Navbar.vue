<template>
  <nav class="navbar">
    <div class="navbar-container">
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

      <!-- search bar -->
      <div class="search-container">
        <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"/>
          <path d="m21 21-4.3-4.3"/>
        </svg>
        <input 
          type="text" 
          v-model="searchQuery"
          placeholder="Search for items..."
          class="search-input"
          @keyup.enter="handleSearch"
        />
      </div>

      <!-- right side - actions -->
      <div class="navbar-actions">
        <template v-if="authStore.isAuthenticated">
          <!-- create auction -->
          <router-link to="/create" class="create-button">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14"/>
              <path d="M12 5v14"/>
            </svg>
            <span>Sell Item</span>
          </router-link>

          <!-- my bids -->
          <router-link to="/bids" class="nav-link">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="m14.5 12.5-8 8a2.119 2.119 0 1 1-3-3l8-8"/>
              <path d="m16 16 6-6"/>
              <path d="m8 8 6-6"/>
              <path d="m9 7 8 8"/>
              <path d="m21 11-8-8"/>
            </svg>
            <span class="nav-link-text">My Bids</span>
          </router-link>

          <!-- profile dropdown -->
          <div class="profile-dropdown" @click="showDropdown = !showDropdown">
            <div class="profile-avatar">
              <img v-if="authStore.user?.profile_image" :src="authStore.user.profile_image" alt="Profile" />
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
            </div>
            <svg class="dropdown-arrow" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="m6 9 6 6 6-6"/>
            </svg>

            <!-- dropdown menu -->
            <div v-if="showDropdown" class="dropdown-menu">
              <div class="dropdown-header">
                <span class="dropdown-name">{{ authStore.user?.first_name }} {{ authStore.user?.last_name }}</span>
                <span class="dropdown-email">{{ authStore.user?.email }}</span>
              </div>
              <div class="dropdown-divider"></div>
              <router-link to="/profile" class="dropdown-item" @click="showDropdown = false">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
                Profile Settings
              </router-link>
              <router-link to="/auctions" class="dropdown-item" @click="showDropdown = false">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/>
                  <path d="m3.3 7 8.7 5 8.7-5"/>
                  <path d="M12 22V12"/>
                </svg>
                My Auctions
              </router-link>
              <div class="dropdown-divider"></div>
              <button class="dropdown-item logout" @click="handleLogout">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                  <polyline points="16 17 21 12 16 7"/>
                  <line x1="21" x2="9" y1="12" y2="12"/>
                </svg>
                Sign Out
              </button>
            </div>
          </div>
        </template>

        <template v-else>
          <router-link to="/login" class="login-button">Sign In</router-link>
          <router-link to="/signup" class="signup-button">Sign Up</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const searchQuery = ref('')
const showDropdown = ref(false)

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ path: '/', query: { search: searchQuery.value } })
  }
}

const handleLogout = async () => {
  await authStore.logout()
  showDropdown.value = false
  router.push('/')
}
</script>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.navbar-container {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0.875rem 2rem;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  flex-shrink: 0;
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
  color: #111827;
}

.search-container {
  flex: 1;
  position: relative;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
}

.search-input {
  width: 100%;
  height: 44px;
  padding: 0 1rem 0 2.75rem;
  font-size: 0.9375rem;
  color: #111827;
  background: #f3f4f6;
  border: 1px solid transparent;
  border-radius: 12px;
  outline: none;
  transition: all 0.2s;
}

.search-input::placeholder {
  color: #9ca3af;
}

.search-input:focus {
  background: #ffffff;
  border-color: #ea580c;
  box-shadow: 0 0 0 3px rgba(234, 88, 12, 0.1);
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-shrink: 0;
}

.create-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #ffffff;
  background: linear-gradient(135deg, #ea580c, #f97316);
  border: none;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s;
}

.create-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(234, 88, 12, 0.3);
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #4b5563;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s;
}

.nav-link:hover {
  color: #111827;
  background: #f3f4f6;
}

.nav-link-text {
  display: none;
}

@media (min-width: 768px) {
  .nav-link-text {
    display: inline;
  }
}

.profile-dropdown {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem;
  cursor: pointer;
  border-radius: 50px;
  transition: background 0.2s;
}

.profile-dropdown:hover {
  background: #f3f4f6;
}

.profile-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: #f3f4f6;
  border-radius: 50%;
  color: #6b7280;
  overflow: hidden;
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.dropdown-arrow {
  color: #6b7280;
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  width: 240px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  animation: dropdown-in 0.15s ease-out;
}

@keyframes dropdown-in {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-header {
  padding: 1rem;
  background: #f9fafb;
}

.dropdown-name {
  display: block;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #111827;
}

.dropdown-email {
  display: block;
  font-size: 0.8125rem;
  color: #6b7280;
  margin-top: 0.125rem;
}

.dropdown-divider {
  height: 1px;
  background: #e5e7eb;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  color: #374151;
  background: none;
  border: none;
  text-decoration: none;
  cursor: pointer;
  transition: background 0.2s;
}

.dropdown-item:hover {
  background: #f3f4f6;
}

.dropdown-item.logout {
  color: #dc2626;
}

.dropdown-item.logout:hover {
  background: #fef2f2;
}

.login-button {
  padding: 0.625rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  background: none;
  border: none;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s;
}

.login-button:hover {
  color: #111827;
  background: #f3f4f6;
}

.signup-button {
  padding: 0.625rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #ffffff;
  background: linear-gradient(135deg, #ea580c, #f97316);
  border: none;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s;
}

.signup-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(234, 88, 12, 0.3);
}

@media (max-width: 768px) {
  .navbar-container {
    padding: 0.75rem 1rem;
    gap: 1rem;
  }

  .logo-text {
    display: none;
  }

  .create-button span {
    display: none;
  }

  .create-button {
    padding: 0.625rem;
  }
}
</style>
