import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const words = defineCollection({
  type: 'content',
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/words" }),
  schema: z.object({
    title: z.string(),
    pubDate: z.date(),
    excerpt: z.string().optional(),
  }),
});

export const collections = { words };
