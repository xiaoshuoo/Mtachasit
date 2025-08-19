import { ref } from 'vue'

interface Notification {
  id: number
  type: 'success' | 'error' | 'warning' | 'info'
  message: string
  duration?: number
}

const notifications = ref<Notification[]>([])
let nextId = 1

export function useNotifications() {
  const showNotification = (type: Notification['type'], message: string, duration = 5000) => {
    const id = nextId++
    const notification: Notification = {
      id,
      type,
      message,
      duration
    }
    
    notifications.value.push(notification)
    
    if (duration > 0) {
      setTimeout(() => {
        removeNotification(id)
      }, duration)
    }
    
    return id
  }
  
  const removeNotification = (id: number) => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }
  
  const clearAll = () => {
    notifications.value = []
  }
  
  // Удобные методы для разных типов уведомлений
  const success = (message: string, duration?: number) => showNotification('success', message, duration)
  const error = (message: string, duration?: number) => showNotification('error', message, duration)
  const warning = (message: string, duration?: number) => showNotification('warning', message, duration)
  const info = (message: string, duration?: number) => showNotification('info', message, duration)
  
  return {
    notifications,
    showNotification,
    removeNotification,
    clearAll,
    success,
    error,
    warning,
    info
  }
}
