<template>
  <header class="bg-white h-16 flex items-center justify-between px-6 border-b border-slate-200 shrink-0">
    <div class="flex items-center space-x-4">
      <button @click="interfaceStore.toggleSidebar" class="p-2 rounded-full text-slate-500 hover:bg-slate-100 focus:outline-none">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h7" />
        </svg>
      </button>

      <div class="relative hidden sm:block">
        <span class="absolute inset-y-0 left-0 flex items-center pl-3">
          <MagnifyingGlassIcon class="w-5 h-5 text-slate-400" />
        </span>
        <input 
          type="text"
          placeholder="Cari..."
          class="w-64 pl-10 pr-4 py-2 bg-slate-100 border border-transparent rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
    </div>

    <div class="flex items-center space-x-5">
      <button class="relative text-slate-500 hover:text-slate-700">
        <span class="absolute -top-1 -right-1 flex h-3 w-3">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
        </span>
        <BellIcon class="w-6 h-6" />
      </button>

      <div class="h-6 w-px bg-slate-200"></div>

      <div class="relative">
        <button @click="toggleDropdown" class="flex items-center space-x-2">
          <img class="h-9 w-9 rounded-full object-cover" src="https://i.pravatar.cc/100" alt="User Avatar">
          <span class="hidden sm:inline text-sm font-medium text-slate-700">{{ user.username }}</span>
          <ChevronDownIcon class="w-4 h-4 text-slate-500 hidden sm:inline" />
        </button>
        <div v-if="isDropdownOpen" class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl z-20 border border-slate-200/80 py-1">
          <router-link to="/profile" class="block px-4 py-2 text-sm text-slate-700 hover:bg-slate-100">Profil</router-link>
          <button @click="logout" class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50">Logout</button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { MagnifyingGlassIcon, BellIcon, ChevronDownIcon } from '@heroicons/vue/24/outline';
import { useInterfaceStore } from '@/stores/interfaceStore'; 

const router = useRouter();
const user = ref({});
const isDropdownOpen = ref(false);
const interfaceStore = useInterfaceStore();

const toggleDropdown = () => { isDropdownOpen.value = !isDropdownOpen.value; };
const logout = () => {
  localStorage.removeItem('auth');
  router.push('/login');
};

onMounted(() => {
  const auth = JSON.parse(localStorage.getItem('auth'));
  user.value = auth?.user || {};
});
</script>