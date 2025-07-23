<template>
  <div>
    <router-link
      v-if="!item.sub_menus || item.sub_menus.length === 0"
      :to="item.route || '/'"
      v-slot="{ isActive }"
      class="w-full flex items-center py-2.5 px-4 rounded-lg text-slate-400 hover:bg-slate-700 hover:text-white transition-colors duration-200"
      :class="{ 'bg-slate-700 !text-white': isActive, 'justify-center': interfaceStore.isSidebarCollapsed }"
    >
      <div class="flex items-center space-x-3">
        <component :is="iconComponent" class="h-6 w-6 shrink-0" />
        <span v-if="!interfaceStore.isSidebarCollapsed" class="font-medium">{{ item.menu_name }}</span>
      </div>
    </router-link>

    <div
      v-else
      @click="toggle"
      role="button"
      class="w-full flex items-center justify-between py-2.5 px-4 rounded-lg text-slate-400 hover:bg-slate-700 hover:text-white transition-colors duration-200 cursor-pointer"
      :class="{ 'justify-center': interfaceStore.isSidebarCollapsed }"
    >
      <div class="flex items-center space-x-3">
        <component :is="iconComponent" class="h-6 w-6 shrink-0" />
        <span v-if="!interfaceStore.isSidebarCollapsed" class="font-medium">{{ item.menu_name }}</span>
      </div>
      <div v-if="!interfaceStore.isSidebarCollapsed" class="flex items-center">
        <ChevronDownIcon :class="['h-4 w-4 transition-transform', { 'rotate-180': isOpen }]" />
      </div>
    </div>

    <div v-if="isOpen && item.sub_menus.length > 0" class="mt-1 space-y-1" :class="{'pl-6': !interfaceStore.isSidebarCollapsed}">
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
import { ref, computed, shallowRef } from 'vue';
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

const iconMap = {
  HomeIcon, UserGroupIcon, ClockIcon, CalendarDaysIcon, CurrencyDollarIcon, 
  DocumentDuplicateIcon, ChartBarIcon, UsersIcon, SparklesIcon, Cog6ToothIcon, 
  KeyIcon, ListBulletIcon, DocumentTextIcon, UserPlusIcon, ShieldCheckIcon
};

const iconComponent = computed(() => {
  const iconName = props.item.icon?.trim();
  // Gunakan shallowRef di sini untuk memastikan ini adalah komponen yang valid untuk :is
  return shallowRef(iconMap[iconName] || HomeIcon);
});
</script>