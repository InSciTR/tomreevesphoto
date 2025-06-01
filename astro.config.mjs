// @ts-check
import { defineConfig } from 'astro/config';

import vue from '@astrojs/vue';

import tailwindcss from '@tailwindcss/vite';

import netlify from '@astrojs/netlify';

import mdx from '@astrojs/mdx';

// https://astro.build/config
export default defineConfig({
  integrations: [vue(), mdx()],

  vite: {
    plugins: [tailwindcss()]
  },

  adapter: netlify()
});