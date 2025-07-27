import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path' 

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      // Tambahkan alias untuk Vue runtime dengan compiler
      'vue': 'vue/dist/vue.esm-bundler.js'
    }
  },
  // Tambahkan define untuk Vue feature flags
  define: {
    __VUE_OPTIONS_API__: true,
    __VUE_PROD_DEVTOOLS__: false
  }
})
