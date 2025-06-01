import { defineCollection, z } from 'astro:content';

const words = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    pubDate: z.date(),
    excerpt: z.string().optional(),
    layout: z.string().optional(), // Enables layout frontmatter
  }),
});

export const collections = {
  words,
};
