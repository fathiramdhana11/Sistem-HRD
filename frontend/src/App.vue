<template>
  <div class="min-h-screen bg-gray-50 transition-colors duration-200">
    <router-view />
    <ToastContainer />
  </div>
</template>

<script setup>
import ToastContainer from '@/components/ToastContainer.vue'
</script>

<style>
</style>
