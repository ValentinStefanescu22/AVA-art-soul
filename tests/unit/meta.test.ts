import { META } from "@/content/meta";
import { PAGES, type PageKey } from "@/lib/routes";
import { pageMetadata } from "@/lib/seo";

const keys = Object.keys(PAGES) as PageKey[];
const SUFFIX = " · AVA Art & Soul";
const fullTitle = (k: PageKey) => (k === "acasa" ? META.ro[k].title : META.ro[k].title + SUFFIX);

describe("search titles and descriptions (launch checklist 2 & 3)", () => {
  it("exist for every page", () => {
    for (const k of keys) {
      expect(META.ro[k].title.trim(), k).not.toBe("");
      expect(META.ro[k].description.trim(), k).not.toBe("");
    }
  });

  it("are unique, so Google doesn't see duplicate pages", () => {
    expect(new Set(keys.map(fullTitle)).size).toBe(keys.length);
    expect(new Set(keys.map((k) => META.ro[k].description)).size).toBe(keys.length);
  });

  it("fit in a search result: title ≤ 65 characters, description 70–160", () => {
    for (const k of keys) {
      expect(fullTitle(k).length, `${k}: ${fullTitle(k)}`).toBeLessThanOrEqual(65);
      const d = META.ro[k].description.length;
      expect(d, `${k} description is ${d} chars`).toBeGreaterThanOrEqual(70);
      expect(d, `${k} description is ${d} chars`).toBeLessThanOrEqual(160);
    }
  });
});

describe("pageMetadata", () => {
  it("sets canonical, hreflang and Open Graph from the page key", () => {
    const m = pageMetadata("ro", "consiliere");
    expect(m.alternates?.canonical).toMatch(/\/ro\/ce-oferim\/consiliere$/);
    expect(m.alternates?.languages).toHaveProperty("ro");
    expect(m.alternates?.languages).toHaveProperty("x-default");
    expect(m.openGraph).toMatchObject({ locale: "ro_RO", siteName: "AVA Art & Soul" });
  });

  it("never lets a page be indexed before launch", () => {
    // SITE_INDEXABLE is not "true" in tests, exactly like the workers.dev preview.
    expect(pageMetadata("ro", "acasa").robots).toMatchObject({ index: false });
  });

  it("keeps the brand once in the home title", () => {
    expect(pageMetadata("ro", "acasa").title).toEqual({ absolute: META.ro.acasa.title });
    expect(pageMetadata("ro", "contact").title).toBe("Contact");
  });
});
