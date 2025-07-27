<template>
  <button 
    :class="buttonClasses"
    :disabled="disabled || loading"
    @click="handleClick"
    v-bind="$attrs"
  >
    <!-- Loading Spinner -->
    <i v-if="loading" class="pi pi-spin pi-spinner text-sm mr-2"></i>
    
    <!-- Icon -->
    <i v-else-if="icon && iconPosition === 'left'" :class="[icon, 'text-sm mr-2']"></i>
    
    <!-- Slot untuk konten custom -->
    <slot>
      <span v-if="label">{{ label }}</span>
    </slot>
    
    <!-- Icon kanan -->
    <i v-if="icon && iconPosition === 'right'" :class="[icon, 'text-sm ml-2']"></i>
  </button>
</template>

<script setup>
import { computed } from 'vue'

// Props dengan default values
const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'outline', 'text', 'header'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  icon: {
    type: String,
    default: ''
  },
  iconPosition: {
    type: String,
    default: 'left',
    validator: (value) => ['left', 'right'].includes(value)
  },
  label: {
    type: String,
    default: ''
  },
  loading: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  rounded: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['click'])

// Computed classes berdasarkan props
const buttonClasses = computed(() => {
  const baseClasses = 'inline-flex items-center justify-center font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2'
  
  const variantClasses = {
    primary: 'bg-emerald-600 hover:bg-emerald-700 text-white focus:ring-emerald-500 shadow-lg hover:shadow-xl',
    secondary: 'bg-gray-600 hover:bg-gray-700 text-white focus:ring-gray-500 shadow-lg hover:shadow-xl',
    outline: 'border border-gray-300 bg-white hover:bg-gray-50 text-gray-700 focus:ring-gray-500',
    text: 'bg-transparent hover:bg-gray-100 text-gray-700',
    header: 'border border-emerald-500 bg-emerald-50 text-emerald-700 hover:bg-emerald-100 hover:border-emerald-600 focus:ring-emerald-200 active:bg-emerald-200'
  }
  
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base'
  }
  
  const roundedClasses = props.rounded ? 'rounded-full w-10 h-10 p-0' : 'rounded-lg'
  
  const disabledClasses = (props.disabled || props.loading) ? 'opacity-50 cursor-not-allowed' : ''
  
  return [
    baseClasses,
    variantClasses[props.variant],
    sizeClasses[props.size],
    roundedClasses,
    disabledClasses
  ].join(' ')
})

// Methods
const handleClick = (event) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>