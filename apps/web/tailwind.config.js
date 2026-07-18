// Palette mirrors packages/design-tokens (kept in sync manually — Tailwind config is loaded as
// CommonJS at build time and can't cleanly require the ESM tokens package).

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./app/**/*.{js,jsx}', './components/**/*.{js,jsx}', './features/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        bg: '#0b0d12',
        surface: '#151922',
        surfaceAlt: '#1e242f',
        border: '#2a313d',
        text: '#f5f7fa',
        muted: '#9aa4b2',
        primary: '#e50914',
      },
    },
  },
  plugins: [],
};
