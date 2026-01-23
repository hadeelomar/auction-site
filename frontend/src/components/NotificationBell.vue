<template>
  <div class="notification-bell" @click="toggleDropdown" :class="{ 'has-notifications': unreadCount > 0 }">
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
      <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
    </svg>
    <span v-if="unreadCount > 0" class="unread-badge">{{ unreadCount }}</span>
    
    <!-- Notification Dropdown -->
    <div v-if="showDropdown" class="notification-dropdown" @click.stop>
      <div class="notification-header">
        <h4>Notifications</h4>
        <button @click="markAllRead" class="mark-all-read">Mark all as read</button>
      </div>
      <div class="notification-list">
        <div v-if="notifications.length === 0" class="no-notifications">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
          </svg>
          <p>No notifications yet</p>
        </div>
        <div 
          v-for="notification in notifications" 
          :key="notification.id"
          :class="['notification-item', { 'unread': !notification.is_read }]"
          @click="markAsRead(notification)"
        >
          <div class="notification-content">
            <div class="notification-type">{{ notification.type }}</div>
            <div class="notification-message">{{ notification.message }}</div>
            <div class="notification-time">{{ formatTime(notification.timestamp) }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps<{
  unreadCount: number
}>()

const emit = defineEmits<{
  notificationClicked: (notification: any) => void
}>()

const showDropdown = ref(false)
const notifications = ref<any[]>([])

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
}

const markAsRead = async (notification: any) => {
  try {
    const response = await fetch(`/api/notifications/${notification.id}/mark-read/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      }
    })
    
    if (response.ok) {
      notification.is_read = true
      emit('notificationClicked', notification)
    }
  } catch (error) {
    console.error('Error marking notification as read:', error)
  }
}

const markAllRead = async () => {
  try {
    const response = await fetch('/api/notifications/mark-all-read/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      }
    })
    
    if (response.ok) {
      // Mark all notifications as read locally
      notifications.value.forEach(notification => {
        notification.is_read = true
      })
      // Update the unread count in navbar
      const event = new CustomEvent('notifications-updated', { 
        detail: { unreadCount: 0 } 
      })
      window.dispatchEvent(event)
    }
  } catch (error) {
    console.error('Error marking all notifications as read:', error)
  }
}

const fetchNotifications = async () => {
  try {
    const response = await fetch('/api/notifications/')
    if (response.ok) {
      const data = await response.json()
      notifications.value = data.notifications || []
    }
  } catch (error) {
    console.error('Error fetching notifications:', error)
  }
}

const formatTime = (timestamp: string) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  if (diff < 60000) { // less than 1 minute
    return 'Just now'
  } else if (diff < 3600000) { // less than 1 hour
    const minutes = Math.floor(diff / 60000)
    return `${minutes}m ago`
  } else if (diff < 86400000) { // less than 1 day
    const hours = Math.floor(diff / 3600000)
    return `${hours}h ago`
  } else {
    const days = Math.floor(diff / 86400000)
    return `${days}d ago`
  }
}

const getCsrfToken = (): string => {
  const cookies = document.cookie.split(';')
  for (let cookie of cookies) {
    const [name, value] = cookie.trim().split('=')
    if (name === 'csrftoken') {
      return decodeURIComponent(value)
    }
  }
  return ''
}

onMounted(() => {
  fetchNotifications()
  
  // Poll for new notifications every 30 seconds
  const interval = setInterval(fetchNotifications, 30000)
  
  onUnmounted(() => {
    clearInterval(interval)
  })
})
</script>

<style scoped>
.notification-bell {
  position: relative;
  cursor: pointer;
  padding: 8px 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  transition: color 0.2s;
  text-decoration: none;
}

.notification-bell:hover {
  color: #111827;
}

.has-notifications {
  color: #ea580c;
}

.unread-badge {
  position: absolute;
  top: 0;
  right: 0;
  background: #dc2626;
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  font-size: 10px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 320px;
  max-height: 400px;
  overflow-y: auto;
  z-index: 1000;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #e5e7eb;
}

.notification-header h4 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #111827;
}

.mark-all-read {
  padding: 6px 12px;
  font-size: 12px;
  background: #f3f4f6;
  color: #6b7280;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.mark-all-read:hover {
  background: #e5e7eb;
}

.notification-list {
  max-height: 300px;
  overflow-y: auto;
}

.no-notifications {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  color: #9ca3af;
}

.no-notifications svg {
  margin-bottom: 0.5rem;
  opacity: 0.5;
}

.no-notifications p {
  margin: 0;
  font-size: 14px;
}

.notification-item {
  padding: 12px 16px;
  border-bottom: 1px solid #f3f4f6;
  cursor: pointer;
  transition: background-color 0.2s;
}

.notification-item:hover {
  background: #f9fafb;
}

.notification-item.unread {
  background: #fef3c7;
  border-left: 3px solid #ea580c;
}

.notification-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.notification-type {
  font-size: 11px;
  font-weight: 600;
  color: #ea580c;
  text-transform: uppercase;
}

.notification-message {
  font-size: 13px;
  color: #374151;
  line-height: 1.4;
}

.notification-time {
  font-size: 11px;
  color: #9ca3af;
}
</style>
