// File: frontend/src/stores/interfaceStore.js
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useInterfaceStore = defineStore('interface', () => {
  const isSidebarCollapsed = ref(false);

  function toggleSidebar() {
    isSidebarCollapsed.value = !isSidebarCollapsed.value;
  }

  return { isSidebarCollapsed, toggleSidebar };
});