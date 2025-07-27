<template>
  <!--    Tailwind untuk layout wrapper -->
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
    <!-- Custom header dengan Tailwind -->
    <div class="bg-gradient-to-r from-blue-600 to-blue-700 px-6 py-4">
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-semibold text-white">Manajemen User</h2>
        <div class="flex space-x-3">
          <!-- PrimeVue Button dengan Tailwind classes -->
          <Button 
            label="Tambah User" 
            icon="pi pi-plus" 
            class="p-button-sm bg-white text-blue-600 hover:bg-gray-100 border-white"
            @click="showAddModal = true"
          />
          <Button 
            label="Export" 
            icon="pi pi-download" 
            class="p-button-sm p-button-outlined border-white text-white hover:bg-white hover:text-blue-600"
            @click="exportData"
          />
        </div>
      </div>
    </div>

    <!-- PrimeVue DataTable dengan custom styling -->
    <DataTable 
      :value="users" 
      :paginator="true" 
      :rows="10"
      :loading="loading"
      filterDisplay="menu"
      :globalFilterFields="['username', 'email', 'role_name']"
      responsiveLayout="scroll"
      class="border-none"
    >
      <!-- Global filter dengan Tailwind styling -->
      <template #header>
        <div class="flex justify-between items-center p-4 bg-gray-50">
          <span class="text-lg font-medium text-gray-900">Daftar User</span>
          <div class="flex items-center space-x-3">
            <InputText 
              v-model="globalFilter" 
              placeholder="Cari user..." 
              class="w-64"
            />
            <Button 
              icon="pi pi-refresh" 
              class="p-button-outlined p-button-sm"
              @click="loadUsers"
            />
          </div>
        </div>
      </template>

      <!-- Columns dengan custom body templates -->
      <Column field="username" header="Username" sortable>
        <template #body="{data}">
          <div class="flex items-center space-x-3">
            <!-- Avatar dengan Tailwind -->
            <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
              <span class="text-blue-600 font-medium text-sm">
                {{ data.username.charAt(0).toUpperCase() }}
              </span>
            </div>
            <span class="font-medium text-gray-900">{{ data.username }}</span>
          </div>
        </template>
      </Column>

      <Column field="email" header="Email" sortable>
        <template #body="{data}">
          <span class="text-gray-600">{{ data.email }}</span>
        </template>
      </Column>

      <Column field="role_name" header="Role" sortable>
        <template #body="{data}">
          <!-- PrimeVue Tag dengan custom colors -->
          <Tag 
            :value="data.role_name" 
            :severity="getRoleSeverity(data.role_name)"
            class="font-medium"
          />
        </template>
      </Column>

      <Column field="status" header="Status" sortable>
        <template #body="{data}">
          <Tag 
            :value="data.status" 
            :severity="data.status === 'active' ? 'success' : 'danger'"
          />
        </template>
      </Column>

      <Column header="Aksi" class="w-32">
        <template #body="{data}">
          <div class="flex space-x-2">
            <Button 
              icon="pi pi-pencil" 
              class="p-button-text p-button-sm text-blue-600 hover:bg-blue-50"
              @click="editUser(data)"
            />
            <Button 
              icon="pi pi-trash" 
              class="p-button-text p-button-sm text-red-600 hover:bg-red-50"
              @click="confirmDelete(data)"
            />
          </div>
        </template>
      </Column>
    </DataTable>
  </div>

  <!-- PrimeVue Dialog dengan Tailwind content -->
  <Dialog 
    v-model:visible="showAddModal" 
    modal 
    header="Tambah User Baru"
    class="w-full max-w-md"
  >
    <div class="space-y-4 p-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Username</label>
        <InputText 
          v-model="newUser.username" 
          placeholder="Masukkan username"
          class="w-full"
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
        <InputText 
          v-model="newUser.email" 
          placeholder="Masukkan email"
          class="w-full"
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Role</label>
        <Select 
          v-model="newUser.role_id" 
          :options="roles" 
          optionLabel="role_name" 
          optionValue="role_id"
          placeholder="Pilih role"
          class="w-full"
        />
      </div>
    </div>
    
    <template #footer>
      <div class="flex justify-end space-x-3 p-4 border-t border-gray-200">
        <Button 
          label="Batal" 
          class="p-button-text"
          @click="showAddModal = false"
        />
        <Button 
          label="Simpan" 
          class="bg-blue-600 hover:bg-blue-700"
          @click="saveUser"
        />
      </div>
    </template>
  </Dialog>

  <!-- Toast untuk notifications -->
  <Toast />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from '@/composables/useToast' // Tambahkan
import userService from '@/services/userService'
import roleService from '@/services/roleService'

const toast = useToast() // Tambahkan

// Reactive data
const users = ref([])
const roles = ref([])
const loading = ref(false)
const globalFilter = ref('')
const showAddModal = ref(false)
const newUser = ref({
  username: '',
  email: '',
  role_id: null
})

// Methods
const loadUsers = async () => {
  loading.value = true
  try {
    const response = await userService.getUsers()
    users.value = response.data
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Gagal memuat data user',
      life: 3000
    })
  } finally {
    loading.value = false
  }
}

const loadRoles = async () => {
  try {
    const response = await roleService.getRoles()
    roles.value = response.data
  } catch (error) {
    console.error('Error loading roles:', error)
  }
}

const getRoleSeverity = (roleName) => {
  switch (roleName) {
    case 'Super Admin': return 'danger'
    case 'Staff HRD': return 'info'
    case 'Manager': return 'warning'
    default: return 'secondary'
  }
}

const editUser = (user) => {
  // Implement edit functionality
  console.log('Edit user:', user)
}

const confirmDelete = (user) => {
  // Implement delete confirmation
  console.log('Delete user:', user)
}

// Update semua fungsi yang memerlukan notifikasi
const saveUser = async () => {
  try {
    await userService.createUser(newUser.value)
    toast.add({
      severity: 'success',
      summary: 'Berhasil',
      detail: 'User berhasil ditambahkan',
      life: 3000
    })
    showAddModal.value = false
    loadUsers()
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Gagal menambahkan user',
      life: 3000
    })
  }
}

const exportData = () => {
  // Implement export functionality
  console.log('Export data')
}

// Lifecycle
onMounted(() => {
  loadUsers()
  loadRoles()
})
</script>