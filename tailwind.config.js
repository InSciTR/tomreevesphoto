/** @type {import('tailwindcss').Config} */
const typography = require('@tailwindcss/typography');

module.exports = {
  content: [
    './src/**/*.{astro,html,js,jsx,ts,tsx,vue,md,mdx}', // kept everything you had
  ],
  plugins: [typography],                                 // ← add the plugin here
  theme: {
    extend: {
      typography: ({ theme }) => ({
        DEFAULT: {
          css: {
            /* breathing room for paragraphs */
            p: {
              marginTop: theme('spacing.4'),
              marginBottom: theme('spacing.4'),
              lineHeight: theme('lineHeight.relaxed'),
            },
            /* headings bold & spaced */
            'h1,h2,h3,h4': {
              marginTop: theme('spacing.8'),
              marginBottom: theme('spacing.2'),
              fontWeight: '700',
            },
            /* friendlier tables */
            table: { width: '100%', fontSize: theme('fontSize.sm') },
            thead: {
              borderBottom: `1px solid ${theme('colors.gray.600')}`,
              th: { paddingBottom: theme('spacing.2'), fontWeight: 600 },
            },
            'tbody tr': {
              borderBottom: `1px solid ${theme('colors.gray.700')}`,
            },
            'th,td': {
              paddingTop: theme('spacing.2'),
              paddingBottom: theme('spacing.2'),
              paddingLeft: theme('spacing.3'),
              paddingRight: theme('spacing.3'),
            },
          },
        },
      }),
    },
  },
};