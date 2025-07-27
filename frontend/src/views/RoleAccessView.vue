<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl font-bold text-slate-800">Manajemen Akses Menu</h1>
    </div>

    <div class="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
      <div class="mb-6">
        <label class="block text-sm font-medium text-slate-700 mb-2"
          >Pilih Role</label
        >
        <select
          v-model="selectedRoleId"
          @change="loadRoleMenuAccess"
          class="w-full md:w-64 px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option :value="null" disabled>Pilih Role</option>
          <option
            v-for="role in roles"
            :key="role.role_id"
            :value="role.role_id"
          >
            {{ role.role_name }}
          </option>
        </select>
      </div>

      <div v-if="selectedRoleId" class="space-y-6">
        <div v-if="isLoading" class="text-center py-4">
          <div
            class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"
          ></div>
          <p class="mt-2 text-slate-500">Memuat data...</p>
        </div>

        <template v-else>
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-semibold text-slate-800">Daftar Menu</h2>
            <button
              @click="saveChanges"
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-slate-400"
              :disabled="isSaving"
            >
              {{ isSaving ? "Menyimpan..." : "Simpan Perubahan" }}
            </button>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-sm text-left text-slate-500">
              <thead class="text-xs text-slate-700 uppercase bg-slate-50">
                <tr>
                  <th scope="col" class="px-6 py-3">Menu</th>
                  <th scope="col" class="px-6 py-3">Route</th>
                  <th scope="col" class="px-6 py-3 text-center">Akses</th>
                </tr>
              </thead>
              <tbody>
                <template
                  v-for="(menu, index) in flattenedMenus"
                  :key="menu.menu_id"
                >
                  <tr class="bg-white border-b hover:bg-slate-50">
                    <td
                      class="px-6 py-4 font-medium text-slate-900"
                      :style="{ paddingLeft: `${menu.depth * 20 + 24}px` }"
                    >
                      <span v-if="menu.depth > 0" class="text-slate-400 mr-2"
                        >└─</span
                      >
                      {{ menu.menu_name }}
                    </td>
                    <td class="px-6 py-4">{{ menu.route }}</td>
                    <td class="px-6 py-4 text-center">
                      <input
                        type="checkbox"
                        :checked="isMenuChecked(menu.menu_id)"
                        @change="toggleMenuAccess(menu.menu_id)"
                        class="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                      />
                    </td>
                  </tr>
                </template>
              </tbody>
            </table>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import roleService from "@/services/roleService";
import menuService from "@/services/menuService";
import roleMenuAccessService from "@/services/roleMenuAccessService";
import { useToast } from "@/composables/useToast"; // Ganti dari useAlert

import { useAuthStore } from "@/stores/authStore";
const authStore = useAuthStore();

const roles = ref([]);
const menus = ref([]);
const roleMenuAccess = ref([]);
const selectedRoleId = ref(null);
const isLoading = ref(false);
const isSaving = ref(false);
const toast = useToast(); // Ganti dari alert

// Tambahkan state untuk melacak menu yang dicentang di UI
const checkedMenuIds = ref([]);

// Fungsi untuk meratakan struktur menu bersarang menjadi array datar dengan informasi kedalaman
const flattenedMenus = computed(() => {
  const result = [];

  function flatten(items, depth = 0) {
    items.forEach((item) => {
      // Salin item dan tambahkan properti depth
      const flatItem = { ...item, depth };
      // Hapus sub_menus agar tidak duplikat dalam hasil akhir
      delete flatItem.sub_menus;
      // Tambahkan ke hasil
      result.push(flatItem);

      // Rekursif untuk sub-menu jika ada
      if (item.sub_menus && item.sub_menus.length > 0) {
        flatten(item.sub_menus, depth + 1);
      }
    });
  }

  flatten(menus.value);
  return result;
});

// Fungsi untuk mengecek apakah menu memiliki akses
const isMenuAccessGranted = (menuId) => {
  return roleMenuAccess.value.some(
    (access) =>
      access.role_id === selectedRoleId.value && access.menu_id === menuId
  );
};

// Fungsi untuk mengecek apakah menu dicentang di UI
const isMenuChecked = (menuId) => {
  return checkedMenuIds.value.includes(menuId);
};

// Fungsi untuk toggle checkbox di UI
const toggleMenuAccess = (menuId) => {
  const index = checkedMenuIds.value.indexOf(menuId);
  if (index >= 0) {
    // Jika sudah ada, hapus dari array
    checkedMenuIds.value.splice(index, 1);
  } else {
    // Jika belum ada, tambahkan ke array
    checkedMenuIds.value.push(menuId);
  }
};

// Fungsi untuk memuat data role
const loadRoles = async () => {
  try {
    const response = await roleService.getRoles();
    roles.value = response.data;
  } catch (error) {
    toast.error("Gagal Memuat Data", "Gagal memuat data role"); // Update
    console.error("Error loading roles:", error);
  }
};

// Fungsi untuk memuat data menu
const loadMenus = async () => {
  try {
    const response = await menuService.getMenuTree();
    menus.value = response.data;
  } catch (error) {
    toast.error("Gagal Memuat Data", "Gagal memuat data menu"); // Update
    console.error("Error loading menus:", error);
  }
};

// Modifikasi loadRoleMenuAccess untuk mengisi checkedMenuIds
const loadRoleMenuAccess = async () => {
  if (!selectedRoleId.value) return;

  isLoading.value = true;
  try {
    const response = await roleMenuAccessService.getAllRoleMenuAccess();
    roleMenuAccess.value = response.data;

    // Isi checkedMenuIds dengan menu_id yang sudah memiliki akses
    checkedMenuIds.value = response.data
      .filter((access) => access.role_id === selectedRoleId.value)
      .map((access) => access.menu_id);
  } catch (error) {
    toast.error("Gagal Memuat Data", "Gagal memuat data akses menu"); // Update
    console.error("Error loading role menu access:", error);
  } finally {
    isLoading.value = false;
  }
};

// Setelah berhasil save changes
const saveChanges = async () => {
  try {
    if (!selectedRoleId.value) return;

    isSaving.value = true;
    // 1. Dapatkan semua akses menu yang ada untuk role ini
    const response = await roleMenuAccessService.getAllRoleMenuAccess();
    const existingAccess = response.data.filter(
      (access) => access.role_id === selectedRoleId.value
    );

    const existingMenuIds = existingAccess.map((access) => access.menu_id);

    // Menu yang perlu ditambahkan (ada di checkedMenuIds tapi tidak ada di existing)
    const menuIdsToAdd = checkedMenuIds.value.filter(
      (id) => !existingMenuIds.includes(id)
    );

    // Menu yang perlu dihapus (ada di existing tapi tidak ada di checkedMenuIds)
    const menuIdsToRemove = existingMenuIds.filter(
      (id) => !checkedMenuIds.value.includes(id)
    );

    // 3. Lakukan operasi tambah dan hapus
    const addPromises = menuIdsToAdd.map((menuId) =>
      roleMenuAccessService.createRoleMenuAccess({
        role_id: selectedRoleId.value,
        menu_id: menuId,
      })
    );

    const removePromises = menuIdsToRemove.map((menuId) =>
      roleMenuAccessService.deleteRoleMenuAccess(selectedRoleId.value, menuId)
    );

    await Promise.all([...addPromises, ...removePromises]);

    toast.success("Berhasil!", "Perubahan hak akses berhasil disimpan");
    
    // Trigger refresh menu
    console.log('🔄 Triggering menu refresh after role access changes');
    window.dispatchEvent(new Event("menu-updated"));
    
    // Show success message
  } catch (error) {
    toast.error("Gagal Menyimpan", "Gagal menyimpan perubahan"); // Update
    console.error("Error saving changes:", error);
  } finally {
    isSaving.value = false;
  }
};

onMounted(async () => {
  await Promise.all([loadRoles(), loadMenus()]);
});
</script>
