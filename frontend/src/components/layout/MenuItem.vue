<template>
  <div>
    <!-- Menu tanpa sub-menu -->
    <router-link
      v-if="!item.sub_menus || item.sub_menus.length === 0"
      :to="getAbsolutePath(item.route)"
      v-slot="{ navigate, isActive }"
      custom
    >
      <div 
        class="group flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-all duration-200 cursor-pointer"
        :class="[
          isActive 
            ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/25' 
            : 'text-slate-300 hover:text-white hover:bg-slate-800',
          interfaceStore.isSidebarCollapsed ? 'justify-center' : 'justify-start'
        ]"
        @click="navigate"
      >
        <component 
          :is="iconComponent" 
          class="w-5 h-5 flex-shrink-0"
          :class="isActive ? 'text-white' : 'text-slate-400 group-hover:text-white'"
        />
        <span 
          v-if="!interfaceStore.isSidebarCollapsed" 
          class="ml-3 transition-opacity duration-200"
        >
          {{ item.menu_name }}
        </span>
      </div>
    </router-link>

    <!-- Menu dengan sub-menu -->
    <div
      v-else-if="item.sub_menus && item.sub_menus.length > 0"
      @click="toggle"
      class="group flex items-center justify-between px-3 py-2.5 text-sm font-medium rounded-lg transition-all duration-200 cursor-pointer text-slate-300 hover:text-white hover:bg-slate-800"
      :class="{ 'justify-center': interfaceStore.isSidebarCollapsed }"
    >
      <div class="flex items-center">
        <component 
          :is="iconComponent" 
          class="w-5 h-5 flex-shrink-0 text-slate-400 group-hover:text-white"
        />
        <span 
          v-if="!interfaceStore.isSidebarCollapsed" 
          class="ml-3 transition-opacity duration-200"
        >
          {{ item.menu_name }}
        </span>
      </div>
      <ChevronDownIcon 
        v-if="!interfaceStore.isSidebarCollapsed"
        :class="[
          'w-4 h-4 transition-transform duration-200 text-slate-400 group-hover:text-white',
          { 'rotate-180': isOpen }
        ]"
      />
    </div>

    <!-- Sub-menu -->
    <div 
      v-if="isOpen && item.sub_menus && item.sub_menus.length > 0" 
      class="mt-1 space-y-1"
      :class="{'ml-8': !interfaceStore.isSidebarCollapsed}"
    >
      <MenuItem
        v-for="child in item.sub_menus"
        :key="child.menu_id"
        :item="child"
        :depth="depth + 1"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useInterfaceStore } from '@/stores/interfaceStore';

// Impor semua ikon yang Anda perlukan dari @heroicons/vue/24/outline
import { 
  ChevronDownIcon, HomeIcon, UserGroupIcon, ClockIcon, CalendarDaysIcon,
  CurrencyDollarIcon, DocumentDuplicateIcon, ChartBarIcon, UsersIcon, 
  SparklesIcon, Cog6ToothIcon, KeyIcon, ListBulletIcon, DocumentTextIcon, UserPlusIcon, ShieldCheckIcon
} from '@heroicons/vue/24/outline';

const props = defineProps({
  item: { type: Object, required: true },
  depth: { type: Number, required: true }
});

const interfaceStore = useInterfaceStore();
const isOpen = ref(false);
const toggle = () => { isOpen.value = !isOpen.value; };

// TAMBAHKAN FUNCTION INI
const getAbsolutePath = (route) => {
  if (!route) return '/';
  // Pastikan path selalu dimulai dengan '/'
  return route.startsWith('/') ? route : `/${route}`;
};

const iconMap = {
  HomeIcon, UserGroupIcon, ClockIcon, CalendarDaysIcon, CurrencyDollarIcon, 
  DocumentDuplicateIcon, ChartBarIcon, UsersIcon, SparklesIcon, Cog6ToothIcon, 
  KeyIcon, ListBulletIcon, DocumentTextIcon, UserPlusIcon, ShieldCheckIcon
};

const iconComponent = computed(() => {
  const iconName = props.item.icon?.trim();
  return iconMap[iconName] || HomeIcon;
});
</script>

<script>
export default {
  methods: {
  }
};
</script>