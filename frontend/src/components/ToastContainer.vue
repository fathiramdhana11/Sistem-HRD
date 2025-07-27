<template>
  <div class="fixed top-4 right-4 z-50 space-y-2 max-w-sm w-full">
    <TransitionGroup name="toast" tag="div">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="[
          'w-full bg-white shadow-lg rounded-lg pointer-events-auto ring-1 ring-black ring-opacity-5 overflow-hidden transition-all duration-300',
          'transform hover:scale-105',
          {
            'border-l-4': true,
            'pl-4': true
          },
          toast.type === 'success' ? 'bg-green-100' : '',
          toast.type === 'error' ? 'bg-red-100' : '',
          toast.type === 'warning' ? 'bg-yellow-100' : '',
          toast.type === 'info' ? 'bg-blue-100' : '',
          toast.type === 'loading' ? 'bg-gray-100' : ''
        ]"
      >
        <div class="p-4">
          <div class="flex items-start">
            <div class="flex-shrink-0">
              <i :class="[
                'text-xl transition-all duration-300',
                toast.type === 'success' ? 'pi pi-check text-green-600' : '',
                toast.type === 'error' ? 'pi pi-times text-red-600' : '',
                toast.type === 'warning' ? 'pi pi-exclamation-triangle text-yellow-600' : '',
                toast.type === 'info' ? 'pi pi-info-circle text-blue-600' : '',
                toast.type === 'loading' ? 'pi pi-spin pi-spinner text-gray-600' : ''
              ]"></i>
            </div>
            <div class="ml-3 w-0 flex-1">
              <p class="text-sm font-medium text-gray-900 break-words transition-colors duration-300">{{ toast.title }}</p>
              <p class="mt-1 text-sm text-gray-500 break-words transition-colors duration-300">{{ toast.message }}</p>
            </div>
            <div class="ml-4 flex-shrink-0 flex">
              <button
                @click="removeToast(toast.id)"
                class="bg-white rounded-md inline-flex text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 p-1 transition-colors duration-200"
              >
                <span class="sr-only">Close</span>
                <i class="pi pi-times text-sm"></i>
              </button>
            </div>
          </div>
          
          <!-- Progress bar untuk loading dan auto-dismiss -->
          <div v-if="toast.type === 'loading' || toast.duration" 
            class="mt-2 w-full bg-gray-200 rounded-full h-1 transition-colors duration-300"
          >
            <div 
              class="h-1 rounded-full transition-all duration-300"
              :class="[
                toast.type === 'success' ? 'bg-green-600' : '',
                toast.type === 'error' ? 'bg-red-600' : '',
                toast.type === 'warning' ? 'bg-yellow-600' : '',
                toast.type === 'info' ? 'bg-blue-600' : ''
              ]"
              :style="{ width: toast.progress + '%' }"
            ></div>
          </div>
        </div>
      </div>
    </TransitionGroup>
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
</style>