import { getCollection, type CollectionEntry } from "astro:content";
import { TOPICS, TOPIC_ORDER, STATIC_PAGES, type Lang, type TopicKey } from "./i18n";

export type Page = CollectionEntry<"pages">;

export function langOf(p: Page): Lang {
  return p.id.split("/")[0] as Lang;
}

export function isIndex(p: Page) {
  return p.id.endsWith("/index");
}

export function slugOf(p: Page) {
  return p.id.split("/").slice(2).join("/");
}

export function urlOf(p: Page) {
  const [lang, folder] = p.id.split("/");
  return isIndex(p) ? `/${lang}/${folder}/` : `/${lang}/${folder}/${slugOf(p)}/`;
}

export function topicUrl(lang: Lang, topic: TopicKey) {
  return `/${lang}/${TOPICS[topic][lang]}/`;
}

export function staticUrl(lang: Lang, key: keyof typeof STATIC_PAGES) {
  return `/${lang}/${STATIC_PAGES[key][lang]}/`;
}

let cache: Page[] | undefined;
export async function allPages() {
  cache ??= await getCollection("pages");
  return cache;
}

export async function pagesFor(lang: Lang) {
  return (await allPages()).filter((p) => langOf(p) === lang);
}

/** Child pages of a topic (excluding its index), in reading order. */
export async function topicPages(lang: Lang, topic: TopicKey) {
  return (await pagesFor(lang))
    .filter((p) => p.data.topic === topic && !isIndex(p))
    .sort((a, b) => a.data.order - b.data.order);
}

export async function topicIndex(lang: Lang, topic: TopicKey) {
  return (await pagesFor(lang)).find((p) => p.data.topic === topic && isIndex(p));
}

/** Same page in the other language, if it exists. */
export async function counterpart(p: Page) {
  const other: Lang = langOf(p) === "en" ? "fr" : "en";
  return (await pagesFor(other)).find((q) => q.data.translationKey === p.data.translationKey);
}

/** Whole-site reading order, used for previous/next links. */
export async function readingOrder(lang: Lang) {
  const out: Page[] = [];
  for (const t of TOPIC_ORDER) {
    const idx = await topicIndex(lang, t);
    if (idx) out.push(idx);
    out.push(...(await topicPages(lang, t)));
  }
  return out;
}

/** Find an emergency page by keyword in its translationKey (falls back to the topic index). */
export async function emergencyLink(lang: Lang, words: string[]) {
  const pages = await topicPages(lang, "emergencies");
  const hit = pages.find((p) => words.some((w) => p.data.translationKey.includes(w)));
  return hit ? urlOf(hit) : topicUrl(lang, "emergencies");
}
