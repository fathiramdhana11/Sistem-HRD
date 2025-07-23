<template>
  <div>
    <div
      class="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-8"
    >
      <div>
        <h1 class="text-3xl font-bold text-slate-800">Dashboard</h1>
        <p class="mt-1 text-slate-500">
          Selamat datang kembali, {{ authStore.user?.username }}! 👋
        </p>
      </div>
      <button
        class="mt-4 sm:mt-0 flex items-center space-x-2 px-4 py-2 font-semibold text-white bg-blue-600 rounded-lg shadow-md hover:bg-blue-700 focus:outline-none transition-colors"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
            clip-rule="evenodd"
          />
        </svg>
        <span>Tambah Karyawan</span>
      </button>
    </div>

    <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
      <div
        v-for="stat in stats"
        :key="stat.title"
        class="bg-white p-6 rounded-xl border border-slate-200/80 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300 cursor-pointer"
      >
        <div class="flex justify-between items-start">
          <p class="text-sm font-medium text-slate-500">{{ stat.title }}</p>
          <div
            :class="`bg-${stat.color}-100 text-${stat.color}-600 p-2 rounded-lg`"
          >
            <component :is="stat.icon" class="w-6 h-6" />
          </div>
        </div>
        <p class="text-3xl font-bold text-slate-800 mt-2">{{ stat.value }}</p>
      </div>
    </div>

    <div class="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div
        class="lg:col-span-2 bg-white p-6 rounded-xl border border-slate-200/80 shadow-sm"
      >
        <h2 class="text-lg font-semibold text-slate-800 mb-4">
          Karyawan Baru per Bulan
        </h2>
        <div class="h-80">
          <Bar
            v-if="chartData.labels.length"
            :data="chartData"
            :options="chartOptions"
          />
        </div>
      </div>

      <div class="bg-white p-6 rounded-xl border border-slate-200/80 shadow-sm">
        <h2 class="text-lg font-semibold text-slate-800 mb-4">
          Aktivitas Terbaru
        </h2>
        <div class="space-y-4">
          <div
            v-for="activity in recentActivities"
            :key="activity.time"
            class="flex items-start space-x-3"
          >
            <div class="bg-slate-100 rounded-full p-2">
              <component :is="activity.icon" class="w-5 h-5 text-slate-500" />
            </div>
            <div class="flex-1">
              <p class="text-sm text-slate-700">
                <span class="font-semibold">{{ activity.name }}</span>
                {{ activity.activity }}
              </p>
              <p class="text-xs text-slate-400 mt-0.5">{{ activity.time }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, shallowRef } from "vue";
import { useAuthStore } from "@/stores/authStore";
import {
  UserGroupIcon,
  BriefcaseIcon,
  CalendarDaysIcon,
  UserPlusIcon,
  PencilSquareIcon,
  UserCircleIcon,
} from "@heroicons/vue/24/outline";
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

// Registrasi komponen chart.js
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);

const authStore = useAuthStore();

// --- Data Dummy untuk Tampilan ---
// TODO: Ganti data ini dengan panggilan API sesungguhnya
const stats = reactive([
  {
    title: "Karyawan Aktif",
    value: "0",
    icon: shallowRef(UserGroupIcon),
    color: "blue",
  },
  {
    title: "Cabang",
    value: "0",
    icon: shallowRef(BriefcaseIcon),
    color: "indigo",
  },
  {
    title: "Pengajuan Cuti",
    value: "0",
    icon: shallowRef(CalendarDaysIcon),
    color: "yellow",
  },
  {
    title: "Karyawan Baru",
    value: "0",
    icon: shallowRef(UserPlusIcon),
    color: "green",
  },
]);

const recentActivities = ref([
  {
    name: "Andi Pratama",
    activity: "mengajukan cuti tahunan.",
    time: "5 menit yang lalu",
    icon: shallowRef(CalendarDaysIcon),
  },
  {
    name: "Admin",
    activity: "menambahkan karyawan baru: Budi Santoso.",
    time: "1 jam yang lalu",
    icon: shallowRef(UserPlusIcon),
  },
  {
    name: "Rina Wijaya",
    activity: "memperbarui profil pribadinya.",
    time: "3 jam yang lalu",
    icon: shallowRef(PencilSquareIcon),
  },
  {
    name: "John Doe",
    activity: "ditetapkan sebagai Manajer Marketing.",
    time: "Kemarin",
    icon: shallowRef(UserCircleIcon),
  },
]);

const chartData = ref({
  labels: [],
  datasets: [],
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
    },
  },
  plugins: {
    legend: {
      display: false,
    },
  },
};

// Fungsi untuk mengambil data chart (simulasi)
const fetchDashboardData = () => {
  // TODO: Ganti dengan panggilan API sesungguhnya
  setTimeout(() => {
    chartData.value = {
      labels: ["Mar", "Apr", "Mei", "Jun", "Jul"],
      datasets: [
        {
          label: "Jumlah Karyawan",
          backgroundColor: "#6366f1", // Warna Indigo-500
          borderRadius: 6,
          data: [2, 5, 3, 6, 8],
        },
      ],
    };
  }, 500);
};

onMounted(() => {
  fetchDashboardData();
});
</script>
