<template>
  <header class="bg-white border-b border-emerald-300 px-6 py-4 flex items-center justify-between shadow-sm">
    <!-- Left Section -->
    <div class="flex items-center space-x-4">
      <!-- Sidebar Toggle -->
      <Button 
        @click="toggleSidebar" 
        icon="pi pi-bars" 
        class="p-button-text p-button-rounded !border-emerald-500 !bg-emerald-50 text-emerald-700 hover:!bg-emerald-100 hover:!border-emerald-600 focus:!outline-none focus:!ring-2 focus:!ring-emerald-200 focus:!border-emerald-500 active:!bg-emerald-200 !w-10 !h-10 !p-0 flex items-center justify-center transition-all duration-200"
        v-tooltip.bottom="'Toggle Menu'"
      />
      
      <!-- Search Bar -->
      <div class="hidden md:flex relative flex-1 max-w-md">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none z-10">
          <i class="pi pi-search text-emerald-500 text-sm"></i>
        </div>
        <input 
          v-model="searchQuery" 
          type="text"
          placeholder="Cari karyawan, dokumen..."
          class="w-full pl-10 pr-4 py-2.5 border border-emerald-300 rounded-lg focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 focus:outline-none text-sm transition-all duration-200 bg-white"
        />
      </div>
    </div>

    <!-- Right Section -->
    <div class="flex items-center space-x-3">
      <!-- Mobile Search -->
      <Button 
        @click="toggleMobileSearch" 
        icon="pi pi-search" 
        class="md:hidden p-button-text p-button-rounded !border-emerald-500 !bg-emerald-50 text-emerald-700 hover:!bg-emerald-100 hover:!border-emerald-600 focus:!outline-none focus:!ring-2 focus:!ring-emerald-200 focus:!border-emerald-500 active:!bg-emerald-200 !w-10 !h-10 !p-0 flex items-center justify-center transition-all duration-200"
        v-tooltip.bottom="'Cari'"
      />
      
      <!-- Notifications -->
      <div class="relative">
        <Button 
          @click="toggleNotifications" 
          icon="pi pi-bell" 
          class="p-button-text p-button-rounded !border-emerald-500 !bg-emerald-50 text-emerald-700 hover:!bg-emerald-100 hover:!border-emerald-600 focus:!outline-none focus:!ring-2 focus:!ring-emerald-200 focus:!border-emerald-500 active:!bg-emerald-200 !w-10 !h-10 !p-0 flex items-center justify-center transition-all duration-200"
          v-tooltip.bottom="'Notifikasi'"
        />
        <span 
          v-if="notificationCount > 0"
          class="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full min-w-[18px] h-[18px] flex items-center justify-center leading-none"
        >
          {{ notificationCount }}
        </span>
      </div>
      
      <!-- Administrator Menu -->
      <div class="relative">
        <Button 
          @click="toggleUserMenu" 
          class="p-button-text !border-emerald-500 !bg-emerald-50 hover:!bg-emerald-100 hover:!border-emerald-600 focus:!outline-none focus:!ring-2 focus:!ring-emerald-200 focus:!border-emerald-500 active:!bg-emerald-200 px-3 py-2 rounded-lg transition-all duration-200"
          v-tooltip.bottom="'Menu Pengguna'"
        >
          <div class="flex items-center space-x-3">
            <Avatar 
              label="A" 
              class="bg-emerald-600 text-white w-8 h-8 text-sm font-semibold"
              shape="circle"
            />
            <span class="text-sm font-medium text-emerald-700 hidden lg:block">Administrator</span>
            <i class="pi pi-chevron-down text-xs text-emerald-600 hidden lg:block transition-transform duration-200 ml-1"></i>
          </div>
        </Button>
      </div>
    </div>

    <!-- Mobile Search Overlay -->
    <div 
      v-if="showMobileSearch"
      class="absolute top-full left-0 right-0 bg-white border-b border-emerald-200 p-4 md:hidden z-40 shadow-sm"
    >
      <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none z-10">
          <i class="pi pi-search text-emerald-500 text-sm"></i>
        </div>
        <input 
          v-model="searchQuery" 
          type="text"
          placeholder="Cari karyawan, dokumen..."
          class="w-full pl-10 pr-4 py-2.5 border border-emerald-300 rounded-lg focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 focus:outline-none text-sm transition-all duration-200 bg-white"
          @blur="hideMobileSearch"
          ref="mobileSearchInput"
        />
      </div>
    </div>
  </header>

  <!-- User Menu Popover -->
  <Teleport to="body">
    <Popover ref="userMenu" class="z-50">
      <div class="bg-white rounded-xl shadow-xl border border-emerald-200 overflow-hidden w-56">
        <!-- Header -->
        <div class="bg-gradient-to-r from-emerald-500 to-emerald-600 p-4 text-white">
          <div class="flex items-center space-x-3">
            <Avatar 
              label="A" 
              class="bg-white/20 text-white w-10 h-10 font-semibold"
              shape="circle"
            />
            <div>
              <p class="font-semibold">Administrator</p>
              <p class="text-sm text-emerald-100">Super Admin</p>
            </div>
          </div>
        </div>
        
        <!-- Menu Items -->
        <div class="p-2">
          <div 
            v-for="item in userMenuItems" 
            :key="item.label"
            @click="item.command"
            class="flex items-center space-x-3 p-3 text-gray-700 hover:bg-emerald-50 hover:text-emerald-700 rounded-lg cursor-pointer transition-all duration-200 group"
          >
            <i :class="item.icon" class="text-gray-500 group-hover:text-emerald-600 w-4 transition-colors duration-200"></i>
            <span class="text-sm font-medium">{{ item.label }}</span>
          </div>
        </div>
      </div>
    </Popover>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useInterfaceStore } from '@/stores/interfaceStore'
import { useAuthStore } from '@/stores/authStore'
import Popover from 'primevue/popover'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Avatar from 'primevue/avatar'
import Badge from 'primevue/badge'

const router = useRouter()
const searchQuery = ref('')
const showMobileSearch = ref(false)
const mobileSearchInput = ref(null)
const interfaceStore = useInterfaceStore()
const authStore = useAuthStore()
const userMenu = ref()
const notificationCount = ref(3)

const userMenuItems = ref([
  {
    label: 'Profil Saya',
    icon: 'pi pi-user',
    command: () => {
      userMenu.value.hide()
      router.push('/profile')
    }
  },
  {
    label: 'Pengaturan',
    icon: 'pi pi-cog',
    command: () => {
      userMenu.value.hide()
      router.push('/settings')
    }
  },
  {
    label: 'Bantuan',
    icon: 'pi pi-question-circle',
    command: () => {
      userMenu.value.hide()
    }
  },
  {
    label: 'Keluar',
    icon: 'pi pi-sign-out',
    command: () => {
      userMenu.value.hide()
      logout()
    }
  }
])

const toggleSidebar = () => {
  interfaceStore.toggleSidebar()
}

const toggleUserMenu = (event) => {
  userMenu.value.toggle(event)
}

const toggleNotifications = () => {
  console.log('Toggle notifications')
}

const toggleMobileSearch = async () => {
  showMobileSearch.value = !showMobileSearch.value
  if (showMobileSearch.value) {
    await nextTick()
    mobileSearchInput.value?.$el?.focus()
  }
}

const hideMobileSearch = () => {
  setTimeout(() => {
    showMobileSearch.value = false
  }, 150)
}

const logout = async () => {
  try {
    await authStore.logout()
  } catch (error) {
    console.error('Logout error:', error)
    router.push('/login')
  }
}
</script>

<style scoped>
:deep(.p-popover) {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  padding: 0 !important;
}

:deep(.p-popover-content) {
  padding: 0 !important;
  background: transparent !important;
}
</style>