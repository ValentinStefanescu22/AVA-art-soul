import { defineConfig, devices } from "@playwright/test";

const PORT = 8788;

// End-to-end tests run against the real build (out/), served by wrangler exactly like Cloudflare serves it in
// production: same redirects, same headers, same CSP. Run `npm run build` first.
export default defineConfig({
  testDir: "tests/e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? [["github"], ["html", { open: "never" }]] : "list",
  use: {
    baseURL: `http://localhost:${PORT}`,
    trace: "retain-on-failure",
  },
  projects: [
    { name: "desktop", use: { ...devices["Desktop Chrome"], viewport: { width: 1440, height: 900 } } },
    // Most visitors come from Instagram on a phone: test both mobile engines.
    { name: "android", use: { ...devices["Pixel 7"] } },
    { name: "iphone", use: { ...devices["iPhone 14"] } },
  ],
  webServer: {
    command: `npx wrangler dev --port ${PORT} --log-level warn`,
    url: `http://localhost:${PORT}/ro`,
    reuseExistingServer: !process.env.CI,
    timeout: 60_000,
  },
});
