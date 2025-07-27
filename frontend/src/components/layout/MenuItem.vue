<template>
  <div>
    <!-- Menu Item tanpa Children -->
    <router-link
      v-if="!item.children"
      :to="item.route"
      class="group flex items-center px-4 py-3 rounded-xl text-gray-700 hover:bg-emerald-50 hover:text-emerald-700 font-medium cursor-pointer transition-all duration-200 ease-in-out transform hover:scale-[1.02]"
      :class="{
        'bg-gradient-to-r from-emerald-500 to-emerald-600 text-white font-medium hover:from-emerald-600 hover:to-emerald-700 hover:text-white shadow-md': $route.path === item.route,
        'justify-center': isCollapsed
      }"
    >
      <i :class="[item.icon, {
        'mr-3': !isCollapsed,
        'group-hover:text-emerald-600': $route.path !== item.route
      }]" class="text-lg transition-colors duration-200"></i>
      <span v-if="!isCollapsed" class="text-sm">{{ item.name }}</span>
    </router-link>

    <!-- Menu Item dengan Children -->
    <div v-else>
      <button
        @click="toggleSubmenu"
        class="group w-full flex items-center px-4 py-3 rounded-xl text-gray-700 hover:bg-emerald-50 hover:text-emerald-700 font-medium cursor-pointer transition-all duration-200 ease-in-out transform hover:scale-[1.02]"
        :class="{
          'justify-center': isCollapsed,
          'bg-emerald-50 text-emerald-700': isSubmenuOpen
        }"
      >
        <i :class="[item.icon, {
          'mr-3': !isCollapsed
        }]" class="text-lg transition-colors duration-200 group-hover:text-emerald-600"></i>
        <span v-if="!isCollapsed" class="text-sm flex-1 text-left">{{ item.name }}</span>
        <i v-if="!isCollapsed" :class="isSubmenuOpen ? 'pi pi-chevron-down' : 'pi pi-chevron-right'" class="text-xs transition-transform duration-200"></i>
      </button>

      <!-- Submenu -->
      <Transition name="submenu">
        <div v-if="isSubmenuOpen && !isCollapsed" class="mt-2 ml-4 mr-2 bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl border border-gray-200/30 overflow-hidden shadow-sm backdrop-blur-sm">
          <router-link
            v-for="child in item.children"
            :key="child.name"
            :to="child.route"
            class="group flex items-center px-3 py-2.5 text-gray-600 hover:bg-white hover:text-emerald-700 text-xs cursor-pointer border-b border-gray-200/50 last:border-b-0 transition-all duration-200 ease-in-out"
            :class="{
              'bg-gradient-to-r from-emerald-500 to-emerald-600 text-white font-medium hover:from-emerald-600 hover:to-emerald-700 hover:text-white shadow-md':
                $route.path === child.route
            }"
          >
            <i class="pi pi-circle text-xs mr-2 transition-colors duration-200" :class="{
              'group-hover:text-emerald-600': $route.path !== child.route
            }"></i>
            <span>{{ child.name }}</span>
          </router-link>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({
  item: {
    type: Object,
    required: true
  },
  isCollapsed: {
    type: Boolean,
    default: false
  }
})

const route = useRoute()
const isSubmenuOpen = ref(false)

const toggleSubmenu = () => {
  if (!props.isCollapsed) {
    isSubmenuOpen.value = !isSubmenuOpen.value
  }
}

// Auto-open submenu if current route matches any child
watch(() => route.path, (newPath) => {
  if (props.item.children) {
    const hasActiveChild = props.item.children.some(child => child.route === newPath)
    if (hasActiveChild) {
      isSubmenuOpen.value = true
    }
  }
}, { immediate: true })

// Close submenu when sidebar is collapsed
watch(() => props.isCollapsed, (newValue) => {
  if (newValue) {
    isSubmenuOpen.value = false
  }
})
</script>

<style scoped>
.submenu-enter-active,
.submenu-leave-active {
  transition: all 0.3s ease;
  transform-origin: top;
}

.submenu-enter-from,
.submenu-leave-to {
  opacity: 0;
  transform: scaleY(0);
}
</style>