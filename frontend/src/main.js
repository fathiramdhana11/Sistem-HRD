// File: frontend/src/main.js

import { createApp } from 'vue'
import { createPinia } from 'pinia' // Asumsikan Anda menggunakan Pinia
import App from './App.vue'
import router from './router'
import './styles/index.css' // File CSS utama Anda

// --- TAMBAHAN BARU ---
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css' // Impor CSS defaultnya

const app = createApp(App)
const pinia = createPinia() // Inisialisasi Pinia

app.use(pinia) // Gunakan Pinia sebelum router
app.use(router)

// --- TAMBAHAN BARU: Konfigurasi Toast ---
const options = {
  position: "top-right",
  timeout: 4000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: "button",
  icon: true,
  rtl: false,
  transition: "Vue-Toastification__bounce",
  maxToasts: 5,
  newestOnTop: true
};

app.use(Toast, options);
// ------------------------------------

app.mount('#app')