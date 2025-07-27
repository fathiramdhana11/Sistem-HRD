module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // Enable class-based dark mode
  theme: {
    extend: {
      // Your existing theme extensions
    },
  },
  plugins: [],
}
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Custom colors yang kompatibel dengan PrimeVue
      colors: {
        'prime-blue': '#3B82F6',
        'prime-blue-dark': '#1E40AF',
        'prime-surface': '#FFFFFF',
        'prime-text': '#495057',
      }
    },
  },
  plugins: [],
  // Pastikan Tailwind tidak override PrimeVue styles
  corePlugins: {
    preflight: true,
  }
}
