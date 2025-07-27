<template>
  <div class="min-h-screen bg-white">
    <router-view />
    <ToastContainer />
  </div>
</template>

<script setup>
import ToastContainer from '@/components/ToastContainer.vue'

// Pastikan tidak ada dark mode yang diaktifkan
if (typeof window !== 'undefined') {
  document.documentElement.classList.remove('dark')
  document.body.classList.remove('dark')
  
  // Hapus dari localStorage jika ada
  localStorage.removeItem('theme')
  localStorage.removeItem('darkMode')
  localStorage.removeItem('color-scheme')
}
</script>

<style>
/* Force light mode only */
html, body {
  background-color: white !important;
  color: #1f2937 !important;
}
</style>
