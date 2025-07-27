<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl font-bold text-slate-800">Manajemen Pengguna</h1>
      <button
        @click="openAddModal"
        class="px-4 py-2 font-semibold text-white bg-blue-600 rounded-md hover:bg-blue-700"
      >
        + Tambah Pengguna
      </button>
    </div>

    <div
      class="overflow-x-auto bg-white rounded-lg shadow-sm border border-slate-200"
    >
      <table class="w-full text-sm text-left text-slate-500">
        <thead class="text-xs text-slate-700 uppercase bg-slate-50">
          <tr>
            <th scope="col" class="px-6 py-3">Username</th>
            <th scope="col" class="px-6 py-3">Email</th>
            <th scope="col" class="px-6 py-3">Role</th>
            <th scope="col" class="px-6 py-3">Status</th>
            <th scope="col" class="px-6 py-3 text-center">Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="isLoading">
            <td colspan="5" class="text-center py-4">Memuat data...</td>
          </tr>
          <tr v-else-if="users.length === 0">
            <td colspan="5" class="text-center py-4">
              Tidak ada data pengguna.
            </td>
          </tr>
          <tr
            v-else
            v-for="user in users"
            :key="user.user_id"
            class="bg-white border-b hover:bg-slate-50"
          >
            <td class="px-6 py-4 font-medium text-slate-900">
              {{ user.username }}
            </td>
            <td class="px-6 py-4">{{ user.email }}</td>
            <td class="px-6 py-4">
              {{ user.role ? user.role.role_name : "N/A" }}
            </td>
            <td class="px-6 py-4">
              <span
                :class="[
                  'px-2 py-1 text-xs font-semibold rounded-full',
                  user.status === 'active'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-yellow-100 text-yellow-800',
                ]"
              >
                {{ user.status }}
              </span>
            </td>
            <td class="px-6 py-4 text-center">
              <button
                @click="openEditModal(user)"
                class="font-medium text-blue-600 hover:underline mr-3"
              >
                Edit
              </button>
              <button
                @click="deleteUser(user)"
                class="font-medium text-red-600 hover:underline"
              >
                Hapus
              </button>
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
import { ref, onMounted } from "vue";
import userService from "@/services/userService";
import { useToast } from "@/composables/useToast"; // Ganti dari useAlert
import UserFormModal from "@/components/users/UserFormModal.vue";

const users = ref([]);
const isLoading = ref(true);
const toast = useToast(); // Ganti dari alert
const isModalOpen = ref(false);
const userToEdit = ref(null);

const fetchUsers = async () => {
  isLoading.value = true;
  try {
    const response = await userService.getUsers();
    users.value = response.data;
  } catch (error) {
    toast.error('Gagal Memuat Data', 'Tidak dapat memuat data pengguna. Silakan coba lagi.'); // Update
    console.error(error);
  } finally {
    isLoading.value = false;
  }
};

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
      const { user_id, ...updateData } = formData;
      await userService.updateUser(user.user_id, updateData);
      toast.success('Berhasil!', `Pengguna ${user.username} berhasil diperbarui!`); // Update
    } else {
      await userService.createUser(formData);
      toast.success('Berhasil!', "Pengguna baru berhasil ditambahkan!"); // Update
    }
    closeModal();
    fetchUsers();
  } catch (error) {
    toast.error('Gagal Menyimpan', error.response?.data?.detail || "Terjadi kesalahan."); // Update
  }
};

const deleteUser = async (user) => {
  if (
    window.confirm(
      `Apakah Anda yakin ingin menghapus pengguna ${user.username}?`
    )
  ) {
    try {
      await userService.deleteUser(user.user_id);
      toast.success('Berhasil!', `Pengguna ${user.username} berhasil dihapus.`); // Update
      fetchUsers();
    } catch (error) {
      toast.error('Gagal Menghapus', error.response?.data?.detail || "Gagal menghapus pengguna."); // Update
    }
  }
};

onMounted(fetchUsers);
</script>
