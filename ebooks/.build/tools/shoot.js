#!/usr/bin/env node
/* shoot.js — rasterize each section.slide of the assembled ebook to shots/pNNN.jpg.
 *
 * Usage:
 *   node tools/shoot.js                 shoot all slides of preview.html
 *   node tools/shoot.js --final         shoot ebooks/prt-converge.html instead
 *   node tools/shoot.js --only p08,p15  shoot only those slide ids
 *   node tools/shoot.js --list          print slide ids in document order, then exit
 *
 * Always writes shots/report.json: console errors, page errors, mermaid errors,
 * and per-slide overflow flags (content exceeding the 1440x900 slide box).
 */
const path = require("path");
const fs = require("fs");
const puppeteer = require("puppeteer-core");

const ROOT = path.resolve(__dirname, "..");
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

const args = process.argv.slice(2);
const flag = (n) => args.includes(n);
const optVal = (n) => {
  const i = args.indexOf(n);
  return i >= 0 ? args[i + 1] : null;
};

const targetFile = flag("--final")
  ? path.resolve(ROOT, "../prt-converge.html")
  : path.join(ROOT, optVal("--preview") || "preview.html");
const reportName = optVal("--report") || "report.json";
const shotsDir = path.join(ROOT, "shots");
fs.mkdirSync(shotsDir, { recursive: true });

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: "new",
    args: ["--force-color-profile=srgb", "--hide-scrollbars", "--disable-lcd-text"],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1.5 });

  const consoleErrors = [];
  const pageErrors = [];
  page.on("console", (m) => {
    if (m.type() === "error") consoleErrors.push(m.text());
  });
  page.on("pageerror", (e) => pageErrors.push(String(e)));

  await page.goto("file://" + targetFile, { waitUntil: "networkidle0", timeout: 120000 });
  await page.evaluate(() => document.fonts.ready);

  // Wait until every .mermaid node has rendered an <svg> or recorded an error.
  let mermaidSettled = true;
  try {
    await page.waitForFunction(
      () => {
        const els = Array.from(document.querySelectorAll(".mermaid"));
        const errs = window.__mermaidErrors || [];
        return els.every((el, i) => el.querySelector("svg") || errs.some((e) => e.index === i));
      },
      { timeout: 90000 }
    );
  } catch (e) {
    mermaidSettled = false;
  }

  const slides = await page.$$("section.slide");
  const order = await page.$$eval("section.slide", (els) =>
    els.map((el, i) => ({ id: el.id || `slide-${i + 1}`, act: el.getAttribute("data-act") || "" }))
  );

  if (flag("--list")) {
    order.forEach((s, i) => console.log(String(i + 1).padStart(2, "0"), s.id, s.act));
    await browser.close();
    return;
  }

  const only = optVal("--only");
  const wanted = only ? new Set(only.split(",").map((s) => s.trim())) : null;

  const mermaidErrors = await page.evaluate(() => window.__mermaidErrors || []);
  const overflow = [];
  const shot = [];

  for (let i = 0; i < slides.length; i++) {
    const meta = order[i];
    const el = slides[i];
    const ov = await page.evaluate((node) => {
      const r = { w: node.scrollWidth - node.clientWidth, h: node.scrollHeight - node.clientHeight };
      // also detect descendants escaping the slide's padding box
      const sr = node.getBoundingClientRect();
      let escapees = [];
      node.querySelectorAll("*").forEach((d) => {
        const dr = d.getBoundingClientRect();
        if (dr.width === 0 || dr.height === 0) return;
        const cs = getComputedStyle(d);
        if (cs.position === "fixed") return;
        if (dr.right > sr.right + 2 || dr.bottom > sr.bottom + 2 || dr.left < sr.left - 2 || dr.top < sr.top - 2) {
          const ghost = d.classList && String(d.className).includes("ghost");
          if (!ghost) escapees.push(d.tagName + "." + String(d.className).split(" ")[0]);
        }
      });
      r.escapees = escapees.slice(0, 5);
      return r;
    }, el);
    if (ov.w > 2 || ov.h > 2 || ov.escapees.length) {
      overflow.push({ id: meta.id, dw: ov.w, dh: ov.h, escapees: ov.escapees });
    }
    if (wanted && !wanted.has(meta.id)) continue;
    const fname = String(meta.id).replace(/^p0*(\d+)$/, (m, n) => "p" + n.padStart(3, "0")) + ".jpg";
    await el.screenshot({ path: path.join(shotsDir, fname), type: "jpeg", quality: 88 });
    shot.push(fname);
  }

  const report = {
    target: targetFile,
    slideCount: slides.length,
    mermaidSettled,
    mermaidErrors,
    consoleErrors,
    pageErrors,
    overflow,
    shot,
  };
  fs.writeFileSync(path.join(shotsDir, reportName), JSON.stringify(report, null, 2));

  console.log(
    `shoot: ${shot.length} shot / ${slides.length} slides | mermaid ${mermaidSettled ? "ok" : "TIMEOUT"} ` +
    `errors=${mermaidErrors.length} | console=${consoleErrors.length} | overflow=${overflow.length}`
  );
  if (overflow.length) console.log("overflow:", overflow.map((o) => o.id).join(", "));
  if (mermaidErrors.length) console.log("mermaid errors:", JSON.stringify(mermaidErrors));
  await browser.close();
  process.exit(mermaidErrors.length || pageErrors.length ? 1 : 0);
})().catch((e) => {
  console.error("shoot.js fatal:", e);
  process.exit(2);
});
