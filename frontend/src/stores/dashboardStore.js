import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import dashboardService from '@/services/dashboardService'
import { useToast } from '@/composables/useToast'

export const useDashboardStore = defineStore('dashboard', () => {
  // State
  const data = ref(null)
  const lastUpdated = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  
  // Constants
  const CACHE_DURATION = 5 * 60 * 1000 // 5 menit
  
  // Composables
  const { showToast } = useToast()
  
  // Computed
  const isDataStale = computed(() => {
    if (!lastUpdated.value) return true
    return Date.now() - lastUpdated.value > CACHE_DURATION
  })
  
  const hasData = computed(() => data.value !== null)
  
  // Actions
  const loadData = async (force = false) => {
    // Return cached data if available and fresh
    if (!force && hasData.value && !isDataStale.value) {
      return data.value
    }
    
    isLoading.value = true
    error.value = null
    
    try {
      const response = await dashboardService.getDashboardStats()
      data.value = response
      lastUpdated.value = Date.now()
      return response
    } catch (err) {
      error.value = err.message || 'Gagal memuat data dashboard'
      showToast('error', 'Gagal memuat data dashboard')
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  const refreshData = () => loadData(true)
  
  const clearCache = () => {
    data.value = null
    lastUpdated.value = null
    error.value = null
  }
  
  return {
    // State
    data,
    isLoading,
    error,
    lastUpdated,
    
    // Computed
    isDataStale,
    hasData,
    
    // Actions
    loadData,
    refreshData,
    clearCache
  }
})