import { builtPages, expect, test } from "./pages";

test("the bare domain goes to the Romanian site", async ({ request }) => {
  const res = await request.get("/", { maxRedirects: 0 });
  expect(res.status()).toBe(301);
  expect(res.headers()["location"]).toBe("/ro");
});

// Same switch as the build: the preview is hidden from search engines, the launched site is open (checklist 6).
const INDEXABLE = process.env.SITE_INDEXABLE === "true";

test("robots.txt matches the launch state", async ({ request }) => {
  const res = await request.get("/robots.txt");
  expect(res.ok()).toBe(true);
  const body = await res.text();
  if (INDEXABLE) {
    expect(body).toMatch(/Allow: \//);
    expect(body).toMatch(/Sitemap: https:\/\//);
  } else {
    expect(body).toMatch(/Disallow: \//);
  }
});

test("the favicon set is linked and served (launch checklist 5)", async ({ page, request }) => {
  await page.goto("/ro");
  const links = await page.$$eval('link[rel~="icon"], link[rel="apple-touch-icon"], link[rel="manifest"]', (ls) =>
    ls.map((l) => (l as HTMLLinkElement).getAttribute("href")!),
  );
  expect(links.some((h) => h.includes("icon.svg"))).toBe(true);
  expect(links.some((h) => h.includes("apple-icon"))).toBe(true);
  expect(links.some((h) => h.includes("manifest"))).toBe(true);
  for (const url of [...links, "/favicon.ico", "/icon-192.png", "/icon-512.png"]) {
    expect((await request.get(url)).ok(), url).toBe(true);
  }
});

test("an unknown address shows the 404 page", async ({ request }) => {
  expect((await request.get("/ro/pagina-care-nu-exista")).status()).toBe(404);
});

for (const path of builtPages()) {
  test.describe(path, () => {
    test("loads cleanly: no JS errors, no CSP violations, no cookies", async ({ page, problems, context }) => {
      const res = await page.goto(path);
      expect(res?.status()).toBe(200);
      await page.waitForLoadState("networkidle");
      expect(problems).toEqual([]);
      // Launch checklist 14: no cookies means no cookie banner is needed.
      expect(await context.cookies()).toEqual([]);
    });

    test("is sent with the security headers", async ({ request }) => {
      const h = (await request.get(path)).headers();
      expect(h["content-security-policy"]).toMatch(/script-src 'self'( 'sha256-[^']+')*(;| https)/);
      expect(h["content-security-policy"]).not.toMatch(/script-src[^;]*unsafe-inline/);
      expect(h["strict-transport-security"]).toContain("max-age=");
      expect(h["x-content-type-options"]).toBe("nosniff");
      expect(h["referrer-policy"]).toBe("strict-origin-when-cross-origin");
      expect(h["x-frame-options"]).toBe("DENY");
      if (INDEXABLE) expect(h["x-robots-tag"]).toBeUndefined();
      else expect(h["x-robots-tag"]).toContain("noindex");
    });

    test("has a language, a title, a description and a canonical URL", async ({ page }) => {
      await page.goto(path);
      await expect(page.locator("html")).toHaveAttribute("lang", /^(ro|en)$/);
      await expect(page).toHaveTitle(/\S/);
      await expect(page.locator('meta[name="description"]')).toHaveAttribute("content", /.{50,}/);
      await expect(page.locator('link[rel="canonical"]')).toHaveAttribute("href", new RegExp(`${path}$`));
      await expect(page.locator("h1")).toHaveCount(1);
    });

    test("every image has an alt attribute (launch checklist 8)", async ({ page }) => {
      await page.goto(path);
      expect(await page.locator("img:not([alt])").count()).toBe(0);
    });
  });
}

test.describe("breakpoints (launch checklist 9)", () => {
  test.skip(({ isMobile }) => isMobile, "widths are set explicitly; one engine is enough");
  for (const width of [320, 390, 768, 1024, 1440]) {
    for (const path of builtPages()) {
      test(`${path} has no sideways scroll at ${width}px`, async ({ page }) => {
        await page.setViewportSize({ width, height: 800 });
        await page.goto(path);
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
        expect(overflow).toBeLessThanOrEqual(0);
      });
    }
  }
});
