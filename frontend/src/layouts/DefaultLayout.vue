<template>
  <div class="flex h-screen bg-slate-50 font-sans">
    <Sidebar />
    <main class="flex-1 flex flex-col overflow-hidden">
      <Header />
      <div class="flex-1 overflow-x-hidden overflow-y-auto">
        <div class="container mx-auto px-6 py-8">
          <router-view />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
// Path impor yang sudah diperbaiki
import Sidebar from '../components/layout/Sidebar.vue'
import Header from '../components/layout/Header.vue' 
</script>