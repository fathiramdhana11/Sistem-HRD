import axios from 'axios'
import { API_URL } from './utils'

class DashboardService {
  constructor() {
    this.baseURL = `${API_URL}/api/dashboard`
  }

  /**
   * Fetch dashboard statistics from API
   * @returns {Promise<Object>} Dashboard statistics data
   */
  async getDashboardStats() {
    try {
      const response = await axios.get(`${this.baseURL}/stats`)
      return response.data
    } catch (error) {
      // Log error untuk debugging
      console.warn('Dashboard API tidak tersedia, menggunakan mock data:', error.message)
      
      // Return mock data sebagai fallback
      return this.getMockData()
    }
  }

  /**
   * Generate mock data untuk development
   * @returns {Object} Mock dashboard data
   */
  getMockData() {
    return {
      totalEmployees: this.randomBetween(200, 250),
      activeEmployees: this.randomBetween(180, 210),
      leaveRequests: this.randomBetween(10, 30),
      activeBranches: this.randomBetween(10, 15),
      chartData: this.generateChartData(),
      recentActivities: this.generateRecentActivities()
    }
  }

  /**
   * Generate random number between min and max
   * @param {number} min 
   * @param {number} max 
   * @returns {number}
   */
  randomBetween(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min
  }

  /**
   * Generate mock chart data
   * @returns {Array} Chart data array
   */
  generateChartData() {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun']
    return months.map(month => ({
      label: month,
      value: this.randomBetween(5, 20)
    }))
  }

  /**
   * Generate mock recent activities
   * @returns {Array} Recent activities array
   */
  generateRecentActivities() {
    const activities = [
      {
        id: 1,
        name: "Andi Pratama",
        activity: "mengajukan cuti tahunan (5 hari)",
        time: "2 menit yang lalu",
        icon: "pi pi-file-edit",
        iconBg: "bg-amber-100 text-amber-600"
      },
      {
        id: 2,
        name: "HR Admin",
        activity: "menambahkan karyawan baru: Siti Nurhaliza",
        time: "15 menit yang lalu",
        icon: "pi pi-user-plus",
        iconBg: "bg-emerald-100 text-emerald-600"
      },
      {
        id: 3,
        name: "Budi Santoso",
        activity: "memperbarui data profil",
        time: "1 jam yang lalu",
        icon: "pi pi-user-edit",
        iconBg: "bg-blue-100 text-blue-600"
      }
    ]
    
    // Return random subset of activities
    return activities.slice(0, this.randomBetween(2, 3))
  }
}

export default new DashboardService()