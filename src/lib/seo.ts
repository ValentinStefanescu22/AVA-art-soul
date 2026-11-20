import type { Metadata } from "next";
import { META } from "@/content/meta";
import { LANG_TAG, PUBLISHED_LOCALES, type Locale } from "./i18n";
import { href, PAGES, type PageKey } from "./routes";
import { SITE } from "./site";

/** Absolute URL of a page on the configured origin. */
export function absoluteUrl(lang: Locale, page: PageKey): string {
  return new URL(href(lang, page), SITE.url).toString();
}

export function pageMeta(lang: Locale, page: PageKey) {
  const meta = META[lang]?.[page] ?? META.ro[page];
  return meta;
}

/**
 * Everything a page tells search engines and social apps: title, description, canonical URL,
 * the same page in the other languages (hreflang), Open Graph, and whether it may be indexed.
 */
export function pageMetadata(lang: Locale, page: PageKey): Metadata {
  const { title, description } = pageMeta(lang, page);
  const languages: Record<string, string> = {};
  for (const l of PUBLISHED_LOCALES) languages[LANG_TAG[l].html] = absoluteUrl(l, page);
  languages["x-default"] = absoluteUrl("ro", page);
  const index = SITE.indexable && PAGES[page].indexed;

  return {
    // The home page title already contains the brand; the others get it from the layout's title template.
    title: page === "acasa" ? { absolute: title } : title,
    description,
    alternates: { canonical: absoluteUrl(lang, page), languages },
    openGraph: {
      type: "website",
      siteName: SITE.name,
      locale: LANG_TAG[lang].og,
      url: absoluteUrl(lang, page),
      title,
      description,
    },
    twitter: { card: "summary_large_image", title, description },
    robots: index ? { index: true, follow: true } : { index: false, follow: false },
  };
}
