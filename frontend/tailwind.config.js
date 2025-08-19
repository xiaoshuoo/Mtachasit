/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        accentPurple: '#8B5CF6',
        accentPink: '#EC4899',
        accentBlue: '#3B82F6',
      },
    },
  },
  plugins: [],
}


