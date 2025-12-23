<template>
  <nav :class="['sidebar', { 'sidebar-collapsed': !open }]">
    <!-- logo section -->
    <div class="sidebar-header">
      <div class="logo-container">
        <div class="logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="currentColor"/>
            <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2"/>
            <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2"/>
          </svg>
        </div>
        <div v-if="open" class="logo-text">
          <span class="logo-title">Auction Site</span>
          <span class="logo-subtitle">Auction Platform</span>
        </div>
      </div>
    </div>

    <!-- navigation items -->
    <div class="nav-items">
      <button
        v-for="item in navItems"
        :key="item.title"
        :class="['nav-item', { 'nav-item-active': selected === item.title }]"
        @click="$emit('select', item.title)"
      >
        <div class="nav-icon">
          <!-- inline SVGs for each nav item-->
          <svg v-if="item.icon === 'home'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
            <polyline points="9 22 9 12 15 12 15 22"/>
          </svg>
          <svg v-else-if="item.icon === 'gavel'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="m14.5 12.5-8 8a2.119 2.119 0 1 1-3-3l8-8"/>
            <path d="m16 16 6-6"/>
            <path d="m8 8 6-6"/>
            <path d="m9 7 8 8"/>
            <path d="m21 11-8-8"/>
          </svg>
          <svg v-else-if="item.icon === 'plus'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="16"/>
            <line x1="8" y1="12" x2="16" y2="12"/>
          </svg>
          <svg v-else-if="item.icon === 'hand'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 11V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v0"/>
            <path d="M14 10V4a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v2"/>
            <path d="M10 10.5V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v8"/>
            <path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"/>
          </svg>
          <svg v-else-if="item.icon === 'package'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12.89 1.45l8 4A2 2 0 0 1 22 7.24v9.53a2 2 0 0 1-1.11 1.79l-8 4a2 2 0 0 1-1.79 0l-8-4a2 2 0 0 1-1.1-1.8V7.24a2 2 0 0 1 1.11-1.79l8-4a2 2 0 0 1 1.78 0z"/>
            <polyline points="2.32 6.16 12 11 21.68 6.16"/>
            <line x1="12" y1="22.76" x2="12" y2="11"/>
          </svg>
          <svg v-else-if="item.icon === 'message'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
        </div>
        <span v-if="open" class="nav-title">{{ item.title }}</span>
        <span v-if="item.badge && open" class="nav-badge">{{ item.badge }}</span>
      </button>
    </div>

    <!-- account section -->
    <div v-if="open" class="account-section">
      <div class="section-label">Account</div>
      <button
        v-for="item in accountItems"
        :key="item.title"
        :class="['nav-item', { 'nav-item-active': selected === item.title }]"
        @click="$emit('select', item.title)"
      >
        <div class="nav-icon">
          <!-- inline SVGs for profile + settings -->
          <svg v-if="item.icon === 'user'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
          </svg>
          <svg v-else-if="item.icon === 'settings'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="3"/>
            <path d="M12 1v6m0 6v6m-5.1-13.9 4.2 4.2m2.8 2.8 4.2 4.2M1 12h6m6 0h6M3.1 6.9l4.2 4.2m2.8 2.8 4.2 4.2"/>
          </svg>
        </div>
        <span class="nav-title">{{ item.title }}</span>
      </button>
    </div>

    <!-- toggle button -->
    <button class="sidebar-toggle" @click="$emit('toggle')">
      <div class="nav-icon">
        <svg :class="{ 'rotate-180': open }" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="9 18 15 12 9 6"/>
        </svg>
      </div>
      <span v-if="open" class="nav-title">Hide</span>
    </button>
  </nav>
</template>

<script setup lang="ts">
defineProps<{
  open: boolean
  selected: string
}>()

defineEmits<{
  toggle: []
  select: [page: string]
}>()

const navItems = [
  { title: 'Dashboard', icon: 'home' },
  { title: 'Browse Auctions', icon: 'gavel', badge: 12 },
  { title: 'Create Auction', icon: 'plus' },
  { title: 'My Bids', icon: 'hand', badge: 3 },
  { title: 'My Auctions', icon: 'package' },
  { title: 'Messages', icon: 'message', badge: 5 },
]

const accountItems = [
  { title: 'Profile', icon: 'user' },
  { title: 'Settings', icon: 'settings' },
]
</script>

<style scoped>
.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  width: 16rem;
  background: #0f1523;
  border-right: 1px solid #1f2937;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.3);
}

.sidebar-collapsed {
  width: 4rem;
}

.sidebar-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #1f2937;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s;
}

.logo-container:hover {
  background: rgba(255, 255, 255, 0.05);
}

.logo {
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-radius: 0.5rem;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);
}

.logo-text {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.logo-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #f3f4f6;
  white-space: nowrap;
}

.logo-subtitle {
  font-size: 0.75rem;
  color: #9ca3af;
  white-space: nowrap;
}

.nav-items {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-bottom: 2rem;
}

.account-section {
  margin-bottom: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #1f2937;
}

.section-label {
  padding: 0.5rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 500;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  height: 2.75rem;
  width: 100%;
  padding: 0;
  background: transparent;
  border: none;
  border-radius: 0.375rem;
  color: #9ca3af;
  cursor: pointer;
  transition: all 0.2s;
  outline: none;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #f3f4f6;
}

.nav-item-active {
  background: rgba(59, 130, 246, 0.15);
  color: #60a5fa;
  border-left: 2px solid #3b82f6;
}

.nav-icon {
  width: 3rem;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.nav-title {
  font-size: 0.875rem;
  font-weight: 500;
  white-space: nowrap;
  flex: 1;
  text-align: left;
}

.nav-badge {
  position: absolute;
  right: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 1.25rem;
  height: 1.25rem;
  padding: 0 0.375rem;
  background: #3b82f6;
  color: white;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.sidebar-toggle {
  display: flex;
  align-items: center;
  height: 3rem;
  width: 100%;
  padding: 0;
  background: transparent;
  border: none;
  border-top: 1px solid #1f2937;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
  outline: none;
}

.sidebar-toggle:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #f3f4f6;
}

.rotate-180 {
  transform: rotate(180deg);
}
</style>
