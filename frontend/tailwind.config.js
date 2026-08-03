/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#2563EB',
          50: '#EFF6FF',
          100: '#DBEAFE',
          500: '#2563EB',
          600: '#1D4ED8',
          700: '#1E40AF',
        },
        secondary: {
          DEFAULT: '#10B981',
          500: '#10B981',
          600: '#059669',
        },
        danger: {
          DEFAULT: '#EF4444',
          500: '#EF4444',
          600: '#DC2626',
        },
        dark: {
          card: '#1E293B',
          bg: '#0F172A',
          border: '#334155'
        }
      },
    },
  },
  plugins: [],
}
