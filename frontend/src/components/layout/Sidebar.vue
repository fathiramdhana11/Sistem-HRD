<template>
  <aside 
    class="bg-white border-r border-gray-200 flex flex-col h-screen relative z-10 shadow-lg transition-all duration-300 ease-in-out"
    :class="{ 'w-64': !isCollapsed, 'w-16': isCollapsed }"
  >
    <!-- Header -->
    <div class="p-4 border-b border-gray-100 bg-gradient-to-r from-emerald-500 to-emerald-600">
      <div class="flex items-center justify-between">
        <div v-if="!isCollapsed" class="flex items-center space-x-3">
          <div class="w-8 h-8 bg-white rounded-lg flex items-center justify-center">
            <i class="pi pi-users text-emerald-600 text-lg"></i>
          </div>
          <div>
            <h1 class="text-white font-bold text-lg">Sistem HRD</h1>
            <p class="text-emerald-100 text-xs">Management Portal</p>
          </div>
        </div>
        <div v-else class="w-full flex justify-center">
          <div class="w-8 h-8 bg-white rounded-lg flex items-center justify-center">
            <i class="pi pi-users text-emerald-600 text-lg"></i>
          </div>
        </div>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 overflow-y-auto py-4">
      <div class="px-3 space-y-1">
        <MenuItem 
          v-for="item in menuItems" 
          :key="item.name"
          :item="item"
          :isCollapsed="isCollapsed"
        />
      </div>
    </nav>

    <!-- User Profile -->
    <div class="p-4 border-t border-gray-100">
      <div 
        v-if="!isCollapsed"
        class="group flex items-center px-4 py-3 rounded-xl text-gray-700 hover:bg-emerald-50 hover:text-emerald-700 font-medium cursor-pointer transition-all duration-200 ease-in-out transform hover:scale-[1.02]"
        @click="logout"
      >
        <i class="pi pi-sign-out text-lg mr-3 group-hover:text-emerald-600 transition-colors duration-200"></i>
        <span class="text-sm">Logout</span>
      </div>
      <div v-else class="flex justify-center">
        <button 
          @click="logout"
          class="w-10 h-10 rounded-lg bg-gray-100 hover:bg-emerald-50 text-gray-600 hover:text-emerald-600 transition-all duration-200 flex items-center justify-center"
        >
          <i class="pi pi-sign-out text-lg"></i>
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useInterfaceStore } from '@/stores/interfaceStore'
import MenuItem from './MenuItem.vue'

const router = useRouter()
const authStore = useAuthStore()
const interfaceStore = useInterfaceStore()

// Menggunakan state dari interfaceStore yang dikontrol oleh header
const isCollapsed = computed(() => interfaceStore.isSidebarCollapsed)

const logout = async () => {
  await authStore.logout()
  router.push('/login')
}

const menuItems = [
  {
    name: 'Dashboard',
    icon: 'pi pi-home',
    route: '/dashboard',
    active: true
  },
  {
    name: 'Manajemen Karyawan',
    icon: 'pi pi-users',
    children: [
      { name: 'Data Karyawan', route: '/karyawan/data' },
      { name: 'Tambah Karyawan', route: '/karyawan/tambah' }
    ]
  },
  {
    name: 'Manajemen Absensi',
    icon: 'pi pi-calendar',
    children: [
      { name: 'Rekap Absensi', route: '/absensi/rekap' },
      { name: 'Input Manual Absensi', route: '/absensi/input' }
    ]
  },
  {
    name: 'Izin dan Cuti',
    icon: 'pi pi-calendar-times',
    children: [
      { name: 'Form Cuti', route: '/izin/cuti' },
      { name: 'Form Sakit', route: '/izin/sakit' }
    ]
  },
  {
    name: 'Penggajian',
    icon: 'pi pi-money-bill',
    children: [
      { name: 'Gaji Bulanan', route: '/penggajian/bulanan' },
      { name: 'Komponen Gaji', route: '/penggajian/komponen' }
    ]
  },
  {
    name: 'Slip Gaji',
    icon: 'pi pi-file-pdf',
    route: '/slip-gaji'
  },
  {
    name: 'Laporan',
    icon: 'pi pi-chart-bar',
    children: [
      { name: 'Laporan Absensi', route: '/laporan/absensi' },
      { name: 'Laporan Gaji', route: '/laporan/gaji' }
    ]
  },
  {
    name: 'Manajemen User',
    icon: 'pi pi-user-edit',
    children: [
      { name: 'Daftar User', route: '/user-management/list' },
      { name: 'Role Akses', route: '/user-management/roles' }
    ]
  },
  {
    name: 'Log Aktivitas',
    icon: 'pi pi-history',
    route: '/logs'
  },
  {
    name: 'Pengaturan',
    icon: 'pi pi-cog',
    route: '/pengaturan'
  }
]
</script>
