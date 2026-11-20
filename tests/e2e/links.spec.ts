import { builtPages, expect, test } from "./pages";

test.skip(({ isMobile }) => isMobile, "links are the same on every device");

// Opens every page, collects every internal link and checks that each one answers (no broken links).
test("every internal link works", async ({ page, request }) => {
  test.setTimeout(120_000); // visits every page of the site
  const links = new Set<string>();
  for (const path of builtPages()) {
    await page.goto(path, { waitUntil: "domcontentloaded" });
    const hrefs = await page.$$eval("a[href]", (as) => as.map((a) => (a as HTMLAnchorElement).href));
    for (const h of hrefs) {
      const url = new URL(h);
      if (url.origin === new URL(page.url()).origin) links.add(url.pathname);
    }
  }
  const broken: string[] = [];
  for (const link of links) {
    const res = await request.get(link);
    if (!res.ok()) broken.push(`${link} → ${res.status()}`);
  }
  expect(broken).toEqual([]);
});
