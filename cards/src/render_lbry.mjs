import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
const require = createRequire("/home/phr0zt/.claude/jobs/5dbbbcbd/tmp/t1d-info/site/package.json");
const puppeteer = require("puppeteer-core");
const D = "/home/phr0zt/.claude/jobs/5dbbbcbd/tmp/lbry/";
const names = JSON.parse(readFileSync(D + "index.json"));
const b = await puppeteer.launch({ executablePath: "/usr/bin/google-chrome-stable", args: ["--no-sandbox"] });
const t = await b.newPage(); await t.setViewport({ width: 1280, height: 1152 });
for (const n of names) {
  await t.goto("file://" + D + n + ".html", { waitUntil: "networkidle0" });
  await t.evaluate(() => document.fonts.ready);
  const over = await t.evaluate(() => { const g=document.querySelector(".grid").getBoundingClientRect(); const f=document.querySelector(".ft").getBoundingClientRect(); return g.bottom > f.top - 10 ? `grid ${Math.round(g.bottom)} > footer ${Math.round(f.top)}` : ""; });
  if (over) console.log(n, over);
  await t.screenshot({ path: D + n + ".png" });
  await t.pdf({ path: D + n + ".pdf", width: "1280px", height: "1152px", printBackground: true, pageRanges: "1" });
}
await b.close(); console.log("done");
