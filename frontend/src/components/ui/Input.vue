<template>
  <div class="form-group">
    <!-- Label -->
    <label v-if="label" :for="inputId" class="form-label">
      {{ label }}
      <span v-if="required" class="text-red-500 ml-1">*</span>
    </label>
    
    <!-- Input Container -->
    <div class="relative">
      <!-- Left Icon -->
      <div v-if="leftIcon" class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <i :class="[leftIcon, 'text-gray-400 text-sm']"></i>
      </div>
      
      <!-- Input Field -->
      <input
        :id="inputId"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :class="inputClasses"
        @input="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
        v-bind="$attrs"
      />
      
      <!-- Right Icon -->
      <div v-if="rightIcon" class="absolute inset-y-0 right-0 pr-3 flex items-center">
        <i :class="[rightIcon, 'text-gray-400 text-sm']"></i>
      </div>
    </div>
    
    <!-- Error Message -->
    <div v-if="error" class="form-error">
      {{ error }}
    </div>
    
    <!-- Help Text -->
    <div v-if="helpText && !error" class="text-sm text-gray-500 mt-1">
      {{ helpText }}
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

// Props
const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  leftIcon: {
    type: String,
    default: ''
  },
  rightIcon: {
    type: String,
    default: ''
  },
  error: {
    type: String,
    default: ''
  },
  helpText: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  readonly: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'search'].includes(value)
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'blur', 'focus'])

// Reactive data
const inputId = ref(`input-${Math.random().toString(36).substr(2, 9)}`)

// Computed classes
const inputClasses = computed(() => {
  const baseClasses = 'form-input'
  const variantClasses = {
    default: '',
    search: 'search-input'
  }
  const paddingClasses = {
    left: props.leftIcon ? 'pl-10' : '',
    right: props.rightIcon ? 'pr-10' : ''
  }
  const errorClasses = props.error ? 'border-red-300 focus:border-red-500 focus:ring-red-100' : ''
  const disabledClasses = props.disabled ? 'bg-gray-100 cursor-not-allowed' : ''
  
  return [
    baseClasses,
    variantClasses[props.variant],
    paddingClasses.left,
    paddingClasses.right,
    errorClasses,
    disabledClasses
  ].filter(Boolean).join(' ')
})

// Methods
const handleInput = (event) => {
  emit('update:modelValue', event.target.value)
}

const handleBlur = (event) => {
  emit('blur', event)
}

const handleFocus = (event) => {
  emit('focus', event)
}
</script>