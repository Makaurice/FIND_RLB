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
        'amber': {
          '400': '#f7ca18',
          '500': '#f7ca18',
          '600': '#dab115',
        },
        'slate': {
          '300': '#cbd5e1',
          '400': '#94a3b8',
          '700': '#334155',
          '900': '#0f172a',
        },
        'blue': {
          '400': '#5bc0eb',
        },
      },
    },
  },
  plugins: [],
};
