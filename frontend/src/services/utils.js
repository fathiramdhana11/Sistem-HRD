// Configuration constants
export const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

/**
 * Get authorization headers for API requests
 * @returns {Object} Headers object with Authorization token
 */
export const getAuthHeaders = () => {
  try {
    const auth = JSON.parse(localStorage.getItem('auth'))
    const token = auth?.access_token

    if (!token) {
      console.warn("Token otentikasi tidak ditemukan di localStorage")
      return {}
    }

    return { Authorization: `Bearer ${token}` }
  } catch (error) {
    console.error("Error parsing auth data from localStorage:", error)
    return {}
  }
}

/**
 * Check if user is authenticated
 * @returns {boolean}
 */
export const isAuthenticated = () => {
  try {
    const auth = JSON.parse(localStorage.getItem('auth'))
    return !!auth?.access_token
  } catch {
    return false
  }
}