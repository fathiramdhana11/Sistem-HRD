<template>
  <div class="fixed top-4 right-4 z-50 space-y-2">
    <div
      v-for="alert in alerts"
      :key="alert.id"
      :class="[
        'px-4 py-3 rounded-lg shadow-lg transition-all duration-300',
        'flex items-center justify-between min-w-80',
        {
          'bg-green-100 border border-green-400 text-green-700': alert.type === 'success',
          'bg-red-100 border border-red-400 text-red-700': alert.type === 'error',
          'bg-yellow-100 border border-yellow-400 text-yellow-700': alert.type === 'warning',
          'bg-blue-100 border border-blue-400 text-blue-700': alert.type === 'info'
        }
      ]"
    >
      <span>{{ alert.message }}</span>
      <button
        @click="removeAlert(alert.id)"
        class="ml-3 text-lg font-bold hover:opacity-70"
      >
        ×
      </button>
    </div>
  </div>
</template>

<script setup>
import { useAlert } from '@/composables/useAlert'

const { alerts, removeAlert } = useAlert()
</script>