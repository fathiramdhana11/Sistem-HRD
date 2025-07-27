<template>
  <div
    class="flex items-center justify-center min-h-screen bg-gradient-to-br from-slate-100 to-slate-200"
  >
    <div class="w-full max-w-md p-8 space-y-8 bg-white rounded-2xl shadow-xl">
      <div class="text-center">
        <h2 class="text-3xl font-bold text-slate-800">Welcome Back</h2>
        <p class="mt-2 text-sm text-slate-500">
          Please sign in to your HRIS account
        </p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div class="relative">
          <span class="absolute inset-y-0 left-0 flex items-center pl-3">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5 text-slate-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
              />
            </svg>
          </span>
          <input
            v-model="username"
            id="username"
            name="username"
            type="text"
            autocomplete="username"
            required
            placeholder="Username"
            class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
          />
        </div>

        <div class="relative">
          <span class="absolute inset-y-0 left-0 flex items-center pl-3">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5 text-slate-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
              />
            </svg>
          </span>
          <input
            v-model="password"
            id="password"
            name="password"
            type="password"
            autocomplete="current-password"
            required
            placeholder="Password"
            class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
          />
        </div>

        <div>
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full px-4 py-3 font-semibold text-white bg-blue-600 rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-slate-400 disabled:cursor-not-allowed transition-all duration-300"
          >
            {{ isLoading ? "Loading..." : "Sign In" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import authService from "@/services/authService";
import { useAuthStore } from "@/stores/authStore";
import { useToast } from "@/composables/useToast"; // Ganti dari useAlert

const username = ref("");
const password = ref("");
const isLoading = ref(false);

const authStore = useAuthStore();
const toast = useToast(); // Ganti dari alert

const handleLogin = async () => {
  isLoading.value = true;
  
  // Bersihkan localStorage sebelum login untuk mencegah konflik
  localStorage.removeItem('auth');
  
  try {
    const response = await authService.login({
      username: username.value,
      password: password.value
    });
    toast.success('Login Berhasil!', `Selamat datang, ${response.data.user.username}!`);
    authStore.login(response.data);
  } catch (err) {
    // Improved error handling dengan pesan yang lebih spesifik
    let errorTitle = 'Login Gagal';
    let errorMessage = 'Terjadi kesalahan saat login';
    
    if (err.response) {
      // Server responded with error status
      switch (err.response.status) {
        case 401:
          errorTitle = 'Username atau Password Salah';
          errorMessage = 'Silakan periksa kembali username dan password Anda.';
          break;
        case 422:
          errorTitle = 'Data Tidak Valid';
          errorMessage = 'Format username atau password tidak valid.';
          break;
        case 500:
          errorTitle = 'Server Error';
          errorMessage = 'Terjadi kesalahan pada server. Silakan coba lagi.';
          break;
        default:
          errorMessage = err.response.data?.detail || 'Terjadi kesalahan saat login';
      }
    } else if (err.request) {
      // Network error
      errorTitle = 'Koneksi Error';
      errorMessage = 'Tidak dapat terhubung ke server. Periksa koneksi internet Anda.';
    }
    
    // Tampilkan alert yang jelas untuk user
    toast.error(errorTitle, errorMessage);
  } finally {
    isLoading.value = false;
  }
};
</script>
