<template>
  <aside
    class="bg-slate-800 text-slate-300 flex flex-col transition-all duration-300 ease-in-out"
    :class="interfaceStore.isSidebarCollapsed ? 'w-20' : 'w-64' " 
    @click="handleSidebarClick"
  >
    <div
      class="h-16 flex items-center shrink-0 border-b border-slate-700/50"
      :class="
        interfaceStore.isSidebarCollapsed
          ? 'justify-center'
          : 'justify-between px-4'
      "
    >
      <h1
        v-if="!interfaceStore.isSidebarCollapsed"
        class="text-xl font-bold text-white tracking-wider"
      >
        HRIS
      </h1>
      <img v-else src="/logo-icon.svg" class="h-8 w-8 text-white" alt="Logo" />
    </div>

    <nav class="flex-1 px-3 py-4 overflow-y-auto">
      <div class="space-y-1">
        <MenuItem
          v-for="item in menuItems"
          :key="item.menu_id"
          :item="item"
          :depth="0"
        />
      </div>
    </nav>

    <div class="shrink-0 p-4 border-t border-slate-700/50">
      <div class="flex items-center space-x-3">
        <img
          class="h-10 w-10 rounded-full object-cover"
          src="https://i.pravatar.cc/100"
          alt="User Avatar"
        />
        <div v-if="!interfaceStore.isSidebarCollapsed">
          <p class="text-sm font-semibold text-white">{{ user.username }}</p>
          <button
            @click="logout"
            class="text-xs text-red-400 hover:text-red-300 hover:underline"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import MenuItem from "./MenuItem.vue";
import axios from "axios";
// --- LOGIKA UNTUK COLLAPSE SIDEBAR ---
import { useInterfaceStore } from "@/stores/interfaceStore";

const handleSidebarClick = () => {
  // Jika sidebar sedang diperkecil, panggil fungsi toggle untuk memperbesarnya
  if (interfaceStore.isSidebarCollapsed) {
    interfaceStore.toggleSidebar();
  }
};

const router = useRouter();
const user = ref({});
const interfaceStore = useInterfaceStore(); // <-- Inisialisasi store untuk collapse

// --- LOGIKA UNTUK MENAMPILKAN DATA MENU ---
const menuItems = ref([]);

const fetchMenus = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/api/menus/tree");
    menuItems.value = response.data;
  } catch (error) {
    console.error("Gagal mengambil data menu:", error);
  }
};

const logout = () => {
  localStorage.removeItem("auth");
  router.push("/login");
};

onMounted(() => {
  const auth = JSON.parse(localStorage.getItem("auth"));
  user.value = auth?.user || {};
  fetchMenus();
});
</script>
