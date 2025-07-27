import { ref, reactive } from 'vue'

const toasts = ref([])
let toastId = 0

export function useToast() {
  const addToast = (type, title, message, duration = 3000, actions = []) => {
    const id = ++toastId
    const toast = {
      id,
      type,
      title,
      message,
      duration,
      actions,
      visible: true,
      progress: 100
    }
    
    toasts.value.push(toast)
    
    // Progress bar animation
    const progressInterval = setInterval(() => {
      toast.progress -= (100 / duration) * 100
      if (toast.progress <= 0) {
        clearInterval(progressInterval)
      }
    }, 100)
    
    // Auto remove
    setTimeout(() => {
      removeToast(id)
    }, duration)
    
    return id
  }

  const removeToast = (id) => {
    const index = toasts.value.findIndex(toast => toast.id === id)
    if (index > -1) {
      toasts.value[index].visible = false
      setTimeout(() => {
        toasts.value.splice(index, 1)
      }, 300) // Animation delay
    }
  }

  const success = (title, message, duration = 2000, actions) => {
    return addToast('success', title, message, duration, actions)
  }

  const error = (title, message, duration = 3000, actions) => {
    return addToast('error', title, message, duration, actions)
  }

  const warning = (title, message, duration = 3000, actions) => {
    return addToast('warning', title, message, duration, actions)
  }

  const info = (title, message, duration = 2000, actions) => {
    return addToast('info', title, message, duration, actions)
  }

  const loading = (title, message) => {
    return addToast('loading', title, message, 0) // No auto-remove for loading
  }

  const clear = () => {
    toasts.value = []
  }

  return {
    toasts,
    success,
    error,
    warning,
    info,
    loading,
    removeToast,
    clear
  }
}