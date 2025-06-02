import { defineCollection, z } from 'astro:content';

const words = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    pubDate: z.date(),
    excerpt: z.string().optional(),
  }),
});

export const collections = {
  words,
};
