// Build-time settings. They come from environment variables so the same code builds the preview (workers.dev,
// hidden from search engines) and, later, the real domain. See `.env.example`.

function siteUrl(): URL {
  const raw = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000";
  const url = new URL(raw);
  if (url.pathname !== "/") throw new Error(`NEXT_PUBLIC_SITE_URL must be an origin without a path, got ${raw}`);
  return url;
}

export const SITE = {
  name: "AVA Art & Soul",
  url: siteUrl(),
  /** Only the real domain is indexed. Until launch, robots.txt and every page say "noindex". */
  indexable: process.env.SITE_INDEXABLE === "true",
  /** Cloudflare Web Analytics token (public by design); empty means "no analytics", e.g. locally and in tests. */
  analyticsToken: process.env.NEXT_PUBLIC_CF_ANALYTICS_TOKEN ?? "",
} as const;
