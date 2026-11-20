// Downloads the site's fonts from Google Fonts with ONLY the characters the site uses, into src/fonts/ (committed).
//
// Why: next/font/google serves each style as two files, "latin" + "latin-ext", and a Romanian page needs both
// (ă, ș, ț live in latin-ext). That made ~167 KB of fonts on every first visit, competing with the first photo on
// a slow phone (Lighthouse, E3). One file per style holding just our characters is much smaller.
//
// When a text needs a character that isn't below, tests/unit/fonts.test.ts fails and names it: add it to CHARS
// and run `npm run fonts`, then commit src/fonts/.
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

const OUT = path.resolve(import.meta.dirname, "../src/fonts");

/** Every character the fonts contain: printable ASCII, Romanian letters, the typography we use (RO and EN). */
export const CHARS =
  Array.from({ length: 0x7f - 0x20 }, (_, i) => String.fromCharCode(0x20 + i)).join("") +
  "ăâîșțĂÂÎȘȚ" +
  "éèêëàáäöüçñóúíÉ" + // names and English loanwords
  "„”“‘’«»–—…·•›‹←→©°×€ ";

/** Each style the site uses, as a Google Fonts css2 family spec (only the axes and weights we use). */
export const FONTS = [
  // Titles: weight 400 only, with the optical-size axis (globals.css sets 'opsz' 20 / 48 / 72 / 96)
  { file: "bodoni.woff2", family: "Bodoni+Moda:opsz,wght@6..96,400" },
  { file: "bodoni-italic.woff2", family: "Bodoni+Moda:ital,opsz,wght@1,6..96,400" },
  // Text: 400 (body), 500 (labels, buttons), 600 (bold)
  { file: "literata.woff2", family: "Literata:wght@400..600" },
  { file: "pinyon.woff2", family: "Pinyon+Script" },
];

// Google picks the format by browser; a current Chrome gets woff2.
const UA =
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36";

async function get(url) {
  const res = await fetch(url, { headers: { "User-Agent": UA } });
  if (!res.ok) throw new Error(`${res.status} for ${url}`);
  return res;
}

async function main() {
  await mkdir(OUT, { recursive: true });
  const text = encodeURIComponent(CHARS);
  for (const { file, family } of FONTS) {
    const css = await (await get(`https://fonts.googleapis.com/css2?family=${family}&text=${text}`)).text();
    const urls = [...css.matchAll(/src: url\(([^)]+)\) format\('woff2'\)/g)].map((m) => m[1]);
    if (urls.length !== 1) throw new Error(`expected one woff2 for ${family}, got ${urls.length}:\n${css}`);
    const bytes = Buffer.from(await (await get(urls[0])).arrayBuffer());
    await writeFile(path.join(OUT, file), bytes);
    console.log(`fonts: ${file} ${(bytes.length / 1024).toFixed(1)} KB`);
  }
}

if (import.meta.url === `file://${process.argv[1]}`) await main();
