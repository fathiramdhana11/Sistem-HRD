// File: frontend/src/stores/authStore.js

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('auth', () => {
  // Coba ambil data dari localStorage saat pertama kali store dibuat
  const initialAuth = JSON.parse(localStorage.getItem('auth'));

  const user = ref(initialAuth?.user || null);
  const token = ref(initialAuth?.access_token || null);
  const router = useRouter();

  // Getter untuk mengecek status login dengan mudah
  const isAuthenticated = computed(() => !!token.value);

  // Action untuk login
  function login(authData) {
    user.value = authData.user;
    token.value = authData.access_token;

    // Simpan ke localStorage agar tidak hilang saat refresh
    localStorage.setItem('auth', JSON.stringify(authData));

    // Arahkan ke dashboard setelah login berhasil
    router.push('/dashboard');
  }

  // Action untuk logout
  function logout() {
    user.value = null;
    token.value = null;
    localStorage.removeItem('auth');
    router.push('/login');
  }

  return { user, token, isAuthenticated, login, logout };
});