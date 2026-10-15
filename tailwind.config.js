/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        slate: {
          50: '#F8FAFC',
          200: '#E2E8F0',
          600: '#475569',
          700: '#334155',
          900: '#0F172A',
        }
      }
    },
  },
  plugins: [],
}
