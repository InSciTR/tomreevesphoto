/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{astro,html,js,jsx,ts,tsx,vue}",
  ],
  theme: {
    extend: {
      boxShadow: {
        glow: '0 -20px 20px #191919',
      },
    },
  },
  plugins: [],
};
