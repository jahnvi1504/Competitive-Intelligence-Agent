/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        darkBg: '#0b0f19',
        darkPanel: '#111827',
        darkBorder: '#1f2937',
        primary: '#4f46e5',
        primaryHover: '#4338ca',
        brandStarbucks: '#00704a',
        brandMcDonalds: '#ffc72c',
        brandSephora: '#e60023',
        brandMarriott: '#002d62',
        brandDelta: '#e01933',
      },
      backdropBlur: {
        xs: '2px',
      }
    },
  },
  plugins: [],
}
