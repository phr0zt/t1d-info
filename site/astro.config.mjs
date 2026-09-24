import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import remarkDirective from "remark-directive";
import { remarkCallouts } from "./src/lib/remark-callouts.mjs";

export default defineConfig({
  site: process.env.SITE_URL || "https://t1de.krkt.co",
  trailingSlash: "always",
  i18n: {
    locales: ["en", "fr"],
    defaultLocale: "en",
    routing: { prefixDefaultLocale: true, redirectToDefaultLocale: false },
  },
  integrations: [
    sitemap({
      filter: (page) => !page.includes("/print/") && !/\/(search|recherche)\/$/.test(page),
      i18n: { defaultLocale: "en", locales: { en: "en-CA", fr: "fr-CA" } },
    }),
  ],
  markdown: {
    remarkPlugins: [remarkDirective, remarkCallouts],
    smartypants: false,
  },
});
