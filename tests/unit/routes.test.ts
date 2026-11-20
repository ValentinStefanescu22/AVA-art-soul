import { href, PAGES, segments, SERVICE_PAGES, type PageKey } from "@/lib/routes";

const keys = Object.keys(PAGES) as PageKey[];

describe("routes", () => {
  it("builds site-relative links per language", () => {
    expect(href("ro", "acasa")).toBe("/ro");
    expect(href("ro", "consiliere")).toBe("/ro/ce-oferim/consiliere");
    expect(href("en", "consiliere")).toBe("/en/ce-oferim/consiliere"); // slugs stay Romanian in English too
  });

  it("gives every page a unique, lowercase, ASCII slug", () => {
    const paths = keys.map((k) => PAGES[k].path);
    expect(new Set(paths).size).toBe(paths.length);
    for (const p of paths) expect(p).toMatch(/^[a-z0-9/-]*$/);
  });

  it("nests every service page under Ce oferim", () => {
    for (const key of SERVICE_PAGES) {
      expect(PAGES[key]).toMatchObject({ parent: "ceOferim" });
      expect(segments(key)[0]).toBe("ce-oferim");
    }
  });

  it("only points parents at pages that exist", () => {
    for (const key of keys) {
      const parent = (PAGES[key] as { parent?: string }).parent;
      if (parent) expect(keys).toContain(parent);
    }
  });

  it("keeps the post-payment pages out of search results", () => {
    expect(PAGES.multumim.indexed).toBe(false);
    expect(PAGES.programareFacuta.indexed).toBe(false);
  });
});
