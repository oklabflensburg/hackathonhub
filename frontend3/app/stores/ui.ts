import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  duration?: number
  action?: {
    label: string
    onClick: () => void
  }
}

export interface Modal {
  id: string
  component: any
  props?: Record<string, any>
  onClose?: () => void
}

export const useUIStore = defineStore('ui', () => {
  const notifications = ref<Notification[]>([])
  const modals = ref<Modal[]>([])
  const sidebarOpen = ref(false)
  const isLoading = ref(false)

  function showNotification(notification: Omit<Notification, 'id'>) {
    const id = Date.now().toString() + Math.random().toString(36).substr(2, 9)
    const fullNotification: Notification = {
      id,
      duration: 5000,
      ...notification
    }
    
    notifications.value.push(fullNotification)
    
    // Auto-remove after duration
    if (fullNotification.duration) {
      setTimeout(() => {
        removeNotification(id)
      }, fullNotification.duration)
    }
    
    return id
  }

  function removeNotification(id: string) {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index !== -1) {
      notifications.value.splice(index, 1)
    }
  }

  function clearNotifications() {
    notifications.value = []
  }

  function showModal(modal: Omit<Modal, 'id'>) {
    const id = Date.now().toString() + Math.random().toString(36).substr(2, 9)
    const fullModal: Modal = {
      id,
      ...modal
    }
    
    modals.value.push(fullModal)
    return id
  }

  function closeModal(id: string) {
    const modal = modals.value.find(m => m.id === id)
    if (modal?.onClose) {
      modal.onClose()
    }
    
    const index = modals.value.findIndex(m => m.id === id)
    if (index !== -1) {
      modals.value.splice(index, 1)
    }
  }

  function closeAllModals() {
    modals.value.forEach(modal => {
      if (modal.onClose) {
        modal.onClose()
      }
    })
    modals.value = []
  }

  function toggleSidebar() {
    sidebarOpen.value = !sidebarOpen.value
  }

  function openSidebar() {
    sidebarOpen.value = true
  }

  function closeSidebar() {
    sidebarOpen.value = false
  }

  function setLoading(loading: boolean) {
    isLoading.value = loading
  }

  // Helper functions for common notifications
  function showSuccess(message: string, title = 'Success') {
    return showNotification({
      type: 'success',
      title,
      message
    })
  }

  function showError(message: string, title = 'Error') {
    return showNotification({
      type: 'error',
      title,
      message
    })
  }

  function showWarning(message: string, title = 'Warning') {
    return showNotification({
      type: 'warning',
      title,
      message
    })
  }

  function showInfo(message: string, title = 'Info') {
    return showNotification({
      type: 'info',
      title,
      message
    })
  }

  return {
    notifications,
    modals,
    sidebarOpen,
    isLoading,
    showNotification,
    removeNotification,
    clearNotifications,
    showModal,
    closeModal,
    closeAllModals,
    toggleSidebar,
    openSidebar,
    closeSidebar,
    setLoading,
    showSuccess,
    showError,
    showWarning,
    showInfo
  }
})