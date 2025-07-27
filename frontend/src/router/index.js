import { createRouter, createWebHistory } from "vue-router";

// Import layout yang benar
import DefaultLayout from "@/layouts/DefaultLayout.vue";

// Import views
import LoginView from "@/views/LoginView.vue";
import DashboardView from "@/views/DashboardView.vue";
import UsersView from "@/views/UsersView.vue";
import RoleAccessView from "@/views/RoleAccessView.vue";

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'), 
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: DefaultLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/dashboard'
      },
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('@/views/DashboardView.vue')
      },
      // Manajemen Karyawan
      {
        path: '/karyawan/data',
        name: 'DataKaryawan',
        component: () => import('@/views/DataKaryawanView.vue')
      },
      {
        path: '/karyawan/tambah',
        name: 'TambahKaryawan',
        component: () => import('@/views/DataKaryawanView.vue')
      },
      // Manajemen Absensi
      {
        path: '/absensi/rekap',
        name: 'RekapAbsensi',
        component: () => import('@/views/DashboardView.vue')
      },
      {
        path: '/absensi/input',
        name: 'InputAbsensi',
        component: () => import('@/views/DashboardView.vue')
      },
      // Pengajuan Izin & Cuti
      {
        path: '/izin/cuti',
        name: 'FormCuti',
        component: () => import('@/views/DashboardView.vue')
      },
      {
        path: '/izin/sakit',
        name: 'FormSakit',
        component: () => import('@/views/DashboardView.vue')
      },
      // Penggajian
      {
        path: '/penggajian/bulanan',
        name: 'GajiBulanan',
        component: () => import('@/views/DashboardView.vue')
      },
      {
        path: '/penggajian/komponen',
        name: 'KomponenGaji',
        component: () => import('@/views/DashboardView.vue')
      },
      // Slip Gaji
      {
        path: '/slip-gaji',
        name: 'SlipGaji',
        component: () => import('@/views/SlipGajiView.vue')
      },
      // Laporan
      {
        path: '/laporan/absensi',
        name: 'LaporanAbsensi',
        component: () => import('@/views/DashboardView.vue')
      },
      {
        path: '/laporan/gaji',
        name: 'LaporanGaji',
        component: () => import('@/views/DashboardView.vue')
      },
      // Manajemen User
      {
        path: '/user-management/list',
        name: 'UserManagementList',
        component: () => import('@/views/UsersView.vue')
      },
      {
        path: '/users',
        name: 'Users',
        component: () => import('@/views/UsersView.vue')
      },
      {
        path: '/user-management/roles',
        name: 'UserManagementRoles',
        component: () => import('@/views/RoleAccessView.vue')
      },
      {
        path: '/role-access',
        name: 'RoleAccess',
        component: () => import('@/views/RoleAccessView.vue')
      },
      // Log Aktivitas
      {
        path: '/log-aktivitas',
        name: 'LogAktivitas',
        component: () => import('@/views/LogAktivitasView.vue')  
      },
      // Pengaturan
      {
        path: '/pengaturan',
        name: 'Settings',
        component: () => import('@/views/PengaturanView.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation Guard yang disempurnakan
router.beforeEach((to, from, next) => {
  // Cukup periksa apakah item 'auth' ada di localStorage
  const isAuthenticated = !!localStorage.getItem("auth");

  // Cek apakah rute yang dituju memerlukan autentikasi
  if (to.meta.requiresAuth && !isAuthenticated) {
    // Jika rute butuh login dan pengguna belum login, arahkan ke /login
    next({ name: "Login" });
  }
  // Cek apakah pengguna yang sudah login mencoba mengakses halaman login
  else if (to.name === "Login" && isAuthenticated) {
    // Jika ya, arahkan mereka ke Dashboard
    next({ name: "Dashboard" });
  }
  // Jika semua kondisi aman, lanjutkan navigasi
  else {
    next();
  }
});

export default router;
