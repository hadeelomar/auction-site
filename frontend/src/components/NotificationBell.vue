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
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useAuthStore } from '../stores/auth'
import websocketService from '../services/websocket'

const authStore = useAuthStore()
const showDropdown = ref(false)
const notifications = ref<any[]>([])
const unreadCount = ref(0)

const emit = defineEmits<{
  notificationClicked: [notification: any]
}>()

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
  if (showDropdown.value) {
    fetchNotifications()
  }
}

const markAsRead = (notification: any) => {
  // Mark as read via WebSocket
  websocketService.markNotificationRead(notification.id)
  
  // Update locally immediately for better UX
  notification.is_read = true
  
  // Also update the count locally immediately, but it will be corrected by backend
  unreadCount.value = Math.max(0, unreadCount.value - 1)
  
  // Update the unread count in navbar
  const event = new CustomEvent('notifications-updated', { 
    detail: { unreadCount: unreadCount.value } 
  })
  window.dispatchEvent(event)
  
  emit('notificationClicked', notification)
}

const markAllRead = () => {
  // Mark all as read via WebSocket
  websocketService.markAllNotificationsRead()
  
  // Update locally immediately for better UX
  notifications.value.forEach(notification => {
    notification.is_read = true
  })
  
  // Set count to 0 immediately
  unreadCount.value = 0
  
  // Update the unread count in navbar
  const event = new CustomEvent('notifications-updated', { 
    detail: { unreadCount: 0 } 
  })
  window.dispatchEvent(event)
}

const fetchNotifications = async () => {
  // For now, just request the current unread count to ensure sync
  // The actual notifications will come via WebSocket
  if (websocketService.isConnected()) {
    websocketService.sendMessage({ type: 'get_unread_count' })
  }
}

const formatTime = (timestamp: string) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  const minutes = Math.floor(diff / (1000 * 60))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (minutes < 1) return 'just now'
  if (minutes < 60) return `${minutes}m ago`
  if (hours < 24) return `${hours}h ago`
  return `${days}d ago`
}

// WebSocket event handlers
const handleNewNotification = (notification: any) => {
  // Add notification to the list
  notifications.value.unshift(notification)
  unreadCount.value = websocketService.getUnreadCount()
  
  // Force dropdown to refresh if it's open
  if (showDropdown.value) {
    // Force Vue to re-render the list
    const temp = notifications.value
    notifications.value = []
    nextTick(() => {
      notifications.value = temp
    })
  }
  
  // Update the unread count in navbar
  const event = new CustomEvent('notifications-updated', { 
    detail: { count: unreadCount.value } 
  })
  window.dispatchEvent(event)
}

const handleExistingNotification = (notification: any) => {
  // Add notification to the list if not already present
  const exists = notifications.value.find(n => n.id === notification.id)
  if (!exists) {
    notifications.value.push(notification)
  }
  
  // Update unread count
  unreadCount.value = websocketService.getUnreadCount()
}

const handleUnreadCountUpdate = (count: number) => {
  unreadCount.value = count
  
  // Update the unread count in navbar
  const event = new CustomEvent('notifications-updated', { 
    detail: { count: count } 
  })
  window.dispatchEvent(event)
}

onMounted(() => {
  // Only connect if user is authenticated
  if (authStore.isAuthenticated) {
    // Connect to WebSocket
    websocketService.connect()
    
    // Set up event listeners
    websocketService.on('new_notification', handleNewNotification)
    websocketService.on('existing_notification', handleExistingNotification)
    websocketService.on('unread_count_update', handleUnreadCountUpdate)
    
    // Request initial unread count after connection
    setTimeout(() => {
      if (websocketService.isConnected()) {
        websocketService.sendMessage({ type: 'get_unread_count' })
      }
    }, 1000)
  }
})

onUnmounted(() => {
  // Clean up WebSocket event listeners
  websocketService.off('new_notification', handleNewNotification)
  websocketService.off('existing_notification', handleExistingNotification)
  websocketService.off('unread_count_update', handleUnreadCountUpdate)
  
  // Disconnect WebSocket
  websocketService.disconnect()
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

.red-dot {
  position: absolute;
  top: 2px;
  right: 2px;
  width: 8px;
  height: 8px;
  background: #ef4444;
  border-radius: 50%;
  border: 2px solid white;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.8;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
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
