#!/usr/bin/env node
// Builds public/downloads/<lang>/krkt-t1de-<bundle>-<lang>.{pdf,docx,pptx}.
//
// Runs locally (needs Google Chrome and pandoc); the outputs are committed so
// the Railway build never needs a browser. Run after `astro build`:
//   npm run build && npm run downloads && npm run build
import { spawn, execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync, readdirSync } from "node:fs";
import { join, resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import pptxgen from "pptxgenjs";
import puppeteer from "puppeteer-core";

const SITE = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const REPO = resolve(SITE, "..");
const DIST = join(SITE, "dist");
const OUT = join(SITE, "public", "downloads");
const CHROME = process.env.CHROME || "google-chrome-stable";
const PORT = 4799;
const LANGS = ["en", "fr"];
const BUNDLES = [
  ["00-overview", "00-master", { en: "The whole picture", fr: "Le portrait complet" }],
  ["01-food", "01-food", { en: "Food", fr: "Alimentation" }],
  ["02-movement", "02-movement", { en: "Movement", fr: "Activité physique" }],
  ["03-medications", "03-medications", { en: "Medications", fr: "Médicaments" }],
  ["04-drugs-alcohol", "04-drugs-alcohol", { en: "Drugs & alcohol", fr: "Drogues et alcool" }],
  ["05-complications", "05-complications", { en: "Complications", fr: "Complications" }],
];
const only = process.argv.slice(2); // optional: formats to build, e.g. `pdf docx`
const want = (f) => only.length === 0 || only.includes(f);

if (!existsSync(DIST)) throw new Error("Run `npm run build` first — dist/ is missing.");

const chrome = (args) => execFileSync(CHROME, ["--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--virtual-time-budget=4000", ...args], { stdio: "pipe" });

async function withServer(fn) {
  const srv = spawn(join(SITE, "node_modules/.bin/serve"), [DIST, "-l", String(PORT), "--no-clipboard"], { stdio: "ignore" });
  await new Promise((r) => setTimeout(r, 1500));
  try { return await fn(`http://localhost:${PORT}`); } finally { srv.kill(); }
}

async function handouts(base) {
  for (const lang of LANGS) {
    mkdirSync(join(OUT, lang), { recursive: true });
    for (const [slug] of BUNDLES) {
      const url = `${base}/${lang}/print/${slug}/`;
      const name = join(OUT, lang, `krkt-t1de-${slug}-${lang}`);
      if (want("pdf")) {
        chrome([`--print-to-pdf=${name}.pdf`, "--no-pdf-header-footer", url]);
        console.log("pdf ", `${name}.pdf`);
      }
      if (want("docx")) {
        const html = join(DIST, lang, "print", slug, "index.html");
        execFileSync("pandoc", [html, "-f", "html", "-t", "docx", "-o", `${name}.docx`, "--metadata", `lang=${lang}-CA`]);
        console.log("docx", `${name}.docx`);
      }
    }
  }
}

// Slide HTML → 1920×1080 PNG via a wrapper page that loads the deck fonts.
function slideShell(section, faces) {
  return `<!doctype html><html><head><meta charset="utf-8">
${faces.map((f) => `<link rel="stylesheet" href="${f}">`).join("\n")}
<style>*{margin:0;padding:0;box-sizing:border-box}html,body{width:1920px;height:1080px;overflow:hidden}
section{width:1920px;height:1080px;position:relative;overflow:hidden}aside{display:none}</style>
</head><body>${section}</body></html>`;
}

const text = (html) => html.replace(/<aside[\s\S]*?<\/aside>/g, "").replace(/<[^>]+>/g, " ").replace(/&[a-z]+;/g, " ").replace(/\s+/g, " ").trim();
const note = (html) => (html.match(/<aside>([\s\S]*?)<\/aside>/)?.[1] ?? "").replace(/<[^>]+>/g, "").trim();

// Renders every slide once in a single browser. Also reports text that
// overflows the 1920×1080 frame (mostly longer French copy).
async function decks() {
  const browser = await puppeteer.launch({ executablePath: execFileSync("which", [CHROME]).toString().trim(), args: ["--no-sandbox"] });
  const tab = await browser.newPage();
  await tab.setViewport({ width: 1920, height: 1080 });
  const overflow = [];
  for (const lang of LANGS) {
    mkdirSync(join(OUT, lang), { recursive: true });
    for (const [slug, deck, label] of BUNDLES) {
      const proj = join(REPO, "decks", deck, "project");
      const meta = JSON.parse(readFileSync(join(proj, "deck.json"), "utf8"));
      const dir = join(proj, lang === "en" ? "slides" : "slides-fr");
      if (!existsSync(dir)) { console.warn(`skip pptx ${deck} ${lang}: ${dir} missing`); continue; }
      const faces = Object.values(meta.faces ?? {}).map((f) => f.href);
      const pres = new pptxgen();
      pres.layout = "LAYOUT_WIDE"; // 13.33 × 7.5 in, 16:9
      pres.title = `${label[lang]} · KRKT:T1DE`;
      pres.author = "KRKT Library";
      pres.company = "KRKT";
      pres.lang = lang === "fr" ? "fr-CA" : "en-CA";
      for (const id of meta.order) {
        const file = join(dir, `${id}.html`);
        if (!existsSync(file)) { console.warn(`  missing ${lang} slide ${deck}/${id}`); continue; }
        const html = readFileSync(file, "utf8");
        await tab.setContent(slideShell(html, faces), { waitUntil: "load", timeout: 90000 });
        await tab.evaluate(() => document.fonts.ready);
        const spill = await tab.evaluate(() => {
          const out = [];
          for (const el of document.querySelectorAll("section *:not(aside):not(aside *)")) {
            const r = el.getBoundingClientRect();
            if (r.width === 0) continue;
            if (r.bottom > 1082 || r.right > 1922) out.push(`${el.tagName} ends at ${Math.round(r.right)}x${Math.round(r.bottom)}`);
            else if (el.scrollHeight > el.clientHeight + 4 && getComputedStyle(el).overflow !== "visible") out.push(`${el.tagName} clipped`);
          }
          // Absolutely-positioned footer lines must not overlap the slide content.
          const all = [...document.querySelectorAll("section *:not(aside):not(aside *)")];
          for (const f of all.filter((e) => getComputedStyle(e).position === "absolute")) {
            const fr = f.getBoundingClientRect();
            for (const el of all) {
              if (el === f || f.contains(el) || el.contains(f) || el.children.length) continue;
              const r = el.getBoundingClientRect();
              if (r.width && r.left < fr.right && r.right > fr.left && r.top < fr.bottom - 2 && r.bottom > fr.top + 2) {
                out.push(`${el.tagName} overlaps footer`);
                break;
              }
            }
          }
          return out.slice(0, 2);
        });
        const data = await tab.screenshot({ type: "jpeg", quality: 82, encoding: "base64" });
        if (spill.length) {
          overflow.push(`${lang} ${deck}/${id}: ${spill.join("; ")}`);
          if (process.env.DUMP) writeFileSync(join(process.env.DUMP, `${lang}-${deck}-${id}.jpg`), Buffer.from(data, "base64"));
        }
        const slide = pres.addSlide();
        slide.addImage({ data: `data:image/jpeg;base64,${data}`, x: 0, y: 0, w: 13.333, h: 7.5, altText: text(html).slice(0, 1000) });
        const n = note(html);
        if (n) slide.addNotes(n);
      }
      const name = join(OUT, lang, `krkt-t1de-${slug}-${lang}.pptx`);
      await pres.writeFile({ fileName: name, compression: true });
      console.log("pptx", name);
    }
  }
  await browser.close();
  if (overflow.length) console.warn(`\nOVERFLOW (${overflow.length}):\n` + overflow.join("\n"));
}

if (want("pdf") || want("docx")) await withServer(handouts);
if (want("pptx")) await decks();
console.log("done:", readdirSync(join(OUT, "en")).length + readdirSync(join(OUT, "fr")).length, "files");
