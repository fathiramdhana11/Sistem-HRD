<template>
  <Teleport to="body">
    <div 
      class="fixed inset-0 z-50"
      @click="$emit('close')"
    >
      <div class="absolute top-16 right-6">
        <div class="bg-white rounded-xl shadow-xl border border-emerald-200 overflow-hidden w-56 animate-fade-in">
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
              v-for="item in menuItems" 
              :key="item.label"
              @click="handleMenuClick(item)"
              class="flex items-center space-x-3 p-3 text-gray-700 hover:bg-emerald-50 hover:text-emerald-700 rounded-lg cursor-pointer transition-all duration-200 group"
            >
              <i :class="[item.icon, 'text-lg group-hover:text-emerald-600 transition-colors duration-200']"></i>
              <span class="font-medium">{{ item.label }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

// Emits
const emit = defineEmits(['close', 'logout'])

// Router
const router = useRouter()

// Menu items
const menuItems = computed(() => [
  {
    label: 'Profil Saya',
    icon: 'pi pi-user',
    action: 'profile'
  },
  {
    label: 'Pengaturan',
    icon: 'pi pi-cog',
    action: 'settings'
  },
  {
    label: 'Bantuan',
    icon: 'pi pi-question-circle',
    action: 'help'
  },
  {
    label: 'Keluar',
    icon: 'pi pi-sign-out',
    action: 'logout'
  }
])

// Methods
const handleMenuClick = (item) => {
  emit('close')
  
  switch (item.action) {
    case 'profile':
      router.push('/profile')
      break
    case 'settings':
      router.push('/settings')
      break
    case 'help':
      router.push('/help')
      break
    case 'logout':
      emit('logout')
      break
    default:
      console.log(`Menu ${item.label} clicked`)
  }
}
</script>