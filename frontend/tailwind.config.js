/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui')
  ],
  daisyui: {
    themes: [
      {
        bumblebee: {
          ...require("daisyui/src/theming/themes")["bumblebee"],
          primary: '#ff850f',
          secondary: '#cdcdcd',
          neutral: '#e5e4e4',
          ".btn": {
            'box-shadow': "2px 2px 6px 0px rgba(0, 0, 0, 0.2)",
            'color': '#fff',
            'padding': '0 2.5rem',
            'font-size': '1.125rem', /* 18px */
            'line-height': '1.75rem', /* 28px */
          }
        }
      }
    ]
  }
}

