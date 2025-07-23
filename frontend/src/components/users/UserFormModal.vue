<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-50 z-40 flex items-center justify-center" @click.self="close">
    <div class="bg-white p-8 rounded-lg shadow-xl w-full max-w-md">
      <h2 class="text-2xl font-bold mb-6">{{ title }}</h2>
      <form @submit.prevent="submitForm">
        <div class="space-y-4">
          <input v-model="form.username" type="text" placeholder="Username" required class="w-full px-3 py-2 border rounded">
          <input v-model="form.email" type="email" placeholder="Email" required class="w-full px-3 py-2 border rounded">
          
          <input v-if="!userToEdit" v-model="form.password" type="password" placeholder="Password" required class="w-full px-3 py-2 border rounded">
          
          <select v-model="form.role_id" required class="w-full px-3 py-2 border rounded">
            <option :value="null" disabled>Pilih Peran</option>
            <option v-for="role in roles" :key="role.role_id" :value="role.role_id">{{ role.role_name }}</option>
          </select>
        </div>
        <div class="flex justify-end space-x-4 mt-8">
          <button type="button" @click="close" class="px-4 py-2 bg-gray-200 rounded">Batal</button>
          <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded">Simpan</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import roleService from '@/services/roleService';

const props = defineProps({
  isOpen: Boolean,
  userToEdit: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['close', 'user-saved']);

const form = ref({
  username: '',
  email: '',
  password: '',
  role_id: null
});
const roles = ref([]);

// Judul dinamis
const title = computed(() => props.userToEdit ? 'Edit Pengguna' : 'Tambah Pengguna Baru');

// Awasi perubahan pada prop userToEdit
watch(() => props.userToEdit, (newUser) => {
  if (newUser) {
    // Mode Edit: isi form dengan data pengguna
    form.value = { ...newUser, password: '' }; // Kosongkan password saat edit
  } else {
    // Mode Tambah: reset form
    form.value = { username: '', email: '', password: '', role_id: null };
  }
});

const fetchRoles = async () => {
  try {
    const response = await roleService.getRoles();
    roles.value = response.data;
  } catch (error) { console.error("Gagal mengambil data peran:", error); }
};

const submitForm = () => {
  // Kirim event dengan membawa data form dan user (jika ada)
  emit('user-saved', { formData: form.value, user: props.userToEdit });
};

const close = () => {
  emit('close');
};

onMounted(fetchRoles);
</script>