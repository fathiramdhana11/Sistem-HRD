<template>
  <div class="dashboard-container bg-gray-50 min-h-full transition-colors duration-300">
    <!-- Header Section dengan Fixed Refresh Button -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-4 lg:p-6 mb-6 transition-all duration-300">
      <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div class="flex-1">
          <h1 class="text-2xl lg:text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent mb-2">
            Dashboard HRD
          </h1>
          <p class="text-gray-600 text-sm lg:text-base transition-colors duration-300">
            Selamat datang, {{ authStore.user?.username || 'Admin' }}! Kelola data karyawan dengan mudah.
          </p>
          <p v-if="lastLoadTime" class="text-xs text-gray-500 mt-1 transition-colors duration-300">
            Terakhir diperbarui: {{ new Date(lastLoadTime).toLocaleString('id-ID') }}
          </p>
        </div>
        
        <!-- Fixed Button Container dengan Spacing yang Lebih Baik -->
        <div class="flex flex-col sm:flex-row gap-2 flex-shrink-0">
          <Button 
            @click="refreshData" 
            :loading="isLoading"
            :disabled="isLoading"
            class="refresh-button p-button-outlined border-emerald-300 text-emerald-700 hover:border-emerald-400 hover:text-emerald-800 hover:bg-emerald-50 transition-all duration-200 font-medium shadow-sm hover:shadow-md h-10 px-4 flex items-center justify-center"
          >
            <i :class="isLoading ? 'pi pi-spin pi-spinner' : 'pi pi-refresh'" class="text-sm mr-2"></i>
            <span class="text-sm">{{ isLoading ? 'Memuat...' : 'Refresh Data' }}</span>
          </Button>
          <Button 
            @click="exportData" 
            class="bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700 text-white border-0 shadow-lg hover:shadow-xl transition-all duration-200 font-medium h-10 px-4 text-sm"
          >
            <i class="pi pi-download text-sm mr-2"></i>
            <span class="text-sm">Export CSV</span>
          </Button>
        </div>
      </div>
    </div>

    <!-- Statistik dengan Spacing yang Diperbaiki -->
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 lg:gap-6 mb-6">
      <div 
        v-for="(stat, index) in stats" 
        :key="index"
        class="relative overflow-hidden bg-gradient-to-br from-white to-gray-50 rounded-2xl shadow-md border border-gray-100 p-4 lg:p-6 hover:shadow-lg hover:border-emerald-200 transition-all duration-300 transform hover:-translate-y-1 hover:scale-[1.02] group cursor-pointer"
      >
        <!-- Background Pattern dengan Ukuran yang Disesuaikan -->
        <div class="absolute -top-2 -right-2 w-16 h-16 lg:w-20 lg:h-20 opacity-8 transition-all duration-300 group-hover:opacity-15 group-hover:scale-105">
          <div class="w-full h-full rounded-full bg-gradient-to-br" :class="stat.gradientClass"></div>
        </div>
        
        <!-- Icon dengan Spacing yang Diperbaiki -->
        <div class="absolute top-3 right-3 lg:top-4 lg:right-4">
          <div 
            class="w-10 h-10 lg:w-12 lg:h-12 rounded-xl lg:rounded-2xl flex items-center justify-center transition-all duration-300 group-hover:scale-110 group-hover:rotate-6 shadow-md"
            :class="stat.bgClass"
          >
            <i :class="[stat.icon, stat.iconClass]" class="text-lg lg:text-xl"></i>
          </div>
        </div>
        
        <div class="relative z-10 mt-2">
          <!-- Trend Indicator dengan Spacing yang Lebih Baik -->
          <div class="flex items-start justify-between mb-3">
            <span 
              class="text-xs font-bold px-2.5 py-1 rounded-full transition-all duration-300 flex items-center gap-1"
              :class="stat.change.startsWith('+') 
                ? 'text-emerald-700 bg-emerald-100' 
                : 'text-red-700 bg-red-100'"
            >
              <i :class="stat.change.startsWith('+') ? 'pi pi-trending-up' : 'pi pi-trending-down'" class="text-xs"></i>
              {{ stat.change }}
            </span>
          </div>
          
          <!-- Main Content dengan Spacing yang Diperbaiki -->
          <div class="space-y-1">
            <p class="text-xs lg:text-sm font-semibold text-gray-600 transition-colors duration-300 uppercase tracking-wide">{{ stat.title }}</p>
            <p class="text-2xl lg:text-3xl xl:text-4xl font-black text-gray-900 transition-colors duration-300 mb-1">{{ stat.value }}</p>
            <div class="flex items-center gap-1.5">
              <div class="w-1.5 h-1.5 rounded-full" :class="stat.change.startsWith('+') ? 'bg-emerald-500' : 'bg-red-500'"></div>
              <p class="text-xs text-gray-500 transition-colors duration-300">vs bulan lalu</p>
            </div>
          </div>
        </div>
        
        <!-- Animated Bottom Border -->
        <div class="absolute bottom-0 left-0 w-full h-1 bg-gradient-to-r opacity-0 group-hover:opacity-100 transition-all duration-300" :class="stat.gradientClass">
          <div class="h-full bg-gradient-to-r from-transparent via-white/30 to-transparent animate-pulse"></div>
        </div>
      </div>
    </div>

    <!-- Charts and Activities Row dengan Spacing yang Diperbaiki -->
    <div class="grid grid-cols-1 xl:grid-cols-3 gap-4 lg:gap-6 mb-6">
      <!-- Chart Section -->
      <div class="xl:col-span-2 bg-white rounded-2xl shadow-md border border-gray-100 p-4 lg:p-6 transition-all duration-300">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h3 class="text-lg lg:text-xl font-bold text-gray-900 transition-colors duration-300">Statistik Karyawan</h3>
            <p class="text-sm text-gray-500 mt-1">Tren pertumbuhan {{ selectedPeriod.label.toLowerCase() }}</p>
          </div>
          <Select 
            v-model="selectedPeriod" 
            :options="periodOptions" 
            optionLabel="label" 
            placeholder="Pilih Periode"
            class="w-40 lg:w-48 text-sm"
            @change="updateChartData"
          />
        </div>
        
        <!-- Chart dengan Spacing yang Diperbaiki -->
        <div class="space-y-4">
          <div v-for="(item, index) in chartData" :key="item.name" class="group">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center space-x-3">
                <div class="w-3 h-3 rounded-full shadow-sm" :class="getChartColor(index)"></div>
                <div>
                  <span class="text-sm font-semibold text-gray-700 transition-colors duration-300">{{ item.name }}</span>
                  <p class="text-xs text-gray-500">{{ getMonthYear(item.name) }}</p>
                </div>
              </div>
              <div class="text-right">
                <span class="text-lg font-bold text-gray-900 transition-colors duration-300">{{ item.value }}</span>
                <p class="text-xs text-gray-500">karyawan</p>
              </div>
            </div>
            <div class="relative">
              <div class="bg-gray-200 rounded-full h-3 transition-colors duration-300 overflow-hidden shadow-inner">
                <div 
                  class="h-3 rounded-full transition-all duration-1000 ease-out relative overflow-hidden shadow-sm"
                  :class="getChartGradient(index)"
                  :style="{ width: (item.value / Math.max(...chartData.map(d => d.value)) * 100) + '%' }"
                >
                  <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-pulse"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Chart Summary dengan Spacing yang Diperbaiki -->
        <div class="mt-6 pt-4 border-t border-gray-200">
          <div class="grid grid-cols-3 gap-3 lg:gap-4 text-center">
            <div class="p-3 lg:p-4 bg-gray-50 rounded-xl">
              <p class="text-xl lg:text-2xl xl:text-3xl font-black text-gray-900">{{ chartData.reduce((sum, item) => sum + item.value, 0) }}</p>
              <p class="text-xs text-gray-500 font-semibold uppercase tracking-wide">Total</p>
            </div>
            <div class="p-3 lg:p-4 bg-emerald-50 rounded-xl">
              <p class="text-xl lg:text-2xl xl:text-3xl font-black text-emerald-600">{{ Math.max(...chartData.map(d => d.value)) }}</p>
              <p class="text-xs text-emerald-600 font-semibold uppercase tracking-wide">Tertinggi</p>
            </div>
            <div class="p-3 lg:p-4 bg-blue-50 rounded-xl">
              <p class="text-xl lg:text-2xl xl:text-3xl font-black text-blue-600">{{ Math.round(chartData.reduce((sum, item) => sum + item.value, 0) / chartData.length) }}</p>
              <p class="text-xs text-blue-600 font-semibold uppercase tracking-wide">Rata-rata</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activities dengan Icon Spacing yang Diperbaiki -->
      <div class="bg-white rounded-2xl shadow-md border border-gray-100 p-4 lg:p-6 transition-all duration-300">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-bold text-gray-900 transition-colors duration-300">Aktivitas Terbaru</h3>
          <Button 
            @click="viewAllActivities" 
            icon="pi pi-list" 
            class="p-button-text p-button-sm text-emerald-600 hover:text-emerald-700 hover:bg-emerald-50 transition-all duration-200 rounded-lg w-8 h-8 p-0"
          />
        </div>
        
        <div class="space-y-3">
          <div 
            v-for="activity in recentActivities" 
            :key="activity.id"
            class="flex items-start space-x-3 p-3 rounded-xl hover:bg-gray-50 transition-all duration-200 group cursor-pointer border border-transparent hover:border-gray-200"
          >
            <div 
              class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 transition-all duration-200 group-hover:scale-105 shadow-sm"
              :class="activity.iconBg"
            >
              <i :class="activity.icon" class="text-sm"></i>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-semibold text-gray-900 transition-colors duration-300 truncate">{{ activity.name }}</p>
              <p class="text-xs text-gray-600 mt-0.5 transition-colors duration-300 line-clamp-2">{{ activity.activity }}</p>
              <p class="text-xs text-gray-500 mt-1 transition-colors duration-300 flex items-center gap-1">
                <i class="pi pi-clock text-xs"></i>
                {{ activity.time }}
              </p>
            </div>
          </div>
        </div>
        
        <!-- View All Button dengan Icon yang Diperbaiki -->
        <div class="mt-4 pt-3 border-t border-gray-200">
          <Button 
            @click="viewAllActivities"
            class="p-button-outlined w-full border-gray-200 text-gray-700 hover:border-emerald-300 hover:text-emerald-700 hover:bg-emerald-50 transition-all duration-200 rounded-lg font-medium text-sm h-9"
          >
            <i class="pi pi-external-link text-xs mr-2"></i>
            Lihat Semua Aktivitas
          </Button>
        </div>
      </div>
    </div>

    <!-- Quick Actions dengan Spacing yang Diperbaiki -->
    <div class="bg-white rounded-2xl shadow-md border border-gray-100 p-4 lg:p-6 transition-all duration-300">
      <h3 class="text-lg lg:text-xl font-bold text-gray-900 mb-4 lg:mb-6 transition-colors duration-300">Aksi Cepat</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3 lg:gap-4">
        <Button 
          v-for="action in quickActions" 
          :key="action.title"
          @click="action.action"
          class="p-button-outlined border-gray-200 text-gray-700 hover:border-emerald-300 hover:text-emerald-700 hover:bg-emerald-50 flex flex-col items-center justify-center p-4 h-24 lg:h-28 rounded-xl transition-all duration-200 hover:-translate-y-1 hover:shadow-md group"
        >
          <i :class="action.icon" class="text-2xl lg:text-3xl mb-2 group-hover:text-emerald-600 transition-all duration-200 group-hover:scale-110"></i>
          <span class="text-xs lg:text-sm font-medium text-center leading-tight">{{ action.title }}</span>
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useToast } from '@/composables/useToast'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

const toast = useToast()
const authStore = useAuthStore()
const router = useRouter()

// Period Selection
const selectedPeriod = ref({ label: '6 Bulan Terakhir', value: '6months' })
const periodOptions = ref([
  { label: '6 Bulan Terakhir', value: '6months' },
  { label: '1 Tahun', value: '1year' },
  { label: '2 Tahun', value: '2years' }
])

// Enhanced Stats Data
const stats = reactive([
  {
    title: "Total Karyawan",
    value: "247",
    icon: "pi pi-users",
    iconClass: "text-emerald-600 dark:text-emerald-400",
    bgClass: "bg-emerald-100 dark:bg-emerald-900/30",
    gradientClass: "from-emerald-500 to-emerald-600",
    change: "+12"
  },
  {
    title: "Karyawan Aktif",
    value: "235",
    icon: "pi pi-check-circle",
    iconClass: "text-blue-600 dark:text-blue-400",
    bgClass: "bg-blue-100 dark:bg-blue-900/30",
    gradientClass: "from-blue-500 to-blue-600",
    change: "+8"
  },
  {
    title: "Pengajuan Cuti",
    value: "18",
    icon: "pi pi-calendar",
    iconClass: "text-amber-600 dark:text-amber-400",
    bgClass: "bg-amber-100 dark:bg-amber-900/30",
    gradientClass: "from-amber-500 to-amber-600",
    change: "-5"
  },
  {
    title: "Cabang Aktif",
    value: "13",
    icon: "pi pi-building",
    iconClass: "text-purple-600 dark:text-purple-400",
    bgClass: "bg-purple-100 dark:bg-purple-900/30",
    gradientClass: "from-purple-500 to-purple-600",
    change: "+2"
  }
])

// Data chart yang lebih dinamis berdasarkan periode
const chartDataSets = {
  '6months': [
    { name: 'Jan', value: 8 },
    { name: 'Feb', value: 12 },
    { name: 'Mar', value: 6 },
    { name: 'Apr', value: 15 },
    { name: 'Mei', value: 10 },
    { name: 'Jun', value: 18 }
  ],
  '1year': [
    { name: 'Q1', value: 26 },
    { name: 'Q2', value: 43 },
    { name: 'Q3', value: 38 },
    { name: 'Q4', value: 52 }
  ],
  '2years': [
    { name: '2022', value: 159 },
    { name: '2023', value: 247 }
  ]
}

const chartData = ref(chartDataSets['6months'])

// Update chart data when period changes
const updateChartData = () => {
  chartData.value = chartDataSets[selectedPeriod.value.value] || chartDataSets['6months']
}

// Watch for period changes
watch(selectedPeriod, updateChartData, { deep: true })

// Helper function untuk format bulan/tahun
const getMonthYear = (name) => {
  const monthMap = {
    'Jan': 'Januari 2024',
    'Feb': 'Februari 2024',
    'Mar': 'Maret 2024',
    'Apr': 'April 2024',
    'Mei': 'Mei 2024',
    'Jun': 'Juni 2024',
    'Q1': 'Kuartal 1',
    'Q2': 'Kuartal 2',
    'Q3': 'Kuartal 3',
    'Q4': 'Kuartal 4',
    '2022': 'Tahun 2022',
    '2023': 'Tahun 2023'
  }
  return monthMap[name] || name
}

// Chart Color Functions
const getChartColor = (index) => {
  const colors = [
    'bg-emerald-500 dark:bg-emerald-400',
    'bg-blue-500 dark:bg-blue-400',
    'bg-purple-500 dark:bg-purple-400',
    'bg-amber-500 dark:bg-amber-400',
    'bg-pink-500 dark:bg-pink-400',
    'bg-indigo-500 dark:bg-indigo-400'
  ]
  return colors[index % colors.length]
}

const getChartGradient = (index) => {
  const gradients = [
    'bg-gradient-to-r from-emerald-500 to-emerald-600 dark:from-emerald-600 dark:to-emerald-700',
    'bg-gradient-to-r from-blue-500 to-blue-600 dark:from-blue-600 dark:to-blue-700',
    'bg-gradient-to-r from-purple-500 to-purple-600 dark:from-purple-600 dark:to-purple-700',
    'bg-gradient-to-r from-amber-500 to-amber-600 dark:from-amber-600 dark:to-amber-700',
    'bg-gradient-to-r from-pink-500 to-pink-600 dark:from-pink-600 dark:to-pink-700',
    'bg-gradient-to-r from-indigo-500 to-indigo-600 dark:from-indigo-600 dark:to-indigo-700'
  ]
  return gradients[index % gradients.length]
}

// Enhanced Recent Activities Data
const recentActivities = ref([
  {
    id: 1,
    name: "Andi Pratama",
    activity: "mengajukan cuti tahunan (5 hari)",
    time: "2 menit yang lalu",
    icon: "pi pi-file-edit",
    iconBg: "bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400"
  },
  {
    id: 2,
    name: "HR Admin",
    activity: "menambahkan karyawan baru: Siti Nurhaliza",
    time: "15 menit yang lalu",
    icon: "pi pi-user-plus",
    iconBg: "bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400"
  },
  {
    id: 3,
    name: "Budi Santoso",
    activity: "memperbarui data profil",
    time: "1 jam yang lalu",
    icon: "pi pi-user-edit",
    iconBg: "bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400"
  },
  {
    id: 4,
    name: "Maya Sari",
    activity: "dipromosikan menjadi Senior Developer",
    time: "2 jam yang lalu",
    icon: "pi pi-star",
    iconBg: "bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400"
  }
])

// Quick Actions Data
const quickActions = ref([
  {
    title: "Tambah Karyawan",
    icon: "pi pi-user-plus",
    action: () => router.push('/user-management/list')
  },
  {
    title: "Kelola Cuti",
    icon: "pi pi-calendar",
    action: () => toast.info('Info', 'Fitur kelola cuti akan segera tersedia')
  },
  {
    title: "Laporan",
    icon: "pi pi-chart-bar",
    action: () => exportData()
  },
  {
    title: "Pengaturan",
    icon: "pi pi-cog",
    action: () => router.push('/pengaturan')
  }
])

// Functions
const isLoading = ref(false)
const isInitialLoad = ref(true)
const lastLoadTime = ref(null)

const loadDashboardData = async (showToast = false) => {
  try {
    isLoading.value = true
    
    if (showToast) {
      toast.info('Loading...', 'Sedang memuat data dashboard')
    }
    
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Update stats dengan data terbaru
    stats[0].value = Math.floor(Math.random() * 50) + 200
    stats[1].value = Math.floor(Math.random() * 30) + 180
    stats[2].value = Math.floor(Math.random() * 20) + 10
    stats[3].value = Math.floor(Math.random() * 5) + 10
    
    // Update chart data based on selected period
    updateChartData()
    
    lastLoadTime.value = new Date()
    isInitialLoad.value = false
    
    if (showToast) {
      toast.success('Berhasil!', 'Data dashboard berhasil dimuat')
    }
  } catch (error) {
    toast.error('Error', 'Gagal memuat data dashboard')
  } finally {
    isLoading.value = false
  }
}

// Load data saat komponen pertama kali dibuka (tanpa toast)
onMounted(() => {
  loadDashboardData(false) // Silent loading untuk initial load
})

// Manual refresh dengan toast
const refreshData = async () => {
  await loadDashboardData(true) // Dengan toast untuk manual refresh
}

const exportData = async () => {
  try {
    toast.info('Processing...', 'Sedang menyiapkan file export')
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    const csvData = [
      ['Kategori', 'Jumlah', 'Perubahan'],
      ['Total Karyawan', stats[0].value, stats[0].change],
      ['Karyawan Aktif', stats[1].value, stats[1].change],
      ['Pengajuan Cuti', stats[2].value, stats[2].change],
      ['Cabang Aktif', stats[3].value, stats[3].change]
    ]
    
    const csvContent = csvData.map(row => row.join(',')).join('\n')
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    
    if (link.download !== undefined) {
      const url = URL.createObjectURL(blob)
      link.setAttribute('href', url)
      link.setAttribute('download', `dashboard-data-${new Date().toISOString().split('T')[0]}.csv`)
      link.style.visibility = 'hidden'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
    
    toast.success('Berhasil!', 'Data berhasil diekspor ke CSV')
  } catch (error) {
    toast.error('Gagal', 'Gagal mengekspor data')
  }
}

const viewAllActivities = () => {
  toast.info('Info', 'Fitur lihat semua aktivitas akan segera tersedia')
}
</script>

<style scoped>
.dashboard-container {
  padding: 12px;
}

@media (min-width: 1024px) {
  .dashboard-container {
    padding: 20px;
  }
}

@media (max-width: 640px) {
  .dashboard-container {
    padding: 8px;
  }
}

/* Fixed refresh button styling */
.refresh-button {
  position: relative;
  overflow: hidden;
}

.refresh-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.refresh-button .p-button-icon {
  transition: transform 0.3s ease !important;
}

.refresh-button:not(:disabled):hover .p-button-icon {
  transform: rotate(180deg);
}

/* Enhanced hover effects dengan animasi yang lebih halus */
.group:hover {
  transform: translateY(-4px) scale(1.01);
}

/* Line clamp utility */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Smooth gradient animation */
@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.animate-shimmer {
  animation: shimmer 2s infinite;
}

/* Better mobile spacing */
@media (max-width: 768px) {
  .space-y-4 > * + * {
    margin-top: 0.75rem;
  }
  
  .space-y-3 > * + * {
    margin-top: 0.5rem;
  }
}

/* Prevent layout shift during loading */
.p-button {
  display: flex;
  align-items: center;
  justify-content: center;
}

.p-button .p-button-icon {
  transition: none !important;
}

.p-button.p-button-loading .p-button-icon {
  animation: none !important;
}

/* Improved responsive design */
@media (max-width: 640px) {
  .grid {
    gap: 0.75rem;
  }
}

@media (min-width: 641px) and (max-width: 1024px) {
  .grid {
    gap: 1rem;
  }
}

/* Better icon spacing - Perbaikan jarak icon */
.p-button .p-button-icon {
  margin-right: 0.5rem !important; /* Ubah dari 1.5rem menjadi 0.5rem agar sama dengan mr-2 */
}

.p-button[data-pc-section="root"] .p-button-icon:last-child {
  margin-right: 0;
  margin-left: 0.5rem !important; /* Ubah dari 0.75rem menjadi 0.5rem untuk konsistensi */
}

/* Khusus untuk tombol dengan iconPos="right" */
.p-button .p-button-label + .p-button-icon {
  margin-left: 0.5rem !important; /* Ubah dari 0.75rem menjadi 0.5rem */
  margin-right: 0;
}

/* Styling khusus untuk tombol "Lihat Semua Aktivitas" */
.p-button-outlined .p-button-icon {
  margin-left: 0.5rem !important; /* Ubah dari 0.75rem menjadi 0.5rem */
}

.p-button .p-button-icon {
  transition: none !important;
}

.p-button.p-button-loading .p-button-icon {
  animation: none !important;
}

/* Improved responsive design */
@media (max-width: 640px) {
  .grid {
    gap: 0.75rem;
  }
}

@media (min-width: 641px) and (max-width: 1024px) {
  .grid {
    gap: 1rem;
  }
}
</style>
