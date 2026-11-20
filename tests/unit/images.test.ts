import { statSync } from "node:fs";
import path from "node:path";
import { IMAGES } from "@/generated/images";
// @ts-expect-error — plain JS build script, tested through its exports
import { keyOf, widthsFor } from "../../scripts/images.mjs";

const PUBLIC = path.resolve(import.meta.dirname, "../../public");
const KB = 1024;

describe("scripts/images.mjs", () => {
  it("derives stable keys from file paths", () => {
    expect(keyOf("hero-lut.jpg")).toBe("hero-lut");
    expect(keyOf(path.join("placeholder", "grup.webp"))).toBe("placeholder-grup");
  });

  it("never upscales and always keeps the original width", () => {
    expect(widthsFor(500)).toEqual([480, 500]);
    expect(widthsFor(2000)).toEqual([480, 768, 1080, 1440, 1920, 2000]);
    expect(widthsFor(4000).at(-1)).toBe(2880);
  });
});

describe("compressed images (launch checklist 17)", () => {
  const files = Object.entries(IMAGES).flatMap(([key, img]) => [...img.avif, ...img.webp].map((v) => ({ key, ...v })));

  it("gives every image AVIF and WebP and a blur preview", () => {
    for (const img of Object.values(IMAGES)) {
      expect(img.avif.length).toBeGreaterThan(0);
      expect(img.webp.length).toBe(img.avif.length);
      expect(img.blur).toMatch(/^data:image\/webp;base64,/);
      expect(img.blur.length).toBeLessThan(1200); // the preview must stay tiny: it is inlined in the HTML
    }
  });

  it.each(files)("$src stays within the size budget", ({ src, w }) => {
    const size = statSync(path.join(PUBLIC, src)).size;
    // What phones download (≤ 1440px wide files) is kept lighter than the big desktop files.
    expect(size).toBeLessThanOrEqual((w <= 1440 ? 300 : 400) * KB);
  });
});
