// @ts-expect-error — plain JS build script, tested through its exports
import { buildHeaders, cspFor, inlineScripts, routeOf, sha256 } from "../../scripts/csp.mjs";

describe("scripts/csp.mjs", () => {
  it("hashes only inline scripts that the browser executes", () => {
    const html = [
      `<script src="/_next/a.js"></script>`,
      `<script>self.__next_f.push([1])</script>`,
      `<script type="application/ld+json">{"@type":"Person"}</script>`,
      `<script type="speculationrules">{"prerender":[]}</script>`,
    ].join("");
    expect(inlineScripts(html)).toEqual(["self.__next_f.push([1])", `{"prerender":[]}`]);
  });

  it("produces the standard CSP hash format", () => {
    // echo -n "alert(1)" | openssl dgst -sha256 -binary | base64
    expect(sha256("alert(1)")).toBe("'sha256-bhHHL3z2vDgxUt0W3dWQOrprscmda2Y5pLsLg4GF+pI='");
  });

  it("maps exported files to the URLs Cloudflare serves them at", () => {
    expect(routeOf("ro.html")).toBe("/ro");
    expect(routeOf("ro/ce-oferim/consiliere.html")).toBe("/ro/ce-oferim/consiliere");
    expect(routeOf("404.html")).toBeNull();
  });

  it("never allows unsafe-inline or eval for scripts", () => {
    const csp = cspFor(["'sha256-abc'"], { analytics: false });
    const scriptSrc = csp.split("; ").find((d: string) => d.startsWith("script-src"));
    expect(scriptSrc).toBe("script-src 'self' 'sha256-abc'");
    expect(csp).toContain("frame-ancestors 'none'");
    expect(csp).toContain("object-src 'none'");
  });

  it("opens only the Cloudflare analytics origins when analytics is on", () => {
    const csp = cspFor([], { analytics: true });
    expect(csp).toContain("script-src 'self' https://static.cloudflareinsights.com");
    expect(csp).toContain("connect-src 'self' https://cloudflareinsights.com");
  });

  it("tells search engines to stay away until launch", () => {
    const pages = [{ route: "/ro", hashes: [] }];
    expect(buildHeaders(pages, { indexable: false, analytics: false })).toContain("X-Robots-Tag: noindex");
    expect(buildHeaders(pages, { indexable: true, analytics: false })).not.toContain("X-Robots-Tag");
  });
});
