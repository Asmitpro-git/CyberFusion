import type { Config } from 'tailwindcss';
import forms from '@tailwindcss/forms';

const config: Config = {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        cyber: {
          bg: '#0D1117',
          sidebar: '#111827',
          card: '#161B22',
          primary: '#00FF88',
          danger: '#EF4444',
          warning: '#F59E0B',
          info: '#3B82F6',
        },
      },
      boxShadow: {
        glow: '0 0 0 1px rgba(0, 255, 136, 0.18), 0 24px 80px rgba(0, 0, 0, 0.45)',
      },
      backgroundImage: {
        'cyber-grid':
          'radial-gradient(circle at top, rgba(0,255,136,0.12), transparent 30%), linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px)',
      },
    },
  },
  plugins: [forms],
};

export default config;
