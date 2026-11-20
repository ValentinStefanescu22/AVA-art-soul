import type { MetadataRoute } from "next";
import { SITE } from "@/lib/site";

export const dynamic = "force-static";

// Before launch (workers.dev preview) search engines are kept out entirely; on the real domain everything is open.
export default function robots(): MetadataRoute.Robots {
  if (!SITE.indexable) return { rules: { userAgent: "*", disallow: "/" } };
  return {
    rules: { userAgent: "*", allow: "/" },
    sitemap: new URL("/sitemap.xml", SITE.url).toString(),
  };
}
