<template>
  <div class="log-aktivitas-container bg-gray-50 min-h-screen">
    <!-- Header Section -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-6">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 mb-2">Log Aktivitas</h1>
          <p class="text-gray-600">Pantau semua aktivitas sistem dan pengguna</p>
        </div>
        <div class="flex space-x-3 mt-4 sm:mt-0">
          <Button 
            @click="refreshLogs" 
            icon="pi pi-refresh" 
            label="Refresh" 
            class="p-button-outlined border-emerald-200 text-emerald-600 hover:bg-emerald-50 hover:border-emerald-300"
            size="small"
          />
          <Button 
            @click="exportLogs" 
            icon="pi pi-download" 
            label="Export" 
            class="bg-gradient-to-r from-emerald-500 to-emerald-600 border-0 hover:from-emerald-600 hover:to-emerald-700 shadow-lg"
            size="small"
          />
        </div>
      </div>
    </div>

    <!-- Filter Section -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Tanggal Mulai</label>
          <DatePicker 
            v-model="filters.startDate" 
            placeholder="Pilih tanggal"
            class="w-full"
            dateFormat="dd/mm/yy"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Tanggal Akhir</label>
          <DatePicker 
            v-model="filters.endDate" 
            placeholder="Pilih tanggal"
            class="w-full"
            dateFormat="dd/mm/yy"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Jenis Aktivitas</label>
          <Select 
            v-model="filters.activityType" 
            :options="activityTypes" 
            optionLabel="label" 
            optionValue="value"
            placeholder="Semua Aktivitas"
            class="w-full"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Pengguna</label>
          <InputText 
            v-model="filters.user" 
            placeholder="Cari pengguna..."
            class="w-full"
          />
        </div>
      </div>
      <div class="flex justify-end mt-4 space-x-2">
        <Button 
          @click="clearFilters" 
          label="Reset" 
          class="p-button-outlined border-gray-200 text-gray-600 hover:bg-gray-50"
          size="small"
        />
        <Button 
          @click="applyFilters" 
          label="Terapkan Filter" 
          class="bg-emerald-600 border-0 hover:bg-emerald-700"
          size="small"
        />
      </div>
    </div>

    <!-- Logs Table -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
      <DataTable 
        :value="logs" 
        :paginator="true" 
        :rows="20"
        :loading="loading"
        class="p-datatable-sm"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        :rowsPerPageOptions="[10, 20, 50]"
        currentPageReportTemplate="Menampilkan {first} sampai {last} dari {totalRecords} log"
        responsiveLayout="scroll"
      >
        <Column field="timestamp" header="Waktu" sortable class="min-w-40">
          <template #body="{ data }">
            <div class="flex flex-col">
              <span class="font-medium text-gray-900">{{ formatDate(data.timestamp) }}</span>
              <span class="text-xs text-gray-500">{{ formatTime(data.timestamp) }}</span>
            </div>
          </template>
        </Column>
        
        <Column field="user" header="Pengguna" sortable class="min-w-32">
          <template #body="{ data }">
            <div class="flex items-center space-x-2">
              <div class="w-8 h-8 bg-emerald-100 rounded-full flex items-center justify-center">
                <i class="pi pi-user text-emerald-600 text-sm"></i>
              </div>
              <span class="font-medium text-gray-900">{{ data.user }}</span>
            </div>
          </template>
        </Column>
        
        <Column field="activity" header="Aktivitas" sortable class="min-w-48">
          <template #body="{ data }">
            <div class="flex items-center space-x-2">
              <div :class="getActivityIcon(data.type).bgClass" class="w-8 h-8 rounded-lg flex items-center justify-center">
                <i :class="[getActivityIcon(data.type).icon, getActivityIcon(data.type).colorClass]" class="text-sm"></i>
              </div>
              <span class="text-gray-900">{{ data.activity }}</span>
            </div>
          </template>
        </Column>
        
        <Column field="type" header="Jenis" sortable class="min-w-28">
          <template #body="{ data }">
            <Tag 
              :value="data.type" 
              :severity="getActivitySeverity(data.type)"
              class="text-xs font-medium"
            />
          </template>
        </Column>
        
        <Column field="ip_address" header="IP Address" class="min-w-32">
          <template #body="{ data }">
            <span class="text-gray-600 font-mono text-sm">{{ data.ip_address }}</span>
          </template>
        </Column>
        
        <Column field="details" header="Detail" class="min-w-48">
          <template #body="{ data }">
            <span class="text-gray-600 text-sm">{{ data.details || '-' }}</span>
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useToast } from '@/composables/useToast'
import { format } from 'date-fns'
import { id } from 'date-fns/locale'

const toast = useToast()

// Reactive data
const loading = ref(false)
const logs = ref([])

// Filters
const filters = reactive({
  startDate: null,
  endDate: null,
  activityType: null,
  user: ''
})

// Activity types for filter
const activityTypes = ref([
  { label: 'Login', value: 'login' },
  { label: 'Logout', value: 'logout' },
  { label: 'Create', value: 'create' },
  { label: 'Update', value: 'update' },
  { label: 'Delete', value: 'delete' },
  { label: 'View', value: 'view' },
  { label: 'Export', value: 'export' }
])

// Sample data - replace with actual API call
const sampleLogs = [
  {
    id: 1,
    timestamp: new Date('2024-01-15 10:30:00'),
    user: 'Admin User',
    activity: 'Login ke sistem',
    type: 'login',
    ip_address: '192.168.1.100',
    details: 'Login berhasil'
  },
  {
    id: 2,
    timestamp: new Date('2024-01-15 10:35:00'),
    user: 'HR Manager',
    activity: 'Menambah data karyawan baru',
    type: 'create',
    ip_address: '192.168.1.101',
    details: 'Karyawan: John Doe'
  },
  {
    id: 3,
    timestamp: new Date('2024-01-15 11:00:00'),
    user: 'Admin User',
    activity: 'Export laporan absensi',
    type: 'export',
    ip_address: '192.168.1.100',
    details: 'Periode: Januari 2024'
  },
  {
    id: 4,
    timestamp: new Date('2024-01-15 11:15:00'),
    user: 'HR Staff',
    activity: 'Update data karyawan',
    type: 'update',
    ip_address: '192.168.1.102',
    details: 'Karyawan: Jane Smith'
  },
  {
    id: 5,
    timestamp: new Date('2024-01-15 11:30:00'),
    user: 'HR Manager',
    activity: 'Hapus data karyawan',
    type: 'delete',
    ip_address: '192.168.1.101',
    details: 'Karyawan: Old Employee'
  }
]

// Methods
const fetchLogs = async () => {
  loading.value = true
  try {
    // TODO: Replace with actual API call
    // const response = await logService.getLogs(filters)
    // logs.value = response.data
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    logs.value = sampleLogs
    
  } catch (error) {
    console.error('Error fetching logs:', error)
    toast.error('Gagal memuat data log aktivitas')
  } finally {
    loading.value = false
  }
}

const refreshLogs = () => {
  fetchLogs()
  toast.success('Data log berhasil diperbarui')
}

const exportLogs = () => {
  // TODO: Implement export functionality
  toast.info('Fitur export sedang dalam pengembangan')
}

const applyFilters = () => {
  fetchLogs()
}

const clearFilters = () => {
  filters.startDate = null
  filters.endDate = null
  filters.activityType = null
  filters.user = ''
  fetchLogs()
}

const formatDate = (date) => {
  return format(new Date(date), 'dd MMM yyyy', { locale: id })
}

const formatTime = (date) => {
  return format(new Date(date), 'HH:mm:ss')
}

const getActivityIcon = (type) => {
  const icons = {
    login: { icon: 'pi pi-sign-in', colorClass: 'text-green-600', bgClass: 'bg-green-100' },
    logout: { icon: 'pi pi-sign-out', colorClass: 'text-red-600', bgClass: 'bg-red-100' },
    create: { icon: 'pi pi-plus', colorClass: 'text-blue-600', bgClass: 'bg-blue-100' },
    update: { icon: 'pi pi-pencil', colorClass: 'text-amber-600', bgClass: 'bg-amber-100' },
    delete: { icon: 'pi pi-trash', colorClass: 'text-red-600', bgClass: 'bg-red-100' },
    view: { icon: 'pi pi-eye', colorClass: 'text-gray-600', bgClass: 'bg-gray-100' },
    export: { icon: 'pi pi-download', colorClass: 'text-purple-600', bgClass: 'bg-purple-100' }
  }
  return icons[type] || { icon: 'pi pi-info-circle', colorClass: 'text-gray-600', bgClass: 'bg-gray-100' }
}

const getActivitySeverity = (type) => {
  const severities = {
    login: 'success',
    logout: 'info',
    create: 'success',
    update: 'warning',
    delete: 'danger',
    view: 'info',
    export: 'info'
  }
  return severities[type] || 'info'
}

// Lifecycle
onMounted(() => {
  fetchLogs()
})
</script>

<style scoped>
/* Custom styles if needed */
.log-aktivitas-container {
  padding: 1.5rem;
}

@media (max-width: 768px) {
  .log-aktivitas-container {
    padding: 1rem;
  }
}
</style>