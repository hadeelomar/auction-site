<template>
  <div class="stat-card">
    <div class="stat-header">
      <div :class="['stat-icon', `stat-icon-${color}`]">
        <svg v-if="icon === 'gavel'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="m14.5 12.5-8 8a2.119 2.119 0 1 1-3-3l8-8"/>
          <path d="m16 16 6-6"/>
          <path d="m8 8 6-6"/>
          <path d="m9 7 8 8"/>
          <path d="m21 11-8-8"/>
        </svg>
        <svg v-else-if="icon === 'hand'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M18 11V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v0"/>
          <path d="M14 10V4a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v2"/>
          <path d="M10 10.5V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v8"/>
          <path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"/>
        </svg>
        <svg v-else-if="icon === 'trophy'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/>
          <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/>
          <path d="M4 22h16"/>
          <path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/>
          <path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/>
          <path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>
        </svg>
        <svg v-else-if="icon === 'dollar'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" x2="12" y1="2" y2="22"/>
          <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
        </svg>
      </div>
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="trending-icon">
        <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
        <polyline points="17 6 23 6 23 12"/>
      </svg>
    </div>
    <h3 class="stat-label">{{ title }}</h3>
    <p class="stat-value">{{ value }}</p>
    <p class="stat-change">{{ change }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  title: string
  value: string
  change: string
  icon: string
  color: string
}>()

const iconComponent = computed(() => {
  const icons: Record<string, any> = {
    gavel: 'gavel',
    hand: 'hand',
    trophy: 'trophy',
    dollar: 'dollar',
  }
  return icons[props.icon] || 'gavel'
})
</script>

<style scoped>
.stat-card {
  background: #0f1523;
  border: 1px solid #1f2937;
  border-radius: 0.75rem;
  padding: 1.5rem;
  transition: all 0.2s;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.stat-card:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
  transform: translateY(-2px);
}

.stat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.stat-icon {
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.5rem;
}

.stat-icon-blue {
  background: rgba(59, 130, 246, 0.15);
  color: #60a5fa;
}

.stat-icon-green {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
}

.stat-icon-purple {
  background: rgba(168, 85, 247, 0.15);
  color: #a78bfa;
}

.stat-icon-orange {
  background: rgba(249, 115, 22, 0.15);
  color: #fb923c;
}

.stat-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #9ca3af;
  margin: 0 0 0.5rem 0;
}

.stat-value {
  font-size: 1.875rem;
  font-weight: 700;
  color: #f3f4f6;
  margin: 0 0 0.5rem 0;
}

.stat-change {
  font-size: 0.875rem;
  color: #34d399;
  margin: 0;
}

.trending-icon {
  color: #34d399;
}
</style>
