/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'emerald-glow': '#10B981',
        'coral-danger': '#F43F5E',
        'amber-warning': '#F59E0B',
        'violet-agent': '#8B5CF6',
        'cyan-supply': '#06B6D4'
      }
    },
  },
  plugins: [],
}
