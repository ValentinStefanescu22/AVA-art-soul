import type { NextConfig } from "next";

// The whole site is exported as plain HTML/CSS/JS files (`out/`) that Cloudflare serves as static assets:
// nothing runs on a server, so there is nothing to attack or keep alive there.
const config: NextConfig = {
  output: "export",
  // Images are optimised by our own build step (scripts/images.mjs), because static export disables next/image's optimiser.
  images: { unoptimized: true },
  poweredByHeader: false,
  reactStrictMode: true,
  // In production `/` → `/ro` is done by Cloudflare (public/_redirects). `next dev` doesn't read that file,
  // so the same redirect is repeated here for local development only (static export ignores redirects anyway).
  ...(process.env.NODE_ENV === "development" && {
    async redirects() {
      return [{ source: "/", destination: "/ro", permanent: false }];
    },
  }),
};

export default config;
