class WebSocketService {
  private socket: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 1000
  private isConnecting = false
  private messageHandlers: Map<string, Function[]> = new Map()
  private unreadCount = 0

  connect() {
    if (this.isConnecting || (this.socket && this.socket.readyState === WebSocket.OPEN)) {
      return
    }

    this.isConnecting = true

    try {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const wsUrl = `${protocol}//${window.location.host.replace(':5173', ':8001')}/ws/notifications/`

      this.socket = new WebSocket(wsUrl)

      this.socket.onopen = () => {
        this.isConnecting = false
        this.reconnectAttempts = 0
        
        // Request initial unread count
        this.sendMessage({ type: 'get_unread_count' })
      }

      this.socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          this.handleMessage(data)
        } catch (error) {
          console.error('Error parsing WebSocket message:', error)
        }
      }

      this.socket.onclose = (event) => {
        this.isConnecting = false
        this.socket = null
        
        // Attempt to reconnect if not a normal closure
        if (event.code !== 1000 && this.reconnectAttempts < this.maxReconnectAttempts) {
          this.scheduleReconnect()
        }
      }

      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error)
        this.isConnecting = false
      }

    } catch (error) {
      console.error('Error creating WebSocket:', error)
      this.isConnecting = false
      this.scheduleReconnect()
    }
  }

  private scheduleReconnect() {
    this.reconnectAttempts++
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1)
    
    setTimeout(() => {
      this.connect()
    }, delay)
  }

  private handleMessage(data: any) {
    const { type } = data

    switch (type) {
      case 'new_notification':
        this.emit('new_notification', data.notification)
        break
      
      case 'existing_notification':
        this.emit('existing_notification', data.notification)
        break
      
      case 'unread_count_update':
        this.unreadCount = data.count
        this.emit('unread_count_update', data.count)
        break
      
      case 'error':
        console.error('WebSocket error from server:', data.message)
        this.emit('error', data.message)
        break
      
      default:
        break
    }
  }

  on(event: string, callback: Function) {
    if (!this.messageHandlers.has(event)) {
      this.messageHandlers.set(event, [])
    }
    this.messageHandlers.get(event)!.push(callback)
  }

  off(event: string, callback: Function) {
    const handlers = this.messageHandlers.get(event)
    if (handlers) {
      const index = handlers.indexOf(callback)
      if (index > -1) {
        handlers.splice(index, 1)
      }
    }
  }

  private emit(event: string, data: any) {
    const handlers = this.messageHandlers.get(event)
    if (handlers) {
      handlers.forEach(callback => callback(data))
    }
  }

  sendMessage(message: any) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(message))
    }
  }

  markNotificationRead(notificationId: number) {
    this.sendMessage({
      type: 'mark_read',
      notification_id: notificationId
    })
  }

  markAllNotificationsRead() {
    this.sendMessage({
      type: 'mark_all_read'
    })
  }

  disconnect() {
    if (this.socket) {
      this.socket.close(1000, 'Client disconnect')
      this.socket = null
    }
    this.isConnecting = false
    this.reconnectAttempts = this.maxReconnectAttempts // Prevent reconnection
  }

  isConnected(): boolean {
    return this.socket !== null && this.socket.readyState === WebSocket.OPEN
  }

  getUnreadCount(): number {
    return this.unreadCount
  }
}

// Create singleton instance
const websocketService = new WebSocketService()

export default websocketService
