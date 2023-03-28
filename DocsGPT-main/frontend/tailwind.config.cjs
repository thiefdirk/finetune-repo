/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      spacing: {
        112: '28rem',
        128: '32rem',
      },
      colors: {
        'eerie-black': '#212121',
        'black-1000': '#343541',
        jet: '#343541',
        'gray-alpha': 'rgba(0,0,0, .1)',
        'gray-1000': '#F6F6F6',
        'gray-2000': 'rgba(0, 0, 0, 0.5)',
        'gray-3000': 'rgba(243, 243, 243, 1)',
        'gray-4000': '#949494',
        'gray-5000': '#BBBBBB',
        'gray-6000': '#757575',
        'red-1000': 'rgb(254, 202, 202)',
        'red-2000': '#F44336',
        'red-3000': '#621B16',
        'blue-1000': '#7D54D1',
        'blue-2000': '#002B49',
        'blue-3000': '#4B02E2',
        'blue-4000': 'rgba(0, 125, 255, 0.36)',
        'blue-5000': 'rgba(0, 125, 255)',
      },
    },
  },
  plugins: [],
};
