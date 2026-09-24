#!/usr/bin/env node
// Post-build checks: internal links resolve, every page has its translation,
// and the editorial word list (README rules 1 and 3) isn't violated in prose.
import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { join, relative } from "node:path";

const DIST = new URL("../dist/", import.meta.url).pathname;
const CONTENT = new URL("../src/content/pages/", import.meta.url).pathname;
const walk = (d) => readdirSync(d).flatMap((f) => (statSync(join(d, f)).isDirectory() ? walk(join(d, f)) : [join(d, f)]));
let problems = 0;
const report = (msg) => { problems++; console.log(msg); };

// 1. Internal links (ignores /print/ pages' own links and downloads, which are built separately)
for (const file of walk(DIST).filter((f) => f.endsWith(".html"))) {
  const html = readFileSync(file, "utf8");
  for (const [, href] of html.matchAll(/href="(\/[^"#?]*)/g)) {
    if (href.startsWith("/downloads/") || href.startsWith("/pagefind/") || href.startsWith("/_astro/")) continue;
    const target = join(DIST, href, href.endsWith("/") ? "index.html" : "");
    if (!existsSync(target) && !existsSync(join(DIST, href))) report(`broken link ${href} in /${relative(DIST, file)}`);
  }
}

// 2. Translation pairs
const keys = { en: new Map(), fr: new Map() };
for (const file of walk(CONTENT).filter((f) => f.endsWith(".md"))) {
  const lang = relative(CONTENT, file).split("/")[0];
  const key = readFileSync(file, "utf8").match(/^translationKey:\s*"?([^"\n]+)"?/m)?.[1];
  keys[lang].set(key, relative(CONTENT, file));
}
for (const [a, b] of [["en", "fr"], ["fr", "en"]])
  for (const [k, f] of keys[a]) if (!keys[b].has(k)) report(`no ${b} twin for ${f} (${k})`);

// 3. Editorial words, outside quoted examples of what not to say
const banned = [
  [/\b(glycemic |blood[- ]sugar |diabetes )control\b/i, "control"],
  [/\b(good|bad) (blood sugar|numbers?|readings?)\b/i, "good/bad blood sugar"],
  [/\b(non-?)?complian(t|ce)\b/i, "compliant"],
  [/\ba diabetic\b|\bdiabetics\b/i, "diabetic as a noun"],
  [/\bwill (cause|kill|lead to)\b/i, "certainty language"],
  [/\bcontrôle (glycémique|de la glycémie|du diabète)\b/i, "contrôle"],
  [/\bbonne?s? glycémies?\b|\bmauvaises? glycémies?\b/i, "bonne/mauvaise glycémie"],
  [/\bles diabétiques\b|\bun diabétique\b/i, "diabétique (nom)"],
];
// Proper names and sentences that describe a belief in order to correct it.
const ALLOW = ["Diabetes Control and Complications Trial", "assume that dosing before the meal will cause"];
for (const file of walk(CONTENT).filter((f) => f.endsWith(".md"))) {
  readFileSync(file, "utf8").split("\n").forEach((line, i) => {
    if (/[“"«]/.test(line)) return; // quoted speech is where these appear on purpose
    if (ALLOW.some((a) => line.includes(a))) return;
    for (const [re, label] of banned) if (re.test(line)) report(`${label}: ${relative(CONTENT, file)}:${i + 1}: ${line.trim().slice(0, 120)}`);
  });
}

console.log(problems ? `\n${problems} problem(s)` : "all checks passed");
process.exit(problems ? 1 : 0);
