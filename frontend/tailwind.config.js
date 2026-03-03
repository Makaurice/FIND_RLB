/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        remax: {
          50: '#f2f7ff',
          100: '#e9f4ff',
          300: '#88b9ff',
          500: '#0033A0',
          700: '#00267a'
        },
        accent: {
          500: '#FF2D2D'
        },
        slate: {
          300: '#cbd5e1',
          400: '#94a3b8',
          700: '#334155',
          900: '#0f172a',
        },
      },
    },
  },
  plugins: [],
};
