import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const pages = defineCollection({
  loader: glob({
    pattern: "**/*.md",
    base: "./src/content/pages",
    // Keep the real path ("en/food/index", "fr/alimentation/lire-une-etiquette").
    generateId: ({ entry }) => entry.replace(/\.md$/, ""),
  }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    topic: z.enum(["start", "emergencies", "food", "movement", "medications", "drugs-alcohol", "complications", "people", "help"]),
    order: z.number(),
    translationKey: z.string(),
    sources: z.array(z.string()).default([]),
    reviewed: z.coerce.date(),
  }),
});

export const collections = { pages };
