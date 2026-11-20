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
export const test = base.extend<{ problems: string[] }>({
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
