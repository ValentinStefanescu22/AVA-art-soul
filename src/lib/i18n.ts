// The site has two languages. Romanian is the main one; English is filled in at the end (Alessia checks it).
export const LOCALES = ["ro", "en"] as const;
export type Locale = (typeof LOCALES)[number];
export const DEFAULT_LOCALE: Locale = "ro";

/** Languages that are actually built and linked. English joins at stage E7, once its texts exist. */
export const PUBLISHED_LOCALES: readonly Locale[] = ["ro"];

export function isLocale(value: string): value is Locale {
  return (LOCALES as readonly string[]).includes(value);
}

/** Turns the `[lang]` route segment into a Locale, failing loudly on anything else (static export never hits this). */
export function toLocale(value: string): Locale {
  if (!isLocale(value)) throw new Error(`Unknown locale: ${value}`);
  return value;
}

/** BCP 47 tags for `<html lang>`, `hreflang` and `og:locale`. */
export const LANG_TAG: Record<Locale, { html: string; og: string }> = {
  ro: { html: "ro", og: "ro_RO" },
  en: { html: "en", og: "en_GB" },
};
