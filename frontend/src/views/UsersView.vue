<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl font-bold text-slate-800">Manajemen Pengguna</h1>
      <button @click="openAddModal" class="px-4 py-2 font-semibold text-white bg-blue-600 rounded-md hover:bg-blue-700">
        + Tambah Pengguna
      </button>
    </div>
    
    <div class="bg-white rounded-lg shadow-sm border border-slate-200">
    <table>
      <tbody>
        <tr v-for="user in users" :key="user.user_id" class="bg-white border-b hover:bg-slate-50">
          <td class="px-6 py-4 font-medium text-slate-900">{{ user.username }}</td>
          <td class="px-6 py-4">{{ user.email }}</td>
          <td class="px-6 py-4">{{ user.role ? user.role.role_name : 'N/A' }}</td>
          <td class="px-6 py-4">
            <span :class="['px-2 py-1 text-xs font-semibold rounded-full', user.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800']">
              {{ user.status }}
            </span>
          </td>
          <td class="px-6 py-4 text-center">
            <button @click="openEditModal(user)" class="font-medium text-blue-600 hover:underline mr-3">Edit</button>
            <button class="font-medium text-red-600 hover:underline">Hapus</button>
          </td>
        </tr>
      </tbody>
    </table>
    </div>

    <UserFormModal 
      :is-open="isModalOpen" 
      :user-to-edit="userToEdit"
      @close="closeModal"
      @user-saved="handleUserSaved"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import userService from '@/services/userService';
import { useAlert } from '@/composables/useAlert';
import UserFormModal from '@/components/users/UserFormModal.vue';

const users = ref([]);
const isLoading = ref(true);
const alert = useAlert();
const isModalOpen = ref(false);
const userToEdit = ref(null); // <-- State untuk menyimpan data user yang akan di-edit

const fetchUsers = async () => { /* ... (biarkan sama) ... */ };

const openAddModal = () => {
  userToEdit.value = null; // Pastikan kosong untuk mode "Tambah"
  isModalOpen.value = true;
};

const openEditModal = (user) => {
  userToEdit.value = { ...user }; // Isi dengan data user yang diklik
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  userToEdit.value = null;
};

const handleUserSaved = async ({ formData, user }) => {
  try {
    if (user) {
      // Mode Edit
      const { user_id, ...updateData } = formData;
      await userService.updateUser(user.user_id, updateData);
      alert.success(`Pengguna ${user.username} berhasil diperbarui!`);
    } else {
      // Mode Tambah
      await userService.createUser(formData);
      alert.success("Pengguna baru berhasil ditambahkan!");
    }
    closeModal();
    fetchUsers(); // Muat ulang data tabel
  } catch (error) {
    alert.error(error.response?.data?.detail || "Terjadi kesalahan.");
  }
};

onMounted(fetchUsers);
</script>