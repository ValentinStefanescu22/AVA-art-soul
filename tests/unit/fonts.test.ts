import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
// @ts-expect-error — plain JS build script, tested through its exports
import { CHARS, FONTS } from "../../scripts/fonts.mjs";

// The fonts hold only the characters in CHARS (scripts/fonts.mjs). A text with any other character would show it
// in a fallback font, so every text in src/ is checked here.

const SRC = path.resolve(import.meta.dirname, "../../src");

function textFiles(dir: string): string[] {
  return readdirSync(dir, { recursive: true, withFileTypes: true })
    .filter((e) => e.isFile() && /\.(ts|tsx)$/.test(e.name))
    .map((e) => path.join(e.parentPath, e.name))
    .filter((f) => !f.includes(`${path.sep}generated${path.sep}`));
}

/** The characters of a source file that can reach the page: everything except comments. */
function visibleText(source: string): string {
  return source.replace(/\/\*[\s\S]*?\*\//g, "").replace(/(^|[^:"'`])\/\/.*$/gm, "$1");
}

describe("fonts", () => {
  it.each(textFiles(SRC))("%s uses only characters the fonts contain", (file) => {
    const missing = [...new Set(visibleText(readFileSync(file, "utf8")))].filter(
      (c) => !(CHARS as string).includes(c) && c !== "\n",
    );
    expect(missing, `add to CHARS in scripts/fonts.mjs, then run npm run fonts`).toEqual([]);
  });

  it("every font file exists, and the preloaded ones are small", () => {
    for (const { file } of FONTS as { file: string }[])
      expect(existsSync(path.join(SRC, "fonts", file)), file).toBe(true);
    // Bodoni upright + Literata are preloaded on every page (budget: E3, Lighthouse)
    const preloaded = ["bodoni.woff2", "literata.woff2"].reduce(
      (n, f) => n + statSync(path.join(SRC, "fonts", f)).size,
      0,
    );
    expect(preloaded).toBeLessThan(80 * 1024);
  });

  it("keeps Romanian letters with comma below (ș ț), not cedilla", () => {
    for (const c of "ăâîșțĂÂÎȘȚ„”") expect(CHARS).toContain(c);
  });
});
