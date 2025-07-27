module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Custom colors yang kompatibel dengan PrimeVue
      colors: {
        'prime-blue': '#3B82F6',
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