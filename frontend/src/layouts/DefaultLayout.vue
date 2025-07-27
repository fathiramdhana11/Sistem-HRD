<template>
  <div class="flex h-screen bg-slate-50">
    <!-- Sidebar -->
    <Sidebar />
    
    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Header -->
      <Header />
      
      <!-- Main Content -->
      <main class="flex-1 overflow-y-auto p-6">
        <router-view />
      </main>
    </div>
    
    <!-- Toast Container -->
    <ToastContainer />
  </div>
</template>

<script setup>
import Header from '@/components/layout/Header.vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import ToastContainer from '@/components/ToastContainer.vue'
</script>