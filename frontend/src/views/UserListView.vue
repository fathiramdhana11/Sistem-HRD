<template>
  <div class="p-6">
    <!-- Breadcrumb dengan Tailwind -->
    <nav class="mb-6">
      <ol class="flex items-center space-x-2 text-sm text-gray-500">
        <li><a href="#" class="hover:text-gray-700">Dashboard</a></li>
        <li class="flex items-center">
          <svg class="w-4 h-4 mx-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
          </svg>
          <span class="text-gray-900 font-medium">User Management</span>
        </li>
      </ol>
    </nav>

    <!-- Main content -->
    <UserTablePrime />
  </div>
</template>

<script setup>
import UserTablePrime from '@/components/users/UserTablePrime.vue'
</script>