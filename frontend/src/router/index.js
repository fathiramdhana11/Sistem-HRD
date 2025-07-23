import { createRouter, createWebHistory } from 'vue-router'

// Impor komponen Layout Utama
import DefaultLayout from '@/layouts/DefaultLayout.vue'

// Impor komponen Views (halaman) dengan nama baru yang sudah kita standarkan
import LoginView from '@/views/LoginView.vue'
import DashboardView from '@/views/DashboardView.vue'
import UsersView from '@/views/UsersView.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    // Semua rute yang berada di dalam path ini akan menggunakan DefaultLayout.vue
    // yang berisi Sidebar dan Header.
    path: '/',
    component: DefaultLayout,
    meta: { requiresAuth: true }, // <-- Semua rute di bawah ini butuh login
    children: [
      {
        // Jika pengguna mengakses '/', arahkan otomatis ke dashboard
        path: '', 
        redirect: '/dashboard'
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: DashboardView
      },
      {
        path: 'users', // <-- Rute baru untuk Manajemen Pengguna
        name: 'Users',
        component: UsersView
      }
      // Tambahkan rute lain yang memerlukan login di sini
    ]
  },
  // (Opsional tapi praktik yang baik) Redirect semua path yang tidak ditemukan ke halaman utama
  { 
    path: '/:pathMatch(.*)*', 
    redirect: '/' 
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation Guard yang disempurnakan
router.beforeEach((to, from, next) => {
  // Cukup periksa apakah item 'auth' ada di localStorage
  const isAuthenticated = !!localStorage.getItem('auth');

  // Cek apakah rute yang dituju memerlukan autentikasi
  if (to.meta.requiresAuth && !isAuthenticated) {
    // Jika rute butuh login dan pengguna belum login, arahkan ke /login
    next({ name: 'Login' });
  } 
  // Cek apakah pengguna yang sudah login mencoba mengakses halaman login
  else if (to.name === 'Login' && isAuthenticated) {
    // Jika ya, arahkan mereka ke Dashboard
    next({ name: 'Dashboard' });
  } 
  // Jika semua kondisi aman, lanjutkan navigasi
  else {
    next();
  }
})

export default router