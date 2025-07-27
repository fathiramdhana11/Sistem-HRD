<template>
  <!-- Header dengan styling yang sama persis seperti sebelumnya -->
  <header class="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between shadow-sm">
    <!-- Bagian Kiri: Logo + Toggle + Search -->
    <div class="flex items-center space-x-4">
      <!-- Toggle Sidebar - Menggunakan PrimeVue Button langsung -->
      <Button 
        icon="pi pi-bars"
        class="p-button-text p-button-rounded header-btn"
        @click="toggleSidebar"
        v-tooltip.bottom="'Toggle Menu'"
      />
      
      <!-- Search Bar -->
      <div class="hidden md:flex relative flex-1 max-w-md">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <i class="pi pi-search text-gray-400 text-sm"></i>
        </div>
        <InputText
          v-model="searchQuery"
          placeholder="Cari karyawan, dokumen..."
          class="search-input"
        />
      </div>
    </div>

    <!-- Bagian Kanan: Notifikasi + User Menu -->
    <div class="flex items-center space-x-3">
      <!-- Mobile Search Toggle -->
      <Button 
        icon="pi pi-search"
        class="p-button-text p-button-rounded header-btn md:hidden"
        @click="toggleMobileSearch"
        v-tooltip.bottom="'Cari'"
      />
      
      <!-- Notifikasi -->
      <div class="relative">
        <Button 
          icon="pi pi-bell"
          class="p-button-text p-button-rounded header-btn"
          v-tooltip.bottom="'Notifikasi'"
        />
        <!-- Badge notifikasi -->
        <span class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">3</span>
      </div>
      
      <!-- User Menu -->
      <div class="relative">
        <Button 
          @click="toggleUserMenu"
          v-tooltip.bottom="'Menu Pengguna'"
          class="p-button-text border border-emerald-500 bg-emerald-50 text-emerald-700 hover:bg-emerald-100 hover:border-emerald-600 focus:ring-emerald-200 active:bg-emerald-200 rounded-lg px-3 py-2 h-auto"
        >
          <div class="flex items-center space-x-2">
            <Avatar 
              label="A" 
              class="bg-emerald-600 text-white w-8 h-8 text-sm font-semibold"
              shape="circle"
            />
            <span class="text-sm font-medium text-emerald-700 hidden lg:block">Administrator</span>
            <i class="pi pi-chevron-down text-xs text-emerald-600 hidden lg:block"></i>
          </div>
        </Button>
        
        <!-- User Menu Dropdown -->
        <UserMenuDropdown 
          v-if="showUserMenu"
          @close="showUserMenu = false"
          @logout="handleLogout"
        />
      </div>
    </div>

    <!-- Mobile Search Overlay -->
    <Transition name="slide-down">
      <div 
        v-if="showMobileSearch"
        class="absolute top-full left-0 right-0 bg-white border-b border-gray-200 p-4 md:hidden z-40 shadow-sm"
      >
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <i class="pi pi-search text-gray-400 text-sm"></i>
          </div>
          <InputText
            v-model="searchQuery"
            placeholder="Cari karyawan, dokumen..."
            class="search-input"
            @blur="hideMobileSearch"
            ref="mobileSearchInput"
          />
        </div>
      </div>
    </Transition>
  </header>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { useInterfaceStore } from '@/stores/interfaceStore'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'
import UserMenuDropdown from '@/components/layout/UserMenuDropdown.vue'

// Stores dan Router
const interfaceStore = useInterfaceStore()
const authStore = useAuthStore()
const router = useRouter()

// Reactive Data
const searchQuery = ref('')
const showMobileSearch = ref(false)
const showUserMenu = ref(false)
const mobileSearchInput = ref(null)

// Methods - Dengan komentar yang jelas
const toggleSidebar = () => {
  // Toggle status sidebar collapse
  interfaceStore.toggleSidebar()
}

const toggleMobileSearch = async () => {
  // Toggle mobile search dan focus input
  showMobileSearch.value = !showMobileSearch.value
  if (showMobileSearch.value) {
    await nextTick()
    mobileSearchInput.value?.$el?.focus()
  }
}

const hideMobileSearch = () => {
  // Sembunyikan mobile search dengan delay
  setTimeout(() => {
    showMobileSearch.value = false
  }, 150)
}

const toggleUserMenu = () => {
  // Toggle user menu dropdown
  showUserMenu.value = !showUserMenu.value
}

const handleLogout = async () => {
  // Proses logout dengan error handling
  try {
    await authStore.logout()
    router.push('/login')
  } catch (error) {
    console.error('Logout error:', error)
  }
}
</script>

<style scoped>
/* Animasi untuk mobile search */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>