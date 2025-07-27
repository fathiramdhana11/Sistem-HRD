<template>
  <aside
    class="bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 flex flex-col h-screen relative z-10 shadow-lg dark:shadow-2xl transition-all duration-300 ease-in-out"
    :class="interfaceStore.isSidebarCollapsed ? 'w-16' : 'w-64'"
  >
    <!-- Logo Section -->
    <div
      class="p-4 border-b border-gray-100 dark:border-gray-700 bg-gradient-to-r from-emerald-500 to-emerald-600 dark:from-emerald-600 dark:to-emerald-700"
    >
      <div
        class="flex items-center space-x-3"
        v-if="!interfaceStore.isSidebarCollapsed"
      >
        <div
          class="w-10 h-10 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center shadow-lg"
        >
          <i class="pi pi-building text-white text-xl"></i>
        </div>
        <div>
          <h1 class="text-white font-bold text-lg leading-tight">
            Sistem HRD
          </h1>
          <p class="text-emerald-100 text-xs font-medium">
            PT Mitrasoft Global
          </p>
        </div>
      </div>
    </div>

    <!-- Navigation Menu -->
    <nav
      class="flex-1 py-4 overflow-y-auto scrollbar-thin scrollbar-thumb-emerald-200 dark:scrollbar-thumb-gray-600 scrollbar-track-gray-100 dark:scrollbar-track-gray-800"
    >
      <ul class="space-y-1 px-3">
        <li v-for="item in menuItems" :key="item.menu_id" class="relative">
          <!-- Menu dengan route langsung (tanpa submenu) -->
          <router-link
            v-if="item.route && (!item.sub_menus || item.sub_menus.length === 0)"
            :to="ensureAbsolutePath(item.route)"
            class="group flex items-center px-4 py-3 rounded-xl text-gray-700 dark:text-gray-300 hover:bg-emerald-50 dark:hover:bg-emerald-900/20 hover:text-emerald-700 dark:hover:text-emerald-400 font-medium cursor-pointer transition-all duration-200 ease-in-out transform hover:scale-[1.02]"
            :class="{
              'bg-gradient-to-r from-emerald-500 to-emerald-600 dark:from-emerald-600 dark:to-emerald-700 text-white shadow-lg hover:from-emerald-600 hover:to-emerald-700 hover:text-white':
                $route.path === ensureAbsolutePath(item.route),
              'justify-center': interfaceStore.isSidebarCollapsed,
            }"
          >
            <i
              :class="item.icon"
              class="text-lg flex-shrink-0 transition-transform duration-200 group-hover:scale-110"
            ></i>
            <span
              v-if="!interfaceStore.isSidebarCollapsed"
              class="ml-3 transition-all duration-200"
            >
              {{ item.menu_name }}
            </span>
          </router-link>

          <!-- Menu parent dengan submenu -->
          <div v-else>
            <div
              class="group flex items-center px-4 py-3 rounded-xl text-gray-700 dark:text-gray-300 hover:bg-emerald-50 dark:hover:bg-emerald-900/20 hover:text-emerald-700 dark:hover:text-emerald-400 hover:font-bold font-medium cursor-pointer transition-all duration-200 ease-in-out transform hover:scale-[1.02]"
              :class="{
                'justify-center': interfaceStore.isSidebarCollapsed,
                'bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-400 shadow-sm font-bold':
                  hasActiveChild(item) ||
                  expandedMenus.includes(item.menu_id),
              }"
              @click.stop="toggleSubmenu(item.menu_id)"
            >
              <i
                :class="item.icon"
                class="text-lg flex-shrink-0 transition-transform duration-200 group-hover:scale-110"
              ></i>
              <span
                v-if="!interfaceStore.isSidebarCollapsed"
                class="ml-3 flex-1 transition-all duration-200"
              >
                {{ item.menu_name }}
              </span>
              <i
                v-if="
                  !interfaceStore.isSidebarCollapsed &&
                  item.sub_menus && item.sub_menus.length > 0
                "
                class="pi pi-chevron-down text-xs transition-all duration-300 ease-in-out"
                :class="{
                  'rotate-180': expandedMenus.includes(item.menu_id),
                  'text-emerald-700 dark:text-emerald-400':
                    hasActiveChild(item) ||
                    expandedMenus.includes(item.menu_id),
                  'text-gray-400 dark:text-gray-500':
                    !hasActiveChild(item) &&
                    !expandedMenus.includes(item.menu_id),
                }"
              ></i>
            </div>

            <!-- Submenu dengan animasi smooth -->
            <transition
              enter-active-class="transition-all duration-300 ease-out"
              enter-from-class="opacity-0 transform -translate-y-2 scale-95"
              enter-to-class="opacity-100 transform translate-y-0 scale-100"
              leave-active-class="transition-all duration-200 ease-in"
              leave-from-class="opacity-100 transform translate-y-0 scale-100"
              leave-to-class="opacity-0 transform -translate-y-2 scale-95"
            >
              <div
                v-if="
                  item.sub_menus && item.sub_menus.length > 0 &&
                  !interfaceStore.isSidebarCollapsed &&
                  expandedMenus.includes(item.menu_id)
                "
                class="mt-2 ml-6 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-700 rounded-xl border border-gray-200 dark:border-gray-600 overflow-hidden shadow-sm backdrop-blur-sm"
              >
                <router-link
                  v-for="child in item.sub_menus"
                  :key="child.menu_id"
                  :to="ensureAbsolutePath(child.route)"
                  class="group flex items-center px-4 py-3 text-gray-600 dark:text-gray-400 hover:bg-white dark:hover:bg-gray-600 hover:text-emerald-700 dark:hover:text-emerald-400 text-sm cursor-pointer border-b border-gray-200/50 dark:border-gray-600/50 last:border-b-0 transition-all duration-200 ease-in-out transform hover:scale-[1.02]"
                  :class="{
                    'bg-gradient-to-r from-emerald-500 to-emerald-600 dark:from-emerald-600 dark:to-emerald-700 text-white font-medium hover:from-emerald-600 hover:to-emerald-700 hover:text-white shadow-md':
                      $route.path === ensureAbsolutePath(child.route),
                  }"
                >
                  <div
                    class="w-2 h-2 rounded-full mr-3 transition-all duration-200"
                    :class="{
                      'bg-white shadow-sm': $route.path === ensureAbsolutePath(child.route),
                      'bg-emerald-400 group-hover:bg-emerald-500':
                        $route.path !== ensureAbsolutePath(child.route),
                    }"
                  ></div>
                  <i
                    :class="child.icon"
                    class="text-sm flex-shrink-0 mr-3 transition-transform duration-200 group-hover:scale-110"
                  ></i>
                  <span class="truncate transition-all duration-200">{{ child.menu_name }}</span>
                </router-link>
              </div>
            </transition>
          </div>
        </li>
      </ul>
    </nav>

    <!-- User Section -->
    <div
      class="p-4 border-t border-gray-100 dark:border-gray-700 bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-700"
    >
      <div
        class="flex items-center space-x-3"
        v-if="!interfaceStore.isSidebarCollapsed"
      >
        <div
          class="w-8 h-8 bg-gradient-to-br from-emerald-500 to-emerald-600 dark:from-emerald-600 dark:to-emerald-700 rounded-full flex items-center justify-center shadow-md"
        >
          <i class="pi pi-user text-white text-sm"></i>
        </div>
        <div class="flex-1">
          <p class="text-sm font-semibold text-gray-900 dark:text-gray-100">
            {{ user.username || "Admin" }}
          </p>
          <p class="text-xs text-emerald-600 dark:text-emerald-400 flex items-center">
            <span
              class="w-2 h-2 bg-emerald-400 rounded-full mr-1 animate-pulse"
            ></span>
            Online
          </p>
        </div>
        <button
          @click="logout"
          class="group p-2 rounded-lg text-gray-400 dark:text-gray-500 hover:text-red-500 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 cursor-pointer transition-all duration-200 transform hover:scale-110"
          title="Logout"
        >
          <i
            class="pi pi-sign-out text-sm transition-transform duration-200 group-hover:scale-110"
          ></i>
        </button>
      </div>
      <div v-else class="flex justify-center">
        <div
          class="w-8 h-8 bg-gradient-to-br from-emerald-500 to-emerald-600 dark:from-emerald-600 dark:to-emerald-700 rounded-full flex items-center justify-center shadow-md"
        >
          <i class="pi pi-user text-white text-sm"></i>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted, computed, nextTick, onUnmounted, watch } from "vue";
import { useRouter } from "vue-router";
import menuService from "@/services/menuService";
import { useInterfaceStore } from "@/stores/interfaceStore";
import { useAuthStore } from "@/stores/authStore";

const router = useRouter();
const user = ref({});
const interfaceStore = useInterfaceStore();
const authStore = useAuthStore();
const expandedMenus = ref([]);

// Reactive menu items dari API
const menuItems = ref([]);

// Function untuk memastikan path absolut
const ensureAbsolutePath = (path) => {
  if (!path) return '/';
  return path.startsWith('/') ? path : `/${path}`;
};

// Function untuk mengecek apakah menu memiliki children
const hasChildren = (menu) => {
  return menu.sub_menus && menu.sub_menus.length > 0;
};

// Function untuk mengecek apakah ada child yang aktif
const hasActiveChild = (menu) => {
  if (!menu.sub_menus || menu.sub_menus.length === 0) return false;
  return menu.sub_menus.some(
    (child) => router.currentRoute.value.path === ensureAbsolutePath(child.route)
  );
};

// Function untuk toggle submenu dengan animasi smooth
const toggleSubmenu = (menuId) => {
  const index = expandedMenus.value.indexOf(menuId);
  if (index > -1) {
    expandedMenus.value.splice(index, 1);
  } else {
    expandedMenus.value = [menuId]; // Hanya buka satu submenu pada satu waktu
  }
};

// Function untuk auto expand submenu yang aktif
const autoExpandActiveSubmenu = () => {
  const currentPath = router.currentRoute.value.path;

  // Find parent menu that has active child
  menuItems.value.forEach((menu) => {
    if (menu.sub_menus && menu.sub_menus.length > 0) {
      const hasActiveChildMenu = menu.sub_menus.some(
        (child) => ensureAbsolutePath(child.route) === currentPath
      );

      if (hasActiveChildMenu && !expandedMenus.value.includes(menu.menu_id)) {
        expandedMenus.value.push(menu.menu_id);
      }
    }
  });
};

// Function untuk fetch menus dari API
const fetchMenus = async () => {
  try {
    const response = await menuService.getUserMenus()
    
    let apiMenus = []
    if (response.data && Array.isArray(response.data)) {
      apiMenus = response.data
    } else if (response.data && response.data.menus && Array.isArray(response.data.menus)) {
      apiMenus = response.data.menus
    }
    
    // Filter out duplicate Dashboard if it exists in API response
    const filteredMenus = apiMenus.filter(menu => 
      menu.menu_name !== 'Dashboard' && 
      menu.route !== '/dashboard'
    )
    
    // Always include Dashboard as first menu
    const dashboardMenu = {
      menu_id: 'dashboard',
      menu_name: 'Dashboard',
      route: '/dashboard',
      icon: 'pi pi-home',
      sub_menus: []
    }
    
    // Set menu items dengan struktur yang benar
    menuItems.value = [dashboardMenu, ...filteredMenus]
    
    // Auto expand active submenu setelah menu dimuat
    nextTick(() => {
      autoExpandActiveSubmenu()
    })
    
  } catch (error) {
    console.error('Error fetching menus:', error)
    
    // Fallback: provide minimal menu
    menuItems.value = [{
      menu_id: 'dashboard',
      menu_name: 'Dashboard',
      route: '/dashboard',
      icon: 'pi pi-home',
      sub_menus: []
    }]
  }
}

const handleMenuUpdate = () => {
  fetchMenus()
}

const handleMenuClear = () => {
  menuItems.value = []
  expandedMenus.value = []
}

// Function untuk logout
const logout = async () => {
  try {
    await authStore.logout();
  } catch (error) {
    console.error('Logout error:', error);
    router.push('/login');
  }
};

onMounted(() => {
  // Get user data from localStorage
  const authData = localStorage.getItem('auth')
  if (authData) {
    try {
      const parsedAuth = JSON.parse(authData)
      user.value = parsedAuth.user || {}
    } catch (error) {
      console.error('Error parsing auth data:', error)
    }
  }
  
  // Initial menu fetch
  fetchMenus()
  
  // Event listeners
  window.addEventListener('menu-updated', handleMenuUpdate)
  window.addEventListener('menu-clear', handleMenuClear)
})

onUnmounted(() => {
  window.removeEventListener('menu-updated', handleMenuUpdate)
  window.removeEventListener('menu-clear', handleMenuClear)
})

// Watch route changes untuk auto expand
watch(
  () => router.currentRoute.value.path,
  () => {
    autoExpandActiveSubmenu()
  }
)
</script>

<style scoped>
/* Custom scrollbar */
.scrollbar-thin {
  scrollbar-width: thin;
}

.scrollbar-thin::-webkit-scrollbar {
  width: 4px;
}

.scrollbar-thin::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 2px;
}

.scrollbar-thin::-webkit-scrollbar-thumb {
  background: #d1fae5;
  border-radius: 2px;
}

.scrollbar-thin::-webkit-scrollbar-thumb:hover {
  background: #a7f3d0;
}
</style>
