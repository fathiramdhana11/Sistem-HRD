import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null
  }),
  actions: {
    setUser(data) {
      this.user = data.user
      this.token = data.token
      localStorage.setItem('auth', JSON.stringify(data))
    },
    loadUser() {
      const data = localStorage.getItem('auth')
      if (data) {
        const parsed = JSON.parse(data)
        this.user = parsed.user
        this.token = parsed.token
      }
    },
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('auth')
    }
  }
})