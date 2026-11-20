import type { Locale } from "./i18n";

// Every page of the site, in one place. Slugs stay Romanian in both languages (/en/ce-oferim/ateliere-de-grup).
// Links, the sitemap, hreflang and the breadcrumb all read from here, so a page can't be "forgotten" in one of them.
export const PAGES = {
  acasa: { path: "", indexed: true },
  despreNoi: { path: "despre-noi", indexed: true },
  ceOferim: { path: "ce-oferim", indexed: true },
  ateliereDeGrup: { path: "ce-oferim/ateliere-de-grup", indexed: true, parent: "ceOferim" },
  pentruCompanii: { path: "ce-oferim/pentru-companii", indexed: true, parent: "ceOferim" },
  consiliere: { path: "ce-oferim/consiliere", indexed: true, parent: "ceOferim" },
  atelierPrivat: { path: "ce-oferim/atelier-privat", indexed: true, parent: "ceOferim" },
  retreaturi: { path: "ce-oferim/retreaturi", indexed: true, parent: "ceOferim" },
  scoliCopii: { path: "ce-oferim/scoli-si-copii", indexed: true, parent: "ceOferim" },
  evenimente: { path: "evenimente", indexed: true },
  galerie: { path: "galerie", indexed: true },
  contact: { path: "contact", indexed: true },
  intrebariFrecvente: { path: "intrebari-frecvente", indexed: true },
  inscriere: { path: "inscriere-plata-si-anulare", indexed: true },
  termeni: { path: "termeni-si-conditii", indexed: true },
  confidentialitate: { path: "politica-de-confidentialitate", indexed: true },
  cookies: { path: "cookies", indexed: true },
  // Reached only after a payment or a booking: useless in search results.
  multumim: { path: "multumim", indexed: false },
  programareFacuta: { path: "programare-facuta", indexed: false },
} as const satisfies Record<string, { path: string; indexed: boolean; parent?: string }>;

export type PageKey = keyof typeof PAGES;

export const SERVICE_PAGES = [
  "ateliereDeGrup",
  "pentruCompanii",
  "consiliere",
  "atelierPrivat",
  "retreaturi",
  "scoliCopii",
] as const satisfies readonly PageKey[];

/** Site-relative URL of a page, e.g. href("ro", "consiliere") → "/ro/ce-oferim/consiliere". */
export function href(lang: Locale, page: PageKey): string {
  const { path } = PAGES[page];
  return path ? `/${lang}/${path}` : `/${lang}`;
}

/** The page's path segments, as `generateStaticParams` and the sitemap need them. */
export function segments(page: PageKey): string[] {
  const { path } = PAGES[page];
  return path ? path.split("/") : [];
}

/** Which page a URL path shows: "/ro/ce-oferim/consiliere" → "consiliere"; unknown paths → null. */
export function pageAt(pathname: string): PageKey | null {
  const rest = pathname.replace(/^\/(ro|en)(?=\/|$)/, "").replace(/^\/|\/$/g, "");
  return (Object.keys(PAGES) as PageKey[]).find((k) => PAGES[k].path === rest) ?? null;
}

/** The top-level menu entry a page belongs to (a service page belongs to Ce oferim). */
export function sectionOf(page: PageKey): PageKey {
  return (PAGES[page] as { parent?: PageKey }).parent ?? page;
}
