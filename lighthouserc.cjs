// Lighthouse CI: measures every built page on a simulated mid-range phone and fails if it gets slower or less
// accessible than our thresholds. Run after `npm run build`: npx @lhci/cli@0.16.1 autorun
const { readdirSync } = require("node:fs");
const path = require("node:path");

const OUT = path.join(__dirname, "out");
const PORT = 8789;
const urls = readdirSync(OUT, { recursive: true, withFileTypes: true })
  .filter((e) => e.isFile() && e.name.endsWith(".html") && !["404.html", "_not-found.html"].includes(e.name))
  .map((e) =>
    path
      .relative(OUT, path.join(e.parentPath, e.name))
      .split(path.sep)
      .join("/")
      .replace(/\.html$/, ""),
  )
  .map((p) => `http://localhost:${PORT}/${p}`);

module.exports = {
  ci: {
    collect: {
      startServerCommand: `npx wrangler dev --port ${PORT} --log-level warn`,
      startServerReadyPattern: "Ready on",
      url: urls,
      numberOfRuns: 3,
    },
    assert: {
      assertions: {
        "categories:performance": ["error", { minScore: 0.95 }],
        "categories:accessibility": ["error", { minScore: 1 }],
        "categories:best-practices": ["error", { minScore: 1 }],
        // The SEO category is checked audit by audit: until launch the preview is "noindex" on purpose,
        // which would otherwise pull the whole category score down.
        "document-title": "error",
        "meta-description": "error",
        "link-text": "error",
        "crawlable-anchors": "error",
        "image-alt": "error",
        hreflang: "error",
        canonical: "error",
        "http-status-code": "error",
        "largest-contentful-paint": ["error", { maxNumericValue: 2000 }],
        "cumulative-layout-shift": ["error", { maxNumericValue: 0.05 }],
        "total-blocking-time": ["error", { maxNumericValue: 150 }],
        // JavaScript budget per page (transfer size, bytes).
        "resource-summary:script:size": ["error", { maxNumericValue: 180000 }],
      },
    },
    // Reports stay local / as a CI artifact; nothing is uploaded to a public server.
    upload: { target: "filesystem", outputDir: ".lighthouseci/reports" },
  },
};
