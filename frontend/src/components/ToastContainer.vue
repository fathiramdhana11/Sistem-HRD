<template>
  <div class="fixed top-4 right-4 z-50 space-y-2 max-w-sm w-full">
    <transition-group name="toast" tag="div">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="[
          'w-full bg-white dark:bg-gray-800 shadow-lg dark:shadow-2xl rounded-lg pointer-events-auto ring-1 ring-black ring-opacity-5 dark:ring-gray-600 overflow-hidden transition-all duration-300',
          toast.visible ? 'opacity-100' : 'opacity-0'
        ]"
      >
        <div class="p-4">
          <div class="flex items-start">
            <div class="flex-shrink-0">
              <div
                :class="[
                  'w-6 h-6 rounded-full flex items-center justify-center',
                  toast.type === 'success' ? 'bg-green-100 dark:bg-green-900/30' : '',
                  toast.type === 'error' ? 'bg-red-100 dark:bg-red-900/30' : '',
                  toast.type === 'warning' ? 'bg-yellow-100 dark:bg-yellow-900/30' : '',
                  toast.type === 'info' ? 'bg-blue-100 dark:bg-blue-900/30' : '',
                  toast.type === 'loading' ? 'bg-gray-100 dark:bg-gray-700' : ''
                ]"
              >
                <i
                  :class="[
                    'text-sm',
                    toast.type === 'success' ? 'pi pi-check text-green-600 dark:text-green-400' : '',
                    toast.type === 'error' ? 'pi pi-times text-red-600 dark:text-red-400' : '',
                    toast.type === 'warning' ? 'pi pi-exclamation-triangle text-yellow-600 dark:text-yellow-400' : '',
                    toast.type === 'info' ? 'pi pi-info-circle text-blue-600 dark:text-blue-400' : '',
                    toast.type === 'loading' ? 'pi pi-spin pi-spinner text-gray-600 dark:text-gray-400' : ''
                  ]"
                ></i>
              </div>
            </div>
            <div class="ml-3 w-0 flex-1 pt-0.5">
              <p class="text-sm font-medium text-gray-900 dark:text-gray-100 break-words transition-colors duration-300">{{ toast.title }}</p>
              <p class="mt-1 text-sm text-gray-500 dark:text-gray-400 break-words transition-colors duration-300">{{ toast.message }}</p>
            </div>
            <div class="ml-4 flex-shrink-0 flex">
              <button
                @click="removeToast(toast.id)"
                class="bg-white dark:bg-gray-800 rounded-md inline-flex text-gray-400 dark:text-gray-500 hover:text-gray-500 dark:hover:text-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-indigo-400 p-1 transition-colors duration-200"
              >
                <span class="sr-only">Close</span>
                <i class="pi pi-times text-sm"></i>
              </button>
            </div>
          </div>
          <!-- Progress bar -->
          <div
            v-if="toast.type !== 'loading' && toast.progress > 0"
            class="mt-2 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1 transition-colors duration-300"
          >
            <div
              :class="[
                'h-1 rounded-full transition-all duration-100',
                toast.type === 'success' ? 'bg-green-600 dark:bg-green-500' : '',
                toast.type === 'error' ? 'bg-red-600 dark:bg-red-500' : '',
                toast.type === 'warning' ? 'bg-yellow-600 dark:bg-yellow-500' : '',
                toast.type === 'info' ? 'bg-blue-600 dark:bg-blue-500' : ''
              ]"
              :style="{ width: toast.progress + '%' }"
            ></div>
          </div>
        </div>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { useToast } from '@/composables/useToast'

const { toasts, removeToast } = useToast()
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.toast-move {
  transition: transform 0.3s ease;
}

/* Mobile responsiveness */
@media (max-width: 640px) {
  .fixed {
    top: 1rem;
    right: 1rem;
    left: 1rem;
    max-width: none;
  }
}
</style>