<template>
  <div class="activity-item">
    <div :class="['activity-icon', `activity-icon-${activity.color}`]">
      <!-- Using inline SVGs based on icon type -->
      <svg v-if="activity.icon === 'gavel'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="m14.5 12.5-8 8a2.119 2.119 0 1 1-3-3l8-8"/>
        <path d="m16 16 6-6"/>
        <path d="m8 8 6-6"/>
        <path d="m9 7 8 8"/>
        <path d="m21 11-8-8"/>
      </svg>
      <svg v-else-if="activity.icon === 'trophy'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/>
        <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/>
        <path d="M4 22h16"/>
        <path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/>
        <path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/>
        <path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>
      </svg>
      <svg v-else-if="activity.icon === 'message'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      </svg>
      <svg v-else-if="activity.icon === 'dollar'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <line x1="12" x2="12" y1="2" y2="22"/>
        <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
      </svg>
      <svg v-else-if="activity.icon === 'bell'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
        <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
      </svg>
    </div>
    <div class="activity-content">
      <p class="activity-title">{{ activity.title }}</p>
      <p class="activity-desc">{{ activity.desc }}</p>
    </div>
    <div class="activity-time">{{ activity.time }}</div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  activity: {
    icon: string
    title: string
    desc: string
    time: string
    color: string
  }
}>()

const iconComponent = computed(() => {
  const icons: Record<string, any> = {
    gavel: 'gavel',
    trophy: 'trophy',
    message: 'message',
    dollar: 'dollar',
    bell: 'bell',
  }
  return icons[props.activity.icon]
})
</script>

<style scoped>
.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  border-radius: 0.5rem;
  transition: background 0.2s;
  cursor: pointer;
}

.activity-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.activity-icon {
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.5rem;
  flex-shrink: 0;
}

.activity-icon-blue {
  background: rgba(59, 130, 246, 0.15);
  color: #60a5fa;
}

.activity-icon-green {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
}

.activity-icon-purple {
  background: rgba(168, 85, 247, 0.15);
  color: #a78bfa;
}

.activity-icon-orange {
  background: rgba(249, 115, 22, 0.15);
  color: #fb923c;
}

.activity-icon-red {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
}

.activity-content {
  flex: 1;
  min-width: 0;
}

.activity-title {
  font-size: 0.875rem;
  font-weight: 500;
  color: #f3f4f6;
  margin: 0 0 0.25rem 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.activity-desc {
  font-size: 0.75rem;
  color: #6b7280;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.activity-time {
  font-size: 0.75rem;
  color: #6b7280;
  white-space: nowrap;
}
</style>
