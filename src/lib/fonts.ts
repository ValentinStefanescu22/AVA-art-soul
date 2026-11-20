import localFont from "next/font/local";

// The fonts are files in src/fonts/, made by scripts/fonts.mjs: each style holds only the characters the site uses
// (Latin, ă â î ș ț with comma below, our punctuation), one small file instead of Google's "latin" + "latin-ext" pair.
// next/font serves them from our own domain and adjusts the fallback font's metrics, so the swap doesn't shift text.
//
// Speed (E2/E3, Lighthouse): only what the first screen needs is preloaded (Bodoni upright for titles, Literata for
// text); Bodoni italic and Pinyon load when a page uses them.

/** Titles. Always used with font-variation-settings: 'opsz' 20 (see globals.css), or the hairlines vanish on screen. */
export const bodoni = localFont({
  src: "../fonts/bodoni.woff2",
  weight: "400",
  style: "normal",
  display: "swap",
  adjustFontFallback: "Times New Roman",
  variable: "--font-bodoni",
});

/** Bodoni italic, its own family (--font-display-italic in globals.css), not preloaded. */
export const bodoniItalic = localFont({
  src: "../fonts/bodoni-italic.woff2",
  weight: "400",
  style: "italic",
  display: "swap",
  preload: false,
  adjustFontFallback: "Times New Roman",
  variable: "--font-bodoni-italic",
});

/** Body text, weights 400–600 (variable). */
export const literata = localFont({
  src: "../fonts/literata.woff2",
  weight: "400 600",
  style: "normal",
  display: "swap",
  adjustFontFallback: "Times New Roman",
  variable: "--font-literata",
});

/** Only for "Art & Soul" and rare accents, never long text. Not preloaded. */
export const pinyon = localFont({
  src: "../fonts/pinyon.woff2",
  weight: "400",
  display: "swap",
  preload: false,
  adjustFontFallback: false,
  variable: "--font-pinyon",
});
