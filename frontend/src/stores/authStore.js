import { defineStore } from 'pinia'
import { ref } from 'vue'
import router from '@/router'
import authService from '@/services/authService'
import { useDashboardStore } from '@/stores/dashboardStore'
import { useToast } from '@/composables/useToast'
import axios from 'axios' // ← TAMBAHKAN INI

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(null)
  const refreshToken = ref(null)
  const toast = useToast()

  // Initialize from localStorage
  const initializeAuth = () => {
    const authData = localStorage.getItem('auth')
    if (authData) {
      try {
        const parsed = JSON.parse(authData)
        user.value = parsed.user
        token.value = parsed.access_token
        refreshToken.value = parsed.refresh_token
        
        // Check if token is expired and try to refresh
        if (isTokenExpired(parsed.access_token)) {
          refreshAccessToken()
        }
      } catch (error) {
        localStorage.removeItem('auth')
      }
    }
  }

  const isTokenExpired = (token) => {
    if (!token) return true
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      return payload.exp * 1000 < Date.now()
    } catch {
      return true
    }
  }

  const refreshAccessToken = async () => {
    try {
      if (!refreshToken.value) {
        throw new Error('No refresh token available')
      }

      const response = await authService.refreshToken(refreshToken.value)
      token.value = response.data.access_token
      
      // Update localStorage
      const authData = JSON.parse(localStorage.getItem('auth'))
      authData.access_token = response.data.access_token
      localStorage.setItem('auth', JSON.stringify(authData))
      
      return response.data.access_token
    } catch (error) {
      // Silent logout jika refresh token gagal
      toast.error('Sesi Berakhir', 'Sesi Anda telah berakhir. Silakan login kembali.')
      logout()
      throw error
    }
  }

  const login = async (authData) => {
    try {
      console.log('Starting login process...', authData) // Debug log
      
      // Bersihkan state dan localStorage sebelum login baru
      user.value = null;
      token.value = null;
      refreshToken.value = null;
      localStorage.removeItem('auth');
      
      // Set data login baru
      user.value = authData.user;
      token.value = authData.access_token;
      refreshToken.value = authData.refresh_token;
      
      localStorage.setItem('auth', JSON.stringify({
        user: authData.user,
        access_token: authData.access_token,
        refresh_token: authData.refresh_token
      }));
      
      // Set authorization header
      axios.defaults.headers.common['Authorization'] = `Bearer ${authData.access_token}`;
      
      console.log('Auth data saved, navigating to dashboard...') // Debug log
      
      // Navigate to dashboard FIRST
      await router.push('/dashboard')
      
      console.log('Navigation completed') // Debug log
      
      // Pre-load dashboard data setelah navigasi (background)
      setTimeout(async () => {
        try {
          const dashboardStore = useDashboardStore()
          await dashboardStore.loadData()
        } catch (dashboardError) {
          console.warn('Dashboard loading failed:', dashboardError)
          // Silent fail untuk dashboard loading
        }
      }, 100)
      
      // Trigger menu update
      setTimeout(() => {
        window.dispatchEvent(new Event('menu-updated'))
      }, 500)
      
    } catch (error) {
      console.error('Login process error:', error)
      throw error;
    }
  }

  const logout = async () => {
    try {
      // Dispatch menu-clear event first
      window.dispatchEvent(new Event('menu-clear'))
      
      // Clear state
      user.value = null
      token.value = null
      
      // Remove from localStorage
      localStorage.removeItem('auth')
      
      // Navigate to login
      await router.push('/login')
      
    } catch (error) {
      // Force navigation even if there's an error
      await router.push('/login')
    }
  }

  const refreshMenu = () => {
    window.dispatchEvent(new Event('menu-updated'))
  }

  // Initialize on store creation
  initializeAuth()

  return {
    user,
    token,
    refreshToken,
    login,
    logout,
    refreshMenu,
    refreshAccessToken,
    isTokenExpired
  }
})
