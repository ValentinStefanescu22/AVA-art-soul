import { readdirSync } from "node:fs";
import path from "node:path";
import { test as base, expect } from "@playwright/test";

const OUT = path.resolve(import.meta.dirname, "../../out");

/** Every page the build produced (out/**.html), as URL paths. New pages are tested automatically. */
export function builtPages(): string[] {
  return readdirSync(OUT, { recursive: true, withFileTypes: true })
    .filter((e) => e.isFile() && e.name.endsWith(".html"))
    .map((e) => path.relative(OUT, path.join(e.parentPath, e.name)).split(path.sep).join("/"))
    .filter((p) => !["404.html", "_not-found.html"].includes(p))
    .map((p) => "/" + p.replace(/\.html$/, ""))
    .sort();
}

/**
 * A `page` that records problems while the test runs: JS errors, console errors and CSP violations.
 * Tests end with `expect(problems).toEqual([])`.
 */
export const test = base.extend<{ problems: string[]; quietPopup: void }>({
  // The newsletter pop-up opens after 8 s or 40% scroll, which would cover whatever a test is clicking. Every test
  // behaves like a visitor who has already seen it, except on URLs with ?popup (the pop-up's own test).
  quietPopup: [
    async ({ page }, use) => {
      await page.addInitScript(() => {
        if (!location.search.includes("popup")) localStorage.setItem("ava.popup.newsletter", "1");
      });
      await use();
    },
    { auto: true },
  ],
  problems: async ({ page }, use) => {
    const problems: string[] = [];
    page.on("pageerror", (e) => problems.push(`pageerror: ${e.message}`));
    page.on("console", (m) => m.type() === "error" && problems.push(`console: ${m.text()}`));
    await page.exposeFunction("__reportCsp", (msg: string) => problems.push(`csp: ${msg}`));
    await page.addInitScript(() => {
      document.addEventListener("securitypolicyviolation", (e) =>
        (window as unknown as { __reportCsp: (m: string) => void }).__reportCsp(
          `${e.violatedDirective} blocked ${e.blockedURI || "inline"}`,
        ),
      );
    });
    await use(problems);
  },
});

export { expect };
